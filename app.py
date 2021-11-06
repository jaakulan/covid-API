from flask import Flask, request, jsonify
import csv
import pandas as pd
from dailyReportTools import dailyCSV as nd
from timeSeriesTools import timeseries as ts

app = Flask(__name__)

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/')
def index():
    return "hello" 

#this will overwrite all databases and create a new database for daily csv file
@app.route('/daily/addNewCSV', methods=['POST'])
def postCSV():
    if request.method == 'POST':
        file = request.files['file']
        data = pd.read_csv(file, header = [0])
        dataDic = data.to_dict('records')
        nd.newCSV(dataDic)
    return "sucess \n" + data.to_string()

@app.route('/daily/viewAll', methods=['GET'])
def view():
    if request.method == 'GET':
        nd.viewData()
    return "success"

@app.route('/daily/deleteAll', methods=['DELETE'])
def deleteAll():
    if request.method == 'DELETE':
        nd.deleteAllData()
    return "success"

@app.route('/timeSeries/addNewCSV', methods=['POST'])
def postCSVTS():
    if request.method == 'POST':
        ## Call Post method
        pass
    return "success"

@app.route('/timeSeries/viewAll', methods=['GET'])
def viewTS():
    if request.method == 'GET':
        ts.viewData()
    return "success"

@app.route('/timeSeries/deleteAll', methods=['DELETE'])
def deleteAllTS():
    if request.method == 'DELETE':
        ## Call delete method
        pass
    return "success"


if __name__ == '__main__':
    app.debug =True
    app.run()