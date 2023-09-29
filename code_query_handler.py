import os
import re

# Define the directory where files are stored
FILE_DIRECTORY = './files/'  # You can change this to the appropriate directory

def handle_file_display(user_input):
    if file_name := re.search(r'\b(file)\b\s+(\w+\.\w+)', user_input):
        file_name = file_name.group(2)
        file_path = os.path.join(FILE_DIRECTORY, file_name)
        if not os.path.exists(file_path):
            return f"File '{file_name}' not found."
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            return content
        except Exception as e:
            return f"Error reading from '{file_name}': {str(e)}"
    return "Please specify a valid file name."

# ... [Rest of the code remains the same]
