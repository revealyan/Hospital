import datetime
import json
import uuid
import dataaccess
from bottle import get, post, put, delete, request, response, abort
from app import app

def authorize(request):
    token = request.get_header("auth_token")

    login = dataaccess.get_login(token)
    
    doc_id = None

    if not login is None:
        ids = dataaccess.doctor_read(login = login)
        if(len(ids) > 0):
            doc_id = ids[0][0]

    return doc_id

def hand_check(data):
    success = True
    message = ""
    mode = None
    angle = None
    speed = None
    repeat = None

    if not 'hand' in data:
        success = False
        message += "hand отсутствует\n"
    else:
        try:
            if not 'mode' in data["hand"]:
                success = False
                message += "mode отсутствует\n"
            else:
                try:
                    mode = int(data["hand"]["mode"])
                except :
                    success = False
                    message += "mode имеет неверный формат, необходимо целое число"
            
            if not 'angle' in data["hand"]:
                success = False
                message += "angle отсутствует\n"
            else:
                try:
                    angle = float(data["hand"]["angle"])
                except :
                    success = False
                    message += "angle имеет неверный формат, необходимо число"
            
            if not 'speed' in data["hand"]:
                success = False
                message += "speed отсутствует\n"
            else:
                try:
                    speed = int(data["hand"]["speed"])
                except :
                    success = False
                    message += "speed имеет неверный формат, необходимо число"
            
            if not 'repeat' in data["hand"]:
                success = False
                message += "repeat отсутствует\n"
            else:
                try:
                    repeat = int(data["hand"]["repeat"])
                except :
                    success = False
                    message += "repeat имеет неверный формат, необходимо целое число"
        except :
            success = False
            message += "hand имеет неверный формат"
    return (success, message, mode, angle, speed, repeat)

def finger_check(data):
    success = True
    message = ""
    mode = None
    kgr = None
    press = None
    angle = None
    speed = None
    repeat = None

    if not 'finger' in data:
        success = False
        message += "finger отсутствует\n"
    else:
        try:
            if not 'mode' in data["finger"]:
                success = False
                message += "mode отсутствует\n"
            else:
                try:
                    mode = int(data["finger"]["mode"])
                except :
                    success = False
                    message += "mode имеет неверный формат, необходимо целое число"
            
            if not 'kgr' in data["finger"]:
                success = False
                message += "kgr отсутствует\n"
            else:
                try:
                    kgr = int(data["finger"]["kgr"])
                except :
                    success = False
                    message += "kgr имеет неверный формат, необходимо целое число"
            
            if not 'press' in data["finger"]:
                success = False
                message += "press отсутствует\n"
            else:
                try:
                    press = int(data["finger"]["press"])
                except :
                    success = False
                    message += "press имеет неверный формат, необходимо целое число"


            if not 'angle' in data["finger"]:
                success = False
                message += "angle отсутствует\n"
            else:
                try:
                    angle = float(data["finger"]["angle"])
                except :
                    success = False
                    message += "angle имеет неверный формат, необходимо число"
            
            if not 'speed' in data["finger"]:
                success = False
                message += "speed отсутствует\n"
            else:
                try:
                    speed = int(data["finger"]["speed"])
                except :
                    success = False
                    message += "speed имеет неверный формат, необходимо число"
            
            if not 'repeat' in data["finger"]:
                success = False
                message += "repeat отсутствует\n"
            else:
                try:
                    repeat = int(data["finger"]["repeat"])
                except :
                    success = False
                    message += "repeat имеет неверный формат, необходимо целое число"
        except :
            success = False
            message += "finger имеет неверный формат"
    return (success, message, mode, kgr, press, angle, speed, repeat)


@app.route('/patient', method=['OPTIONS', 'GET'])
@app.route('/patient/<patient_id>', method=['OPTIONS', 'GET'])
def get_patients(patient_id = None):
    doc_id = authorize(request)
    
    if doc_id is None:
        abort(401, "Access denied")

    if patient_id != None:
        pg = dataaccess.patient_graphics_read(id = None, patient_id = patient_id)
        graphics = []
        for x in pg:
            g = dataaccess.graphics_read(x[2])
            if(len(g) == 0):
                continue
            graphics.append({
                    "name": g[0][2],
                    "data": json.loads(g[0][1])
                });
        return json.dumps(graphics)

    patients = dataaccess.patient_read(patient_id, doc_id)
    results = []
    for i in patients:
        hand = dataaccess.hand_read(i[12])[0]
        finger = dataaccess.finger_read(i[13])[0]
        results.append({"id"                : i[0],
                        "number"            : i[2],
                         "last_name"        : i[3],
                         "first_name"       : i[4],
                         "second_name"      : i[5],
                         "birth_date"       : "{0:%Y-%m-%d %H:%M:%S}".format(i[6]),
                         "gender"           : bool(i[7]),
                         "receipt_date"     : "{0:%Y-%m-%d %H:%M:%S}".format(i[8]),
                         "diagnosis"        : i[9],
                         "comments"         : i[10],
                         "discharge_date"   : None if i[11] is None else "{0:%Y-%m-%d %H:%M:%S}".format(i[11]),
                         "hand"             : {
                                                "mode": hand[1],
                                                "angle": hand[2],
                                                "speed": hand[3],
                                                "repeat": hand[4]
                                              },                         
                         "finger"           : {
                                                "mode": finger[1],
                                                "kgr": finger[2],
                                                "press": finger[3],
                                                "angle": finger[4],
                                                "speed": finger[5],
                                                "repeat": finger[6]
                                              }
                       })
    return json.dumps(results)

