from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 


@app.route('/', methods=['POST'])
def evaluate():
    
    data_dict = request.get_json()
    
    try:
        data_dict = request.get_json()
        print(data_dict)

    except Exception as e:
        message = f"Error1 eval: {str(e)}"

    # doing number 2
    try:
        problem_name = {
            "problem": data_dict["problem"]
        }
    except Exception as e:
        message = f"Error2 eval: {str(e)}"
        
    
    return "TRUE"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port = 1111)