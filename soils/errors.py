from flask import jsonify


def error(status=500, detail='generic error'):
    error = {
        'status': status,
        'detail': detail
    }
    return jsonify(errors=[error]), status
