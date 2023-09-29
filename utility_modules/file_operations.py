import os
import json

DEFAULT_DIRECTORY = "C:\\Users\\timot\\Desktop\\Python\\AutoFix"

def list_files(directory=DEFAULT_DIRECTORY):
    try:
        return os.listdir(directory)
    except Exception as e:
        return f"Error listing files: {str(e)}"

def list_directories(directory=DEFAULT_DIRECTORY):
    try:
        return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    except Exception as e:
        return f"Error listing directories: {str(e)}"

def create_directory(directory_name, parent_directory=DEFAULT_DIRECTORY):
    dir_path = os.path.join(parent_directory, directory_name)
    if os.path.exists(dir_path):
        return f"Error: Directory {dir_path} already exists."
    try:
        os.mkdir(dir_path)
        return f"Successfully created directory: {dir_path}"
    except Exception as e:
        return f"Error creating directory {dir_path}: {str(e)}"

def delete_directory(directory_name, parent_directory=DEFAULT_DIRECTORY):
    dir_path = os.path.join(parent_directory, directory_name)
    if not os.path.exists(dir_path):
        return f"Error: Directory {dir_path} does not exist."
    try:
        os.rmdir(dir_path)
        return f"Successfully deleted directory: {dir_path}"
    except Exception as e:
        return f"Error deleting directory {dir_path}: {str(e)}"

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

def search_file_content(content, directory=DEFAULT_DIRECTORY):
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            try:
                with open(os.path.join(root, file), 'r') as f:
                    if content in f.read():
                        matching_files.append(os.path.join(root, file))
            except Exception as e:
                continue  # Skip files that can't be read
    return matching_files
