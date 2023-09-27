from file_operations import (
    list_files,
    display_file_content,
    save_file_content,
    create_new_file,
    delete_file,
    rename_file
)
from code_generations import (
    natural_language_to_code,
    provide_code_feedback,
    interactive_code_correction,
    analyze_python_code_ast
)

def chatbot_response(query):
    query = query.strip().lower()

    # File operations
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
    elif "create new file" in query:
        filename = query.split("named")[-1].strip()
        return create_new_file(filename)
    elif "delete file" in query:
        filename = query.split("named")[-1].strip()
        return delete_file(filename)
    elif "rename file" in query:
        parts = query.split("to")
        old_filename = parts[0].split("rename file")[-1].strip()
        new_filename = parts[1].strip()
        return rename_file(old_filename, new_filename)

    # Code generation and analysis
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

    # Default response
    else:
        return "Sorry, I couldn't understand that query."

def main():
    print("Chatbot is now active. Type 'exit', 'quit', or 'bye' to end the session.")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit", "bye"]:
            print("Bot: Goodbye!")
            break
        response = chatbot_response(query)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
