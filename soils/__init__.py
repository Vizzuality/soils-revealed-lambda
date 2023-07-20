import json
import logging
import sys

from flask import Flask, Blueprint, make_response
from werkzeug.exceptions import HTTPException

from soils.analysis.analysis import analysis
from soils.encoders import NpEncoder
from soils.errors import error
from soils.logs import setup_logLevels
from soils.validator import sanitize_parameters, validate_body_params

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Log setup
setup_logLevels()

# Initialization of Flask application.
app = Flask(__name__)
app.url_map.strict_slashes = False

################################################################################
# Routes handle with Blueprint is always a good idea
################################################################################
analysisService = Blueprint('raster', __name__)


@analysisService.route('/analysis', methods=['POST'])
@sanitize_parameters
# @validate_body_params
def get_data(**kwargs):
    try:
        result = analysis(kwargs['params'])
        response = make_response(json.dumps(
            {'data': result}, cls=NpEncoder
        ), 200)
        response.content_type = "application/json"
        return response
    except Exception as e:
        app.logger.debug(f"Error while calculating  new impact factors: {e}", exc_info=True)
        raise e
        response = make_response({}, 500)
        # replace the body with JSON
        response.data = json.dumps({
            "code": 500,
            "name": 'Unknown',
            "description": f'{e}',
        }, cls=NpEncoder)
    response.content_type = "application/json"
    return response 


app.register_blueprint(analysisService, url_prefix='/api/v1')


################################################################################
# Error handler
################################################################################
@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    #TODO: This should be more elegant 
    # start with the correct headers and status code from the error
    if isinstance(e, HTTPException):
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }, cls=NpEncoder)
        
    else:
        response = make_response({}, 500)
        # replace the body with JSON
        response.data = json.dumps({
            "code": 500,
            "name": 'Unknown',
            "description": f'{e}',
        }, cls=NpEncoder)
    response.content_type = "application/json"
    return response

@app.errorhandler(403)
def forbidden(e):
    return error(status=403, detail='Forbidden')


@app.errorhandler(404)
def page_not_found(e):
    return error(status=404, detail='Not Found')


@app.errorhandler(405)
def method_not_allowed(e):
    return error(status=405, detail='Method Not Allowed')


@app.errorhandler(410)
def gone(e):
    return error(status=410, detail='Gone')


@app.errorhandler(500)
def internal_server_error(e):
    return error(status=500, detail='Internal Server Error')


