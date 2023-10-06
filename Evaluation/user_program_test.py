import json
from flask import Flask, request, jsonify
import os
import requests
# from binary_search_test import Solution
import save_string_as_py
from user_binary_search import Solution
"""
This function imports a .py file that has the user written program, runs it, and returns whether the program
passed all test cases, or if not returns the test case that it failed on in a json object.
"""
folder_path = "QnA/test_cases_and_answers"
file_name = "binary_search.json"

main_url = 'http://Main:2727'
database_url = 'http://Databases/7432'


def main():
    """
    1. get the json object from main that has
        "user_code" : user code that is in str format
        "problem" : name of problem ex. binary search (need to check if it's like binary search or binarySearch)
    2. get the corresponding test cases (input arr, input num, etc) and answers from database
    3. take the user_code str and run save_string_as_py func
    4. run the .py code function and run it using test cases you got from the database
    5. depending on whether it matches the answers from database json obj, return a json obj:
        "result" : either you didn't pass all test cases or congratulations you did
    """

    # doing number 1
    try:
        data = request.get_json()
        main_response_data = data.json()
        data_dict = json.load(main_response_data)
    except Exception as e:
        message = f"Error: {str(e)}"

    # doing number 2
    try:
        problem_name = {
            "problem": data_dict["problem"]
        }
        data = requests.post(database_url, json=jsonify(problem_name))
        database_response_data = data.json()
        test_cases_answers = json.load(database_response_data)
    except Exception as e:
         message = f"Error: {str(e)}"
    
    # doing number 3
    save_string_as_py("user_binary_search.py", data_dict["user_code"])

    # doing number 4 (assuming import works with save_string_as_py file)
    my_solution = Solution()
    passed = True
    arr_length = len(test_cases_answers["input_arrays"])
    for i in range(arr_length):
        result = my_solution.binary_search(test_cases_answers["input_arrays"][i], test_cases_answers["input_targets"][i])
    # doing number 5
        if result != test_cases_answers["answers"][i]:
            passed = False
            result = {
                "result" : "You did not pass all the test cases :("
            }
            break
    if passed:
        result = {
            "result" : "You passed all the test cases, congrats!"
        }
    return jsonify(result)



if __name__ == "__main__":
    main()