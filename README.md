# Factory Feature

Factory Feature is a project that aims to create a Generative AI program that analyzes all elements of a given project directory and uses the LLM by WatsonX.ai to create a Vector Database. This database stores all the projects, and when prompted about a feature to include, the program analyzes all elements of the project and creates a new project with all the elements updated, tailored to the feature requested in the prompt. The original project is located in the `project_old` folder, and the new project is copied to the `project_new` folder.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Factory Feature leverages the power of Generative AI to analyze the structure and elements of existing projects and create new, customized versions based on specific feature requests. By using LLM by WatsonX.ai, Factory Feature can intelligently understand the context and relationships within the project and generate a new project that incorporates the desired features seamlessly.

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/factory-feature.git
```

2. Change the working directory:

```
cd factory-feature
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Place your original project in the `project_old` folder.

2. Run the Factory Feature program:

```
python main.py --prompt "your feature request"
```

3. The new project with the requested feature will be generated in the `project_new` folder.

## Contributing

We welcome contributions from the community! If you'd like to contribute to Factory Feature, please follow these steps:

1. Fork the repository.
2. Create a new branch with a descriptive name.
3. Make your changes and commit them to the branch.
4. Create a pull request describing the changes you made.
5. Wait for a maintainer to review your changes and merge them if approved.

## License

Factory Feature is released under the [MIT License](LICENSE.md).