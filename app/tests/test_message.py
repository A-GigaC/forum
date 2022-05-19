from auth import auth

import requests

body = "Hi there, Im using whatsapp!"

def test_message():
    # login and get_jwt
    jwt, rt = auth()
    url_thread = 'http://localhost:8080/api/messages/'
    create_message = {"body" : body, "thread" : 1}
    cm_header = {"Authorization" : jwt}
    message = requests.post(url_thread, headers=cm_header, json=create_message)
    print(message.text)

test_message()