from auth import auth

import requests

def test_profile():
    # login and get_jwt
    jwt, rt = auth()
    url_profile = 'http://localhost:8080/api/profiles/'
    profiles_data = {"name" : "name1.1"}
    headerT = {"Authorization" : jwt}
    message = requests.put(url_profile, headers=headerT, json=profiles_data)
    print(message.text)
    wrong_jwt = 'qwerty1231456asdfghzxcvbn'
    headerF = {"Authorization" : wrong_jwt}
    wrong_data = {"name" : "name1.1"}
    error_message = requests.put(url_profile, headers=headerF, json=wrong_data)
    print(error_message.text)
    assert error_message.text == '{"error": "wrong token"}', "Принимает несуществующие jwt!"

test_profile()