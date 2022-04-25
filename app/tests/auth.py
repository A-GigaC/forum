import requests
import json
from datetime import datetime

name = "sergey"

def sign_up():
        # регистрируемя
    url_signUp = 'http://localhost:8080/api/auth/signup/'
    data1 = {"nickname" : "s3rg3y",
        "password" : "qwerty123",
        "profile" : {
        "name" : name}}
    message1 = requests.post(url_signUp, json=data1)
    print(message1.text)

def auth():
    ### sign_up()
    ## логинимся
    url_signIn = 'http://localhost:8080/api/auth/signin/'
    data2 = {"nickname" : "s3rg3y",
        "password" : "qwerty123"}
    message2 = requests.post(url_signIn, json=data2)
    #print(message2.text)
    rt = json.loads(message2.text)['refresh_token']
    #print(rt)
    ## обновляем токены
    url_refresh = 'http://localhost:8080/api/auth/get_jwt/'
    data3 = {"nickname" : "s3rg3y",        
            "refresh_token" : f'{rt}'}
    message3 = requests.post(url_refresh, json=data3)
    #print(message3.text)
    jwt = json.loads(message3.text)['jwt']
    return jwt, rt
