import logging
# Initialize the logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
def get_prompt_request(stage: str):
    """
    Returns a template for prompts based on the stage of the FACTACON algorithm.

    Args:
        stage (str): The stage of the algorithm.

    Returns:
        str: Prompt template for the specified stage.
    """
    prompts = {
        "preprocessing_request": (
            "Using the results of the feature analysis, identify the specific files to be handled for the following feature request:\n\n"
            "Feature Request: {feature_request}\n\n"
            "Feature Analysis Results:\n{analysis_results}\n\n"
            "For each impacted file:\n"
            "- Provide the file path.\n"
            "- Specify the task to be performed on the file (e.g., modify, add functionality).\n\n"
            "For any new file required:\n"
            "- Specify the file path.\n"
            "- Provide a brief description of its purpose.\n"
            "- Suggest the initial content or structure the file should include.\n\n"
            "Ensure the output clearly separates existing files and new files to be created. "
            "Output this information as a JSON file with the following format:\n\n"
            "```json\n"
            "{{\n"
            "  \"feature_request\": \"{feature_request}\",\n"
            "  \"analysis_results\": \" \",\n"


            "  \"existing_files\": [\n"
            "    {{\n"
            "      \"file_path\": \"path/to/file.extension\",\n"
            "      \"task\": \"Modification needed in this file\"\n"
            "    }}\n"
            "  ],\n"
            "  \"new_files\": [\n"
            "    {{\n"
            "      \"file_path\": \"path/to/new/file.extension\",\n"
            "      \"purpose\": \"Purpose of the new file\" \n"
            "    }}\n"
            "  ]\n"
            "}}\n"
            "```"
        )
    }
    return prompts.get(stage, "Stage not found.")


import json
import re

def extract_json_from_response(response_text):
  """
  Extracts the JSON file from the given LLM response.

  Args:
    response_text: The LLM response containing the JSON file.

  Returns:
    A Python dictionary representing the JSON object, or None if no JSON is found.
  """
  try:
    # Find the JSON string using regular expression
    match = re.search(r'```json\n(.*?)```', response_text, re.DOTALL)
    if match:
      json_string = match.group(1)
      # Parse the JSON string
      json_object = json.loads(json_string)
      return json_object
    else:
      return None
  except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    return None