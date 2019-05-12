import mysql.connector
import datetime
import uuid

__host__="localhost"
__port__=3306
__user__="root"
__pswd__=""
__d_db__="hospital"

__settings__ = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "pswd": "",
        "d_db": "hospital"    
    }

'''common'''
def ticks(dt):
    return int((dt - datetime.datetime(1, 1, 1)).total_seconds() * 10000000)
'''common'''



'''Авторизация'''
__tokens__ = {}

def get_login(token):
    login = None
    if token in __tokens__:
        login = __tokens__[token]
    return login

def get_token(login):
    token = str(uuid.uuid4())

    while token in __tokens__:
        token = str(uuid.uuid4())

    __tokens__.setdefault(token, login)

    return token

'''Авторизация'''

'''Настройки'''

def __check_connect__(host, port, user, pswd, d_db):
    conn = mysql.connector.connect(user     =   user,
                                   password =   pswd,
                                   host     =   host,
                                   port     =   port,
                                   database =   d_db)

def __execute_procedure__(procedure, parameters):
    if not isinstance(parameters, (list, tuple)):
        parameters = [parameters]

    conn = mysql.connector.connect(user     =   __settings__["user"],
                                   password =   __settings__["pswd"],
                                   host     =   __settings__["host"],
                                   port     =   __settings__["port"],
                                   database =   __settings__["d_db"])

    results = []
    cursor = conn.cursor()        
    try:
        res = cursor.callproc(procedure, parameters)
        conn.commit()
        results.append(res)
        reader = []
        for result in cursor.stored_results():
            reader.append(result.fetchall())
        results.append(reader)
    except Exception as e:
        print(e)
        raise Exception(e)
    finally:
        cursor.close()
        conn.close()
    return results

def set_settings(host = __host__, port = __port__, 
                 user = __user__, pswd = __pswd__,
                 d_db = __d_db__):
    try:
        __check_connect__(host, port, user, pswd, d_db)
        __settings__["host"] = host
        __settings__["port"] = port
        __settings__["user"] = user
        __settings__["pswd"] = pswd
        __settings__["d_db"] = d_db
    except Exception as e:
        raise Exception("Invalid database configuration", e)
'''Настройки'''

'''doctor'''
def doctor_exists(login, password = None):
    parameters = [login, password, 0]
    results = __execute_procedure__("doctor_exists", parameters)
    is_exists = results[0][2]
    return is_exists > 0

def doctor_create(login, password, last_name, first_name, second_name):
    parameters = [login, password, last_name, first_name, second_name, 0]
    results = __execute_procedure__("doctor_create", parameters)
    id = results[0][5]
    return id

def doctor_read(id = None, login = None):
    parameters = [id, login]
    results = __execute_procedure__("doctor_read", parameters)
    res = results[1][0]
    return res
'''doctor'''

'''patient'''
def patient_create(doc_id, number, last_name, first_name, second_name, birth_date, gender, receipt_date, hand_id, finger_id, diagnosis = None, comments = None, discharge_date = None):
    parameters = [doc_id, number, last_name, first_name, second_name, birth_date, gender, receipt_date, diagnosis, comments, discharge_date, hand_id, finger_id, 0]
    #parameters = [doc_id, last_name, first_name, second_name, birth_date, gender, receipt_date, diagnosis, comments, discharge_date, 0]
    id = __execute_procedure__("patient_create", parameters)
    return id

def patient_read(id = None, doctor_id = None):
    parameters = [id, doctor_id]
    result = __execute_procedure__("patient_read", parameters)[1][0]
    return result

def patient_update(id, last_name, first_name, second_name, birth_date, gender, diagnosis, comments, discharge_date):
    parameters = [id, last_name, first_name, second_name, birth_date, gender, diagnosis, comments, discharge_date]
    result = __execute_procedure__("patient_update", parameters)
    return result

def patient_delete(id):
    parameters = [id]
    result = __execute_procedure__("patient_delete", parameters)
    return result
'''patient'''

'''hand'''
def hand_create(mode, angle, speed, repeat):
    parameters = [mode, angle, speed, repeat, 0]
    id = __execute_procedure__("hand_create", parameters)
    return id

def hand_read(id = None):
    parameters = [id]
    result = __execute_procedure__("hand_read", parameters)[1][0]
    return result

def hand_update(id, mode, angle, speed, repeat):
    parameters = [id, mode, angle, speed, repeat]
    result = __execute_procedure__("hand_update", parameters)
    return result

def hand_delete(id):
    parameters = [id]
    result = __execute_procedure__("hand_delete", parameters)
    return result
'''hand'''


'''finger'''
def finger_create(mode, kgr, press, angle, speed, repeat):
    parameters = [mode, kgr, press, angle, speed, repeat, 0]
    id = __execute_procedure__("finger_create", parameters)
    return id

def finger_read(id = None):
    parameters = [id]
    result = __execute_procedure__("finger_read", parameters)[1][0]
    return result

def finger_update(id, mode, kgr, press, angle, speed, repeat):
    parameters = [id, mode, kgr, press, angle, speed, repeat]
    result = __execute_procedure__("finger_update", parameters)
    return result

def finger_delete(id):
    parameters = [id]
    result = __execute_procedure__("finger_delete", parameters)
    return result
'''finger'''



'''graphics'''
def graphics_create(json_data, name):
    parameters = [json_data, name, 0]
    id = __execute_procedure__("graphics_create", parameters)
    return id

def graphics_read(id = None):
    parameters = [id]
    result = __execute_procedure__("graphics_read", parameters)[1][0]
    return result

def graphics_update(id, json_data, name):
    parameters = [id, json_data, name]
    result = __execute_procedure__("graphics_update", parameters)
    return result

def graphics_delete(id):
    parameters = [id]
    result = __execute_procedure__("graphics_delete", parameters)
    return result
'''graphics'''



'''patient_graphics'''
def patient_graphics_create(patient_id, graphics_id):
    parameters = [patient_id, graphics_id, 0]
    id = __execute_procedure__("patient_graphics_create", parameters)
    return id

def patient_graphics_read(id = None, patient_id = None):
    parameters = [id, patient_id]
    result = __execute_procedure__("patient_graphics_read", parameters)[1][0]
    return result

def patient_graphics_update(id, patient_id, graphics_id):
    parameters = [id, patient_id, graphics_id]
    result = __execute_procedure__("patient_graphics_update", parameters)
    return result

def patient_graphics_delete(id):
    parameters = [id]
    result = __execute_procedure__("patient_graphics_delete", parameters)
    return result
'''patient_graphics'''