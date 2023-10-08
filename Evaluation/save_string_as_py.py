def save_string_as_python_file(file_name, code):
    """
    Save a string as a Python file.

    INPUT SIGNATURE:
        file_name (str): The name of the Python file to be created.
        code (str): The Python code to be written to the file.
    
    OUTPUT SIGNATURE:
        bool: True if the file was successfully created and written, False otherwise.
    """
    try:

        with open(file_name, 'w') as file:
            file.write(code)

        return True
    
    except Exception as e:

        print(f"Error: {e}")
        return False

if __name__ == "__main__":

    file_name = input("Enter the name of the file to be created: ")
    code = input("Write the code: ")