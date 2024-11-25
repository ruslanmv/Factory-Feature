import os

def get_tree(folder_path, content=False, exclude_folders=None):
    """
    Generate a tree structure of the given folder path, including file names, paths, 
    and optionally their content.

    Args:
        folder_path (str): Path to the folder to generate the tree structure from.
        content (bool): Whether to include file contents in the tree. Default is False.
        exclude_folders (list): A list of folder names to exclude from the tree.

    Returns:
        dict: Nested dictionary representing the folder structure.
    """
    if exclude_folders is None:
        exclude_folders = ["__pycache__", ".git", ".idea", "node_modules", "venv"]  # Default excluded folders

    def build_tree(path):
        structure = []
        if os.path.isdir(path):
            for item in os.listdir(path):
                if item in exclude_folders:
                    continue  # Skip excluded folders

                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    # Recursively add subdirectory
                    structure.append({
                        "type": "directory",
                        "name": item,
                        "path": item_path,
                        "children": build_tree(item_path)
                    })
                else:
                    # Add file details
                    file_info = {
                        "type": "file",
                        "name": item,
                        "path": item_path
                    }
                    if content:
                        try:
                            with open(item_path, 'r', encoding='utf-8') as file:
                                file_info["content"] = file.read()
                        except Exception as e:
                            file_info["content"] = f"Error reading file: {e}"
                    structure.append(file_info)
        return structure

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")

    return {
        "project_name": os.path.basename(folder_path),
        "structure": build_tree(folder_path)
    }

if __name__ == "__main__":
    old_project_path = "project_old"
    try:
        # Get the tree structure without content
        tree = get_tree(old_project_path)
        print(tree)

        # Get the tree structure with content
        tree_with_content = get_tree(old_project_path, content=True)
        print(tree_with_content)
    except FileNotFoundError as e:
        print(e)