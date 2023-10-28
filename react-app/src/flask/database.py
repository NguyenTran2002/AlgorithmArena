from flask_cors import CORS

from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app) 


@app.route('/get_all_problems', methods=['POST'])
def get_all_problems():
    
    data = {'problems' : ['binary_search', 'koko_eating_bananas', 'contains_duplicates']}
    
    return jsonify(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port = 7432)