import openai
import os
from typing import List, Union, Tuple
from utility_modules.api_integrations import (
    wolfram_alpha_query,
    analyze_text as external_analyze_text,
    get_dialogflow_response
)
from utility_modules.file_operations import (
    list_files,
    list_directories,
    create_directory,
    delete_directory,
    display_file_content,
    save_file_content,
    search_file_content,
)
from utility_modules.code_generations import (
    natural_language_to_code,
    provide_code_feedback,
    interactive_code_correction,
    analyze_python_code_ast,
)
from utility_modules.web_operations import fetch_wikipedia_summary, search_python_documentation
from code_db.advanced_constructs import PYTHON_CODE_DB as ADVANCED_DB
from code_db.basic_constructs import PYTHON_CODE_DB as BASIC_DB
from code_db.python_modules import PYTHON_CODE_DB as MODULES_DB

# Set up the OpenAI API
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

DEFAULT_DIRECTORY = "C:\\Users\\timot\\Desktop\\Python"
TOKEN_LIMIT = 150

from handlers.command_handler import CommandHandler

class ChatbotEngine:
    def __init__(self):
        self.command_handler = CommandHandler()

    def chatbot_response(self, user_input: str) -> str:
        # Check if the user's input is a command
        if self.command_handler.is_command(user_input):
            return self.command_handler.execute_command(user_input)
        
        # If not a command, process the input normally (you can expand this section later)
        return f"Processed input: {user_input}"

    def respond_to_chat(self, query: str) -> str:
        if code_db_response := self.check_code_db(query):
            return code_db_response
        
        sentiment_score, _ = self.analyze_text(query)
        if sentiment_score > 0.7:
            return "I'm glad to hear that!"
        elif sentiment_score < -0.7:
            return "I'm sorry to hear that. How can I assist you further?"
        else:
            return self.handle_openai_response(query, self.context)

    def handle_openai_response(self, query: str, context: List[str]) -> str:
        return f"OpenAI response for: {query}"

    def check_code_db(self, query: str) -> Union[str, None]:
        return None

    def handle_query(self, query: str) -> str:
        self.update_context(query)
        if self.command_handler.is_command(query):
            return self.command_handler.execute_command(query)
        elif "list files" in query:
            return list_files()
        elif "execute code" in query:
            code = self.extract_parameter(query, "execute code")
            return execute_code(code)
        else:
            return self.respond_to_chat(query)

    def extract_parameter(self, query: str, command: str) -> str:
        return query.split(command)[-1].strip()

    def update_context(self, user_query: str) -> None:
        CONTEXT_SIZE = 10
        if len(self.context) >= CONTEXT_SIZE:
            self.context.pop(0)
        self.context.append(user_query)

    def analyze_text(self, query: str) -> Tuple[float, float]:
        return external_analyze_text(query)

    def store_feedback(self, query: str, response: str, rating: str) -> None:
        pass


def main() -> None:
    chatbot = ChatbotEngine()
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit", "bye"]:
            break
        response = chatbot.handle_query(query)
        print(f"Bot: {response}")

        rating = input(
            "Rate the response (1-5, 5 being very helpful, or 'skip' to skip): ")
        if rating.isdigit() and 1 <= int(rating) <= 5:
            chatbot.store_feedback(query, response, rating)
        elif rating.lower() != 'skip':
            print("Invalid rating. Skipping feedback for this response.")


if __name__ == "__main__":
    main()
