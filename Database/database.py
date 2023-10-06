import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def get_test_cases():

    try:
        
        data = request.get_json()

        # Check if problem is given in post request
        if 'problem' not in data:
            return jsonify({'error': 'Missing "problem" in the request data'}), 400
        
        else:

            problem = data['problem']
        
            file_name = f'{problem}.json'
            file_path = f'test_cases_and_answers/{file_name}'
            
            # Check if the json file exists in the solutions directory
            if not os.path.exists(file_path):
                return jsonify({'error': f'File {file_name} not found'}), 404
            
            else:
                return read_json_file(file_name)
            
    except Exception as e:
        return jsonify({'error': "Didn't receive any json."}), 500

def read_json_file(file_name):

    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
        return data
    
    except Exception as e:
        return jsonify({'error': "No such file found"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 7432)