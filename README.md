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

## Project Overview
The Factory Feature project automates feature integration into software projects, leveraging AI-driven analysis, feature mapping, and project generation techniques. This ensures scalable and efficient updates to existing codebases.
```
factory-feature/
├── LICENSE.md                      # License for the project
├── README.md                       # Main project documentation
├── app.py                          # Main script to launch the application
├── config/                         # Configuration files
│   └── default_config.yaml         # Default configuration settings
├── content.py                      # Content management script
├── data/                           # Data and example feature requests
│   ├── app.py                      # Example application file
│   ├── feature_requests/           # Directory for feature request prompts
│   │   ├── add_authentication.txt  # Feature request example for authentication
│   │   └── improve_ui.txt          # Feature request example for UI improvement
│   └── utils/                      # Utility scripts for data handling
│       └── helpers.py              # Helper functions for data management
├── docs/                           # Documentation directory
│   ├── API_REFERENCE.md            # API reference for developers
│   ├── CONTRIBUTING.md             # Contribution guidelines
│   ├── README.md                   # Main documentation for the docs folder
│   ├── STRUCUTRE.md                # Explanation of the project structure
│   └── USAGE.md                    # Usage instructions for the project
├── factory_feature.log             # Log file for project execution
├── main.ipynb                      # Jupyter Notebook for interactive exploration
├── main.py                         # Entry point for running the project
├── project_new/                    # Folder for the updated project
│   ├── app.py                      # Updated application file
│   ├── requirements.txt            # Dependency list for the new project
│   └── utils/                      # Utilities for the updated project
│       └── helpers.py              # Updated helper functions
├── project_new.zip                 # Compressed archive of the updated project
├── project_old/                    # Folder for the original project
│   ├── app.py                      # Original application file
│   ├── requirements.txt            # Dependency list for the old project
│   └── utils/                      # Utilities for the old project
│       └── helpers.py              # Original helper functions
├── project_old.zip                 # Compressed archive of the original project
├── requirements.txt                # Python dependencies
├── setup.py                        # Script for installing the project as a Python package
├── src/                            # Source code directory
│   ├── __init__.py                 # Package initializer
│   ├── analysis/                   # Project analysis module
│   │   ├── __init__.py
│   │   ├── content.py              # Content extraction utilities
│   │   ├── dependency_resolver.py  # Resolves dependencies in the project
│   │   ├── feature_mapper.py       # Maps features to project components
│   │   ├── project_parser.py       # Parses and analyzes project structure
│   │   └── tree.py                 # Utilities for tree-based analysis
│   ├── generation/                 # Feature generation module
│   │   ├── __init__.py
│   │   ├── feature_integration.py  # Integrates new features into the project
│   │   ├── preprocessing.py        # Preprocessing utilities for feature integration
│   │   ├── project_generator.py    # Generates updated project files
│   │   ├── project_structure.py    # Validates and updates project structure
│   │   └── task_prompts.py         # Generates task prompts for feature integration
│   ├── models/                     # LLM interaction module
│   │   ├── __init__.py
│   │   ├── llm_inference.py        # Interacts with WatsonX.ai LLM
│   │   └── prompt_templates.py     # Templates for LLM prompts
│   ├── utils/                      # Utility scripts
│   │   ├── __init__.py
│   │   ├── config_loader.py        # Loads and manages configuration settings
│   │   ├── file_operations.py      # Utilities for file I/O
│   │   ├── logger.py               # Logging utilities
│   │   └── tools.py                # General-purpose tools
│   └── vector_database/            # Module for vector database management
│       ├── __init__.py
│       ├── db_builder.py           # Builds vector databases
│       ├── db_builder_simple.py    # Simplified vector database builder
│       ├── db_load.py              # Loads vector databases
│       ├── db_query.py             # Queries the vector database
│       └── display_content.py      # Displays content from the vector database
├── tests/                          # Automated test suite
│   ├── __init__.py
│   ├── test_analysis.py            # Tests for the analysis module
│   ├── test_generation.py          # Tests for the feature generation module
│   ├── test_main.py                # Tests for the main application logic
│   └── test_vector_database.py     # Tests for the vector database module
└── utils/                          # General utilities
    ├── __init__.py
    └── extractor.py                # Extractor utilities for data management
```

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
python main.py --prompt "Add logging functionality to all major modules in the project"
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

## Front End Application

You can execute the program by doing 

```bash
python app.py
```

![](assets/2024-11-26-16-09-23.png)


## License

Factory Feature is released under the MIT License. See the [LICENSE](LICENSE.md) file for more details.

