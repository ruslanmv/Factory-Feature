import os
def extract_file_content_old(file_path):
    """
    Extracts the content of a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: The content of the file, or an error message if the file cannot be read.
    """

    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file {file_path}: {e}"
    else:
        return f"File not found: {file_path}"

def extract_file_content(file_path):
    """
    Extracts the content of a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: The content of the file, or an error message if the file cannot be read.
    """
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file {file_path}: {e}"
    else:
        return f"File not found: {file_path}"


import json

def count_tasks_from_json(json_data: str) -> int:
    """
    Counts all tasks to perform from the given JSON data.

    Args:
        json_data (str): JSON data as a string.

    Returns:
        int: Total number of tasks.
    """
    data = json.loads(json_data)
    existing_tasks = len(data.get("existing_files", []))
    new_tasks = len(data.get("new_files", []))
    return existing_tasks + new_tasks