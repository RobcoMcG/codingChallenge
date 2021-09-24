# -*- coding: utf-8 -*-
"""
@author: Robert McGuinness
"""

from flask import Flask, render_template, url_for, jsonify, request, redirect
from flask_restful import Api, Resource
import requests
import json

app = Flask(__name__)
api = Api(app)

class Supervisor():
    def __init__(self, sID, sPhone, sJurisdiction, sIDN, sFirstName, sLastName):
        self.sID = sID if sID is not None else ""
        self.sPhone = sPhone if sPhone is not None else ""
        self.sJurisdiction = sJurisdiction
        self.sIDN = sIDN if sIDN is not None else ""
        self.sFirstName = sFirstName
        self.sLastName = sLastName
    
def populateSupervisors(data):
    supervisors = []
    for item in data:
        if item['jurisdiction'].isdigit():
            pass        
        else:
            supervisors.append(Supervisor(item['id'], item['phone'], item['jurisdiction'], item['identificationNumber'], item['firstName'], item['lastName']))
    return supervisors
    
def filterSupervisors(supervisors):
    for s in supervisors:
        if s.sJurisdiction.isdigit():
            supervisors.remove(s)    
    supervisors = sorted(supervisors, key=lambda x: (x.sJurisdiction, x.sLastName, x.sFirstName))
    return supervisors

def validate(firstName, lastName, supervisor):
    if firstName == None or lastName == None or supervisor == None:
        return False
    else:
        return True

@app.route("/", methods={'GET', 'POST'})
def index():
    return render_template('index.html')
    
@app.route("/new_entry", methods={'GET', 'POST'})
def new():
    if (request.method == 'POST'):
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        supervisor = request.form['supervisor']
        valid = validate(firstName, lastName, supervisor)
        if (valid):
            print(f'Entry {firstName} {lastName}, {email}, {phoneNumber}, {supervisor} added!')
            return redirect(url_for('index'))
        if (valid == False):
            error = "Missing required field"
            return render_template('new_supervisor', error=error)
    else:
        return render_template('new_supervisor.html')

@app.route("/supervisors", methods={'GET', 'POST'})
def getSupervisorList():
    req = requests.get("https://o3m5qixdng.execute-api.us-east-1.amazonaws.com/api/managers")
    data = req.content
    json_data = json.loads(data)
    supervisors = populateSupervisors(json_data)
    supervisors = filterSupervisors(supervisors)
    return render_template('supervisors.html', data=supervisors)

@app.route("/about", methods={"GET"})
def about():
    return render_template('about.html')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    app.run(debug=True)