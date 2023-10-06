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
            # Check if problem is a string
            if not isinstance(problem, str):
                return jsonify({'error': 'Invalid data type for "problem"'}), 400
            else:
        
                file_name = f'{problem}.json'
                file_path = f'test_cases_and_answers/{file_name}'
                
                # Check if the json file exists in the solutions directory
                if not os.path.exists(file_path):
                    return jsonify({'error': f'File {file_name} not found'}), 404
                else:
                    # Read the content of the json file
                    with open(file_path, "r") as file:
                        content = file.read()
                    # Parse the json content
                    data = json.loads(content)
                    response = {
                        'solutions': data,
                    }
                    return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 7432)
