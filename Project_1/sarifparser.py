import json
import os
import glob

def read_sarif_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_info(data):
    # Extract the necessary information from the parsed JSON
    # For now, let's just return the 'runs' part of the data
    return data['runs']

def main():import json
import os
import glob
import shutil

def read_sarif_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_info(data):
    # Extract the necessary information from the parsed JSON
    # For now, let's just return the 'results' part of the data
    return data['runs'][0]['results']

def main():
    root_dir = 'C:\\Users\\Andrew\\Desktop\\C++ mini test'  # Replace with your root directory
    output_file_path = 'output.txt'  # Replace with the path to your output file
    with open(output_file_path, 'w') as output_file:
        for dir_name, _, file_list in os.walk(root_dir):
            for file_name in file_list:
                if file_name == 'manifest.sarif':
                    file_path = os.path.join(dir_name, file_name)
                    data = read_sarif_file(file_path)
                    results = extract_info(data)
                    for result in results:
                        rule_id = result['ruleId']
                        start_line = result['locations'][0]['physicalLocation']['region']['startLine']
                        src_file_uri = result['locations'][0]['physicalLocation']['artifactLocation']['uri']
                        src_file_name = os.path.basename(src_file_uri)
                        src_file_path = os.path.join(dir_name, src_file_uri)
                        new_file_name = f"{src_file_name[:-4]}_{rule_id}_{start_line}{src_file_name[-4:]}"
                        new_file_path = os.path.join(dir_name, 'src', new_file_name)
                        shutil.copy(src_file_path, new_file_path)  # Copy the source file to the new file
                        output_file.write(f"Copied {src_file_path} to {new_file_path}\n")

if __name__ == '__main__':
    main()
    
    import json
    import os
    import glob
    import shutil

    def read_sarif_file(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def extract_info(data):
        # Extract the necessary information from the parsed JSON
        # For now, let's just return the 'results' part of the data
        return data['runs'][0]['results']

    def main():
        root_dir = 'C:\\Users\\Andrew\\Desktop\\Taxonomy of buffer overflows'  # Replace with your root directory
        for dir_name, _, file_list in os.walk(root_dir):
            for file_name in file_list:
                if file_name == 'manifest.sarif':
                    file_path = os.path.join(dir_name, file_name)
                    data = read_sarif_file(file_path)
                    results = extract_info(data)
                    for result in results:
                        rule_id = result['ruleId']
                        start_line = result['locations'][0]['physicalLocation']['region']['startLine']
                        src_file_uri = result['locations'][0]['physicalLocation']['artifactLocation']['uri']
                        src_file_name = os.path.basename(src_file_uri)
                        src_file_path = os.path.join(dir_name, src_file_uri)
                        new_file_name = f"{src_file_name[:-4]}_{rule_id}_{start_line}{src_file_name[-4:]}"
                        new_file_path = os.path.join(dir_name, 'src', new_file_name)
                        shutil.copy(src_file_path, new_file_path)  # Copy the source file to the new file

    if __name__ == '__main__':
        main()
    root_dir = 'C:\\Users\\Andrew\\Desktop\\C++ mini test'  # Replace with your root directory
    for dir_name, _, file_list in os.walk(root_dir):
        for file_name in file_list:
            if file_name == 'manifest.sarif':
                file_path = os.path.join(dir_name, file_name)
                data = read_sarif_file(file_path)
                info = extract_info(data)
                print(info)  # For now, just print the extracted information
                src_files = glob.glob(os.path.join(dir_name, 'src', '*'))
                for src_file in src_files:
                    print(src_file)  # For now, just print the source file paths

