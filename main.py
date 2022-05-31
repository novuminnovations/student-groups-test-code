#Imports
from flask import Flask, render_template, request, session, url_for, redirect, jsonify, send_from_directory, abort
from werkzeug.utils import secure_filename
import csv
import os
import random as r
from algo import *

app = Flask(__name__, template_folder='templates', static_folder='static')
#Configurations for uploading files
app.config["DEBUG"]=True
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.csv', '.xls', '.xlsx']
app.config['UPLOAD_PATH'] =  'static/uploads'

#Parsing function to retrieve and parse data from csv
def parse():
  data=[]
  ga=[]
  gb=[]
  with open('./static/uploads/data.csv', 'r') as datafile:
    reader = csv.reader(datafile, skipinitialspace=False,delimiter=',', quoting=csv.QUOTE_NONE)
    for i in reader:
      data.append(i)
  for i in data:
    if i[3]=='A':
      ga.append(i)
    elif i[3]=='B':
      gb.append(i)
  r.shuffle(ga)
  r.shuffle(gb)
  data=[ga, gb]
  return data

#In the case the file is too large, this function will run
@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

#Index app route//init page/needs to be changed to login page
@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

#For uploading csv file
@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = 'initial input data.csv'
    #Saves input file as 'initial input data.csv' so it can be copied and parsed
    if filename != '':
      file_ext = os.path.splitext(filename)[1]
      if file_ext not in app.config['UPLOAD_EXTENSIONS']:
        return "Invalid spreadsheet", 400
      uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    #Copying the input data into new csv
    copyInitData()
    return '', 204

#Uploads file (DEPRECATED)
@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

#Loads page with student groups, using data from parser
@app.route('/home.html')
def home():
  return render_template('home.html', data=parse())

#Reloads page with new groups and edited data csv
@app.route("/random/", methods=['POST'])
def random():
  randomizeGroups()
  return render_template('home.html', data=parse())

#Runs flask app using local port, however repl handles this to run on a domain// needs to be edited to account for Ms. Bailey's domain
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)

