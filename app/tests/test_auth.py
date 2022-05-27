import requests
from auth import auth


def test_auth():
    # login and get_jwt
    jwt, rt = auth()
    # logout имся
    url_logout = 'http://localhost:8080/api/auth/logout/'
    json4 = {"refresh_token":f"{rt}"}
    message4 = requests.post(url_logout, json=json4)
    assert message4.text != "403", "Не работает logout"

    ## # пробуем повторно зарегестрировать пользователя
    '''1- с темже НИКом '''
    url_signUp = 'http://localhost:8080/api/auth/signup/'
    dataX = {"nickname" : "testname1",
        "password" : "othpsswd1",
        "profile" : {
        "name" : "othname1"}}
    messageX = requests.post(url_signUp, json=dataX)
    assert messageX.text != "409", "Регистрация пользователя с повторяющимся ником!!"
    print("messageX.text == ", messageX.text)
    # пробуем логинимся с неправильным паролем
    url_signIn = 'http://localhost:8080/api/auth/signin/'
    data = {"nickname" : "testname1",
        "password" : "passwd2"}
    message = requests.post(url_signIn, json=data)
    print("message.text == ", message.text)
    assert message.text == "403", "можно зайти с неправильным паролем!"


test_auth()
