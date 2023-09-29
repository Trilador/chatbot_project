from utility_modules.file_operations import (
    list_files,
    list_directories,
    create_directory,
    delete_directory,
    display_file_content,
    save_file_content,
    search_file_content,
)

class CommandHandler:
    def __init__(self):
        # Define a dictionary mapping commands to their respective functions
        self.commands = {
            "list files": self.list_files,
            "list directories": self.list_directories,
            "create directory": self.create_directory,
            "delete directory": self.delete_directory,
            "display file content": self.display_file_content,
            "save file content": self.save_file_content,
            "search file content": self.search_file_content,
        }

    def is_command(self, query: str) -> bool:
        return any(command in query for command in self.commands)

    def execute_command(self, query: str) -> str:
        for command, function in self.commands.items():
            if command in query:
                # Extract parameters if needed and execute the command
                param = query.replace(command, "").strip()
                return function(param)
        return "Command not recognized."

    def list_files(self, _=None) -> str:
        return list_files()

    def list_directories(self, _=None) -> str:
        return list_directories()

    def create_directory(self, dir_name: str) -> str:
        return create_directory(dir_name)

    def delete_directory(self, dir_name: str) -> str:
        return delete_directory(dir_name)

    def display_file_content(self, file_name: str) -> str:
        return display_file_content(file_name)

    def save_file_content(self, file_name: str) -> str:
        # For simplicity, I'm assuming the format "save file content [e
        # ase] [content]"
        content = file_name.split(" ")[1:]
        file_name = file_name.split(" ")[0]
        return save_file_content(file_name, " ".join(content))

    def search_file_content(self, search_term: str) -> str:
        return search_file_content(search_term)
