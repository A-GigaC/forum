from aiohttp.web import Response
from jsonschema import ValidationError, validate
from json import dumps
from aiohttp import web

from utils.access import AuthorizedRequest


class ValidatedRequest(AuthorizedRequest):

    def __init__(self, json, *arg, **kw):
        self.json_input = json
        super().__init__(*arg, **kw)


def validation(json, schema):
<<<<<<< Updated upstream
    try: 
        validate(instance=json, schema=schema)
        return False
    except ValidationError as error:
        response = dumps({"reason":error.message})
        return response
    
=======
  try: 
    validate(instance=json, schema=schema)
    return False
  except ValidationError as error:
    response = dumps({"reason":error.message})
    return response

def DTOGuard(schema):
    def decorator(controller):
        async def wrapped(authorized_request):
            json_input = await authorized_request.json()
            error = validation(json_input, schema)
            if error: 
                return Response(text="400")
            else:
                validated_request  = ValidatedRequest(json_input, authorized_request)
                return controller(validated_request)
        return wrapped
    return decorator
>>>>>>> Stashed changes
