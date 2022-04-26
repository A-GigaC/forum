from auth import auth

import requests

name = "howToStartProgramming"
def test_thread():
    # login and get_jwt
    jwt, rt = auth()
    url_thread = 'http://localhost:8080/api/threads/'
    create_thread = {"jwt" : jwt, "name" : name}
    message = requests.post(url_thread, json=create_thread)
    print(message.text)

test_thread()