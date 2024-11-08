import os

def read_file(file_path):
    """
    Reads the content of a file.

    Args:
        file_path: Path to the file.

    Returns:
        Content of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(file_path, content):
    """
    Writes content to a file.

    Args:
        file_path: Path to the file.
        content: Content to write.

    Returns:
        None
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
