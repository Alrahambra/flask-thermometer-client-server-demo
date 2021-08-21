#!/usr/bin/python3

from functions import ThermalDataValidator, Store_thermo_entry
from config import *
from flask_restful import Resource, Api, abort
from flask import Flask, jsonify, request, escape, make_response
from flask_httpauth import HTTPBasicAuth, Response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
#####################################################
#Initial setup
app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

users = {
    "api": generate_password_hash(api_pass)
}

#Really basic HTTP authentication block, in real world passwords should be also salted etc.
@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@auth.error_handler
def custom_401(error):
    errordata = {'status': 'AUTH_FAILURE', 'code': 401, 'resolution': 'CHECK_CREDENTIALS'}
    return make_response(jsonify(errordata)), 401

#Classes and functions
#####################################################
class RecordTemp(Resource):
    @auth.login_required
    def get(self):
        #Gives temperature data
        return "Nothing to return yet"

    @auth.login_required
    def post(self):
        #Receives temperature data as JSON
        tempdata = request.json
        #Validate form inputs
        if ThermalDataValidator(tempdata):
            #Store here and return input
            tempdata['status'] = {}
            tempdata['status'] = "SUCCESS"
            tempdata['device_id'] = {}
            #User agent identifies our devices, escaping string just in case someone should get their hand on the thermometer...
            device_id = escape(request.headers.get('User-Agent'))
            #other necessary values from json
            temp = request.json['temperature']
            humidity = request.json['humidity']
            timestamp  = request.json['timestamp']
            tempdata['device_id'] = device_id

            #In case we don't know or want to rely on server time
            if timestamp == 0:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #Ready to store into DB...
            write_db = Store_thermo_entry(device_id, temp, humidity,timestamp)
            if write_db:
                return jsonify(tempdata)
            #if write_db:
            else:
                errordata = {'status': 'SQLERROR', 'code': 500, 'resolution': 'INVESTIGATE_SYSLOG'}
                return make_response(jsonify(errordata), 500)
            
            
        else:
            errordata = {'status': 'INVALID_JSON_INPUT', 'code': 401, 'resolution': 'FIX_INPUT'}
            return make_response(jsonify(errordata), 401)
#Routing
api.add_resource(RecordTemp, '/records')
 
##########################################################
if __name__ == "__main__":
    #Because this would be behind gunicorn + apache2/nginx/other www-server
    app.run(host='127.0.0.1')