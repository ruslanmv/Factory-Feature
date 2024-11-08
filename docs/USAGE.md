
# Factory Feature - Usage Guide

This guide explains how to use Factory Feature to analyze and update projects.

## Prerequisites
- Python 3.8 or higher.
- WatsonX.ai credentials (API Key and Project ID).

## Step-by-Step Usage

1. **Prepare Your Environment**:
   - Clone the repository and install dependencies:
     ```bash
     git clone https://github.com/ruslanmv/factory-feature.git
     cd factory-feature
     pip install -r requirements.txt
     ```

   - Set up a `.env` file with the following variables:
     ```plaintext
     API_KEY=<your_ibm_watson_api_key>
     PROJECT_ID=<your_ibm_watson_project_id>
     ```

2. **Place Your Project**:
   - Place the original project in the `project_old` folder.

3. **Run the Application**:
   - Provide a feature request:
     ```bash
     python app.py --prompt "Add logging functionality to the project"
     ```

4. **Check the Output**:
   - The updated project will be in the `project_new` folder.

## Advanced Options
- Modify the default configuration in `config/default_config.yaml` to change LLM parameters.

For more examples, see the [README.md](README.md) file.