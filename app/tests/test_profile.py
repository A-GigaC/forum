from auth import auth

import requests

def test_profile():
    # login and get_jwt
    jwt, rt = auth()
    url_profile = 'http://localhost:8080/api/profiles/'
    profiles_data = {"name" : "SirGamer","jwt" : jwt}
    message = requests.put(url_profile, json=profiles_data)
    print(message.text)
    wrong_jwt = 'qwerty1231456asdfghzxcvbn'
    wrong_data = {"name" : "SirGamer","jwt" : wrong_jwt}
    error_message = requests.put(url_profile, json=wrong_data)
    print(error_message.text)
    assert error_message.text == '{"error": "wrong token"}', "Принимает несуществующие jwt!"

test_profile()