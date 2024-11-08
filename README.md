# Factory Feature

![alt text](./assets/logo.jpeg)

Factory Feature is a project that leverages Generative AI with WatsonX.ai to analyze the structure and elements of an existing project directory. Using a Vector Database, the program enables efficient retrieval and analysis of project components. Based on a user-provided feature request, it generates a new version of the project with all elements updated and tailored to include the requested feature. The original project resides in the `project_old` folder, and the updated project is stored in the `project_new` folder.

---

## Table of Contents
1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Example](#example)
6. [Contributing](#contributing)
7. [License](#license)

---

## Introduction

Factory Feature harnesses the power of WatsonX.ai's Large Language Models (LLMs) to automate the process of understanding, modifying, and updating software projects. It uses a Vector Database to store project components for efficient analysis and retrieval. By combining advanced AI capabilities with an intuitive workflow, Factory Feature enables developers to:
- Save time and resources.
- Customize software projects rapidly.
- Maintain coherence and consistency across updates.

Factory Feature works seamlessly with a wide range of programming languages, libraries, and frameworks, making it a versatile tool for developers.

---

## Key Features

- **Generative AI-powered software customization**: Leverages WatsonX.ai LLM to analyze projects and intelligently generate new versions with requested features.
- **Vector Database creation**: Stores project components for efficient retrieval and analysis.
- **Context-aware feature integration**: Ensures that requested features are integrated coherently within the existing project structure.
- **Streamlined project updates**: Automates the process of modifying and updating software projects.
- **Language and framework agnostic**: Supports a wide range of programming languages and technologies.

## Structure of the Project
```
factory-feature/
├── project_old/                  # Folder for the original project
│   └── ...                       # Original project files and directories
├── project_new/                  # Folder for the generated project
│   └── ...                       # New project files with added features
├── src/                          # Source code directory
│   ├── __init__.py               # Package initializer
│   ├── main.py                   # Entry point of the application
│   ├── vector_database/          # Module for Vector Database creation and management
│   │   ├── __init__.py
│   │   ├── db_builder.py         # Code for building and populating the vector database
│   │   └── db_query.py           # Code for querying the vector database
│   ├── analysis/                 # Project analysis module
│   │   ├── __init__.py
│   │   ├── project_parser.py     # Parses and analyzes the project structure
│   │   ├── dependency_resolver.py# Resolves dependencies in the project
│   │   └── feature_mapper.py     # Maps features to project components
│   ├── generation/               # Feature generation module
│   │   ├── __init__.py
│   │   ├── feature_integration.py# Code for integrating new features into the project
│   │   └── project_generator.py  # Generates the updated project files
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── logger.py             # Logging utilities
│   │   ├── file_operations.py    # File I/O utilities
│   │   └── config_loader.py      # Loads and manages configuration settings
│   └── models/                   # LLM integration module
│       ├── __init__.py
│       ├── llm_inference.py      # Code for interacting with WatsonX.ai LLM
│       └── prompt_templates.py   # Templates for LLM prompts
├── tests/                        # Automated test suite
│   ├── __init__.py
│   ├── test_main.py              # Tests for the main application logic
│   ├── test_vector_database.py   # Tests for the Vector Database module
│   ├── test_analysis.py          # Tests for the analysis module
│   ├── test_generation.py        # Tests for the feature generation module
│   └── test_utils.py             # Tests for utility functions
├── docs/                         # Documentation directory
│   ├── README.md                 # Main project documentation
│   ├── CONTRIBUTING.md           # Contribution guidelines
│   ├── USAGE.md                  # Usage instructions
│   └── API_REFERENCE.md          # API documentation for developers
├── data/                         # Sample data for testing
│   ├── sample_project/           # Sample project for testing purposes
│   └── feature_requests/         # Example feature request prompts
│       ├── add_authentication.txt
│       └── improve_ui.txt
├── config/                       # Configuration files
│   ├── default_config.yaml       # Default configuration settings
│   └── custom_config.yaml        # User-provided configuration settings
├── requirements.txt              # Python dependencies
├── app.py                        # Script to run the Factory Feature application
├── LICENSE                       # License information
├── .gitignore                    # Git ignore rules
└── setup.py                      # Script for installing the project as a Python package
```

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ruslanmv/factory-feature.git
   ```

2. **Change the working directory**:
   ```bash
   cd factory-feature
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file** with the following variables:
   ```plaintext
   API_KEY=<your_ibm_watson_api_key>
   PROJECT_ID=<your_ibm_watson_project_id>
   ```

---

## Usage

1. Place your original project in the `project_old` folder.
2. Run the Factory Feature program with your desired feature request:
   ```bash
   python app.py --prompt "Add a user authentication feature to the project"
   ```
3. The updated project will be generated in the `project_new` folder.

---

## Example

### Original Project Structure
The `project_old` folder contains the following files:
```
project_old/
├── app.py
├── requirements.txt
└── utils/
    └── helpers.py
```

### Feature Request
Add a logging mechanism to the project.

### Command to Execute
```bash
python app.py --prompt "Add logging functionality to all major modules in the project"
```

### Updated Project Structure
After execution, the `project_new` folder contains:
```
project_new/
├── app.py       # Updated with logging functionality
├── requirements.txt  # Updated to include `logging` dependency
└── utils/
    └── helpers.py  # Updated to include logging
```

### Example Output in `app.py`
```python
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the application...")
    # Original application code
    print("Hello, World!")
    logger.info("Application finished successfully.")

if __name__ == "__main__":
    main()
```

---

## Contributing

We welcome contributions from the community! To contribute:
1. **Fork the repository**:
   ```bash
   git fork https://github.com/ruslanmv/factory-feature.git
   ```

2. **Create a new branch**:
   ```bash
   git checkout -b feature/new-feature
   ```

3. **Make your changes and commit**:
   ```bash
   git add .
   git commit -m "Add new feature"
   ```

4. **Push the branch and open a Pull Request**:
   ```bash
   git push origin feature/new-feature
   ```

---

## License

Factory Feature is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

