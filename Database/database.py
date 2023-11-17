from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json
from flask_cors import CORS, cross_origin
import collections
import collections.abc
collections.Iterable = collections.abc.Iterable

from flask import Flask, jsonify, request

from mongo_helper import *
from aws_sql_helper import *
from leaderboard_helper import *

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

try:
    client = connect_to_mongo()
    print("DATABASE CONNECTED TO MONGO")

except Exception as e:
    print("DATABASE CANNOT CONNECT TO MONGO")
    print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

try:

    aws_credentials_object = create_AWS_credentials_object()

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)
        print("DATABASE CONNECTED TO AWS")
        connection.close()

    except Exception as e:
        print("DATABASE CANNOT CONNECT TO AWS")
        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

except Exception as e:
    print("DATABASE CANNOT CREATE CREDENTIALS OBJECT.\nCheck if the relevant .env file exist.")
    print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

easy_problems = set()
medium_problems = set()
hard_problems = set()

@app.route('/get_problem_md', methods=['POST'])
@cross_origin(origin='*')
def get_problem_md():

    global client

    print("Received a request to retrieve the markdown of a problem")

    try:
        
        data = request.get_json()

        # Check if problem is given in post request
        if 'problem' not in data:
            print("Error 1 Database: Missing 'problem' in the request data")
            return jsonify({'Error 1 Database': 'Missing "problem" in the request data'})
        
        else:

            problem = data['problem']

            collection = get_collection(
                client = client,
                database_name = 'qa-repo',
                collection_name = 'markdown_repo')

            markdown = collection.find_one({"problem_name" : problem})['markdown']

            if markdown is None:
                return jsonify({'markdown': 'Cannot find the problem in the database'})
            
            else:
                return jsonify({'markdown': markdown})
            
    except Exception as e:

        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

        return jsonify({'markdown': "Didn't receive any json"})

@app.route('/get_problem_md_and_arguments', methods=['POST'])
@cross_origin(origin='*')
def get_problem_md_and_arguments():

    global client

    print("Received a request to retrieve the markdown of a problem")

    try:
        
        data = request.get_json()
        markdown_and_inputs = {}

        # Check if problem is given in post request
        if 'problem' not in data:
            print("Error 1 Database: Missing 'problem' in the request data")
            return jsonify({'Error 1 Database': 'Missing "problem" in the request data'})

        else:

            problem = data['problem']

            collection = get_collection(
                client = client,
                database_name = 'qa-repo',
                collection_name = 'markdown_repo')

            markdown = collection.find_one({"problem_name" : problem})['markdown']

            if markdown is None:
                return jsonify({'markdown': 'Cannot find the problem in the database'})
            
            else:
                markdown_and_inputs['markdown'] = markdown

        collection = get_collection(
            client = client,
            database_name = 'qa-repo',
            collection_name = 'qa')
        
        inputs = collection.find_one({"problem_name" : problem})['inputs']
        
        arguments = []

        for input in inputs:
            
            # remove "input_" from the beginning of the input and "s" from the end of the input
            # if those don't exist, then just append the input

            if input[:6] == "input_":
                input = input[6:]

            if input[-1] == "s":
                input = input[:-1]

            arguments.append(input)

        markdown_and_inputs['arguments'] = arguments

        return jsonify(markdown_and_inputs)
            
    except Exception as e:

        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

        return jsonify({'markdown': "Didn't receive any json"})

@app.route('/get_test_cases', methods=['POST'])
@cross_origin(origin='*')
def get_test_cases():

    global client

    print("Received a request to retrieve test cases")

    try:
        
        data = request.get_json()

        # Check if problem is given in post request
        if 'problem' not in data:
            print("Error 1 Database: Missing 'problem' in the request data")
            return jsonify({'Error 1 Database': 'Missing "problem" in the request data'})
        
        else:

            problem = data['problem']

            collection = get_collection(
                client = client,
                database_name = 'qa-repo',
                collection_name = 'qa')

            test_suite = collection.find_one({"problem_name": problem})
            del test_suite["_id"] # this is needed because the _id field is not json serializable

            if test_suite is None:
                return jsonify({'Error 2 Database': 'Cannot find the problem in the database'})

            return jsonify(test_suite)
            
    except Exception as e:

        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

        return jsonify({'Error 3 Database': "Didn't receive any json."})

@app.route('/get_all_problems', methods=['POST'])
@cross_origin(origin='*')
def get_all_problems():

    global easy_problems
    global medium_problems
    global hard_problems

    global aws_credentials_object

    if len(easy_problems) == 0 and len(medium_problems) == 0 and len(hard_problems) == 0:
        
        print("\n\n\nTOP-------------------------")

        easy_problems = filter_by(
            aws_credentials_object=aws_credentials_object,
            table_name="problems",
            column_name="difficulty",
            filter_value="easy",
            filter_value_type="str"
        )

        easy_problems = [row[0] for row in easy_problems]
        print("EASY PROBLEMS:\n", easy_problems)

        medium_problems = filter_by(
            aws_credentials_object=aws_credentials_object,
            table_name="problems",
            column_name="difficulty",
            filter_value="medium",
            filter_value_type="str"
        )

        medium_problems = [row[0] for row in medium_problems]
        print("MEDIUM PROBLEMS:\n", medium_problems)

        hard_problems = filter_by(
            aws_credentials_object=aws_credentials_object,
            table_name="problems",
            column_name="difficulty",
            filter_value="hard",
            filter_value_type="str"
        )

        hard_problems = [row[0] for row in hard_problems]
        print("HARD PROBLEMS:\n", hard_problems)

        print("\n\n\nBOTTOM-------------------------")

    # prepare the data into json
    data = {
        'easy_problems' : list(easy_problems),
        'medium_problems' : list(medium_problems),
        'hard_problems' : list(hard_problems)
    }

    return jsonify(data)

