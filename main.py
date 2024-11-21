import argparse
import os
import shutil
from src.analysis.project_parser import parse_project
from src.analysis.dependency_resolver import resolve_dependencies
from src.analysis.feature_mapper import map_features_to_components
from src.generation.project_generator import generate_project
from src.generation.feature_integration import integrate_features

from src.models.prompt_templates import get_prompt_template
from src.utils.logger import logger
from src.utils.file_operations import read_file, write_file
from src.vector_database.db_builder import build_vector_database
from src.vector_database.db_query import query_vector_database

from src.vector_database.db_load import load_vector_db
from src.models.llm_inference import query_llm

prompt = "How to integrate the specified features into the project components?"
# Define the persistent directory and collection name
persist_directory = "./notebooks/chroma_db"
collection_name = "my_vector_collection"

# Load the vector database
vector_db = load_vector_db(collection_name, persist_directory)

# Query the vector database using the `query_llm` function
response = query_llm(user_input=prompt, vector_db=vector_db)

# Print the response
print("Generated Response:")
print(response)