@app.route('/patient', method=['OPTIONS', 'POST'])
def create_patient():
    doc_id = authorize(request)
    if doc_id is None:
        abort(401, "Access denied")

    number = str(doc_id) + str(dataaccess.ticks(datetime.datetime.now()))
    last_name = None
    first_name = None
    second_name = None
    birth_date = None
    gender = None
    receipt_date = datetime.datetime.now()
    diagnosis = ""
    comments = ""
    discharge_date = None
    hand_mode = None
    hand_angle = None
    hand_speed = None
    hand_repeat = None
    finger_mode = None
    finger_kgr = None
    finger_press = None
    finger_angle = None
    finger_speed = None
    finger_repeat = None
    hand_id = None
    finger_id = None
    
    data = request.json

    success = True
    message = ""
    
    
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

    if success and not 'birth_date' in data:
        success = False
        message += "birth_date отсутствует\n"
    else:
        try:
            birth_date = datetime.datetime.strptime(data["birth_date"], "%Y-%m-%d")
        except :
            success = False
            message += "birth_date имеет неверный формат, необходим YYYY-mm-dd"

    
    
    if success and not 'gender' in data:
        success = False
        message += "gender отсутствует\n"
    else:
        try:
            gender = bool(data["gender"])
        except :
            success = False
            message += "gender имеет неверный формат, необходим 0 или 1"
            
    if 'diagnosis' in data:
        diagnosis = data["diagnosis"]

    if 'comments' in data:
        comments = data["comments"]
    
    if success:
        hand_success, hand_message, hand_mode, hand_angle, hand_speed, hand_repeat = hand_check(data)
        success &= hand_success
        message += hand_message
    
    if success:
        finger_success, finger_message, finger_mode, finger_kgr, finger_press, finger_angle, finger_speed, finger_repeat = finger_check(data)
        success &= finger_success
        message += finger_message

    if success:
        try:
            hand_id = dataaccess.hand_create(hand_mode, hand_angle, hand_speed, hand_repeat)[0][4]
        except Exception as e:
            print(e)
            success = False;
            message = "Не удалось создать пациента"
    
    if success:
        try:
            finger_id = dataaccess.finger_create(finger_mode, finger_kgr, finger_press, finger_angle, finger_speed, finger_repeat)[0][6]
        except Exception as e:
            print(e)
            success = False;
            message = "Не удалось создать пациента"

    if success:
        try:
            dataaccess.patient_create(doc_id, number, last_name, first_name, second_name, birth_date, gender, receipt_date, hand_id, finger_id, diagnosis, comments, discharge_date)
        except Exception as e:
            print(e)
            success = False;
            message = "Не удалось создать пациента"

    result = {
        "success":      success,
        "message":      message
        }
    return json.dumps(result)

