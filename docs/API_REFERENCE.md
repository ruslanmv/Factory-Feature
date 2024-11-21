# Factory Feature - API Reference

## Modules

### 1. **Vector Database**
- **`build_vector_database(project_data)`**:
  - Converts project data into a vector database for efficient retrieval.

- **`query_vector_database(vector_db, query, top_k=5)`**:
  - Queries the vector database for relevant documents.

### 2. **Analysis**
- **`parse_project(project_path)`**:
  - Parses the project directory and extracts file contents.

- **`resolve_dependencies(project_path)`**:
  - Analyzes dependencies in the project.

### 3. **Generation**
- **`generate_project(old_project_path, new_project_path, feature_instructions)`**:
  - Generates an updated project based on feature instructions.

- **`integrate_features(project_components, feature_instructions)`**:
  - Integrates features into project components.

For usage examples, refer to the [USAGE.md](USAGE.md) file.
