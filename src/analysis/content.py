import os

def get_content(file_path):
    """
    Extracts the content of a file and returns it as a string.
    Handles errors for non-existent files, directories, and binary files.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: The content of the file as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        IsADirectoryError: If the given path is a directory.
        Exception: For any other errors that occur during reading.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file path '{file_path}' does not exist.")

    if os.path.isdir(file_path):
        raise IsADirectoryError(f"The path '{file_path}' is a directory, not a file.")

    try:
        with open(file_path, 'rb') as file:
            # Try reading the file in binary mode to check for binary content
            sample = file.read(1024)
            if b'\x00' in sample:  # Null bytes indicate binary content
                raise ValueError("Cannot open binary files.")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except ValueError as ve:
        raise ve
    except UnicodeDecodeError:
        raise ValueError("Cannot open binary files.")
    except Exception as e:
        raise Exception(f"Error reading file: {e}")
