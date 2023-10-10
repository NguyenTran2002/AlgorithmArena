def run_method_from_string(code_string, method_name, *argv):
    # Create an empty namespace dictionary to execute the code
    # namespace = {}
    namespace = {method_name : 'method_name'}

    try:
        print("Running the exec str func")
        # Execute the code in the provided string
        exec(code_string, namespace)
        print("the namespace dict has: ", namespace)
        print("the code str is:", code_string)
        print("getting past exec call")

        # Check if the specified method exists in the namespace and is callable
        if method_name in namespace and callable(namespace[method_name]):
            print("into if statement")
            # Call the specified method and return its result
            result = namespace[method_name](*argv)
            print("the result of method run is: ", result)
            return result
        else:
            print("into else statement")
            return f"Function '{method_name}' not found or not callable in the code."

    except Exception as e:
        return f"Error executing code: {str(e)}"

# Example usage:
python_code = """
def testing(x):
    return x + 10

"""

# Run the example code
run_method_from_string(python_code, 'testing')
