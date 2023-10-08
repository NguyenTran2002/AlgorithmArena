from flask import Flask, request, render_template, jsonify
import markdown
import requests

app = Flask(__name__)

problem = "binary_search"

# Define the path to the Markdown problem file
problem_file = 'Problems/' + problem + '.md'
evaluation_service_url = 'http://evaluation:1111'  # Replace with the actual URL of the evaluation microservice

@app.route('/', methods=['GET', 'POST'])
def index():

    with open(problem_file, 'r') as f:
        markdown_text = f.read()
        html_text = markdown.markdown(markdown_text)
    
    if request.method == 'POST':
        
        user_code = request.form['user_code']
        
        # Prepare data to send to the evaluation microservice
        data = {
            "user_code": user_code,
            "problem": problem
        }
        
        # Send a POST request to the evaluation microservice
        try:
            response = requests.post(evaluation_service_url, json = data)
            response_data = response.json()
            message = response_data["result"]

        except Exception as e:
            message = f"Error1 main: {str(e)}"
        
        return render_template('result.html', problem = html_text, message = message)
    
    return render_template('index.html', problem=html_text)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 2727)