from flask import Flask, request, jsonify
import csv
import pandas as pd
import datetime
from dailyReportTools import dailyCSV as nd

app = Flask(__name__)

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
        data = []
        data = nd.viewData(data)
        print(data)
    return "success"

@app.route('/daily/deleteAll', methods=['DELETE'])
def deleteAll():
    if request.method == 'DELETE':
        nd.deleteAllData()
    return "success"

@app.route('/daily/info', methods=['GET'])
def getInfo():
    if request.method == 'GET':
        data = request.args.getlist('data')
        data = cleanDataQuery(data)
        dateStart = request.args.getlist('dateStart')
        dateEnd = request.args.getlist('dateEnd')
        dateSpecific = request.args.getlist('date')
        dates = cleanDateQuery(dateStart, dateEnd, dateSpecific)
        print(data)
        print(dates)
        return "success"
    else:
        return "Incorrect HTTP Method!"

def cleanDateQuery(dateStart, dateEnd, dateSpecific):
    if dateStart == [] and dateEnd == []:
        if len(dateSpecific) == 1:
            #do cleansing of dateSpecific
            cleanDates = checkDates(dateSpecific)
            if(cleanDates[0]):
                return [True, [dateSpecific]]
            else:
                return cleanDates[1] + " is an incorrect data format, should be YYYY-MM-DD"
        elif len(dateSpecific) == 0:
            # because no dates were specified
            return [True, None] 
        else:
            return [False, "Only 1 specific date can be queried at a time!"]
    elif dateSpecific == []:
        #this means dateStart or dateEnd both have queries and we will clean the duration
        if (len(dateStart) == 1 and len(dateEnd) == 1):
            cleanDates = checkDates([dateStart[0], dateEnd[0]])
            if(cleanDates[0]):
                #since dates are in iso format we can do direct comparison
                if cleanDates[1][0] < cleanDates[1][1]:
                    return [True, [dateStart[0], dateEnd[0]]]
                else:
                    return [False, "The start date needs to have occured before entered the end date"]
            else:
                return cleanDates[1] + " is an incorrect data format, should be YYYY-MM-DD"
        else:
            return [False, "Incorrect amount of dates entered for dateStart/dateEnd, Or missing date for one of those parameters!"]
    else:
        return [False, "Only 1 specific date Or 1 duration of two dates can be queried at a time!"]

def checkDates(dates):
    for i in dates:
        if not checkValidDate(i):
            return [False, i]
    return [True]

def checkValidDate(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except:
        return False # "Incorrect data format, should be YYYY-MM-DD"]

def cleanDataQuery(data):
    #get rid of repeated data queries
    data = list(set(data))
    length = len(data)
    #return null if data contains illegal queries
    legal = ['deaths', 'confirmed', 'active', 'recovered']
    illegal = []
    

    for i in range(length):
        data[i] = data[i].strip().lower()
        if data[i] not in legal:
            illegal.append(data[i])
    

    if len(illegal) > 0:
        return [False, illegal]
    elif len(data)<1:
        return [False, None]
    return [True, data]

if __name__ == '__main__':
    app.debug =True
    app.run()