#Imports
from flask import Flask, render_template, request, session, url_for, redirect, jsonify, send_from_directory, abort, make_response, Response
from werkzeug.utils import secure_filename
import csv
import os
import random as r
import bcrypt, jwt, time
from algo import *

app = Flask(__name__, template_folder='templates', static_folder='static')
#Configurations for uploading files
app.config["DEBUG"]=True
app.config['UPLOAD_EXTENSIONS'] = ['.csv']
app.config['UPLOAD_PATH'] =  'static/uploads'

#Login settings
JWT_KEY = "GLOBAL-STUDENT-GROUPS-KEY"
JWT_ISS = "JANICE-BAILEY"
JWT_ALGO = "HS512"
#Login information
password = "[REDACTED]"
encpw=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
USERS = {
  "[REDACTED]" : encpw
}

def jwtSign(username):
  rnd = "".join(r.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~!@#$%^_-") for i in range(24))
  now = int(time.time())
  return jwt.encode({
    "iat" : now, 
    "nbf" : now, 
    "exp" : now + 3600, 
    "jti" : rnd, 
    "iss" : JWT_ISS,
    "data" : { "username" : username }
  }, JWT_KEY, algorithm=JWT_ALGO)
#Using cookies for login
def jwtVerify(cookies):
  try:
    token = cookies.get("JWT")
    decoded = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGO])
    return True
  except:
    return False
  
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
  data=[ga, gb]
  return data
#Creating subgroups through modular arithmetic (Needs to be improved for very large number of groups)
def createSubgroups(x):
  data=[]
  with open('./static/uploads/data.csv', 'r') as datafile:
    reader = csv.reader(datafile, skipinitialspace=False,delimiter=',', quoting=csv.QUOTE_NONE)
    for i in reader:
      data.append(i)
  boys=[]
  girls=[]
  other=[]
  for i in data:
    if i[2]=="Male":
      boys.append(i)
    elif i[2]=="Female":
      girls.append(i)
    elif i[2]=="Other":
      other.append(i)
  ga=[]
  gb=[]
  for i in range(x):
    ga.append('********** Subgroup' + ' ' + str((i+1)) + 'A **********')
    gb.append('********** Subgroup' + ' ' + str((i+1)) + 'B **********')
    c1=0
    c2=0
    c3=0
    for j in boys:
      if j[3]=='A':
        if c1%x==i:
          ga.append(j)
      else:
        if c1%x==i:
          gb.append(j)
      c1+=1
    for j in girls:
      if j[3]=='A':
        if c2%x==i:
          ga.append(j)
      else:
        if c2%x==i:
          gb.append(j)
      c2+=1
    for j in other:
      if j[3]=='A':
        if c3%x==i:
          ga.append(j)
      else:
        if c3%x==i:
          gb.append(j)
      c3+=1
  data=[ga, gb]
  return data

#Function for checking if file is csv
def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower()=="csv"
  
#In the case the file is too large, this function will run
@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

#Redirecting default page to login page
@app.route('/')
def redir():
  return redirect(url_for("login"))

#Simple login page, every other web page will also include "jwtVerify" to check if device has logged in before with cookies
@app.route('/login')
def login():
  if jwtVerify(request.cookies):
    return redirect(url_for("upload"))
  else:
    return render_template("login.html")

#Rendering upload page
@app.route('/upload')
def upload():
  if jwtVerify(request.cookies):
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)
  else:
    return redirect(url_for("login"))

#Login verification/Post handling
@app.route("/lin", methods=["POST"])
def lin():
  data = dict(request.form)
  valid = data["username"] in USERS
  if valid:
    valid = bcrypt.checkpw(data["password"].encode("utf-8"), USERS["janicebailey"])
  msg = "OK" if valid else "Invalid username/password"
  res = make_response(msg, 200)
  if valid:
    res.set_cookie("JWT", jwtSign(data["username"]))
  return res

