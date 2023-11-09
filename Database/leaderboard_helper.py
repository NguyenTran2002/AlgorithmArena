import pymysql
from dotenv import load_dotenv
import os
from aws_sql_helper import *

"""
The function expects a JSON object with 4 fields

    'username' : string
    'solved_problem' : string
    'cursor' : cursor object
    'connection' : connection object

The function doesn't return anything

    'authentication_result' : 'string'

The result will be 1 of the following 3 possibilities

'Username Doesn't Exist'
'Incorrect Password'
'Success'

This function will take in the username and the problem the user just solved, and check if the user has already
solved it. If not, it will update the database to contain the newly solved problem.

"""
def update_leaderboard_database(aws_credentials_object, username, newly_solved_problem):
    """
    DESCRIPTION:
        When called, this function will update the leaderboard database to reflect the newly solved problem by the user.

    INPUT SIGNATURE:
        aws_credentials_object: AWS credentials object (check aws_sql_helper.py for more info)
        username: string
        newly_solved_problem: string

    OUTPUT SIGNATURE:
        "Success" if the database was updated successfully, otherwise an error message will be returned.
    """

    try:

        # find correct row given username in db
        # update both value of problem list and problem number
        solved_problems = get_column2_given_column1(
            aws_credentials_object=aws_credentials_object,
            table_name = 'leaderboard',
            column_1 = 'username',
            column_2 = 'solved_problems',
            column_1_val = username
        )

        num_problems_solved = get_column2_given_column1(
            aws_credentials_object=aws_credentials_object,
            table_name = 'leaderboard',
            column_1 = 'username',
            column_2 = 'number_of_solved_problems',
            column_1_val = username
        )

        # want to check if problem already solved then don't need this code
        if newly_solved_problem not in solved_problems:
            solved_problems = solved_problems[1:-1]
            solved_problems = '[' + solved_problems + ", " + newly_solved_problem + "]"
            num_problems_solved += 1
        
        # update_row method was not in aws sql helper in database but in the aws console version, updated aws sql helper
        # in the database folder
        update_row(
            aws_credentials_object=aws_credentials_object,
            table_name = 'leaderboard',
            identifier_column = 'username',
            identifier_value = username,
            edit_column = 'solved_problems',
            new_value = solved_problems
        )

        update_row(
            aws_credentials_object=aws_credentials_object,
            table_name = 'leaderboard',
            identifier_column = 'username',
            identifier_value = username,
            edit_column = 'number_of_solved_problems',
            new_value = num_problems_solved
        )

        return "Success"
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return e

"""
The function expects a JSON object with 3 fields

    'cursor' : cursor object
    'connection' : connection object
    'users_wanted' : int

The function returns a list of tuples that has the X users with the most solved problems

    'result' : 'list of tuples'

This function will take in the number of users wanted and return the top X users with the
most problems solved in a tuple format.
"""
    
def get_top_n_users(aws_credentials_object, n):
    """
    DESCRIPTION:
        Return the top n users with the most problems solved.
        The format is a 2D array.

    INPUT SIGNATURE:
        aws_credentials_object: AWS credentials object (check aws_sql_helper.py for more info)
        n: int (number of top users wanted)

    OUTPUT SIGNATURE:
        top_n_users_and_number_of_solved_problems: 2D array
            1st place user is top_n_users_and_number_of_solved_problems[0]
                - To get the username, do top_n_users_and_number_of_solved_problems[0][0]
                - To get the number of solved problems, do top_n_users_and_number_of_solved_problems[0][1]
    """

    rows = get_table_sorted_by(
        aws_credentials_object=aws_credentials_object,
        table_name = "leaderboard",
        sort_column = "number_of_solved_problems"
        )
    
    top_n_users_and_number_of_solved_problems = []

    for i in range(n):
        top_n_users_and_number_of_solved_problems.append([rows[i][0], rows[i][2]])

    return top_n_users_and_number_of_solved_problems