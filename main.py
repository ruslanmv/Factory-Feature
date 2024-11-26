import argparse
import os
import shutil
import json
from src.analysis.project_parser import parse_project
from src.analysis.dependency_resolver import resolve_dependencies
from src.analysis.feature_mapper import map_features_to_components
from src.generation.project_generator import generate_project
from src.generation.feature_integration import integrate_features
from src.models.llm_inference import query_llm
from src.models.prompt_templates import get_prompt_template, get_prompt_template_feature
from src.utils.logger import logger
from src.utils.file_operations import read_file, write_file
from src.vector_database.db_query import query_vector_database
from src.vector_database.db_load import load_vector_database
from src.vector_database.db_builder_simple import build_vector_database_simple
from src.vector_database.db_builder import build_vector_database
from src.vector_database.display_content import display_first_five_documents
from src.analysis.tree import get_tree
from src.generation.preprocessing import get_prompt_request
from src.utils.tools import extract_file_content, count_tasks_from_json
from src.generation.task_prompts import generate_task_prompts
from src.generation.project_structure import (
    update_project_structure,
    create_expected_files_from_json,
    validate_project_consistency,
)
from src.generation.preprocessing import extract_json_from_response
from src.utils.tools import count_tasks_from_json
from src.generation.task_prompts import generate_task_prompts



