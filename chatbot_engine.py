from utility_modules.file_operations import *
from utility_modules.code_generations import *
import openai

# Configuration Setup:##
# Set up the OpenAI API
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")
# Set up the Wikipedia API
#wiki_wiki = wikipediaapi.Wikipedia('ttriladorr@gmail.com/0.1')
# Set default directory for access 
DEFAULT_DIRECTORY = "C:\\Users\\timot\\Desktop\\Python\\AutoFix"


def chatbot_response(query):
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
    elif "generate code" in query:
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
    else:
        # Forward the query to OpenAI for a natural language response
        response = openai.Completion.create(engine="davinci", prompt=query, max_tokens=150)
        return response.choices[0].text.strip()

def main():
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit", "bye"]:
            break
        response = chatbot_response(query)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
