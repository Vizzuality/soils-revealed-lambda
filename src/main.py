# try:
#   import unzip_requirements
# except ImportError:
#   pass
import os
import logging
from colorlog import ColoredFormatter
import sys
from flask import Flask, request, redirect, url_for, abort, jsonify, Blueprint, make_response

from errors import error
from validator import sanitize_parameters, validate_body_params, validate_point_params

import numpy as np
import xarray as xr
from xhistogram.xarray import histogram
from datetime import datetime
from affine import Affine
from rasterio import features
from shapely.geometry import Polygon
import _pickle as pickle
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)
        
def transform_from_latlon(lat, lon):
    lat = np.asarray(lat)
    lon = np.asarray(lon)
    trans = Affine.translation(lon[0], lat[0])
    scale = Affine.scale(lon[1] - lon[0], lat[1] - lat[0])
    return trans * scale

def rasterize(shapes, coords, latitude='latitude', longitude='longitude',
              fill=np.nan, **kwargs):
    """Rasterize a list of (geometry, fill_value) tuples onto the given
    xray coordinates. This only works for 1d latitude and longitude
    arrays.
    """
    transform = transform_from_latlon(coords[latitude], coords[longitude])
    out_shape = (len(coords[latitude]), len(coords[longitude]))
    raster = features.rasterize(shapes, out_shape=out_shape,
                                fill=fill, transform=transform,
                                dtype=float, **kwargs)
    spatial_coords = {latitude: coords[latitude], longitude: coords[longitude]}
    return xr.DataArray(raster, coords=spatial_coords, dims=(latitude, longitude))

def compute_values(ds, geometry, years, depth, variable, dataset_type, group, nBinds, bindsRange):
    
    if dataset_type == 'global-dataset' and group == 'historic':
        start_date = years[0]
        end_date = years[1]
        mean_years = ds.coords.get('time').values
    else:
        start_date = np.datetime64(datetime.strptime(f'{years[0]}-12-31', "%Y-%m-%d"))
        end_date = np.datetime64(datetime.strptime(f'{years[1]}-12-31', "%Y-%m-%d"))
        mean_years = [int(str(x).split('-')[0]) for x in ds.coords.get('time').values]
    
    xmin, ymax, xmax, ymin = geometry.bounds
    ds_index = ds.where(ds['mask'].isin(0.0)).sel(depth=depth, lon=slice(xmin, xmax), lat=slice(ymin, ymax))

    # Get difference between two dates
    diff = ds_index.loc[dict(time=end_date)] - ds_index.loc[dict(time=start_date)]
                    
    # Get counts and binds of the histogram
    if dataset_type == 'experimental-dataset' and variable == 'concentration':
        diff = diff[variable]/10.
    else:
        diff = diff[variable]

    bins = np.linspace(bindsRange[0], bindsRange[1], nBinds+1)
    h = histogram(diff, bins=[bins], dim=['lat', 'lon'], block_size=1)

    counts = h.values
    mean_diff = diff.mean(skipna=True).values 
    mean_values = ds_index[variable].mean(['lon', 'lat']).values
        
    return counts, bins, mean_diff, mean_years, mean_values

def serializer(counts, bins, mean_diff, mean_years, mean_values):

    return {
        'counts': counts,
        'bins': bins,
        'mean_diff': mean_diff,
        'mean_years': mean_years,
        'mean_values':mean_values
    }

def analysis(event, context):
    
    logger.info(f'## EVENT\r {event}')
    logger.info(f'## CONTEXT\r {context}')
    request = event#.get_json()
    
    # Read xarray.Dataset from pkl
    dataset_type = request['dataset_type']
    group = request['group']

    logger.info(f'## DATASET\r {dataset_type}')
    parent = os.getcwd()

    with open(f'{parent}/src/{dataset_type}_{group}.pkl', 'rb') as input:
        ds = pickle.load(input)
    
    # Create the data mask by rasterizing the vector data
    geometry = Polygon(request['geometry'].get('features')[0].get('geometry').get('coordinates')[0])
    
    # Get bbox and filter
    xmin, ymax, xmax, ymin = geometry.bounds
    ds = ds.sel(lon=slice(xmin, xmax), lat=slice(ymin, ymax))

    shapes = zip([geometry], range(1))
    da_mask = rasterize(shapes, ds.coords, longitude='lon', latitude='lat').rename('mask')
    ds['mask'] = da_mask   
    
    # Compute output values
    counts, bins, mean_diff, mean_years, mean_values = compute_values(ds, geometry, request['years'], request['depth'], 
                                                                      request['variable'], request['dataset_type'], 
                                                                      request['group'], request['nBinds'], 
                                                                      request['bindsRange'])
    # create response only for lambda function
    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps(serializer(counts, bins, mean_diff, mean_years, mean_values), cls=NpEncoder)
    # }

    # return response
    return serializer(counts, bins, mean_diff, mean_years, mean_values)

#Log setup
def setup_logLevels(level: str ="DEBUG"):
    """Sets up logs level."""
    formatter = ColoredFormatter(
	"%(log_color)s [%(levelname)-8s%(reset)s%(name)s:%(funcName)s]- %(lineno)d: %(bold)s%(message)s",
	datefmt=None,
	reset=True,
	log_colors={
		'DEBUG':    'cyan',
		'INFO':     'green',
		'WARNING':  'yellow',
		'ERROR':    'red',
		'CRITICAL': 'red,bg_white',
	},
	secondary_log_colors={},
	style='%'
)
    root = logging.getLogger()
    root.setLevel(level)
    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.WARN)
    error_handler.setFormatter(formatter)
    root.addHandler(error_handler)

    output_handler = logging.StreamHandler(sys.stdout)
    output_handler.setLevel(level)
    output_handler.setFormatter(formatter)
    root.addHandler(output_handler)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    logging.getLogger('rasterio').setLevel(logging.ERROR)
    logging.getLogger('botocore').setLevel(logging.ERROR)

setup_logLevels()

# Initialization of Flask application.

app = Flask(__name__)
app.url_map.strict_slashes = False

################################################################################
# Routes handle with Blueprint is allways a good idea
################################################################################
analysisService = Blueprint('raster', __name__)

@analysisService.route('/analysis', methods=['POST'])
@sanitize_parameters
# @validate_body_params
def get_data(**kwargs):
    result = analysis()
    return jsonify(
            {'data': result}
        ), 200


app.register_blueprint(analysisService, url_prefix='/api/v1')

################################################################################
# Error handler
################################################################################

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

################################################################################
# app runner
################################################################################
if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5020
    )