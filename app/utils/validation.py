from jsonschema import ValidationError, validate
from json import dumps
from aiohttp import web

def validation(json, schema):
    try: 
        validate(instance=json, schema=schema)
        return False
    except ValidationError as error:
        response = dumps({"reason":error.message})
        return response
    
