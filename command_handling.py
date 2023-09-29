import re
import os
import webbrowser
from typing import Callable, Dict, Union


# Define the directory where files are stored
FILE_DIRECTORY = './AutoFix/'  # You can change this to the appropriate directory

# Handler functions
def handle_file_display(user_input):
    """
    Handles the user's request to display the content of a file.
    """
    if file_name_match := re.search(
        r'\b(file|document|txt|pdf|jpg|png)\b\s+(\w+\.\w+)', user_input
    ):
        file_name = file_name_match.group(2)
        file_path = os.path.join(FILE_DIRECTORY, file_name)
        if not os.path.exists(file_path):
            return f"File '{file_name}' not found."
        if file_name.endswith(('.txt', '.pdf')):
            with open(file_path, 'r') as file:
                content = file.read()
            return content
        elif file_name.endswith(('.jpg', '.png')):
            return f"This is an image file named '{file_name}'. I cannot display its content here."
        else:
            return f"File '{file_name}' is of an unsupported type."
    return "Please specify a valid file name."

def handle_file_write(user_input):
    if match := re.search(
        r'\b(file)\b\s+(\w+\.\w+)\s+with\s+content\s+(.*)', user_input
    ):
        file_name, content = match[2], match[3]
        file_path = os.path.join(FILE_DIRECTORY, file_name)
        with open(file_path, 'w') as file:
            file.write(content)
        return f"Content written to '{file_name}'."
    return "Please specify a valid file name and content."

def handle_file_delete(user_input):
    """
    Deletes the specified file after confirmation.
    """
    if not (
        file_name_match := re.search(
            r'\b(file|document)\b\s+(\w+\.\w+)', user_input
        )
    ):
        return "Please specify a valid file name."
    file_name = file_name_match.group(2)
    file_path = os.path.join(FILE_DIRECTORY, file_name)
    if not os.path.exists(file_path):
        return f"File '{file_name}' not found."
    # Ask for confirmation before deleting
    confirmation = input(f"Are you sure you want to delete '{file_name}'? (yes/no): ")
    if confirmation.lower() != 'yes':
        return f"File '{file_name}' was not deleted."
    os.remove(file_path)
    return f"File '{file_name}' has been deleted."


def handle_file_create(user_input):
    """
    Creates a new file.
    """
    if file_name_match := re.search(
        r'\b(file|document)\b\s+(\w+\.\w+)', user_input
    ):
        file_name = file_name_match.group(2)
        file_path = os.path.join(FILE_DIRECTORY, file_name)
        if os.path.exists(file_path):
            return f"File '{file_name}' already exists."
        with open(file_path, 'w') as file:
            file.write('')  # Create an empty file
        return f"File '{file_name}' has been created."
    return "Please specify a valid file name."

def list_directories(user_input: str) -> str:
    """
    Lists all directories in the specified path.
    """
    try:
        # some code here
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    if directories := [
        d
        for d in os.listdir(FILE_DIRECTORY)
        if os.path.isdir(os.path.join(FILE_DIRECTORY, d))
    ]:
        return "\n".join(directories)
    return "No directories found."

def create_directory(user_input: str) -> str:
    """
    Creates a new directory.
    """
    if dir_name_match := re.search(
        r'\b(directory|folder)\b\s+(\w+)', user_input
    ):
        dir_name = dir_name_match.group(2)
    try:
            dir_path = os.path.join(FILE_DIRECTORY, dir_name)
            if os.path.exists(dir_path):
                return f"Directory '{dir_name}' already exists."
            os.makedirs(dir_path)
            return f"Directory '{dir_name}' has been created."
    except Exception as e:
            return f"An error occurred: {e}"
    return "Please specify a valid directory name."


def delete_directory(dir_name: str) -> str:
    """
    Deletes the specified directory.
    """
    dir_path = os.path.join(FILE_DIRECTORY, dir_name)
    try:
        if os.path.exists(dir_path):
            os.rmdir(dir_path)
            return f"Directory '{dir_name}' has been deleted."
        else:
            return f"Directory '{dir_name}' not found."
    except OSError as e:
        if e.errno == errno.ENOTEMPTY:
            return f"Directory '{dir_name}' is not empty."
        elif e.errno == errno.EACCES:
            return f"Permission denied to delete directory '{dir_name}'."
        else:
            return f"An error occurred while deleting directory '{dir_name}': {e}"


def handle_google_search(user_input):
    """
    Opens the default web browser and searches Google for the user's query.
    """
    # Extract the search query from the user input
    search_query = user_input.replace("search", "").replace("find", "").replace("lookup", "").strip()
    
    # Construct the Google search URL
    google_url = f"https://www.google.com/search?q={search_query}"
    
    # Open the web browser with the Google search URL
    webbrowser.open(google_url)
    
    return f"Searching Google for '{search_query}'..."


def handle_music_play(user_input):
    """
    Opens YouTube based on the user's music request.
    """
    search_query = user_input.replace("play ", "")
    full_url = f"https://www.youtube.com/results?search_query={search_query}"
    webbrowser.open(full_url)
    return f"Playing '{search_query}' on YouTube..."

from typing import Callable, Dict, Union

# Define regex patterns for commands
# Dictionary for command patterns and their respective handlers
COMMAND_PATTERNS: Dict[str, Union[str, Callable[[str], str]]] = {
    r'(?i)\b(search|find|lookup)\b': 'handle_google_search',
    r'(?i)\b(play)\b.*\b(song|music|track)\b': 'handle_music_play',
    # File-related commands
    r'(?i)\b(show|display|open)\b.*\b(file|document|txt|pdf|jpg|png)\b': 'handle_file_display',
    r'(?i)\b(write|save)\b.*\b(file|document|txt|pdf)\b': 'handle_file_write',
    r'(?i)\b(delete|remove)\b.*\b(file|document)\b': 'handle_file_delete',
    r'(?i)\b(create|new)\b.*\b(file|document)\b': 'handle_file_create',
    # Directory-related commands
    r'(?i)\b(list|show)\b.*\b(directories|folders)\b': 'list_directories',
    r'(?i)\b(create|make)\b.*\b(directory|folder)\b': 'create_directory',
    r'(?i)\b(delete|remove)\b.*\b(directory|folder)\b': 'delete_directory',
}

# The actual handler functions will be implemented in their respective modules.
