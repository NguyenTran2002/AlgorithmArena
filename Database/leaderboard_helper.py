import pymysql
from dotenv import load_dotenv
import os
from aws_sql_helper import *

"""
1. given a username and problem solved, then will add that to database, need to check if problem already in solved list
2. return x number of users that have solved the most problems
"""

def update_problem_list(username, solved_problem, cursor, connection):
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
    if solved_problem not in solved_problems:
        solved_problems = solved_problems[1:-1]
        solved_problems = '[' + solved_problems + ", " + solved_problem + "]"
        num_problems_solved += 1
    
    # update_row method was not in aws sql helper in database but in the aws console version, updated aws sql helper
    # in the database folder
    update_row(connection = connection,
    cursor = cursor,
    table_name = 'leaderboard',
    identifier_column = 'username',
    identifier_value = 'albert',
    edit_column = 'solved_problems',
    new_value = solved_problems
)
    update_row(connection = connection,
    cursor = cursor,
    table_name = 'leaderboard',
    identifier_column = 'username',
    identifier_value = 'albert',
    edit_column = 'number_of_solved_problems',
    new_value = num_problems_solved
)
    
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