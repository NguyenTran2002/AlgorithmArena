import pymysql
from dotenv import load_dotenv
import os

class AWS_credentials:

    def __init__(self, host, port, user, password, database_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database_name = database_name

    def get_host(self):
        return self.host
    
    def get_port(self):
        return self.port
    
    def get_user(self):
        return self.user
    
    def get_password(self):
        return self.password
    
    def get_database_name(self):
        return self.database_name
    
    def print_credentials(self):
        print(f"HOST: {self.host}")
        print(f"PORT: {self.port}")
        print(f"USER: {self.user}")
        print(f"PASSWORD: {self.password}")
        print(f"DATABASE NAME: {self.database_name}")

def create_AWS_credentials_object():
    """
    Load aws credentials
        1. host
        2. port
        3. user
        4. password
        5. database name
        from the .env file

    And return them as a credentials object
    """

    load_dotenv()

    credentials = AWS_credentials(
        os.getenv('aws_host'),
        int(os.getenv('aws_port')),
        os.getenv('aws_user'),
        os.getenv('aws_password'),
        os.getenv('aws_database')
    )

    return credentials

def connect_to_aws(aws_credentials_object):
    """
    DESCRIPTION:
        Return a connection and a cursor object to the AWS RDS database.

    INPUT SIGNATURE:
        aws_credentials_object
    """

    connection = pymysql.connect(
        host = aws_credentials_object.get_host(),
        port = aws_credentials_object.get_port(),
        user = aws_credentials_object.get_user(),
        password = aws_credentials_object.get_password(),
        database = aws_credentials_object.get_database_name()
    )

    cursor = connection.cursor()

    return connection, cursor

def create_table(aws_credentials_object, table_name, columns, data_types):
    """
    INPUT SIGNATURE:
        aws_credentials_object: AWS_credentials object
        table_name: string
        columns: a list of strings (each is a column name)
        data_types: a list of strings containing datatype corresponding to the columns
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the create_table function.")
        print(f"An error occurred: {e}")

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

        connection.close()
        
        print("Table created successfully.")

    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def delete_table(aws_credentials_object, table_name):
    """
    INPUT SIGNATURE:

        aws_credentials_object: AWS_credentials object
        table_name: string
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the delete_table function.")
        print(f"An error occurred: {e}")
    
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        connection.commit()
        connection.close()
        print(f"Table '{table_name}' deleted successfully.")

    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def get_column_names(aws_credentials_object, table_name):
    """
    INPUT SIGNATURE:
        aws_credentials_object: AWS_credentials object
        table_name: string
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the get_column_names function.")
        print(f"An error occurred: {e}")

    try:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]
        connection.close()
        return column_names
    
    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def get_columns_data_types(aws_credentials_object, table_name):
    """
    DESCRIPTION:
        Given a table name, return the data types of the columns in the table.

    INPUT SIGNATURE:
        aws_credentials_object: AWS_credentials object
        table_name: string

    OUTPUT SIGNATURE:
        A list of strings, each string is a data type of a column
        The datatype is SQL datatype, not python
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the get_columnns_datatype function.")
        print(f"An error occurred: {e}")

    try:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        column_data_types = [column[1] for column in columns]
        connection.close()
        return column_data_types
    
    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def get_a_column_data_type(aws_credentials_object, table_name, column_name):
    """
    DESCRIPTION:
        Given a table name and A column name, return the data type of the column.

    INPUT SIGNATURE:
        aws_credentials_object: AWS_credentials object
        table_name: string
        column_name: string

    OUTPUT SIGNATURE:
        A string, the data type of the column
        The datatype is SQL datatype, not python
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the get_a_column_data_type function.")
        print(f"An error occurred: {e}")

    try:
        cursor.execute(f"DESCRIBE `{table_name}`")
        columns = cursor.fetchall()
        for column in columns:
            if column[0] == column_name:
                connection.close()
                return column[1]
        return None
    
    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")
        return None

def add_entry_to_table(aws_credentials_object, table_name, entry_list):
    """
    INPUT SIGNATURE:
        aws_credentials_object: AWS_credentials object
        table_name: string
        entry_list: a list of values to be inserted into the table,
            corresponding to the columns
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the add_entry_to_table function.")
        print(f"An error occurred: {e}")

    try:

        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()

        if len(columns) != len(entry_list):
            raise Exception("Number of columns in the table and length of the entry list don't match.")
        
        column_names = [column[0] for column in columns]
        query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['%s']*len(entry_list))})"
        cursor.execute(query, entry_list)

        connection.commit()
        connection.close()

        print("Entry added successfully.")

    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def delete_row(aws_credentials_object, table_name, column_name, column_value):
    """
    DESCRIPTION:
        Look for a row that has the value 'column_value' at the column 'column_name'.
        Delete that row.

    INPUT SIGNATURE:
        aws_credentials_object: AWS_credentials object
        table_name: string
        column_name: string
        column_value: same type as the database type
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the delete_row function.")
        print(f"An error occurred: {e}")

    try:
        query = f"DELETE FROM {table_name} WHERE {column_name} = %s"
        cursor.execute(query, (column_value,))
        connection.commit()
        connection.close()
        print(f"Row with {column_name} value '{column_value}' deleted successfully.")

    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def retrieve_all_rows(aws_credentials_object, table_name):
    """
    INPUT SIGNATURE:
        aws_credentials_object: AWS_credentials object
        table_name: string

    OUTPUT SIGNATURE:
        A list of tuples, each tuple is a row in the table
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the retrieve_all_rows function.")
        print(f"An error occurred: {e}")

    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        connection.close()
        return rows
    
    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def retrieve_all_rows_of_column(aws_credentials_object, table_name, column_name):
    """
    DESCRIPTION:
        Given a table name and a column name, return all the values in that column.

    INPUT SIGNATURE:
        cursor: cursor object
        table_name: string
        column_name: string

    OUTPUT SIGNATURE:
        A list of values in the column
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the retrieve_all_rows_of_column function.")
        print(f"An error occurred: {e}")

    try:
        query = f"SELECT `{column_name}` FROM `{table_name}`"
        cursor.execute(query)
        rows = cursor.fetchall()
        column_data = [row[0] for row in rows]
        connection.close()
        return column_data
    
    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def filter_by(aws_credentials_object, table_name, column_name, filter_value, filter_value_type):
    """
    DESCRIPTION:
        Given a table name, a column name, and a value,
            return all the rows in the table that have that value at that column.

    INPUT SIGNATURE:
        aws_credentials_object: AWS_credentials object
        table_name: string
        column_name: string
        filter_value: same type as the database type
        filter_value_type: string
            "str" if the filter value is a string

    OUTPUT SIGNATURE:
        A list of tuples, each tuple is a row in the table
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the filter_by function.")
        print(f"An error occurred: {e}")

    try:
        if filter_value_type == "str":
            query = f"SELECT * FROM {table_name} WHERE {column_name} = '{filter_value}'"
        else:
            query = f"SELECT * FROM {table_name} WHERE {column_name} = {filter_value}"
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        return rows
    
    except Exception as e:
        connection.close()
        print(f"An error occurred in HELPER: {e}")
        return None

