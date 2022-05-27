from auth import auth

import requests

name = "howToStartProgramming"
def test_thread():
    # login and get_jwt
    jwt, rt = auth()
    url_thread = 'http://localhost:8080/api/threads/'
    create_thread = {"Authorization" : jwt, "name" : name}
    message = requests.post(url_thread, json=create_thread)
    print(message.text)
    wrong_jwt = 'qwerty1231456asdfghzxcvbn'
    header = {"Authorization" : wrong_jwt}
    wrong_data = {"name" : "wrong_name"}
    error_message = requests.post(url_thread, headers=header, json=wrong_data)
    print(error_message.text)
    assert error_message.text == 403, "Принимает несуществующие jwt!"

test_thread()