import pymysql
from dotenv import load_dotenv
import os

def load_aws_connection_properties():
    """
    Load aws
        1. host
        2. port
        3. user
        4. password
        5. database
    from the .env file
    """
    load_dotenv()
    return os.getenv('aws_host'), os.getenv('aws_port'), os.getenv('aws_user'), os.getenv('aws_password'), os.getenv('aws_database')

def connect_to_aws(host, port, user, password, database):
    # Connect to the database
    connection = pymysql.connect(
        host = host,
        port = port,
        user = user,
        password = password,
        database = database)
    cursor = connection.cursor()
    return connection, cursor

def create_table(connection, cursor, table_name, columns, data_types):

    try:

        if len(columns) != len(data_types):
            raise ValueError("Number of columns and data types should be the same.")
        
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

        for i in range(len(columns)):
            query += f"{columns[i]} {data_types[i]}, "

        query = query.rstrip(", ") + ")"

        cursor.execute(query)

        connection.commit()
        
        print("Table created successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def delete_table(connection, cursor, table_name):
    
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        connection.commit()
        print(f"Table '{table_name}' deleted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def get_column_names(cursor, table_name):

    try:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]
        return column_names
    
    except Exception as e:
        print(f"An error occurred: {e}")

def add_entry_to_table(connection, cursor, table_name, entry_list):

    try:

        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()

        if len(columns) != len(entry_list):
            raise Exception("Number of columns in the table and length of the entry list don't match.")
        
        column_names = [column[0] for column in columns]
        query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['%s']*len(entry_list))})"
        cursor.execute(query, entry_list)
        connection.commit()

        print("Entry added successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def retrieve_all_rows(cursor, table_name):

    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        return rows
    
    except Exception as e:
        print(f"An error occurred: {e}")

def get_column2_given_column1(cursor, table_name, column_1, column_2, column_1_val):

    try:

        query = f"SELECT {column_2} FROM {table_name} WHERE {column_1} = %s"
        cursor.execute(query, (column_1_val,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
        
    except Exception as e:
        print(f"An error occurred: {e}")