from flask import Flask, request, jsonify
import csv
import pandas as pd

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
        print(data.to_dict('records'))
    return "sucess \n" + data.to_string()

if __name__ == '__main__':
    app.debug =True
    app.run()