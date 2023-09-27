from file_operations import *
from code_generation import *

def chatbot_response(query):
    if "list files" in query:
        return list_files()
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
        return "Sorry, I couldn't understand that query."

def main():
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit", "bye"]:
            break
        response = chatbot_response(query)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