@app.route('/patient/<patient_id>', method=['OPTIONS', 'PUT'])
def update_patient(patient_id):
    if patient_id is None:
        abort(500, "Patient ID uncorrect")

    doc_id = authorize(request)
    if doc_id is None:
        abort(401, "Access denied")
        
    patient = dataaccess.patient_read(patient_id, doc_id)
    patient_id = None if len(patient) == 0 else patient[0][0]
    if patient_id is None:
        abort(401, "Access denied")
    hand_id = patient[0][12]
    finger_id = patient[0][13]    
    hand_mode = None
    hand_angle = None
    hand_speed = None
    hand_repeat = None
    finger_mode = None
    finger_kgr = None
    finger_press = None
    finger_angle = None
    finger_speed = None
    finger_repeat = None


    last_name = None
    first_name = None
    second_name = None
    birth_date = None
    gender = None
    diagnosis = None
    comments = None
    
    data = request.json

    success = True
    message = ""

    
    if 'last_name' in data:
        last_name = data["last_name"]
    if 'first_name' in data:
        first_name = data["first_name"]
    if 'second_name' in data:
        second_name = data["second_name"]
    if 'birth_date' in data:
        try:
            birth_date = datetime.datetime.strptime(data["birth_date"], "%Y-%m-%d")
        except :
            success = False
            message += "birth_date имеет неверный формат, необходим YYYY-mm-dd"               
    if 'gender' in data:
        try:
            gender = bool(data["gender"])
        except :
            success = False
            message += "gender имеет неверный формат, необходим 0 или 1"    
    if 'diagnosis' in data:
        diagnosis = data["diagnosis"]
    if 'comments' in data:
        comments = data["comments"]
    if 'hand' in data:
        if 'mode' in data['hand']:
            try:
                hand_mode = int(data['hand']['mode'])
            except :
                success = False
                message += "hand['mode'] имеет неверный формат, необходимо целое число"
        if 'angle' in data['hand']:
            try:
                hand_angle = float(data['hand']['angle'])
            except :
                success = False
                message += "hand['angle'] имеет неверный формат, необходимо число"
        if 'speed' in data['hand']:
            try:
                hand_speed = float(data['hand']['speed'])
            except :
                success = False
                message += "hand['speed'] имеет неверный формат, необходимо число"
        if 'repeat' in data['hand']:
            try:
                hand_repeat = int(data['hand']['repeat'])
            except :
                success = False
                message += "hand['repeat'] имеет неверный формат, необходимо целое число"

    if 'finger' in data:
        if 'mode' in data['finger']:
            try:
                finger_mode = int(data['finger']['mode'])
            except :
                success = False
                message += "finger['mode'] имеет неверный формат, необходимо целое число"
        if 'kgr' in data['finger']:
            try:
                finger_kgr = int(data['finger']['kgr'])
            except :
                success = False
                message += "finger['kgr'] имеет неверный формат, необходимо целое число"
        if 'press' in data['finger']:
            try:
                finger_angle = float(data['finger']['press'])
            except :
                success = False
                message += "finger['press'] имеет неверный формат, необходимо число"
        if 'angle' in data['finger']:
            try:
                finger_angle = float(data['finger']['angle'])
            except :
                success = False
                message += "finger['angle'] имеет неверный формат, необходимо число"
        if 'speed' in data['finger']:
            try:
                finger_speed = float(data['finger']['speed'])
            except :
                success = False
                message += "finger['speed'] имеет неверный формат, необходимо число"
        if 'repeat' in data['finger']:
            try:
                finger_repeat = int(data['finger']['repeat'])
            except :
                success = False
                message += "finger['repeat'] имеет неверный формат, необходимо целое число"

    
    if success:
        try:
            dataaccess.hand_update(hand_id, hand_mode, hand_angle, hand_speed, hand_repeat)
            dataaccess.finger_update(finger_id, finger_mode, finger_kgr, finger_press, finger_angle, finger_speed, finger_repeat)
            dataaccess.patient_update(id                = patient_id,
                                      last_name         = last_name, 
                                      first_name        = first_name,
                                      second_name       = second_name,
                                      birth_date        = birth_date,
                                      gender            = gender,
                                      diagnosis         = diagnosis,
                                      comments          = comments,
                                      discharge_date    = None)
        except Exception as e:
            print(e)
            success = False;
            message = "Не удалось обновить данные пациента"

    result = {
        "success":      success,
        "message":      message
        }

    return json.dumps(result)

@app.route('/patient/<patient_id>', method=['OPTIONS', 'DELETE'])
def delete_patient(patient_id):    
    if patient_id is None:
        abort(500, "Patient ID uncorrect")

    doc_id = authorize(request)
    if doc_id is None:
        abort(401, "Access denied")
        
    patient = dataaccess.patient_read(patient_id, doc_id)
    patient_id = None if len(patient) == 0 else patient[0][0]
    if patient_id is None:
        abort(401, "Access denied")

    last_name = None
    first_name = None
    second_name = None
    birth_date = None
    gender = None
    diagnosis = None
    comments = None


    data = request.json

    success = True
    message = ""
        
    if success:
        try:
            dataaccess.patient_update(id                = patient_id,
                                      last_name         = last_name, 
                                      first_name        = first_name,
                                      second_name       = second_name,
                                      birth_date        = birth_date,
                                      gender            = gender,
                                      diagnosis         = diagnosis,
                                      comments          = comments,
                                      discharge_date    = datetime.datetime.now())
        except Exception as e:
            print(e)
            success = False;
            message = "Не удалось обновить данные пациента"

    result = {
        "success":      success,
        "message":      message
        }

    return json.dumps(result)

