import json
from flask import Flask, request, jsonify, Response
import os
import requests
from exec_class import run_method_from_string

"""
This function imports a .py file that has the user written program, runs it, and returns whether the program
passed all test cases, or if not returns the test case that it failed on in a json object.
"""

main_url = 'http://main:2727'
database_url = 'http://database:7432/get_test_cases'

app = Flask(__name__)

@app.route('/', methods=['POST'])
def evaluate():
    """
    1. get the json object from main that has
        "user_code" : user code that is in str format
        "problem" : name of problem ex. binary search (need to check if it's like binary search or binarySearch)
    2. get the corresponding test cases (input arr, input num, etc) and answers from database
    3. run the .py code function and run it using test cases you got from the database
    4. depending on whether it matches the answers from database json obj, return a json obj:
        "result" : either you didn't pass all test cases or congratulations you did
    """

    # doing number 1
    try:
        data_dict = request.get_json()

    except Exception as e:
        message = f"Error1 eval: {str(e)}"

    # doing number 2
    try:
        problem_name = {
            "problem": data_dict["problem"]
        }

        data = requests.post(database_url, json=problem_name)
        test_cases_answers = data.json()

    except Exception as e:
        message = f"Error2 eval: {str(e)}"

    # doing number 3
    passed = True
    params = []
    num_testcases = len(test_cases_answers[test_cases_answers["inputs"][0]])
    for param in test_cases_answers["inputs"]:
        for key in test_cases_answers:
            if key == param:
                params.append(test_cases_answers[key])
    for i in range(num_testcases): # may want to find a better way to pass params than hard-coded if statements
        if len(params) == 1:
            sol_result = run_method_from_string(data_dict["user_code"],
                "Solution",
                test_cases_answers["problem_name"],
                [params[0][i]])
        elif len(params) == 2:
            sol_result = run_method_from_string(data_dict["user_code"],
                "Solution",
                test_cases_answers["problem_name"],
                [params[0][i], params[1][i]])
        elif len(params) == 3:
            sol_result = run_method_from_string(data_dict["user_code"],
                "Solution", test_cases_answers["problem_name"],
                [params[0][i], params[1][i], params[2][i]])
        elif len(params) == 4:
            sol_result = run_method_from_string(data_dict["user_code"], 
                "Solution", test_cases_answers["problem_name"], 
                [params[0][i], params[1][i], params[2][i], params[3][i]])
        elif len(params) == 5:
            sol_result = run_method_from_string(data_dict["user_code"],
                "Solution", test_cases_answers["problem_name"],
                [params[0][i], params[1][i], params[2][i], params[3][i], params[4][i]])
        else:
            sol_result = "Error: More than 5 parameters"
    
    # doing number 4
        answer = test_cases_answers["answers"][i]
        if sol_result != answer:
            passed = False
            result = {
                "result" : f"You did not pass all the test cases :(. You messed up on test case number {i+1}. Your answer was: {sol_result}, but the actual answer was: {answer}"
            }
            break
    if passed:
        result = {
            "result" : "You passed all the test cases, congrats!"
        }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port = 1111)