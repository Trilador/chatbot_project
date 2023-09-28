import openai
import os
from typing import List, Union
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

DEFAULT_DIRECTORY = "C:\\Users\\timot\\Desktop\\Python\\AutoFix"
TOKEN_LIMIT = 150

# Contextual Understanding
context: List[str] = []

def store_feedback(query: str, response: str, rating: Union[int, str]) -> None:
    with open("feedback_data.txt", "a", encoding="utf-8") as f:
        f.write(f"Query: {query}\\n")
        f.write(f"Response: {response}\\n")
        f.write(f"Rating: {rating}\\n")
        f.write("-" * 50 + "\\n")

def check_code_db(query: str) -> Union[str, None]:
    return next(
        (
            f"{description}\n\nCode:\n{code}"
            for topic, (code, description) in {
                **ADVANCED_DB,
                **BASIC_DB,
                **MODULES_DB,
            }.items()
            if topic in query
        ),
        None,
    )

def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {e}"

def chatbot_response(query: str) -> str:
    global context
    context.append(query)
    if len(context) > 5:  # Keep the last 5 interactions for context
        context.pop(0)

    response = ""  # Initialize the response variable

    # Check for file reading requests
    if "C:\\" in query and ("read" in query or "open" in query or "type out" in query):
        file_path = query.split('"')[1]
        return read_file_content(file_path)

    if code_response := check_code_db(query):
        return code_response

    # Generate response using OpenAI API
    # ... [Rest of the OpenAI API call]

    # If the generated response is too similar to the user's query, provide a default response
    if response.strip() == query.strip():
        response = "I'm sorry, I didn't understand that. Can you please rephrase or provide more details?"



    # Enhanced File operations
    if any(phrase in query for phrase in ["show files", "list files", "display files"]):
        return list_files()
    if "list directories" in query:
        return list_directories()
    elif "create directory" in query:
        directory_name = query.split("named")[-1].strip()
        return create_directory(directory_name)
    elif "delete directory" in query:
        directory_name = query.split("named")[-1].strip()
        return delete_directory(directory_name)
    elif "display content" in query:
        filename = query.split("of")[-1].strip()
        return display_file_content(filename)
    elif "save content" in query:
        parts = query.split("of")
        filename = parts[-2].strip()
        content = parts[-1].strip()
        return save_file_content(filename, content)
    elif "search content" in query:
        content = query.split("for")[-1].strip()
        return search_file_content(content)

    # Enhanced Code generation and analysis
    if "write code" in query or "generate code" in query:
        return natural_language_to_code(query)
    elif "provide feedback" in query:
        code = query.split("for")[-1].strip()
        return provide_code_feedback(code)
    elif "correct code" in query:
        code = query.split("for")[-1].strip()
        feedback, corrected_code = interactive_code_correction(code)
        return feedback
    elif "analyze code" in query:
        code = query.split("for")[-1].strip()
        return analyze_python_code_ast(code)
    elif "wikipedia summary" in query:
        return fetch_wikipedia_summary(query)
    elif "search documentation" in query:
        topic = query.split("for")[-1].strip()
        return search_python_documentation(topic)
    else:
        return _extracted_from_chatbot_response_52(context, query)

def _extracted_from_chatbot_response_52(context, query):
    
    # Using the entire conversation history for context
    full_prompt = "\\n".join(context + [f"User: {query}\\nBot:"])
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=full_prompt,
            temperature=0.7,
            max_tokens=TOKEN_LIMIT,
            top_p=1,
            frequency_penalty=-0.25,
            presence_penalty=-0.25,
            stop=["\\n", "User:", "Bot:"]
        )
        response_text = response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        return f"OpenAI Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}. I'm having some issues right now. Try again later."
    
    # Enhanced Response Filtering
    last_user_query = context[-2] if len(context) > 1 else None
    last_bot_response = context[-1] if len(context) > 1 else None
    if response_text == last_bot_response and query == last_user_query:
        response_text = "I've already provided that response. Can you please rephrase or ask a different question?"


    # Adjusted condition
    if len(response_text.split()) > TOKEN_LIMIT:
        response_text = "My response seems too long. Would you like a more concise answer or should I clarify something specific?"

    return response_text

def main() -> None:
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit", "bye"]:
            break
        response = chatbot_response(query)
        print(f"Bot: {response}")

        # Feedback mechanism
        rating = input("Rate the response (1-5, 5 being very helpful, or 'skip' to skip): ")
        if rating.isdigit() and 1 <= int(rating) <= 5:
            store_feedback(query, response, rating)
        elif rating.lower() != 'skip':
            print("Invalid rating. Skipping feedback for this response.")

if __name__ == "__main__":
    main()