@app.route('/authenticate', methods=['POST'])
@cross_origin(origin='*')
def authenticate():

    global aws_credentials_object

    try:

        data = request.get_json()

        # Check if problem is given in post request
        if 'username' not in data or 'password' not in data:
            print("Error in Database Container within the authenticate function:\nMissing 'username' or 'password' in the request data")
            return jsonify({'authentication_result' : 'Missing "username" or "password" in the request data'})
        
        else:

            username = data['username']
            password = data['password']

            # get the correct password from the database
            correct_password = get_column2_given_column1(
                aws_credentials_object,
                "user_logins",
                "username",
                "password",
                username)

            if correct_password is None:
                return jsonify({'authentication_result' : "Username Doesn't Exist"})
        
            if correct_password != password:
                return jsonify({'authentication_result' : 'Incorrect Password'})

            else:
                return jsonify({'authentication_result' : 'Success'})
            
    except Exception as e:
        
        print("WHat is going on")

        print ("\n\n\n-----------------------------")
        print("Error in Database Container within the authenticate function.")
        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)
        print ("-----------------------------\n\n\n")

        return jsonify({'authentication_result' : "Didn't receive any json"})

@app.route('/sign_up', methods=['POST'])
@cross_origin(origin='*')
def sign_up():

    global aws_credentials_object

    try:

        data = request.get_json()

        # Check if problem is given in post request
        if 'username' not in data or 'password' not in data:
            print("Error in Database Container within the sign_up function:\nMissing 'username' or 'password' in the request data")
            return jsonify({'sign_up_result': 'Missing "username" or "password" in the request data'})
        
        else:

            username = data['username']
            password = data['password']

            username_exists = check_value_exists(aws_credentials_object, "user_logins", "username", username)

            if username_exists:
                return jsonify({'sign_up_result' : "Username already exists"})
            
            else:

                try:

                    new_login_entry = [username, password]
                    add_entry_to_table(aws_credentials_object, "user_logins", new_login_entry)

                    new_leaderboard_entry = [username, "[]", 0]
                    add_entry_to_table(aws_credentials_object, "leaderboard", new_leaderboard_entry)

                    return jsonify({'sign_up_result' : 'Success'})
                
                except Exception as e:
                    print ("\n\n\n-----------------------------")
                    print("Error in Database Container within the sign_up function.")
                    print("Error encountered at MARK 1")
                    print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)
                    print ("-----------------------------\n\n\n")
                    return jsonify({'sign_up_result' : "Failed"})
            
    except Exception as e:

        print ("\n\n\n-----------------------------")
        print("Error in Database Container within the sign_up function.")
        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)
        print ("-----------------------------\n\n\n")

        return jsonify({'sign_up_result' : "Didn't receive any json"})

@app.route('/update_leaderboard', methods=['POST'])
@cross_origin(origin='*')
def update_leaderboard():

    global aws_credentials_object

    try:

        data = request.get_json()

        # Check if problem is given in post request
        if 'username' not in data:
            print("Error in Database Container within the update_learderboard function:\nMissing 'username' in the request data")
            return jsonify({'update_leaderboard_result': 'Missing "username" in the request data'})
        
        else:

            username = data['username']
            newly_solved_problem = data['newly_solved_problem']

            username_exists = check_value_exists(aws_credentials_object, "user_logins", "username", username)

            if username_exists:
                
                result = update_leaderboard_database(
                    aws_credentials_object=aws_credentials_object,
                    username=username,
                    newly_solved_problem=newly_solved_problem
                )

                if result == "Success":
                    return jsonify({'update_leaderboard_result' : 'Success'})
                
                else:
                    return jsonify({'update_leaderboard_result' : 'Failed'})
            
            else:
                print("Error in Database Container within the update_learderboard function:\nThe username doesn't exist.")
                return jsonify({'update_leaderboard_result' : "The username does not exist"})
            
    except Exception as e:

        print ("\n\n\n-----------------------------")
        print("Error in Database Container within the update_leaderboard function.")
        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)
        print ("-----------------------------\n\n\n")

        return jsonify({'update_leaderboard_result' : "Didn't receive any json"})
    
@app.route('/get_top_users', methods=['POST'])
@cross_origin(origin='*')
def get_top_users():

    print("\n\n\nDatabase /get_top_users endpoint is called\n\n\n")

    global aws_credentials_object

    try:

        data = request.get_json()
        user_number = data['user_number']

        print("\n\n\nDatabase Receives Request to Print Out Top", user_number, "Users\n\n\n")

        result = get_top_n_users(aws_credentials_object, user_number)
        return jsonify({'get_top_users_result' : result})
        
    except Exception as e:

        print ("\n\n\n-----------------------------")
        print("Error in Database Container within the get_top_users function.")
        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)
        print ("-----------------------------\n\n\n")

        return jsonify({'update_leaderboard_result' : "Didn't receive any json"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 7432)