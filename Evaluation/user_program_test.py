import json
import os
from binary_search_test import Solution
"""
This function imports a .py file that has the user written program, runs it, and returns whether the program
passed all test cases, or if not returns the test case that it failed on in a json object.
"""
folder_path = "QnA/test_cases_and_answers"
file_name = "binary_search.json"

def main():
    my_solution = Solution()
    full_file_path = os.path.join(folder_path, file_name)
    with open(full_file_path, 'r') as json_file:
        binary_search_info = json.load(json_file)
    arr_length = len(binary_search_info["input_arrays"])
    for i in range(arr_length):
        result = my_solution.search(binary_search_info["input_arrays"][i], binary_search_info["input_targets"][i])
        if result != binary_search_info["answers"][i]:
            result = {
                "input_array" : binary_search_info["input_arrays"][i],
                "input_target" : binary_search_info["input_targets"][i],
                "expected answer" : binary_search_info["answers"][i],
                "your answer" : result
            }
            return result
    return "You passed all the test cases, congrats!"



if __name__ == "__main__":
    print(main())