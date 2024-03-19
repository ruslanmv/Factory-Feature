import os
import pandas as pd

def search_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def get_file_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lstrip('.') if file_extension != '' else ''

def check_file_readability(file_list):
    df = pd.DataFrame(columns=['Path', 'Read', 'Extension', 'Content'])
    for file_path in file_list:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                extension = get_file_extension(file_path)
                df = df.append({'Path': file_path, 'Read': 'YES', 'Extension': extension, 'Content': content}, ignore_index=True)
        except (UnicodeDecodeError, IOError):
            extension = get_file_extension(file_path)
            df = df.append({'Path': file_path, 'Read': 'NO', 'Extension': extension, 'Content': ''}, ignore_index=True)
    return df

def save_to_txt(file_list):
    with open("files.txt", "w") as file:
        for file_name in file_list:
            file.write(file_name + "\n")
    print("File names saved to files.txt")

if __name__ == "__main__":
    directory = "./project_old"
    file_list = search_files(directory)
    save_to_txt(file_list)
    df = check_file_readability(file_list)
    print(df)
    
    # Save the DataFrame as a pickle file in the 'data' folder
    output_directory = "./data"
    os.makedirs(output_directory, exist_ok=True)
    output_file_path = os.path.join(output_directory, "output.pkl")
    df.to_pickle(output_file_path)
    print(f"DataFrame saved as {output_file_path}")