def get_column2_given_column1(aws_credentials_object, table_name, column_1, column_2, column_1_val):
    """
    DESCRIPTION:
        Given a specific value of column_1,
            find the row with that specific value at column_1,
            then return the value of column_2 in that row.

    INPUT SIGNATURE:
        aws_credentials_object: AWS_credentials object
        table_name: string
        column_1: string
        column_2: string
        column_1_val: same type as the database type

    OUTPUT SIGNATURE:
        The value of column_2 in the row that has column_1_val at column_1
            The type depends on the data type of column_2
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the get_column2_given_column1 function.")
        print(f"An error occurred: {e}")

    try:

        query = f"SELECT {column_2} FROM {table_name} WHERE {column_1} = %s"
        cursor.execute(query, (column_1_val,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return result[0]
        else:
            return None
        
    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def get_tables_names(aws_credentials_object):
    """
    DESCRIPTION:
        Given an AWS credentials object, return all available tables within the database.
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the get_tables_names function.")
        print(f"An error occurred: {e}")

    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        connection.close()
        return table_names
    
    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def add_column(aws_credentials_object, table_name, column_name, data_type):
    """
    DESCRIPTION:
        Add a column to the table.

    INPUT SIGNATURE:
        aws_credentials_object: AWS_credentials object
        table_name: string
        column_name: string
        data_type: corresponding SQL data type
            input this as a string
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the add_column function.")
        print(f"An error occurred: {e}")

    try:
        query = f"ALTER TABLE {table_name} ADD {column_name} {data_type}"
        cursor.execute(query)
        connection.commit()
        connection.close()
        print(f"Column '{column_name}' added successfully to the table '{table_name}'.")

    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def remove_column(aws_credentials_object, table_name, column_name):
    """
    DESCRIPTION:
        Remove a column from the table.

    INPUT SIGNATURE:
        aws_credentials_object: AWS_credentials object
        table_name: string
        column_name: string
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the remove_column function.")
        print(f"An error occurred: {e}")

    try:
        query = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
        cursor.execute(query)
        connection.commit()
        connection.close()
        print(f"Column '{column_name}' removed successfully from the table '{table_name}'.")
        
    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def rename_column(aws_credentials_object, table_name, old_column_name, new_column_name):
    """
    DESCRIPTION:
        Rename a column in the table.

    INPUT SIGNATURE:
        table_name: string
        old_column_name: string
        new_column_name: string
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the rename_column function.")
        print(f"An error occurred: {e}")

    try:

        data_type = get_a_column_data_type(aws_credentials_object, table_name, old_column_name)

        if data_type:
            query = f"ALTER TABLE `{table_name}` CHANGE `{old_column_name}` `{new_column_name}` {data_type}"
            cursor.execute(query)
            connection.commit()
            print(f"Column '{old_column_name}' renamed to '{new_column_name}' successfully in the table '{table_name}'.")

        else:
            print(f"Column '{old_column_name}' not found in the table '{table_name}'.")

        connection.close()

    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def update_row(aws_credentials_object, table_name, identifier_column, identifier_value, edit_column, new_value):
    """
    DESCRIPTION:
        Given a table name, an identifier column name, and a value of that row at that identifier column,
            update the value at another column in that row.
        THE IDENTIFIER COLUMN MUST BE A COLUMN THAT CONTAINS ONLY UNIQUE VALUES

    INPUT SIGNATURE:
        table_name: string
        identifier_column: string
        identifier_value: same type as the database type
        edit_column: string
        new_value: same type as the database type
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the update_row function.")
        print(f"An error occurred: {e}")

    try:
        query = f"UPDATE {table_name} SET {edit_column} = %s WHERE {identifier_column} = %s"
        cursor.execute(query, (new_value, identifier_value))
        connection.commit()
        connection.close()
        print(f"Row with {identifier_column} value '{identifier_value}' updated successfully.")

    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")

