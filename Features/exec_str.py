def run_method_from_string(code_string, method_name):
    # Create an empty namespace dictionary to execute the code
    namespace = {}

    try:
        print("Running")
        # Execute the code in the provided string
        exec(code_string, namespace)

        # Check if the specified method exists in the namespace and is callable
        if method_name in namespace and callable(namespace[method_name]):
            # Call the specified method and return its result
            result = namespace[method_name](1)
            print(result)
        else:
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