def main(user_request: str):
    """
    Main function to integrate a feature request into the project.

    Args:
        user_request (str): The feature request prompt.
    """

    logger.info(f"Processing feature request: {user_request}")
    # Define paths
    OLD_PROJECT_PATH = "project_old"
    NEW_PROJECT_PATH = "project_new"

    logger.info("Starting the Factory Feature program")

    # Step 1: Parse the project
    logger.info("Parsing the project structure")
    try:
        project_data = parse_project(OLD_PROJECT_PATH)
        logger.info("Project parsed successfully.")
    except FileNotFoundError as e:
        logger.error(f"Failed to parse project: {e}")
        exit(1)

    # Step 2: Build vector database
    logger.info("Building vector database")
    try:
        vector_db = build_vector_database(project_data, persist_directory="./chroma_db")
        logger.info("Vector database created successfully.")
    except Exception as e:
        logger.error(f"Failed to build vector database: {e}")
        exit(1)

    # Step 3: Resolve dependencies
    logger.info("Resolving project dependencies")
    try:
        dependencies = resolve_dependencies(OLD_PROJECT_PATH)
        logger.info(f"Dependencies resolved: {list(dependencies.keys())}")
    except Exception as e:
        logger.error(f"Dependency resolution failed: {e}")
        exit(1)

    # Step 4: Map features to components
    logger.info("Mapping feature request to project components")
    try:
        feature_template = get_prompt_template_feature()
        project_context = "\n".join(
            [f"{key}: {value}" for key, value in dependencies.items()]
        )
        tree = get_tree(OLD_PROJECT_PATH)
        project_context += f"\n{tree}"
        logger.info("Feature mapping completed successfully.")
    except Exception as e:
        logger.error(f"Feature mapping failed: {e}")
        exit(1)

    # Step 5: Perform feature analysis
    logger.info("Performing feature analysis")
    try:
        feature_nodes_template = get_prompt_template("feature_analysis_nodes")
        feature_edges_template = get_prompt_template("feature_analysis_edges")
        impact_report_template = get_prompt_template("feature_impact_report")

        feature_nodes = feature_nodes_template.format(
            feature_request=user_request, project_context=project_context
        )
        feature_edges = feature_edges_template.format(
            feature_request=user_request, project_context=project_context
        )
        impact_report = impact_report_template.format(
            feature_request=user_request, project_context=project_context
        )

        feature_nodes_response = query_llm(user_input=feature_nodes, vector_db=vector_db)
        feature_edges_response = query_llm(user_input=feature_edges, vector_db=vector_db)
        impact_report_response = query_llm(user_input=impact_report, vector_db=vector_db)

        analysis_results = (
            f"Nodes:\n{feature_nodes_response}\n\n"
            f"Edges:\n{feature_edges_response}\n\n"
            f"Report:\n{impact_report_response}"
        )
        logger.info("Feature analysis completed successfully.")
    except Exception as e:
        logger.error(f"Feature analysis failed: {e}")
        exit(1)

    # Step 6: Preprocessing results
    logger.info("Preprocessing results of feature analysis")
    try:
        preprocessing_template = get_prompt_request("preprocessing_request")
        preprocessing_prompt = preprocessing_template.format(
            feature_request=user_request,
            analysis_results=analysis_results,
        )
        preprocessing_response = query_llm(user_input=preprocessing_prompt, vector_db=vector_db)
        logger.info("Preprocessing completed successfully.")
    except Exception as e:
        logger.error(f"Preprocessing failed: {e}")
        exit(1)

    # Step 5.1: Performing preprocessing
    try:
        logger.info("Performing preprocessing")
        json_object = extract_json_from_response(preprocessing_response)
        if json_object:
            #print(json.dumps(json_object, indent=2))
            logger.info("Preprocessing completed extraction successfully.")
        else:
            print("No JSON found in the response.")
        
    except Exception as e:
        logger.error(f"Preprocessing  extraction failed: {e}")
        exit(1)  

    # Step 5.2: Perform preprocessing extension
    try:
        # Extend the JSON object
        logger.info("Performing preprocessing extension")
        for file_info in json_object['existing_files']:
            file_path = file_info.get('file_path', '')
            if file_path:
                file_info['content'] = extract_file_content(file_path)

        # Display the updated JSON object
        #import json
        #print(json.dumps(json_object, indent=4))            
        logger.info("Preprocessing completed extension successfully.")        
    except Exception as e:
        logger.error(f"Preprocessing  extension failed: {e}")
        exit(1)  
    # Step 5.3: Count tasks
    try:
        # Extend the JSON object
        logger.info("Performing counts")

        json_data=json.dumps(json_object, indent=4)
        # Count tasks
        task_count = count_tasks_from_json(json_data)
        print(f"Total tasks to perform: {task_count}")
    except Exception as e:
        logger.error(f"Count tasks failed: {e}")
        exit(1)     

    # Step 5.4:  Generate task prompts
    try:
        # Extend the JSON object
        logger.info("Generate task prompts")
        task_prompts = generate_task_prompts(json_data)
        logger.info("Generate task prompts successfully.")  
    except Exception as e:
        logger.error(f"Generate task prompts failed: {e}")
        exit(1)    
    # Step 5.5:  Generate task prompts
    try:
        # Extend the JSON object
        logger.info("Generate task_responses")
        task_responses=[]
        # Query the LLM for each prompt and ensure the response is limited to source code
        for i, task_prompt in enumerate(task_prompts, start=1):
            print(f"\nPrompt {i}:\n{task_prompt}\n")
            task_response = query_llm(user_input=task_prompt)  # Replace with the appropriate LLM query function
            task_responses.append(task_response)

        # Print the raw source code responses
        for i, response in enumerate(task_responses, start=1):
            print(f"\nSource Code for Task {i}:\n{response}")

        logger.info("Generate task_responses successfully.")     
    except Exception as e:
        logger.error(f"Generate task_responses prompts failed: {e}")
        exit(1)  

    # Step 7: update project
    logger.info("updating project files")
    try:
        update_project_structure(
            json.dumps(json_object, indent=4), task_responses, OLD_PROJECT_PATH, NEW_PROJECT_PATH
        )
        logger.info("Project files updated successfully.")
    except Exception as e:
        logger.error(f"Failed to update project: {e}")
        exit(1)     

    # Step 8: Validate the new project structure
    logger.info("Validating the new project structure")
    try:
        expected_files = create_expected_files_from_json(json.dumps(json_object, indent=4))
        is_valid = validate_project_consistency(NEW_PROJECT_PATH, expected_files)
        if is_valid:
            logger.info("The project structure is consistent.")
        else:
            logger.error("The project structure is inconsistent.")
            exit(1)
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        exit(1)
    # Completion message
    logger.info(f"Feature integration completed. Updated project saved in: {NEW_PROJECT_PATH}")
import argparse
import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Factory Feature Program")
    parser.add_argument("--prompt", required=True, help="Feature request prompt")   
    try:
        args = parser.parse_args()
        main(args.prompt)
    except SystemExit as e:
        if e.code == 2:  # Indicates missing required arguments
            logger.error("Argument parsing failed. Please provide the required '--prompt' argument.")
            parser.print_help()
        else:
            raise
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

#python main.py --prompt "Add logging functionality to all major modules in the project"
