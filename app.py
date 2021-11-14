from flask import Flask, request
import pandas as pd
import json
from dailyReportTools import dailyCSV as nd
from timeSeriesTools import timeseries as ts
from cleaningTools import dataCleaning as clean

app = Flask(__name__)

@app.route('/')
def index():

    return "Welcome to Jaakulan and Alexandra's Covid Api!" 

"""

    DAILY FUNCTIONS BELOW

"""
#this will overwrite all databases and create a new database for daily csv file
@app.route('/daily/addNewCSV', methods=['POST'])
def postCSVnd():
    if request.method == 'POST':
        file = request.files['file']
        fileDate = file.filename.split(".")[0]
        data = pd.read_csv(file, header = [0])
        dataDic = data.to_dict('records')
        if nd.newCSV(dataDic,fileDate):
            return "success"
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
            return "success"
        else:
            return "Unexpected failure, please check connection or database"
    else:
        return "Incorrect HTTP Method!"

@app.route('/daily/viewAll', methods=['GET'])
def viewnd():
    if request.method == 'GET':
        data = []
        format=request.args.get('type')
        if(clean.validType(format)):
            data = nd.viewData(data)
            data = json.dumps(data)
            if(format == 'json' or format =='JSON'):
                return data
            else:
                data = pd.read_json(data)
                return data.to_csv(index=False).replace("to_char", "d")
        else:
            return "Return type was not valid Or type was not specified"
    else:
        return "Incorrect HTTP Method!"


@app.route('/daily/deleteAll', methods=['DELETE'])
def deleteAllnd():
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
            format=request.args.get('type')
            if(clean.validType(format)):
                data = nd.queryData(data, dates, countries, region, key)
                data = json.dumps(data)
                if(format == 'json' or format=='JSON'):
                    return data
                else:
                    data = pd.read_json(data)
                    return data.to_csv(index=False).replace("to_char", "d")
            else:
                return "Return type was not valid Or type was not specified"
        return validityCheck[1]
    else:
        return "Incorrect HTTP Method!"


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


    else:
        return "Incorrect HTTP Method!"


if __name__ == '__main__':
    app.debug =True
    app.run()