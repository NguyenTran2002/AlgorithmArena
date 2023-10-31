from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json
from flask_cors import CORS
import collections
import collections.abc
collections.Iterable = collections.abc.Iterable

from flask import Flask, jsonify, request

from mongo_helper import *
from aws_sql_helper import *

app = Flask(__name__)
CORS(app)

client = connect_to_mongo()

aws_host, aws_port, aws_user, aws_password, aws_database = load_aws_connection_properties()
aws_connection, aws_cursor = connect_to_aws(aws_host, aws_port, aws_user, aws_password, aws_database)

all_problems = set()

@app.route('/get_test_cases', methods=['POST'])
def get_test_cases():

    global client

    print("Received a request to retrieve test cases")

    try:
        
        data = request.get_json()

        # Check if problem is given in post request
        if 'problem' not in data:
            print("Error 1 Database: Missing 'problem' in the request data")
            return jsonify({'Error 1 Database': 'Missing "problem" in the request data'}), 400
        
        else:

            problem = data['problem']

            collection = get_collection(
                client = client,
                database_name = 'qa-repo',
                collection_name = 'qa')

            test_suite = collection.find_one({"problem_name": problem})
            del test_suite["_id"] # this is needed because the _id field is not json serializable

            if test_suite is None:
                return jsonify({'Error 2 Database': 'Cannot find the problem in the database'}), 500

            return jsonify(test_suite)
            
    except Exception as e:

        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

        return jsonify({'Error 3 Database': "Didn't receive any json."}), 500
    

@app.route('/get_all_problems', methods=['POST'])
def get_all_problems():

    global client
    global all_problems

    if len(all_problems) == 0:

        collection = get_collection(client = client,
            database_name = 'qa-repo',
            collection_name = 'qa')
        
        for problem in collection.find():
            all_problems.add(problem['problem_name'])

    # prepare the data into json
    data = {'problems' : list(all_problems)}

    return jsonify(data)


@app.route('/authenticate', methods=['POST'])
def authenticate():

    global aws_connection
    global aws_cursor

    try:

        data = request.get_json()

        # Check if problem is given in post request
        if 'username' not in data or 'password' not in data:
            print("Error 1 Database: Missing 'username' or 'password' in the request data")
            return jsonify({'Error 1 Database': 'Missing "username" or "password" in the request data'}), 400
        
        else:

            username = data['username']
            password = data['password']

            # get the correct password from the database
            correct_password = get_column2_given_column1(
                aws_cursor,
                "user_logins",
                "username",
                "password",
                username)

            if correct_password is None:
                return jsonify({'authentication_result' : "Username Doesn't Exist"}), 500
        
            if correct_password != password:
                return jsonify({'authentication_result' : 'Incorrect Password'}), 500

            else:
                return jsonify({'authentication_result' : 'Success'})
            
    except Exception as e:

        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

        return jsonify({'Error 1 Database': "Didn't receive any json."}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 7432)