#Logout
@app.route("/lout", methods=["POST"])
def lout():
  res = make_response("OK", 200)
  res.delete_cookie("JWT")
  return res
    
#For uploading csv file
@app.route('/upload', methods=['POST'])
def upload_files():
  uploaded_file = request.files['file']
  filename = secure_filename(uploaded_file.filename)
  #Saves input file as 'initial input data.csv' so it can be copied and parsed
  if filename != '' and allowed_file(filename):
    filename='initial input data.csv'
    file_ext = os.path.splitext(filename)[1]
    if file_ext not in app.config['UPLOAD_EXTENSIONS']:
      return "Invalid spreadsheet", 400
    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
  #Copying the input data into new csv
  copyInitData()
  return '', 204

#Loads page with student groups, using data from parser
@app.route('/home.html')
def home():
  if jwtVerify(request.cookies):
    return render_template('home.html', data=parse())
  else:
    return redirect(url_for("login"))

#Reloads page with new groups and edited data csv
@app.route("/random/", methods=['POST'])
def random():
  if jwtVerify(request.cookies):
    if 'formA' in request.form:
      data=[]
      attendees=[]
      with open('./static/uploads/data.csv', 'r') as datafile:
        reader = csv.reader(datafile, skipinitialspace=False,delimiter=',', quoting=csv.QUOTE_NONE)
        for i in reader:
          data.append(i)
      if request.method=='POST':
        for i in data:
          if request.form.get(str(i))!=None:
            attendees.append(i)
      with open('./static/uploads/attendance.csv', 'w+') as file:
        writer=csv.writer(file)
        writer.writerows(attendees)
        file.close()
      return redirect(url_for("attendance"))
    else:
      randomizeGroups()
      return render_template('home.html', data=parse())
  else:
    return redirect(url_for("login"))

#Creates subgroups using algorithm function
@app.route("/subgroups/", methods=['POST'])
def subgroups():
  if jwtVerify(request.cookies):
    if request.method == 'POST':
      if 'formA' in request.form:
        data=[]
        attendees=[]
        with open('./static/uploads/data.csv', 'r') as datafile:
          reader = csv.reader(datafile, skipinitialspace=False,delimiter=',', quoting=csv.QUOTE_NONE)
          for i in reader:
            data.append(i)
        if request.method=='POST':
          for i in data:
            if request.form.get(str(i))!=None:
              attendees.append(i)
        with open('./static/uploads/attendance.csv', 'w+') as file:
          writer=csv.writer(file)
          writer.writerows(attendees)
          file.close()
        return redirect(url_for("attendance"))
      else:
        if len(request.form.get("subgroups"))>0:
          return render_template('home.html', data=createSubgroups(int(request.form.get("subgroups"))))
        else:
          return '', 204
  else:
    return redirect(url_for("login"))

#Looks at checked boxes through post and exports csv with attendance
@app.route("/attendance/")
def attendance():
  if jwtVerify(request.cookies):
    with open('./static/uploads/attendance.csv', 'r') as datafile:
      csv=datafile.read()
      return Response(
          csv,
          mimetype="text/csv",
          headers={"Content-disposition":
                   "attachment; filename=attendance.csv"})
  else:
    return redirect(url_for("login"))

#Post handling for attendance, edits attendance csv
@app.route('/home.html', methods=['GET', 'POST'])
def markAttendanceHomePage():
  data=[]
  attendees=[]
  with open('./static/uploads/data.csv', 'r') as datafile:
    reader = csv.reader(datafile, skipinitialspace=False,delimiter=',', quoting=csv.QUOTE_NONE)
    for i in reader:
      data.append(i)
  if request.method == 'POST':
    for i in data:
      if request.form.get(str(i))!=None:
        attendees.append(i)
  with open('./static/uploads/attendance.csv', 'w+') as file:
    writer=csv.writer(file)
    writer.writerows(attendees)
    file.close()
  return redirect(url_for("attendance"))
  
  
#Runs flask app using local port, however repl handles this to run on a domain
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)

