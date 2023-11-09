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
from leaderboard_helper import *

app = Flask(__name__)
CORS(app)

try:
    client = connect_to_mongo()
    print("DATABASE CONNECTED TO MONGO")

except Exception as e:
    print("DATABASE CANNOT CONNECT TO MONGO")
    print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

try:
    aws_host, aws_port, aws_user, aws_password, aws_database = load_aws_connection_properties()
    aws_connection, aws_cursor = connect_to_aws(aws_host, aws_port, aws_user, aws_password, aws_database)
    print("DATABASE CONNECTED TO AWS")

except Exception as e:
    print("DATABASE CANNOT CONNECT TO AWS")
    print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

easy_problems = set()
medium_problems = set()
hard_problems = set()

@app.route('/get_problem_md', methods=['POST'])
def get_problem_md():

    global client

    print("Received a request to retrieve the markdown of a problem")

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
                collection_name = 'markdown_repo')

            markdown = collection.find_one({"problem_name" : problem})['markdown']

            if markdown is None:
                return jsonify({'markdown': 'Cannot find the problem in the database'}), 500
            
            else:
                return jsonify({'markdown': markdown})
            
    except Exception as e:

        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

        return jsonify({'markdown': "Didn't receive any json"}), 500

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

    global easy_problems
    global medium_problems
    global hard_problems

    global aws_connection
    global aws_cursor

    if len(easy_problems) == 0 and len(medium_problems) == 0 and len(hard_problems) == 0:
        
        print("\n\n\nTOP-------------------------")

        easy_problems = filter_by(
            cursor=aws_cursor,
            table_name="problems",
            column_name="difficulty",
            filter_value="easy",
            filter_value_type="str"
        )

        print("EASY PROBLEMS:\n", easy_problems)

        medium_problems = filter_by(
            cursor=aws_cursor,
            table_name="problems",
            column_name="difficulty",
            filter_value="medium",
            filter_value_type="str"
        )

        print("MEDIUM PROBLEMS:\n", medium_problems)

        hard_problems = filter_by(
            cursor=aws_cursor,
            table_name="problems",
            column_name="difficulty",
            filter_value="hard",
            filter_value_type="str"
        )

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
def authenticate():

    global aws_connection
    global aws_cursor

    try:

        data = request.get_json()

        # Check if problem is given in post request
        if 'username' not in data or 'password' not in data:
            print("Error in Database Container within the authenticate function:\nMissing 'username' or 'password' in the request data")
            return jsonify({'authentication_result' : 'Missing "username" or "password" in the request data'}), 400
        
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

        print ("\n\n\n-----------------------------")
        print("Error in Database Container within the authenticate function.")
        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)
        print ("-----------------------------\n\n\n")

        return jsonify({'authentication_result' : "Didn't receive any json"}), 500

@app.route('/sign_up', methods=['POST'])
def sign_up():

    global aws_connection
    global aws_cursor

    try:

        data = request.get_json()

        # Check if problem is given in post request
        if 'username' not in data or 'password' not in data:
            print("Error in Database Container within the sign_up function:\nMissing 'username' or 'password' in the request data")
            return jsonify({'sign_up_result': 'Missing "username" or "password" in the request data'}), 400
        
        else:

            username = data['username']
            password = data['password']

            username_exists = check_value_exists(aws_cursor, "user_logins", "username", username)

            if username_exists:
                return jsonify({'sign_up_result' : "Username already exists"}), 500
            
            else:

                try:
                    new_entry = [username, password]
                    add_entry_to_table(aws_connection, aws_cursor, "user_logins", new_entry)
                    return jsonify({'sign_up_result' : 'Success'})
                
                except Exception as e:
                    print ("\n\n\n-----------------------------")
                    print("Error in Database Container within the sign_up function.")
                    print("Error encountered at MARK 1")
                    print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)
                    print ("-----------------------------\n\n\n")
                    return jsonify({'sign_up_result' : "Failed"}), 500
            
    except Exception as e:

        print ("\n\n\n-----------------------------")
        print("Error in Database Container within the sign_up function.")
        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)
        print ("-----------------------------\n\n\n")

        return jsonify({'sign_up_result' : "Didn't receive any json"}), 500

@app.route('/update_leaderboard', methods=['POST'])
def update_leaderboard():

    global aws_connection
    global aws_cursor

    try:

        data = request.get_json()

        # Check if problem is given in post request
        if 'username' not in data:
            print("Error in Database Container within the update_learderboard function:\nMissing 'username' in the request data")
            return jsonify({'update_leaderboard_result': 'Missing "username" in the request data'}), 400
        
        else:

            username = data['username']
            newly_solved_problem = data['newly_solved_problem']

            username_exists = check_value_exists(aws_cursor, "user_logins", "username", username)

            if username_exists:
                
                result = update_leaderboard_database(
                    connection=aws_connection,
                    cursor=aws_cursor,
                    username=username,
                    newly_solved_problem=newly_solved_problem
                )

                if result == "Success":
                    return jsonify({'update_leaderboard_result' : 'Success'})
                
                else:
                    return jsonify({'update_leaderboard_result' : 'Failed'}), 500
            
            else:
                print("Error in Database Container within the update_learderboard function:\nThe username doesn't exist.")
                return jsonify({'update_leaderboard_result' : "The username does not exist"}), 400
            
    except Exception as e:

        print ("\n\n\n-----------------------------")
        print("Error in Database Container within the update_leaderboard function.")
        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)
        print ("-----------------------------\n\n\n")

        return jsonify({'update_leaderboard_result' : "Didn't receive any json"}), 500
    
@app.route('/get_top_users', methods=['POST'])
def get_top_users():

    global aws_connection
    global aws_cursor

    try:

        data = request.get_json()

        # Check if problem is given in post request

        user_number = data['user_number']
        result = get_top_n_users(aws_cursor, user_number)
        return jsonify({'get_top_users_result' : result})
        
    except Exception as e:

        print ("\n\n\n-----------------------------")
        print("Error in Database Container within the update_leaderboard function.")
        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)
        print ("-----------------------------\n\n\n")

        return jsonify({'update_leaderboard_result' : "Didn't receive any json"}), 500
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 7432)