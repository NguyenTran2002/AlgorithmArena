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
            print("GEOFFREY\n\n\ngetting before request\n\n\n")
            response = requests.post(evaluation_service_url, json = data)
            print("NGUYEN got past this line")
            # print("HELLO", response.content, "GOODBYE")
            # print("TYPESTART", type(response), "TYPEEND")
            response_data = response.json()
            print("past response")
            # message = response_data.get('result', 'Error: No response from the evaluation microservice')
            message = response_data["result"]
            print("past message initialize")
            # message = response.get('result', 'Error: No response from the evaluation microservice')

        except Exception as e:
            message = f"Error1 main: {str(e)}"
        
        return render_template('result.html', problem = html_text, message = message)
    
    return render_template('index.html', problem=html_text)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 2727)