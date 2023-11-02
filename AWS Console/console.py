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
        
@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():

    # Triggered when the user clicks the "Add Entry" button
    if request.method == 'GET':

        try:
            columns_names = get_column_names(cursor, session['selected_table'])
            data_types = get_column_data_types(cursor, session['selected_table'])
            return render_template('add_entry.html', columns_names=columns_names, data_types=data_types, error_message=None)
        
        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")

    # Triggered when the user filled out the form and clicked the "Submit" button
    elif request.method == 'POST':

        try:
            columns_names = get_column_names(cursor, session['selected_table'])
            data_types = get_column_data_types(cursor, session['selected_table'])
            entry_list = [request.form[column] for column in columns_names]
            add_entry_to_table(connection, cursor, session['selected_table'], entry_list)
            return render_template('success.html', message="Entry added successfully.")
        
        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2828)