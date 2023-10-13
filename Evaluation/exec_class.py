def run_method_from_string(code_string, class_name, method_name, params):
    # Create an empty namespace dictionary to execute the code
    namespace = {}

    try:
        # Execute the code in the provided string
        exec(code_string, namespace)

        # Check if the specified class and method exist in the namespace
        if class_name in namespace and method_name in dir(namespace[class_name]):
            # Create an instance of the class
            instance = namespace[class_name]()

            # Call the specified method and return its result
            method = getattr(instance, method_name)
            result = method(*params)
            print(result)
            return result
        else:
            return f"Class '{class_name}' or method '{method_name}' not found in the code."

    except Exception as e:
        return f"Error executing code: {str(e)}"

# Example usage:
python_code = """
class Solution:
    def containsDuplicate(self, nums):
        nums_set = self.create_set()
        for item in nums:
            if item in nums_set:
                return True
            else:
                nums_set.add(item)
        return False

    def create_set(self):
        return set()
"""


# Run the example code
# run_method_from_string(python_code, 'Solution', 'containsDuplicate')
