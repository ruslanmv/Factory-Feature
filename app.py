import argparse
import os
import shutil
from src.analysis.project_parser import parse_project
from src.analysis.dependency_resolver import resolve_dependencies
from src.analysis.feature_mapper import map_features_to_components
from src.generation.project_generator import generate_project
from src.generation.feature_integration import integrate_features
from src.models.llm_inference import query_llm
from src.models.prompt_templates import get_prompt_template
from src.utils.logger import logger
from src.utils.file_operations import read_file, write_file
from src.vector_database.db_builder_old import build_vector_database
from src.vector_database.db_query import query_vector_database


def main(prompt):
    logger.info("Starting the Factory Feature program")

    # Define paths
    old_project_path = "project_old"
    new_project_path = "project_new"

    # Step 1: Parse the old project
    logger.info("Parsing the project structure")
    project_data = parse_project(old_project_path)
    vector_db = build_vector_database(project_data)
    logger.info("Vector database created for the project")

    # Step 2: Resolve dependencies
    logger.info("Resolving project dependencies")
    dependencies = resolve_dependencies(old_project_path)
    logger.info(f"Dependencies found: {dependencies.keys()}")

    # Step 3: Map features to project components
    logger.info("Mapping feature request to project components")
    feature_template = get_prompt_template()
    project_context = "\n".join([f"{key}: {value}" for key, value in dependencies.items()])
    feature_request = feature_template.format(feature_request=prompt, project_context=project_context)
    relevant_docs = query_vector_database(vector_db, feature_request)
    logger.info(f"Relevant documents for the feature request: {[doc.metadata['source'] for doc in relevant_docs]}")

    # Step 4: Generate new project structure
    logger.info("Generating the updated project structure")
    if os.path.exists(new_project_path):
        shutil.rmtree(new_project_path)
    shutil.copytree(old_project_path, new_project_path)

    # Step 5: Integrate new features
    logger.info("Integrating new features into the project")
    for doc in relevant_docs:
        integrate_features([doc.metadata["source"]], f"# Feature: {prompt}\n{doc.page_content}")

    # Step 6: Generate additional files or modify existing ones
    feature_instructions = [
        {"file": os.path.relpath(doc.metadata["source"], old_project_path), "content": f"# Feature: {prompt}\n{doc.page_content}"}
        for doc in relevant_docs
    ]
    generate_project(old_project_path, new_project_path, feature_instructions)

    logger.info("Feature integration completed")
    print(f"Project updated with the feature: {prompt}")
    print(f"Updated project saved in: {new_project_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Factory Feature Program")
    parser.add_argument("--prompt", required=True, help="Feature request prompt")
    args = parser.parse_args()

    try:
        main(args.prompt)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
