from flask import Flask, request, jsonify
import csv
import pandas as pd
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
        print(nd.newCSV(dataDic,fileDate))
    return "sucess \n" + data.to_string()

@app.route('/daily/updateWithCSV', methods=['PATCH'])
def patchCSV():
    if request.method == 'PATCH':
        file = request.files['file']
        fileDate = file.filename.split(".")[0]
        data = pd.read_csv(file, header = [0])
        dataDic = data.to_dict('records')
        print(nd.updateData(dataDic, fileDate))
    return "sucess \n" + data.to_string()

@app.route('/daily/viewAll', methods=['GET'])
def view():
    if request.method == 'GET':
        data = []
        data = nd.viewData(data)
        print(data)
    return "success"

@app.route('/daily/deleteAll', methods=['DELETE'])
def deleteAll():
    if request.method == 'DELETE':
        nd.deleteAllData()
    return "success"

@app.route('/deleteDB', methods=['DELETE'])
def deleteDB():
    if request.method == 'DELETE':
        nd.resetAllData()
    return "success"

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
        print(countries)
        print(region)
        print(key)
        print(data)
        print(dates)
        validityCheck = clean.infoValidity(data, dates, countries, region, key)
        if validityCheck[0]:
            print(nd.queryData(data, dates, countries, region, key))
            return "success"
        print(validityCheck[1])
        return validityCheck[1]
    else:
        return "Incorrect HTTP Method!"


if __name__ == '__main__':
    app.debug =True
    app.run()