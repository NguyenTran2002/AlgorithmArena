from universal_imports import *

def txt_file_to_py_file(txt_path):
    """
    DESCRIPTION:
        Convert a text file (.txt) to a Python file (.py) by renaming the file.

    INPUT SIGNATURE:
        txt_path (string): a path pointing to a text file to be converted to python file

    OUTPUT SIGNATURE:
        py_path (string): a path pointing to the converted python file
        error_message (string) IF the input file does not exist

    CAUTION:
        Both path variables above are RELATIVE to the directory of the file that called this function
    """

    if os.path.exists(txt_path):

        py_path = txt_path.replace('.txt', '.py')
		
        # rename the original file
        os.rename(txt_path, py_path)

        return py_path

    else:

        # get realpath
        real_path = os.path.realpath(txt_path)

        error_message = "Text file does not exist in given path.\n" + real_path

        return error_message
    

# driver code for txt_file_to_py_files
if __name__ == "__main__":

    # ask for input
    txt_path = input("Enter path to text file: ")

    # call function
    print(txt_file_to_py_file(txt_path))