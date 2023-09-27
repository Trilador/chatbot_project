import os
import json

DEFAULT_DIRECTORY = "C:\\Users\\timot\\Desktop\\Python\\AutoFix"

def list_files(directory=DEFAULT_DIRECTORY):
    try:
        return os.listdir(directory)
    except Exception as e:
        return f"Error listing files: {str(e)}"

def display_file_content(filename, directory=DEFAULT_DIRECTORY):
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        return f"Error: {filepath} does not exist."
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error reading from {filepath}: {str(e)}"

def save_to_file(data, filename, directory=DEFAULT_DIRECTORY):
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as file:
        json.dump(data, file)

def load_from_file(filename, directory=DEFAULT_DIRECTORY):
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r') as file:
        return json.load(file)

def append_to_file(data, filename, directory=DEFAULT_DIRECTORY):
    existing_data = load_from_file(filename, directory)
    existing_data.update(data)
    save_to_file(existing_data, filename, directory)

def save_file_content(filename, content, directory=DEFAULT_DIRECTORY):
    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, 'w') as file:
            file.write(content)
        return f"Successfully saved changes to {filepath}."
    except Exception as e:
        return f"Error writing to {filepath}: {str(e)}"

def create_new_file(filename, content="", directory=DEFAULT_DIRECTORY):
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        return f"Error: {filepath} already exists."
    try:
        with open(filepath, 'w') as file:
            file.write(content)
        return f"Successfully created {filepath}."
    except Exception as e:
        return f"Error creating {filepath}: {str(e)}"

def delete_file(filename, directory=DEFAULT_DIRECTORY):
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        return f"Error: {filepath} does not exist."
    try:
        os.remove(filepath)
        return f"Successfully deleted {filepath}."
    except Exception as e:
        return f"Error deleting {filepath}: {str(e)}"

def rename_file(old_filename, new_filename, directory=DEFAULT_DIRECTORY):
    old_filepath = os.path.join(directory, old_filename)
    new_filepath = os.path.join(directory, new_filename)
    if not os.path.exists(old_filepath):
        return f"Error: {old_filepath} does not exist."
    if os.path.exists(new_filepath):
        return f"Error: {new_filepath} already exists."
    try:
        os.rename(old_filepath, new_filepath)
        return f"Successfully renamed {old_filepath} to {new_filepath}."
    except Exception as e:
        return f"Error renaming {old_filepath}: {str(e)}"
