import os

def parse_project(project_path):
    """
    Parses a project directory, reading the content of each file.

    Args:
      project_path: The path to the project directory.

    Returns:
      A list of dictionaries, where each dictionary represents a file
      and contains the file path and its content.
    """
    project_data = []
    for root, dirs, files in os.walk(project_path):
        # Skip __pycache__ directories
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')

        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                project_data.append({"path": file_path, "content": content})
            except UnicodeDecodeError:
                print(f"Skipping binary file: {file_path}")
    return project_data