import requests
import json
from datetime import datetime

name = "oleg"

def sign_up():
    # регистрируемя
    url_signUp = 'http://localhost:8080/api/auth/signup/'
    data1 = {"nickname" : "1o4le8g8",
        "password" : "7733m",
        "name" : name}
    message1 = requests.post(url_signUp, json=data1)
    print(message1.text)

def auth():
    sign_up()
    ## логинимся
    url_signIn = 'http://localhost:8080/api/auth/signin/'
    data2 = {"nickname" : "1o4le8g8",
        "password" : "7733m",}
    message2 = requests.post(url_signIn, json=data2)
    #print(message2.text)
    rt = json.loads(message2.text)['refresh_token']
    #print(rt)
    ## обновляем токены
    url_refresh = 'http://localhost:8080/api/auth/get_jwt/'
    data3 = {"nickname" : "1o4le8g8",        
            "refresh_token" : f'{rt}'}
    message3 = requests.post(url_refresh, json=data3)
    #print(message3.text)
    jwt = json.loads(message3.text)['jwt']
    return jwt, rt

print(auth())

