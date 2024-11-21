import os

def parse_project(project_path):
    project_data = []
    for root, _, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            project_data.append({"path": file_path, "content": content})
    return project_data
