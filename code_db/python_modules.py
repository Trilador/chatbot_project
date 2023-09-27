PYTHON_CODE_DB = {
    "working with datetime": (
        "from datetime import datetime\nnow = datetime.now()\nformatted_date = now.strftime('%Y-%m-%d %H:%M:%S')",
        "Working with the datetime module in Python to get the current date and time."
    ),
    "working with json": (
        "import json\ndata = {'name': 'John', 'age': 30}\njson_string = json.dumps(data)\nparsed_data = json.loads(json_string)",
        "Serializing and deserializing JSON data in Python."
    ),
    "regular expressions": (
        "import re\npattern = r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b'\nresult = re.search(pattern, 'my email is example@email.com')",
        "Using regular expressions in Python to find an email in a string."
    ),
    "working with os module": (
        "import os\n\n# Get current working directory\npath = os.getcwd()\n\n# List files in directory\nfiles = os.listdir(path)",
        "Using the os module in Python to interact with the operating system."
    ),
    "working with sys module": (
        "import sys\n\n# Get Python version\nversion = sys.version",
        "Using the sys module in Python to get the Python version."
    ),
    "working with pathlib": (
        "from pathlib import Path\n\n# Create a new Path object\npath = Path('example_directory/example_file.txt')\n\n# Check if path exists\nexists = path.exists()",
        "Using the pathlib module in Python for path-related tasks."
    ),
    "asyncio basics": (
        "import asyncio\n\nasync def main():\n    print('Hello')\n    await asyncio.sleep(1)\n    print('World')\n\nasyncio.run(main())",
        "Basic usage of asyncio in Python for asynchronous programming."
    ),
    "working with requests": (
        "import requests\n\nresponse = requests.get('https://www.example.com')\ncontent = response.text",
        "Using the requests module in Python to make an HTTP GET request."
    ),
    "creating a virtual environment": (
        "import venv\n\n# Create a new virtual environment\nvenv.create('path_to_new_virtual_environment')",
        "Using the venv module in Python to create a new virtual environment."
    ),
    "unpacking sequences": (
        "data = (1, 2, 3)\na, b, c = data",
        "Unpacking a sequence into multiple variables in Python."
    )
}
