from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json

def load_user_password():
    """
    Load the username and password from the .env file
    """
    load_dotenv()
    return os.getenv('username'), os.getenv('password]')

def connect_to_mongo():
    """
    Return the MongoClient object
    """

    username, password = load_user_password()
    uri = "mongodb+srv://" + username + ":" + password + "@main.3vgxubm.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(uri, server_api=ServerApi('1'))

    return client

def get_collection(client, database_name, collection_name):
    """
    Return the collection from the database
    """
    db = client[database_name]
    collection = db[collection_name]
    return collection

def get_problem_tests_and_answers(problem_name):
    """
    Return the test cases and answers for the given problem
    """
    client = connect_to_mongo()
    collection = get_collection(client, 'qa-repo', 'qa')

    test_suite = collection.find_one({'problem_name': problem_name})

    if test_suite is None:
        return None, None

    return test_suite['test_cases'], test_suite['answers']