from flask import Flask, render_template, request, session
from flask_session import Session
from aws_sql_helper import *

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SECRET_KEY"] = 'Unicorn Rainbow Eating Ice Cream Cone'
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = '/session/flask_session'
Session(app)

# Load AWS connection properties from .env file
aws_host, aws_port, aws_user, aws_password, aws_database = load_aws_connection_properties()

# Connect to AWS RDS database
try:
    connection, cursor = connect_to_aws(aws_host, aws_port, aws_user, aws_password, aws_database)
    connection_successful = True
except:
    connection_successful = False

@app.route('/')
def index():
    return render_template(
        'index.html', 
        aws_host=aws_host, 
        aws_port=aws_port, 
        aws_user=aws_user, 
        aws_password=aws_password, 
        aws_database=aws_database, 
        connection_status="Connection successful" if connection_successful else "Connection failed")

@app.route('/all_tables')
def all_tables():
    table_names = get_table_names(cursor)
    return render_template('all_tables.html', table_names=table_names)

@app.route('/table', methods=['GET', 'POST'])
def table():

    if request.method == 'GET':

        session['selected_table'] = request.args['selected_table']

        try:
            columns_names = get_column_names(cursor, session['selected_table'])
            rows = retrieve_all_rows(cursor, session['selected_table'])
            return render_template(
                'selected_table.html',
                table_name=session['selected_table'],
                rows=rows,
                columns_names=columns_names)
        
        except Exception as e:
            return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=2828)