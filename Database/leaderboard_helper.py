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
def update_leaderboard_database(connection, cursor, username, newly_solved_problem):
    """
    DESCRIPTION:
        When called, this function will update the leaderboard database to reflect the newly solved problem by the user.

    INPUT SIGNATURE:
        connection: connection object
        cursor: cursor object
        username: string
        newly_solved_problem: string

    OUTPUT SIGNATURE:
        "Success" if the database was updated successfully, otherwise an error message will be returned.
    """

    try:

        # find correct row given username in db
        # update both value of problem list and problem number
        solved_problems = get_column2_given_column1(
            cursor = cursor,
            table_name = 'leaderboard',
            column_1 = 'username',
            column_2 = 'solved_problems',
            column_1_val = username
        )

        num_problems_solved = get_column2_given_column1(
            cursor = cursor,
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
            connection = connection,
            cursor = cursor,
            table_name = 'leaderboard',
            identifier_column = 'username',
            identifier_value = username,
            edit_column = 'solved_problems',
            new_value = solved_problems
        )

        update_row(
            connection = connection,
            cursor = cursor,
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
    
def get_best_users(cursor, connection, users_wanted):
    try:
        query = f"SELECT username, solved_problems, num_problems_solved FROM leaderboard order by number_of_solved_problems DESC LIMIT {users_wanted}"
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        print(f"Result of x most solved problems users' saved successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    return result