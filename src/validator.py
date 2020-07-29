from flask import request
from functools import wraps
import logging
from cerberus import Validator
from errors import error


def myCoerc(n):
    try:
        return lambda v: None if v in ('null') else n(v)
    except Exception:
        return None


null2int = myCoerc(int)
null2float = myCoerc(float)

to_bool = lambda v: v.lower() in ('true', '1')
to_lower = lambda v: v.lower()
# to_list = lambda v: json.loads(v.lower())
to_list = lambda v: json.loads(v)


def sanitize_parameters(func):
    """Sets any queryparams in the kwargs"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            #logging.debug(f'[middleware] [sanitizer] args: {args}')
            #logging.debug(f'[middleware] [sanitizer] kargs: {kwargs}')

            #myargs={**kwargs, **request.args, **request.args.get('payload', {})}
            myargs={**kwargs, **request.args}
            logging.debug(f'[middleware] [sanitizer] User_args: {myargs}')
            kwargs['params'] = myargs
        except Exception as err:
            return error(status=502, detail=f'{err}')

        return func(*args, **kwargs)

    return wrapper

def validate_body_params(func):
    """analysis validation params"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        validation_schema = {
            'dataset_type': {
                'type': 'string',
                'required': True
            },
            'group': {
                'type': 'string',
                'required': True
            },
            'years': {
                'type': 'list',
                'required': True
            },
            'depth': {
                'type': 'string',
                'required': True
            },
            'variable': {
                'type': 'string',
                'required': True
            },
            'nBinds': {
                'type': 'integer',
                'required': True
            },
            'bindsRange': {
                'type': 'list',
                'required': True
            },
            'geometry': {
                'type': 'dictionary',
                'required': True
            }
            
        }
        try:
            logging.debug(f"[VALIDATOR - data and mask params]: {kwargs}")
            validator = Validator(validation_schema, allow_unknown=True, purge_unknown=True)
            if not validator.validate(kwargs['params']):
                return error(status=400, detail=validator.errors)
            
            kwargs['sanitized_params'] = validator.normalized(kwargs['params'])
            return func(*args, **kwargs)
        except Exception as err:
            return error(status=502, detail=f'{err}')

    return wrapper