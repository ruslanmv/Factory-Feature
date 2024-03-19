import os

def search_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def save_to_txt(file_list):
    with open("files.txt", "w") as file:
        for file_name in file_list:
            file.write(file_name + "\n")
    print("File names saved to files.txt")

if __name__ == "__main__":
    directory = "./"
    file_list = search_files(directory)
    save_to_txt(file_list)
    
