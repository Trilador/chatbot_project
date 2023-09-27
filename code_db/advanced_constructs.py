PYTHON_CODE_DB = {
    "class definition": (
        "class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    def greet(self):\n        return f'Hello, my name is {self.name} and I am {self.age} years old.'",
        "A basic class definition in Python with an initializer and a method."
    ),
    "file read": (
        "with open('filename.txt', 'r') as file:\n    content = file.read()",
        "Reading the content of a file in Python."
    ),
    "file write": (
        "with open('filename.txt', 'w') as file:\n    file.write('Hello, World!')",
        "Writing to a file in Python."
    ),
    "decorators": (
        "def my_decorator(func):\n    def wrapper():\n        print('Something is happening before the function is called.')\n        func()\n        print('Something is happening after the function is called.')\n    return wrapper\n\n@my_decorator\ndef say_hello():\n    print('Hello!')",
        "A basic decorator in Python that wraps a function to execute code before and after it."
    ),
    "generators": (
        "def fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        yield a\n        a, b = b, a + b",
        "A generator function in Python that yields the Fibonacci sequence."
    ),
    "list slicing": (
        "my_list = [0, 1, 2, 3, 4, 5]\nsub_list = my_list[1:4]",
        "Slicing a list in Python to get a sublist."
    ),
    "dictionary comprehension": (
        "{x: x**2 for x in (2, 4, 6)}",
        "A dictionary comprehension in Python that maps numbers to their squares."
    ),
    "set comprehension": (
        "{x for x in 'abracadabra' if x not in 'abc'}",
        "A set comprehension in Python that extracts unique letters excluding 'a', 'b', and 'c'."
    )
}
