from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json

from flask import Flask, jsonify, request

from helper import *

app = Flask(__name__)

client = connect_to_mongo()
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 7432)