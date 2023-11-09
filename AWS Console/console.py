from flask import Flask, render_template, request, session
from flask_session import Session
from aws_sql_helper import *

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SECRET_KEY"] = 'Unicorn Rainbow Eating Ice Cream Cone'
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = '/session/flask_session'
Session(app)

connection_successful = False

try:

    aws_credentials_object = create_AWS_credentials_object()

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)
        print("DATABASE CONNECTED TO AWS")
        connection_successful = True
        connection.close()

    except Exception as e:
        print("DATABASE CANNOT CONNECT TO AWS")
        print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

except Exception as e:
    print("DATABASE CANNOT CREATE CREDENTIALS OBJECT.\nCheck if the relevant .env file exist.")
    print("ENCOUNTERED THE FOLLOWING EXCEPTION:\n", e)

@app.route('/')
def index():

    global aws_credentials_object

    return render_template(
        'index.html', 
        aws_host=aws_credentials_object.get_host(), 
        aws_port=aws_credentials_object.get_port(),
        aws_user=aws_credentials_object.get_user(),
        aws_password=aws_credentials_object.get_password(), 
        aws_database_name=aws_credentials_object.get_database_name(),
        connection_status="Connection successful" if connection_successful else "Connection failed")

@app.route('/all_tables')
def all_tables():

    global aws_credentials_object

    table_names = get_tables_names(aws_credentials_object)

    return render_template('all_tables.html', table_names=table_names)

@app.route('/table', methods=['GET', 'POST'])
def table():

    global aws_credentials_object

    if request.method == 'GET':

        session['selected_table'] = request.args['selected_table']

        try:
            columns_names = get_column_names(aws_credentials_object, session['selected_table'])
            rows = retrieve_all_rows(aws_credentials_object, session['selected_table'])
            return render_template(
                'selected_table.html',
                table_name=session['selected_table'],
                rows=rows,
                columns_names=columns_names)
        
        except Exception as e:
            return f"An error occurred: {e}"
        
@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():

    global aws_credentials_object

    # Triggered when the user clicks the "Add Entry" button
    if request.method == 'GET':

        try:
            columns_names = get_column_names(aws_credentials_object, session['selected_table'])
            data_types = get_columns_data_types(aws_credentials_object, session['selected_table'])
            return render_template('add_entry.html', columns_names=columns_names, data_types=data_types, error_message=None)
        
        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")

    # Triggered when the user filled out the form and clicked the "Submit" button
    elif request.method == 'POST':

        try:
            columns_names = get_column_names(aws_credentials_object, session['selected_table'])
            data_types = get_columns_data_types(aws_credentials_object, session['selected_table'])
            entry_list = [request.form[column] for column in columns_names]
            add_entry_to_table(aws_credentials_object, session['selected_table'], entry_list)
            return render_template('success.html', message="Entry added successfully.")
        
        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")

@app.route('/delete_entry', methods=['GET', 'POST'])
def delete_entry():

    if request.method == 'GET':

        try:
            table_name = session['selected_table']
            columns_names = get_column_names(aws_credentials_object, table_name)
            return render_template('delete_entry.html', columns_names=columns_names, error_message=None)
        
        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")

    elif request.method == 'POST':
        try:
            table_name = session['selected_table']
            column_name = request.form['selected_column']
            column_value = request.form['column_value']
            delete_row(aws_credentials_object, table_name, column_name, column_value)
            return render_template('success.html', message=f"Row with value '{column_value}' at column {column_name} deleted successfully.")
        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")

@app.route('/add_column', methods=['GET', 'POST'])
def add_column_flask():

    if request.method == 'GET':

        try:
            return render_template('add_column.html', error_message=None)

        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")

    elif request.method == 'POST':

        try:
            column_name = request.form['column_name']
            data_type = request.form['data_type']
            add_column(aws_credentials_object, session['selected_table'], column_name, data_type)
            return render_template('success.html', message="Column added successfully.")

        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")
        
@app.route('/remove_column', methods=['GET', 'POST'])
def remove_column_flask():

    if request.method == 'GET':

        try:
            table_name = session['selected_table']
            columns_names = get_column_names(aws_credentials_object, table_name)
            return render_template('remove_column.html', columns_names=columns_names, error_message=None)
        
        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")

    elif request.method == 'POST':
        try:
            table_name = session['selected_table']
            column_name = request.form['selected_column']
            remove_column(aws_credentials_object, table_name, column_name)
            return render_template('success.html', message=f"Column '{column_name}' removed successfully from the table '{table_name}'.")
        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")

@app.route('/edit_entry', methods=['GET', 'POST'])
def edit_entry():

    if request.method == 'GET':

        try:
            table_name = session['selected_table']
            columns_names = get_column_names(aws_credentials_object, table_name)
            return render_template('edit_entry.html', columns_names=columns_names, error_message=None)
        
        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")

    elif request.method == 'POST':
        try:
            table_name = session['selected_table']
            identifier_column = request.form['identifier_column']
            identifier_value = request.form['identifier_value']
            edit_column = request.form['edit_column']
            new_value = request.form['new_value']
            update_row(aws_credentials_object, table_name, identifier_column, identifier_value, edit_column, new_value)
            return render_template('success.html', message=f"Row with {identifier_column} value '{identifier_value}' updated successfully.")
        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")

@app.route('/rename_column', methods=['GET', 'POST'])
def rename_column_flask():

    if request.method == 'GET':

        try:
            table_name = session['selected_table']
            columns_names = get_column_names(aws_credentials_object, table_name)
            return render_template('rename_column.html', columns_names=columns_names, error_message=None)
        
        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")

    elif request.method == 'POST':
        try:
            table_name = session['selected_table']
            old_column_name = request.form['old_column_name']
            new_column_name = request.form['new_column_name']
            rename_column(aws_credentials_object, table_name, old_column_name, new_column_name)
            return render_template('success.html', message=f"Column '{old_column_name}' renamed to '{new_column_name}' successfully.")
        except Exception as e:
            return render_template('error.html', error=f"An error occurred: {e}")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2828)