from auth import auth

import requests

def test_profile():
    # login and get_jwt
    jwt, rt = auth()
    url_profile = 'http://localhost:8080/api/profiles/'
    profiles_data = {"name" : "SirGamer","jwt" : jwt}
    message = requests.put(url_profile, json=profiles_data)
    print(message.text)

test_profile()