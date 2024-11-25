import json
def generate_task_prompts(json_data: str) -> list:
    """
    Generates prompts for each task based on the provided JSON data.

    Args:
        json_data (str): JSON data as a string.

    Returns:
        list: A list of prompts, one for each task.
    """
    data = json.loads(json_data)
    feature_request = data["feature_request"]
    analysis_results = data["analysis_results"]
    prompts = []

    # Generate prompts for existing files
    for file in data.get("existing_files", []):
        task_prompt = (
            f"You are an expert at writing source code. Perform the following task:\n\n"
            f"Task Request: {file['task']}\n\n"
            f"Feature Request: {feature_request}\n\n"
            f"File Path: {file['file_path']}\n\n"
            f"File Content:\n{file['content']}\n\n"
            f"Analysis Results: {analysis_results}\n\n"
            f"Output ONLY the complete modified source code for the specified file. Do not include comments, explanations, or any other text."
        )
        prompts.append(task_prompt)

    # Generate prompts for new files
    for file in data.get("new_files", []):
        task_prompt = (
            f"You are an expert at writing source code. Perform the following task:\n\n"
            f"Task Request: Create a new file for {file['purpose']}\n\n"
            f"Feature Request: {feature_request}\n\n"
            f"File Path: {file['file_path']}\n\n"
            f"Analysis Results: {analysis_results}\n\n"
            f"Output ONLY the complete source code for the new file. Do not include comments, explanations, or any other text."
        )
        prompts.append(task_prompt)

    return prompts