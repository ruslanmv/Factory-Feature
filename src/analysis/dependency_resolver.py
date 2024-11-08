import os

def resolve_dependencies(project_path):
    """
    Resolves dependencies in the project by scanning for dependency files.

    Args:
        project_path: Path to the project directory.

    Returns:
        List of dependencies.
    """
    dependency_files = ["requirements.txt", "package.json", "pom.xml"]
    dependencies = {}

    for root, _, files in os.walk(project_path):
        for file in files:
            if file in dependency_files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    dependencies[file] = f.readlines()

    return dependencies
