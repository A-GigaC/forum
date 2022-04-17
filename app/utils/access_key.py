import jwt
from datetime import datetime

limit = 86400 * 3

def aproved(token):
    decoded = jwt.decode(token, algorithms=["RS256"])
    if datetime.strptime(decoded['datetime'], "%Y-%m-%d").timestamp() <= datetime.now().simestamp() - limit:
        return 0
    else: return 1