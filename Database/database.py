from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_test_cases():

    print("Received a request")

    username, password = load_user_password()

    try:
        
        data = request.get_json()

        # Check if problem is given in post request
        if 'problem' not in data:
            print("Error 1 Database: Missing 'problem' in the request data")
            return jsonify({'Error 1 Database': 'Missing "problem" in the request data'}), 400
        
        else:

            problem = data['problem']

            uri = "mongodb+srv://" + username + ":" + password + "@main.3vgxubm.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(uri, server_api=ServerApi('1'))
            db = client['qa-repo']
            collection = db['qa']

            test_suite = collection.find_one({"problem_name": problem})
            del test_suite["_id"] # this is needed because the _id field is not json serializable

            if test_suite is None:
                return jsonify({'Error 2 Database': 'Cannot find the problem in the database'}), 500

            return json.dumps(test_suite)
            
    except Exception as e:

        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

        return jsonify({'Error 3 Database': "Didn't receive any json."}), 500
    

def load_user_password():
    """
    Load the username and password from the .env file
    """
    load_dotenv()
    return os.getenv('username'), os.getenv('password')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 7432)