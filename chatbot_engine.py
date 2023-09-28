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
        f.write(f"Query: {query}\n")
        f.write(f"Response: {response}\n")
        f.write(f"Rating: {rating}\n")
        f.write("-" * 50 + "\n")

def chatbot_response(query: str) -> str:
    global context
    context.append(query)
    if len(context) > 5:  # Keep the last 5 interactions for context
        context.pop(0)

    # Enhanced File operations
    if any(phrase in query for phrase in ["show files", "list files", "display files"]):
        return list_files()
    if "list files" in query:
        return list_files()
    elif "list directories" in query:
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


# TODO Rename this here and in `chatbot_response`
def _extracted_from_chatbot_response_52(context, query):
    else:
        full_prompt = "\n".join(context + [query])
        response = openai.Completion.create(engine="davinci", prompt=full_prompt, max_tokens=TOKEN_LIMIT)
        response_text = response.choices[0].text.strip()

        # Response Filtering
        if len(response_text.split()) < 3 or "I think" in response_text or "I believe" in response_text:
            response_text = "I'm sorry, I couldn't generate a relevant response. Can you please rephrase or provide more details?"

        # Adjusted condition
        if len(response_text.split()) > TOKEN_LIMIT:
            return "My response seems too long. Would you like a more concise answer or should I clarify something specific?"
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
