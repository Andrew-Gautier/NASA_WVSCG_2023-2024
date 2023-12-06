# Python
import os
import re

def remove_comments(filename):
    with open(filename, 'r') as file:
        content = file.read()

    # Remove single-line comments
    content = re.sub(r'//.*', '', content)

    # Remove multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    with open(filename, 'w') as file:
        file.write(content)

# Replace 'your_directory' with the path to the directory you want to search
for root, dirnames, filenames in os.walk(r'C:\Users\Andrew\Desktop\Cleaned C++ mini output'):
    for filename in filenames:
        if filename.endswith(('.cpp', '.cs', '.java', '.php', '.c')):
            remove_comments(os.path.join(root, filename))