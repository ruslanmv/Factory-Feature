"""
Factory Feature - Main CLI Entry Point.

This module provides the command-line interface for the Factory Feature system.
It orchestrates the entire pipeline from project analysis to feature integration.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

import argparse
import json
import logging
import sys
from typing import Any, Dict, List, Optional

from src.analysis.dependency_resolver import resolve_dependencies
from src.analysis.feature_mapper import map_features_to_components
from src.analysis.project_parser import parse_project
from src.analysis.tree import get_tree
from src.generation.preprocessing import extract_json_from_response, get_prompt_request
from src.generation.project_generator import generate_project
from src.generation.project_structure import (
    create_expected_files_from_json,
    update_project_structure,
    validate_project_consistency,
)
from src.generation.task_prompts import generate_task_prompts
from src.models.llm_inference import query_llm
from src.models.prompt_templates import get_prompt_template, get_prompt_template_feature
from src.utils.file_operations import read_file, write_file
from src.utils.logger import logger
from src.utils.tools import count_tasks_from_json, extract_file_content
from src.vector_database.db_builder import build_vector_database
from src.vector_database.db_load import load_vector_database
from src.vector_database.db_query import query_vector_database
from src.vector_database.display_content import display_first_five_documents

# Configure additional logging for CLI
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
cli_logger = logging.getLogger(__name__)


def main(user_request: str) -> None:
    """
    Main orchestration function for the Factory Feature pipeline.

    This function coordinates the entire feature integration workflow:
    1. Parse the existing project structure
    2. Build a vector database for context retrieval
    3. Resolve project dependencies
    4. Analyze feature impact and generate tasks
    5. Execute LLM-powered code generation
    6. Update project structure with new features
    7. Validate the consistency of the updated project

    Args:
        user_request: Natural language description of the feature to integrate.

    Raises:
        FileNotFoundError: If the project directory is not found.
        ValueError: If JSON extraction or preprocessing fails.
        RuntimeError: If any critical step in the pipeline fails.

    Example:
        >>> main("Add logging functionality to all major modules")
    """
    logger.info(f"Processing feature request: {user_request}")

    # Define project paths
    OLD_PROJECT_PATH = "project_old"
    NEW_PROJECT_PATH = "project_new"

    logger.info("=" * 80)
    logger.info("Starting Factory Feature Pipeline")
    logger.info("=" * 80)

    # Step 1: Parse the project structure
    logger.info("[Step 1/8] Parsing project structure...")
    try:
        project_data = parse_project(OLD_PROJECT_PATH)
        logger.info(f"✓ Project parsed successfully ({len(project_data)} files)")
    except FileNotFoundError as e:
        logger.error(f"✗ Failed to parse project: {e}")
        logger.error(f"Please ensure '{OLD_PROJECT_PATH}' directory exists")
        sys.exit(1)
    except Exception as e:
        logger.error(f"✗ Unexpected error during project parsing: {e}")
        sys.exit(1)

    # Step 2: Build vector database for RAG
    logger.info("[Step 2/8] Building vector database for context retrieval...")
    try:
        vector_db = build_vector_database(project_data, persist_directory="./chroma_db")
        logger.info("✓ Vector database created successfully")
    except Exception as e:
        logger.error(f"✗ Failed to build vector database: {e}")
        sys.exit(1)

    # Step 3: Resolve project dependencies
    logger.info("[Step 3/8] Resolving project dependencies...")
    try:
        dependencies = resolve_dependencies(OLD_PROJECT_PATH)
        dep_types = list(dependencies.keys())
        logger.info(f"✓ Dependencies resolved: {', '.join(dep_types) if dep_types else 'None'}")
    except Exception as e:
        logger.error(f"✗ Dependency resolution failed: {e}")
        sys.exit(1)

    # Step 4: Build project context for LLM
    logger.info("[Step 4/8] Building project context...")
    try:
        project_context = "\n".join([f"{key}: {value}" for key, value in dependencies.items()])
        tree = get_tree(OLD_PROJECT_PATH)
        project_context += f"\n\nProject Structure:\n{tree}"
        logger.info("✓ Project context built successfully")
    except Exception as e:
        logger.error(f"✗ Failed to build project context: {e}")
        sys.exit(1)

    # Step 5: Perform AI-powered feature analysis
    logger.info("[Step 5/8] Performing AI-powered feature analysis...")
    try:
        # Get prompt templates
        feature_nodes_template = get_prompt_template("feature_analysis_nodes")
        feature_edges_template = get_prompt_template("feature_analysis_edges")
        impact_report_template = get_prompt_template("feature_impact_report")

        # Format prompts with context
        feature_nodes_prompt = feature_nodes_template.format(
            feature_request=user_request, project_context=project_context
        )
        feature_edges_prompt = feature_edges_template.format(
            feature_request=user_request, project_context=project_context
        )
        impact_report_prompt = impact_report_template.format(
            feature_request=user_request, project_context=project_context
        )

        # Query LLM for analysis
        logger.info("  - Analyzing feature nodes...")
        feature_nodes_response = query_llm(user_input=feature_nodes_prompt, vector_db=vector_db)

        logger.info("  - Analyzing feature edges...")
        feature_edges_response = query_llm(user_input=feature_edges_prompt, vector_db=vector_db)

        logger.info("  - Generating impact report...")
        impact_report_response = query_llm(user_input=impact_report_prompt, vector_db=vector_db)

        # Combine analysis results
        analysis_results = (
            f"Nodes:\n{feature_nodes_response}\n\n"
            f"Edges:\n{feature_edges_response}\n\n"
            f"Impact Report:\n{impact_report_response}"
        )
        logger.info("✓ Feature analysis completed successfully")
    except Exception as e:
        logger.error(f"✗ Feature analysis failed: {e}")
        sys.exit(1)

    # Step 6: Preprocessing and task extraction
    logger.info("[Step 6/8] Preprocessing analysis results and extracting tasks...")
    try:
        preprocessing_template = get_prompt_request("preprocessing_request")
        preprocessing_prompt = preprocessing_template.format(
            feature_request=user_request,
            analysis_results=analysis_results,
        )
        preprocessing_response = query_llm(
            user_input=preprocessing_prompt, vector_db=vector_db
        )

        # Extract JSON object from response
        json_object = extract_json_from_response(preprocessing_response)
        if not json_object:
            raise ValueError("No valid JSON found in preprocessing response")

        # Enrich JSON with file contents
        for file_info in json_object.get("existing_files", []):
            file_path = file_info.get("file_path", "")
            if file_path:
                file_info["content"] = extract_file_content(file_path)

        # Count and log tasks
        json_data = json.dumps(json_object, indent=4)
        task_count = count_tasks_from_json(json_data)
        logger.info(f"✓ Preprocessing completed: {task_count} tasks identified")

    except ValueError as e:
        logger.error(f"✗ JSON extraction failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"✗ Preprocessing failed: {e}")
        sys.exit(1)

    # Step 7: Generate and execute task prompts
    logger.info("[Step 7/8] Generating task prompts and executing code generation...")
    try:
        task_prompts = generate_task_prompts(json_data)
        task_responses: List[str] = []

        logger.info(f"  - Executing {len(task_prompts)} LLM queries...")
        for i, task_prompt in enumerate(task_prompts, start=1):
            logger.info(f"    Processing task {i}/{len(task_prompts)}...")
            task_response = query_llm(user_input=task_prompt)
            task_responses.append(task_response)

        logger.info("✓ All tasks executed successfully")

    except Exception as e:
        logger.error(f"✗ Task execution failed: {e}")
        sys.exit(1)

    # Step 8: Update project structure
    logger.info("[Step 8/8] Updating project structure with generated code...")
    try:
        update_project_structure(json_data, task_responses, OLD_PROJECT_PATH, NEW_PROJECT_PATH)
        logger.info("✓ Project files updated successfully")
    except Exception as e:
        logger.error(f"✗ Failed to update project structure: {e}")
        sys.exit(1)

    # Final validation
    logger.info("Validating updated project structure...")
    try:
        expected_files = create_expected_files_from_json(json_data)
        is_valid = validate_project_consistency(NEW_PROJECT_PATH, expected_files)

        if is_valid:
            logger.info("✓ Project structure validation passed")
        else:
            logger.warning("⚠ Project structure has inconsistencies")
            sys.exit(1)

    except Exception as e:
        logger.error(f"✗ Validation failed: {e}")
        sys.exit(1)

    # Success message
    logger.info("=" * 80)
    logger.info("✓ Feature integration completed successfully!")
    logger.info(f"✓ Updated project saved in: {NEW_PROJECT_PATH}")
    logger.info("=" * 80)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed command-line arguments.

    Example:
        >>> args = parse_arguments()
        >>> print(args.prompt)
        'Add logging functionality'
    """
    parser = argparse.ArgumentParser(
        description="Factory Feature - AI-Powered Feature Integration System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --prompt "Add logging functionality to all major modules"
  python main.py --prompt "Implement user authentication with JWT"
  python main.py --prompt "Add comprehensive error handling"

For more information, visit: https://ruslanmv.com
        """,
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Natural language description of the feature to integrate",
        metavar="FEATURE_REQUEST",
    )
    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = parse_arguments()
        main(args.prompt)
        sys.exit(0)
    except KeyboardInterrupt:
        cli_logger.info("\n\nOperation cancelled by user")
        sys.exit(130)
    except SystemExit as e:
        if e.code == 2:  # Argument parsing error
            cli_logger.error("Argument parsing failed. Use --help for usage information.")
        sys.exit(e.code)
    except Exception as e:
        cli_logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
