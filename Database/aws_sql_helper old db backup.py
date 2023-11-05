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
    return os.getenv('aws_host'), int(os.getenv('aws_port')), os.getenv('aws_user'), os.getenv('aws_password'), os.getenv('aws_database')

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
    """
    INPUT SIGNATURE:
        table_name: string
        columns: a list of strings (each is a column name)
        data_types: a list of strings containing datatype corresponding to the columns
    """

    try:

        if len(columns) != len(data_types):
            raise ValueError("Number of columns and data types should be the same.")
        
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

        for i in range(len(columns)):
            query += f"{columns[i]} {data_types[i]}, "

        query = query.rstrip(", ") + ")"

        print(query)

        cursor.execute(query)

        connection.commit()
        
        print("Table created successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def delete_table(connection, cursor, table_name):
    """
    INPUT SIGNATURE:
        table_name: string
    """
    
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        connection.commit()
        print(f"Table '{table_name}' deleted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def get_column_names(cursor, table_name):
    """
    INPUT SIGNATURE:
        table_name: string
    """

    try:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]
        return column_names
    
    except Exception as e:
        print(f"An error occurred: {e}")

def get_column_data_types(cursor, table_name):
    """
    DESCRIPTION:
        Given a table name, return the data types of the columns in the table.
    """

    try:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        column_data_types = [column[1] for column in columns]
        return column_data_types
    
    except Exception as e:
        print(f"An error occurred: {e}")

def add_entry_to_table(connection, cursor, table_name, entry_list):
    """
    INPUT SIGNATURE:
        table_name: string
        entry_list: a list of values to be inserted into the table,
            corresponding to the columns
    """

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
        return rows
    
    except Exception as e:
        print(f"An error occurred: {e}")

def get_column2_given_column1(cursor, table_name, column_1, column_2, column_1_val):
    """
    DESCRIPTION:
        Given a specific value of column_1,
            find the row with that specific value at column_1,
            then return the value of column_2 in that row.
    """

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

def get_table_names(cursor):

    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        return table_names
    
    except Exception as e:
        print(f"An error occurred: {e}")

def add_column(connection, cursor, table_name, column_name, data_type):

    try:
        query = f"ALTER TABLE {table_name} ADD {column_name} {data_type}"
        cursor.execute(query)
        connection.commit()
        print(f"Column '{column_name}' added successfully to the table '{table_name}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

def remove_column(connection, cursor, table_name, column_name):

    try:
        query = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
        cursor.execute(query)
        connection.commit()
        print(f"Column '{column_name}' removed successfully from the table '{table_name}'.")
        
    except Exception as e:
        print(f"An error occurred: {e}")