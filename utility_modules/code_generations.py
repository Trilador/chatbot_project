import ast
import autopep8
import spacy
import openai

nlp = spacy.load("en_core_web_sm")

def get_main_verb_from_query(query):
    """Extract the main verb from the given query."""
    doc = nlp(query)
    return next((token for token in doc if "VERB" in token.pos_), None)

def natural_language_to_code(query: str) -> str:
    # Extract the main verb from the query to understand the context
    main_verb = get_main_verb_from_query(query)

    # Refine the query based on the main verb for better code generation
    refined_query = f"Write Python code for: {query}"
    if main_verb:
        verb_actions = {
            "loop": "Write a Python loop to",
            "check": "Write a Python conditional to",
            "function": "Write a Python function to",
            "import": "Write Python code to"
        }
        refined_query = f"{verb_actions.get(main_verb.lemma_, refined_query)} {query}"

    # Generate code using OpenAI
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=refined_query,
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=-0.25,
            presence_penalty=-0.25,
            stop=["\n", "User:", "Bot:"]
        )
        generated_code = response.choices[0].text.strip()
    except Exception as e:
        return f"Error generating code: {str(e)}"

    # Post-process and validate the generated code
    formatted_code = autopep8.fix_code(generated_code)
    try:
        ast.parse(formatted_code)
    except SyntaxError as e:
        return f"Generated code has a syntax error: {str(e)}"

    return formatted_code

def generate_loop_code(query):
    if "for" in query:
        return "for i in range(10):\n    print(i)"
    elif "while" in query:
        return "while condition:\n    # Do something"
    else:
        return "Sorry, I couldn't generate a loop code snippet for that query."

def provide_code_feedback(code):
    feedback = []
    if "import" in code and "os" in code:
        feedback.append("You've imported the 'os' module. Ensure you handle file operations safely.")
    if "open" in code and "with" not in code:
        feedback.append("It's recommended to use the 'with' statement when opening files for automatic closure.")
    return "\n".join(feedback)

def interactive_code_correction(code):
    corrected_code = autopep8.fix_code(code)
    if corrected_code == code:
        return "The code looks fine. No corrections needed.", code
    diff = difflib.ndiff(code.splitlines(), corrected_code.splitlines())
    changes = '\n'.join(diff)
    return f"Here are the suggested changes:\n{changes}", corrected_code

def analyze_python_code_ast(code):
    try:
        parsed_code = ast.parse(code)
        functions = [node.name for node in ast.walk(parsed_code) if isinstance(node, ast.FunctionDef)]
        classes = [node.name for node in ast.walk(parsed_code) if isinstance(node, ast.ClassDef)]
        variables = [node.id for node in ast.walk(parsed_code) if isinstance(node, ast.Name) and not any(isinstance(parent, (ast.FunctionDef, ast.ClassDef)) for parent in ast.iter_child_nodes(node))]
        
        feedback = []
        if not variables and not functions and not classes:
            feedback.append('The code doesn\'t seem to have any variables, functions, or classes.')
        if variables:
            feedback.append(f'Identified variables: {", ".join(variables)}')
        if functions:
            feedback.append(f'Identified functions: {", ".join(functions)}')
        if classes:
            feedback.append(f'Identified classes: {", ".join(classes)}')
        
        return "\n".join(feedback)
    except Exception as e:
        return f"Error analyzing the code: {str(e)}"
