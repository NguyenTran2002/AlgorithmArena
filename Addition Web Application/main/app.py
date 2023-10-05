from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

RANDOM_API_URL = 'http://random:4747/random-number'
ADD_API_URL = 'http://add:3737/add'

@app.route('/', methods=['GET', 'POST'])
def add_numbers():
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        
        # Fetch a random number from the random API
        response = requests.get(RANDOM_API_URL)
        random_number = response.json()['random_number']
        
        # Prepare data for the add API
        data = {'num1': num1, 'num2': num2}
        
        # Make a POST request to the add API
        response = requests.post(ADD_API_URL, json=data) # ADD API CURRENTLY HAVE PROBLEMS
        result = response.json()['result']

        # add the random number to the result
        result += random_number
        
        return render_template('result.html', num1=num1, num2=num2, random_number=random_number, result=result)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2727)