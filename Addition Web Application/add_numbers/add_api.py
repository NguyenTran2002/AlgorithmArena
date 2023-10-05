from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add_numbers():
    data = request.get_json()
    if 'num1' in data and 'num2' in data:
        num1 = float(data['num1'])
        num2 = float(data['num2'])
        result = num1 + num2
        response = {
            'result': result
        }
        return jsonify(response), 200
    else:
        return jsonify({'error': 'Please provide "num1" and "num2" in the request body'}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 3737)