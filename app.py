from flask import Flask, request, jsonify
import csv
import pandas as pd
from dailyReportTools import dailyCSV as nd
from timeSeriesTools import timeseries as ts
from cleaningTools import dataCleaning as clean
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/')
def index():
    return "We need to put instructions here on how to use our backend."

"""

    DAILY FUNCTIONS BELOW

"""

#this will overwrite all databases and create a new database for daily csv file
@app.route('/daily/addNewCSV', methods=['POST'])
def postCSVnd():
    if request.method == 'POST':
        file = request.files['file']
        data = pd.read_csv(file, header = [0])
        dataDic = data.to_dict('records')
        nd.newCSV(dataDic)
    return "sucess \n" + data.to_string()

@app.route('/daily/viewAll', methods=['GET'])
def viewnd():
    if request.method == 'GET':
        nd.viewData()
    return "success"


@app.route('/daily/deleteAll', methods=['DELETE'])
def deleteAllnd():
    if request.method == 'DELETE':
        nd.deleteAllData()
    return "success"

"""

    TIME SERIES FUNCTIONS BELOW

"""
@app.route('/timeSeries/addNewCSV', methods=['POST'])
def addNewCSVts():
    if request.method == 'POST':
        datatypels = request.args.getlist('type')

        if len(datatypels) == 0:
            return "No Data Type Specified in this query"
        datatype = datatypels[0]


        file = request.files['file']
        data = pd.read_csv(file, header=[0])
        dataDic = data.to_dict('records')
        ts.newCSV(dataDic, datatype)
    return "success"

@app.route('/timeSeries/updateCSV', methods=['POST'])
def updateCSVts():
    if request.method == 'POST':
        print("here")
        datatypels = request.args.getlist('type')
        if len(datatypels) == 0:
            return "No Data Type Specified in this query"
        datatype = datatypels[0]

        print(datatype)

        file = request.files['file']
        data = pd.read_csv(file, header=[0])
        dataDic = data.to_dict('records')
        ts.addCSV(dataDic, datatype)
    return "success"

@app.route('/timeSeries/viewAll', methods=['GET'])
def viewts():
    if request.method == 'GET':

        datatypels = request.args.getlist('type')
        if len(datatypels) == 0:
            return "No Data Type Specified in this query"
        datatype = datatypels[0]

        filetypels = request.args.getlist('file')
        if len(filetypels) == 0:
            return "No File Type Specified in this query"
        filetype = filetypels[0]

        data = ts.viewData(datatype)
        data = json.dumps(data)
        if (filetype == 'json' or filetype == 'JSON'):
            return data
        else:
            data = pd.read_json(data)
            return data.to_csv(index=False).replace("to_char", "d")
    return "failure"

@app.route('/timeSeries/deleteAll', methods=['DELETE'])
def deleteAllts():
    if request.method == 'DELETE':
        datatypels = request.args.getlist('type')
        if len(datatypels) == 0:
            return "No Data Type Specified in this query"
        datatype = datatypels[0]

        ts.deleteAllData(datatype)
    return "success"

@app.route('/timeSeries/info', methods=['GET'])
def getInfots():
    if request.method == 'GET':

        #Version without cleaning

        datatypels = request.args.getlist('type')
        datels = request.args.getlist('date')
        countryls = request.args.getlist('country')
        regionls = request.args.getlist('region')


        # Ensure type exists
        if len(datatypels) == 0:
            return "No Type Specified in this query"

        # Assign date accordingly
        if len(datels) == 0:
            date = None
        else:
            date = datels[0]

        #Assign combined key accordingly
        combined = None
        if len(countryls) != 0:
            if len(regionls) != 0:
                combined = regionls[0]+countryls[0]
                combined = ''.join(c for c in combined if c.isalnum())
            else:
                combined = countryls[0]
                combined = ''.join(c for c in combined if c.isalnum())

        return json.dumps(ts.query(date, combined,datatypels[0]))
        #return jsonify(ts.query(typerls[0], date, combined))


    else:
        return "Incorrect HTTP Method!"


if __name__ == '__main__':
    app.debug =True
    app.run()