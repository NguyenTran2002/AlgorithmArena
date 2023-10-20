from flask import Flask, request, render_template, jsonify
import markdown
import requests

app = Flask(__name__)

problem = "binary_search"

# Define the path to the Markdown problem file
problem_file = 'Problems/' + problem + '.md'
evaluation_service_url = 'http://evaluation:1111'  # Replace with the actual URL of the evaluation microservice
database_url = 'http://database:7432'

@app.route('/', methods=['GET', 'POST'])
def index():

    # display the problem in the browser
    with open(problem_file, 'r') as f:
        markdown_text = f.read()
        html_text = markdown.markdown(markdown_text)

    # get all available problems from the database
    try:

        response = requests.post(database_url + '/get_all_problems')
        response_data = response.json()
        problems = response_data["problems"]

    except Exception as e:
        message = f"Error 1 main while retrieving all problems: {str(e)}"
        print(message)
        problems = []  # Set an empty list if there's an error

    # send user's code to the evaluation microservice
    if request.method == 'POST':
        
        user_code = request.form['user_code']
        selected_problem = request.form['problem']
        
        # Prepare data to send to the evaluation microservice
        data = {
            "user_code": user_code,
            "problem": selected_problem
        }
        
        # Send a POST request to the evaluation microservice
        try:
            response = requests.post(evaluation_service_url, json = data)
            response_data = response.json()
            message = response_data["result"]

        except Exception as e:
            message = f"Error 2 main: {str(e)}"
            print(message)
        
        return render_template('result.html', problem = html_text, message = message)
    
    return render_template('index.html', problem = html_text, problems = problems)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 2727)