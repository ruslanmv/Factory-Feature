import os
import shutil

def generate_project(old_project_path, new_project_path, feature_instructions):
    # Copy old project structure to new directory
    if os.path.exists(new_project_path):
        shutil.rmtree(new_project_path)
    shutil.copytree(old_project_path, new_project_path)

    # Apply feature instructions
    for instruction in feature_instructions:
        file_path = os.path.join(new_project_path, instruction["file"])
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(instruction["content"])
