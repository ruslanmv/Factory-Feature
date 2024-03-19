# Factory Feature
![alt text](./assets/logo.jpeg)
Factory Feature is a project that aims to create a Generative AI program that analyzes all elements of a given project directory and uses the LLM by WatsonX.ai to create a Vector Database. This database stores all the projects, and when prompted about a feature to include, the program analyzes all elements of the project and creates a new project with all the elements updated, tailored to the feature requested in the prompt. The original project is located in the `project_old` folder, and the new project is copied to the `project_new` folder.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Factory Feature leverages the power of Generative AI to analyze the structure and elements of existing projects and create new, customized versions based on specific feature requests. By using LLM by WatsonX.ai, Factory Feature can intelligently understand the context and relationships within the project and generate a new project that incorporates the desired features seamlessly.

The primary objective of Factory Feature is to save time and resources by automating the process of understanding, modifying, and updating existing projects according to specific user requirements. Through its advanced AI-driven approach, Factory Feature can rapidly adapt to any project type and generate a new version tailored to the desired features, significantly reducing the manual effort and complexity usually involved in customizing software projects.

Key Features:

1. Generative AI-powered software customization: Factory Feature employs LLM by WatsonX.ai to intelligently analyze existing projects and generate new versions with the desired features.
2. Vector Database creation: The AI program creates a Vector Database that stores all project components, facilitating efficient retrieval and analysis of project elements.
3. Context-aware feature integration: Factory Feature understands the context and relationships within the project, ensuring that new features are integrated coherently and consistently.
4. Streamlined project updates: Factory Feature automates the process of updating and modifying projects, significantly reducing the time and effort required for software customization.
5. Language and framework agnostic: The AI-driven approach of Factory Feature enables it to work seamlessly with a wide range of programming languages, libraries, and frameworks.

By providing a powerful and intuitive solution for software customization, Factory Feature has the potential to revolutionize the way developers approach project updates and modifications, leading to more efficient and effective software development processes.



## Installation

1. Clone the repository:

```
git clone https://github.com/ruslanmv/factory-feature.git
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
python app.py --prompt "your feature request"
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