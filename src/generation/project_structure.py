import os
import shutil
import logging
import json

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_project_structure(json_data: str, task_responses: list, old_project_path: str, new_project_path: str, overwrite: bool = True):
    """
    Updates the project structure by cloning the original project, modifying files based on task responses,
    and saving the updated files into a new project directory.

    Args:
        json_data (str): JSON data as a string.
        task_responses (list): List of source code responses for each task.
        old_project_path (str): Path to the original project directory.
        new_project_path (str): Path to save the new project directory.
        overwrite (bool): Whether to overwrite existing files in the new project structure.
    """
    # Step 1: Parse the JSON data
    data = json.loads(json_data)
    existing_files = data.get("existing_files", [])

    # Step 2: Clone the original project structure
    logger.info("Cloning the original project structure")
    if os.path.exists(new_project_path):
        shutil.rmtree(new_project_path)
    shutil.copytree(old_project_path, new_project_path)

    # Step 3: Update modified files with task responses
    logger.info("Updating modified files based on task responses")
    for i, file_info in enumerate(existing_files):
        old_file_path = file_info["file_path"]
        new_file_path = old_file_path.replace("project_old/", "project_new/")
        updated_content = task_responses[i]

        # Check if file exists and handle overwrite flag
        if not overwrite and os.path.exists(new_file_path):
            logger.info(f"File exists and overwrite is disabled: {new_file_path}. Keeping the original file.")
            continue

        # Ensure the new file directory exists
        new_file_dir = os.path.dirname(new_file_path)
        if not os.path.exists(new_file_dir):
            os.makedirs(new_file_dir)

        # Write the updated content to the new file
        with open(new_file_path, "w") as f:
            f.write(updated_content)
        logger.info(f"Updated file saved: {new_file_path}")

    # Step 4: Verify the new project structure
    logger.info("New project structure generated successfully")
    for root, _, files in os.walk(new_project_path):
        for file in files:
            logger.info(f"File in new project: {os.path.join(root, file)}")


import os
import json
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_expected_files_from_json(json_data: str) -> list:
    """
    Extracts the expected file paths from the given JSON data.

    Args:
        json_data (str): JSON data as a string.

    Returns:
        list: A list of expected file paths relative to the project root.
    """
    data = json.loads(json_data)
    existing_files = data.get("existing_files", [])
    expected_files = [file["file_path"].replace("project_old/", "") for file in existing_files]
    return expected_files
def validate_project_consistency(new_project_path: str, expected_files: list):
    """
    Validates the consistency of the new project structure by checking for expected files.

    Args:
        new_project_path (str): Path to the new project directory.
        expected_files (list): List of expected file paths relative to the project root.

    Returns:
        bool: True if all expected files are present, False otherwise.
    """
    logger.info("Validating consistency of the project tree")
    missing_files = []

    for expected_file in expected_files:
        expected_path = os.path.join(new_project_path, expected_file)
        if not os.path.exists(expected_path):
            missing_files.append(expected_path)

    if missing_files:
        logger.error("Validation failed. Missing files:")
        for file in missing_files:
            logger.error(file)
        return False

    logger.info("Validation passed. All files are present in the new project structure.")
    return True