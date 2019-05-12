import json
import uuid
import dataaccess
from bottle import get, post, request
from app import app


@get("/")
def home():
    return "welcome home"

@app.route('/authorize', method=['OPTIONS', 'POST'])
def authorize():
    success = True
    message = ""
    token = None
    last_name = None
    first_name = None
    second_name = None

    try:
        login = None;
        password = None;

        data = request.json

    
        if success and not 'login' in data:
            success = False
            message += "login отсутствует\n"
        else:
            login = data["login"]
    
        if success and not 'pass' in data:
            success = False
            message += "pass отсутствует\n"
        else:
            password = data["pass"]

        if success and not dataaccess.doctor_exists(login, password):
            success = False
            message = "Неверные логин и/или пароль"
        else:
            token = dataaccess.get_token(login)
            doc = dataaccess.doctor_read(login = login)[0]
            last_name = doc[3]
            first_name = doc[4]
            second_name = doc[5]
    except Exception as e:
        success = False
        message = "Error"
        print("AUTH POST")
        print(e)
        print("AUTH POST")

    result = {
            "success":  success,
            "message":  message,
            "token":    token,
            "person": {
                    "last_name": last_name,
                    "first_name": first_name,
                    "second_name": second_name,
                }
            }
    return json.dumps(result)

@app.route('/register', method=['OPTIONS', 'POST'])
def create_doctors():
    success = True
    message = ""

    try:
        login = None
        password = None
        last_name = None
        first_name = None
        second_name = None

        data = request.json

    
        if success and not 'login' in data:
            success = False
            message += "login отсутствует\n"
        else:
            login = data["login"]
    
        if success and not 'pass' in data:
            success = False
            message += "pass отсутствует\n"
        else:
            password = data["pass"]

    
        if success and not 'last_name' in data:
            success = False
            message += "last_name отсутствует\n"
        else:
            last_name = data["last_name"]

        if success and not 'first_name' in data:
            success = False
            message += "first_name отсутствует"
        else:
            first_name = data["first_name"]

        if 'second_name' in data:
            second_name = data["second_name"]

        if dataaccess.doctor_exists(login):
            success = False
            message = "Данный логин занят"

        if success:
            try:
                id = dataaccess.doctor_create(login, password, last_name, first_name, second_name)
                success = id > 0
            except Exception as e:
                print(e)
                success = False
                message = "Не удалось создать аккаунт"
    except Exception as e:
        success = False
        message = "Error"
        print("REG POST")
        print(e)
        print("REG POST")
   
    result = {
        "success": success,
        "message": message
        }

    return json.dumps(result)