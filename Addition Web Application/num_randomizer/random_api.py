from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/random-number')
def generate_random_number():
    random_num = random.randint(1, 100)  # Generate a random number between 1 and 100
    response = {
        'random_number': random_num
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 4747)