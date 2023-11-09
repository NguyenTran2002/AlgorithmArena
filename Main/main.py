from flask import Flask, request, render_template, session, jsonify, redirect, url_for
from flask_session import Session
import markdown
import requests

from helper import *

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SECRET_KEY"] = 'Unicorn Rainbow Eating Ice Cream Cone'
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = '/session/flask_session'
Session(app)

problems = []  # List of all available problems

# Define the path to the Markdown problem file
evaluation_service_url = 'http://evaluation:1111'  # Replace with the actual URL of the evaluation microservice
database_url = 'http://database:7432'

print("\n\n\n\n_____________________________\n")
print("Access the REACT application at\nhttp://localhost:8080")
print("\n\nAccess the LEGACY FLASK application at\nhttp://localhost:2727")
print("_____________________________\n\n\n\n")



@app.route('/', methods=['GET', 'POST'])
def index():

    global problems

    # get all available problems from the database
    try:

        response = requests.post(database_url + '/get_all_problems')
        response_data = response.json()
        problems = response_data["problems"]

    except Exception as e:
        message = f"Error 1 main while retrieving all problems: {str(e)}"
        print(message)
        problems = []  # Set an empty list if there's an error

    if request.method == 'POST':
        session["selected_problem"] = request.form['problem']
        return redirect(url_for('solve'))
    
    return render_template('index.html', problems=problems)

# -----------------------------------

@app.route('/solve', methods=['GET', 'POST'])
def solve():

    problem_file = 'Problems/' + session["selected_problem"] + '.md'

    # display the problem in the browser
    with open(problem_file, 'r') as f:
        markdown_text = f.read()
        selected_problem_html = markdown.markdown(markdown_text)

    # send user's code to the evaluation microservice
    if request.method == 'POST':
        
        user_code = request.form['user_code']
        
        # Prepare data to send to the evaluation microservice
        data = {
            "user_code": user_code,
            "problem": session["selected_problem"]
        }
        
        # Send a POST request to the evaluation microservice
        try:
            response = requests.post(evaluation_service_url, json = data)
            response_data = response.json()
            message = response_data["result"]
            success = bool(response_data["success"])

        except Exception as e:
            message = f"Error 2 main: {str(e)}"
            print(message)
        
        if success == True:
            return render_template('result_success.html', problem = selected_problem_html, message = message)
        
        else:
            return render_template('result_failure.html', problem = selected_problem_html, message = message)
    
    return render_template(
        'solve.html',
        problem_markdown = selected_problem_html,
        problems = problems
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 2727)