def check_value_exists(aws_credentials_object, table_name, column_name, value):
    """
    DESCRIPTION:
        Given a table name, a column name, and a value,
            check if the value exists in the column.

    INPUT SIGNATURE:
        aws_credentials_object: AWS_credentials object
        table_name: string
        column_name: string
        value: same type as the database type

    OUTPUT SIGNATURE:
        True if value exists in the column, False otherwise
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the check_value_exists function.")
        print(f"An error occurred: {e}")

    try:
        query = f"SELECT * FROM {table_name} WHERE {column_name} = %s"
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return True
        else:
            return False
        
    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")
        return False
    
def get_table_sorted_by(aws_credentials_object, table_name, sort_column, ascending = False):
    """
    DESCRIPTION:
        Given a table name and a column name,
            return all the rows in the table sorted by the column name.

    INPUT SIGNATURE:
        aws_credentials_object: AWS_credentials object
        table_name: string
        sort_column: string
        ascending: boolean
            True if ascending, False if descending
    """

    try:
        connection, cursor = connect_to_aws(aws_credentials_object)

    except Exception as e:
        print("Cannot connect to AWS RDS database within the get_table_sorted_by function.")
        print(f"An error occurred: {e}")

    try:
        query = f"SELECT * FROM {table_name} ORDER BY {sort_column}"
        if not ascending:
            query += " DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        return rows
    
    except Exception as e:
        connection.close()
        print(f"An error occurred: {e}")