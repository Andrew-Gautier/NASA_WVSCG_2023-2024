# Python
import os
import re
from sarif_om import SarifLog
import json
from db_loader import Folder, SourceCodeFile, Manifest, Vulnerability, session

def remove_comments(root_dir):
    for dir_name, _, file_list in os.walk(root_dir):
        for file_name in file_list:
            if file_name.endswith(('.c', '.php', '.cpp', '.java', '.cs')):
                file_path = os.path.join(dir_name, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Remove single-line comments
                content = re.sub(r'//.*|^\s*#.*', '', content, flags=re.MULTILINE)

                # Remove multi-line comments
                content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

                content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)

def remove_files_except_code_and_sarif(root_dir):
                        code_extensions = ['.c', '.cpp', '.php', '.java', '.cs']
                        manifest_file = 'manifest.sarif'

                        for dir_name, _, file_list in os.walk(root_dir):
                            for file_name in file_list:
                                file_path = os.path.join(dir_name, file_name)
                                file_extension = os.path.splitext(file_name)[1]

                                if file_extension.lower() not in code_extensions and file_name != manifest_file:
                                    os.remove(file_path)
class SarifLog:
    def __init__(self, state, start_line, codepath):
        self.state = state
        self.start_line = start_line
        self.codepath = codepath

# 11-29 I am experimenting with using this class to store the information from the sarif file.
# class Info:
#     def __init__(self, state, start_line, codepath):
#         self.state = state
#         self.start_line = start_line
#         self.codepath = codepath        

def read_sarif_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file, strict=False)
    except IOError:
        print(f"Cannot open file: {file_path}")
        return []

    # Extract the state from the data
    state = data['runs'][0]['properties']['state']

    # Initialize an empty list to hold the SarifLog objects
    sarif_logs = []

    # Iterate over the results
    for result in data['runs'][0]['results']:
        # Iterate over the locations in each result
        for location in result['locations']:
            # Extract the startLine and codepath from the location
            start_line = location['physicalLocation']['region']['startLine']
            codepath = location['physicalLocation']['artifactLocation']['uri']

            # Create a new SarifLog object and add it to the list
            sarif_log = SarifLog(state, start_line, codepath)
            sarif_logs.append(sarif_log)

    return sarif_logs

def extract_info(sarif_logs):
    state = sarif_logs.state
    start_line = sarif_logs.start_line
    codepath = sarif_logs.codepath  
    return state, start_line, codepath  

def sarifparser(root_dir): 
    info_list = []
    for dir_name, _, file_list in os.walk(root_dir):
        for file_name in file_list:
            if file_name == 'manifest.sarif':
                file_path = os.path.join(dir_name, file_name)
                sarif_logs = read_sarif_file(file_path)
                if sarif_logs is None:
                    continue
                for sarif_log in sarif_logs:
                    state, start_line, codepath = extract_info(sarif_log)  
                    info_list.append((state, start_line, codepath))  
    return info_list


def store_in_database(info_list):
    # Add code to store info_list in the database
    pass

def main():
    output_dir = ''
    root_dir = 'C:\\Users\\Andrew\\Desktop\\C++ mini test 2'

    remove_comments(root_dir)
    remove_files_except_code_and_sarif(root_dir)
    info_list = sarifparser(root_dir)

    # Get the file extensions in the root_dir
    file_extensions = set()
    file_list = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file_name in filenames:
            file_extension = os.path.splitext(file_name)[1]
            file_extensions.add(file_extension)
            file_list.append(file_name)
            print(file_name)
            print(file_extension)
    for info in info_list:
        full_path = os.path.join(root_dir, info.codepath)
        with open(full_path, 'r') as file:
            file_content = file.read()


        # 11-28-2023 Here is where I am going to start working on the database loading. 
        new_folder = Folder(folder_name='11-29_test_folder')
        session.add(new_folder)

        new_file = SourceCodeFile(folder=new_folder, file_name=info.codepath, file_extension=file_extensions, file_content=file_content)
        session.add(new_file)

        # Create a new manifest for the new file
        new_manifest = Manifest(source_code_file=new_file, sarif_content='{}')
        session.add(new_manifest)

        # Create a new vulnerability for the new manifest
        new_vulnerability = Vulnerability(manifest=new_manifest, line_number= info.start_line, vulnerability_type=info.state)
        session.add(new_vulnerability) 

        # Commit the session to save the objects to the database
        session.commit()

if __name__ == '__main__':
    main()