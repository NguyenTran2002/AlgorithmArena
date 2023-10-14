import json
from flask import Flask, request, jsonify, Response
import os
import requests
from exec_class import run_method_from_string

"""
This function imports a .py file that has the user written program, runs it, and returns whether the program
passed all test cases, or if not returns the test case that it failed on in a json object.
"""
folder_path = "QnA/test_cases_and_answers"
file_name = "binary_search.json"

main_url = 'http://main:2727'
database_url = 'http://database:7432'

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
    arr_length = len(test_cases_answers["input_arrays"])
    for i in range(arr_length):
        result = run_method_from_string(data_dict["user_code"], "Solution", "binary_search", [test_cases_answers["input_arrays"][i], test_cases_answers["input_targets"][i]])
    # doing number 4
        answer = test_cases_answers["answers"][i]
        if result != answer:
            passed = False
            result = {
                "result" : f"You did not pass all the test cases :(. You messed up on test case number {i+1} the actual answer was: {answer}"
            }
            break
    if passed:
        result = {
            "result" : "You passed all the test cases, congrats!"
        }
    return jsonify(result)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port = 1111)