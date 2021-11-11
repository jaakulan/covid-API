from flask import Flask, request, jsonify
import csv
import pandas as pd
import json
from dailyReportTools import dailyCSV as nd
from cleaningTools import dataCleaning as clean

app = Flask(__name__)

@app.route('/')
def index():
    return "hello" 

#this will overwrite all databases and create a new database for daily csv file
@app.route('/daily/addNewCSV', methods=['POST'])
def postCSV():
    if request.method == 'POST':
        file = request.files['file']
        fileDate = file.filename.split(".")[0]
        data = pd.read_csv(file, header = [0])
        dataDic = data.to_dict('records')
        if nd.newCSV(dataDic,fileDate):
            return "sucess"
        else:
            return "Unexpected failure, please check connection or database"
    else:
        return "Incorrect HTTP Method!"

@app.route('/daily/updateWithCSV', methods=['PATCH'])
def patchCSV():
    if request.method == 'PATCH':
        file = request.files['file']
        fileDate = file.filename.split(".")[0]
        data = pd.read_csv(file, header = [0])
        dataDic = data.to_dict('records')
        if nd.updateData(dataDic, fileDate):
            return "sucess \n" + data.to_string()
        else:
            return "Unexpected failure, please check connection or database"
    else:
        return "Incorrect HTTP Method!"

@app.route('/daily/viewAll', methods=['GET'])
def view():
    if request.method == 'GET':
        data = []
        type=request.args.get('type')
        if(clean.validType(type)):
            data = nd.viewData(data)
            data = json.dumps(data)
            if(type == 'json' or type=='JSON'):
                return data
            else:
                data = pd.read_json(data)
                return data.to_csv(index=False).replace("to_char", "d")
        else:
            return "Return type was not valid Or type was not specified"
    else:
        return "Incorrect HTTP Method!"

@app.route('/daily/deleteAll', methods=['DELETE'])
def deleteAll():
    if request.method == 'DELETE':
        if nd.deleteAllData():
            return "success"
        else: 
            return "Unexpected failure, please check connection or database"
    else:
        return "Incorrect HTTP Method!"

@app.route('/deleteDB', methods=['DELETE'])
def deleteDB():
    if request.method == 'DELETE':
        if nd.resetAllData():
            return "success"
        else:
            return "Unexpected failure, please check connection or database"
    else:
        return "Incorrect HTTP Method!"

@app.route('/daily/info', methods=['GET'])
def getInfo():
    if request.method == 'GET':
        data = request.args.getlist('data')
        dateStart = request.args.getlist('dateStart')
        dateEnd = request.args.getlist('dateEnd')
        dateSpecific = request.args.getlist('date')
        #clean all the data that was requested through URL
        countries = clean.locationQuery(request.args.getlist('country'))
        #Region is for province or state
        region = clean.locationQuery(request.args.getlist('region'))
        key = clean.locationQuery(request.args.getlist('combined'))
        data = clean.dataQuery(data)
        dates = clean.dateQuery(dateStart, dateEnd, dateSpecific)
        validityCheck = clean.infoValidity(data, dates, countries, region, key)
        if validityCheck[0]:
            type=request.args.get('type')
            if(clean.validType(type)):
                data = nd.queryData(data, dates, countries, region, key)
                data = json.dumps(data)
                if(type == 'json' or type=='JSON'):
                    return data
                else:
                    data = pd.read_json(data)
                    return data.to_csv(index=False).replace("to_char", "d")
            else:
                return "Return type was not valid Or type was not specified"
        return validityCheck[1]
    else:
        return "Incorrect HTTP Method!"


if __name__ == '__main__':
    app.debug =True
    app.run()