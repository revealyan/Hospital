import dataaccess
from datetime import datetime
import json, csv, os, glob


DB_HOST = "92.255.195.45"
DB_PORT = "33060"
DB_USER = "jarvis"
DB_PASS = "YesMrStark"
DB_NAME = "hospital"

dataaccess.set_settings(DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME)

pathDir = "C:/Users/Revealyan/Desktop/graphics/"


def getAllCSV(rootDirectory):
    results = []
    for top, dirs, files in os.walk(rootDirectory):
        for nm in files:
            if nm[-3:].lower() == "csv":
                results.append(os.path.join(top, nm).replace('\\', '/'))
        for dir in dirs:
            results += getAllCSV(dir)
    return results


def csv2json(filePath):
    data = {}
    names = {}
    results = []

    rows = []
    with open(filePath, 'r') as file: 
        csvData = csv.reader(file)
        for x in csvData:
            rows.append([i.strip() for i in x[0].split(';')])
    for i, name in enumerate(rows[0]):
        if len(name) > 0:
            names.setdefault(name, i)
            data.setdefault(i, [])
    for row in rows[1:]:
        for i, x in enumerate(row):
            if i in data:
                xf = 0
                try:
                    xf = float(x)
                except :
                    pass
                data[i].append(xf)
    for x in names:
        results.append({"name": x, 
                        "data": data[names[x]]})
    return json.dumps(results)

csvFiles = getAllCSV(pathDir)

for csvFile in csvFiles:
    jsonData = csv2json(csvFile)
    jsonPath = csvFile[:-3] + "json"
    jsonName = csvFile.split('/')[-2] + csvFile.split('/')[-1][:-3]
    with open(jsonPath, 'w') as file:
        file.write(jsonData)
        id = dataaccess.graphics_create(jsonData, jsonName)[0][2]
        print(id)