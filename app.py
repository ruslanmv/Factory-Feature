import gradio as gr
import zipfile
import os
import time
from main import main  # Importing the main function from main.py


def generate_tree(path, prefix=""):
    """Generates a tree-like representation of a directory structure."""
    tree_str = ""
    entries = os.listdir(path)
    entries.sort()
    num_entries = len(entries)
    for i, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        if i == num_entries - 1:
            connector = "└── "
            next_prefix = prefix + "    "
        else:
            connector = "├── "
            next_prefix = prefix + "│   "

        tree_str += f"{prefix}{connector}{entry}\n"
        if os.path.isdir(full_path):
            tree_str += generate_tree(full_path, next_prefix)
    return tree_str


def display_tree(dummy_input):
    """Generates and displays the directory tree for 'project_new'."""
    if os.path.exists("project_new"):
        return generate_tree("project_new")
    return "The 'project_new' folder does not exist."


def unzip_file(file_obj):
    """Unzips an uploaded zip file to the 'project_old' folder, flattening the top-level directory."""
    try:
        with zipfile.ZipFile(file_obj.name, 'r') as zip_ref:
            # Create the target directory if it doesn't exist
            target_dir = "project_old"
            os.makedirs(target_dir, exist_ok=True)

            for member in zip_ref.namelist():
                # Adjust the path to strip the top-level directory
                member_path = member.split('/', 1)[-1] if '/' in member else member
                target_path = os.path.join(target_dir, member_path)

                # Handle directories and files
                if member.endswith('/'):
                    os.makedirs(target_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with open(target_path, 'wb') as f:
                        f.write(zip_ref.read(member))
                        
        return "File unzipped successfully!"

    except Exception as e:
        return f"Error unzipping file: {e}"


def zip_folder():
    """Zips the 'project_new' folder if it exists."""
    if os.path.exists("project_new"):
        try:
            with zipfile.ZipFile("project_new.zip", 'w') as zipf:
                for folderName, subfolders, filenames in os.walk("project_new"):
                    for filename in filenames:
                        filePath = os.path.join(folderName, filename)
                        zipf.write(filePath, os.path.relpath(filePath, "project_new"))
            return "Folder zipped successfully!", "project_new.zip"
        except Exception as e:
            return f"Error zipping folder: {e}", None
    else:
        return "Folder 'project_new' was not found.", None


def run_pipeline(user_request):
    """Executes the main pipeline with the provided user request."""
    try:
        # Call the main function from main.py
        main(user_request)
        return "Pipeline executed successfully! The updated project is ready for download."
    except Exception as e:
        return f"Error during pipeline execution: {e}"


def submit_settings(api_key, project_id, watsonx_url):
    """Sets the environment variables with the provided credentials."""
    os.environ["API_KEY"] = api_key
    os.environ["PROJECT_ID"] = project_id
    os.environ["WATSONX_URL"] = watsonx_url
    return "Environment variables loaded successfully!"


if __name__ == "__main__":
    _TITLE = "Factory Feature"
    _DESCRIPTION = """
    <div>
    Factory Feature is a project that leverages Generative AI with WatsonX.ai to analyze the structure and elements of an existing project directory. 
    Using a Vector Database, the program enables efficient retrieval and analysis of project components. Based on a user-provided feature request, 
    it generates a new version of the project with all elements updated and tailored to include the requested feature. 
    The original project resides in the <code>project_old</code> folder, and the updated project is stored in the <code>project_new</code> folder.
    </div>
    """
    _INSTRUCTIONS = """
    ## Instructions:
    1. **Upload Old Project**: Upload your existing project directory as a ZIP file under the 'Project' tab.
    2. **Enter Request**: Provide a description of the feature you want to add to your project.
    3. **Run Pipeline**: Click 'Generate Response' to execute the pipeline and generate the updated project.
    4. **Download New Project**: Download the updated project as a ZIP file.
    5. **Settings**: Set API key, Project ID, and Watsonx URL in the 'Settings' tab if needed.
    """

    _DUPLICATE = '''
    [![Duplicate this Space](https://huggingface.co/datasets/huggingface/badges/resolve/main/duplicate-this-space-md.svg)](https://huggingface.co/spaces/ruslanmv/FactoryFeature?duplicate=true)
    '''

    with gr.Blocks(title=_TITLE, theme=gr.themes.Soft()) as demo:
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("# " + _TITLE)
                gr.Image("./assets/logos.jpg", label="Logo", elem_id="logo-image", show_label=False)
            with gr.Column(scale=0):
                gr.Markdown(_DUPLICATE)
        
        gr.Markdown(_DESCRIPTION)
        gr.Markdown(_INSTRUCTIONS)

        with gr.Tabs():
            with gr.TabItem("Project"):
                with gr.Row(variant='panel'):
                    with gr.Column(scale=5):
                        unzip_input = gr.File(
                        file_types=['.zip'], 
                        label="Upload Old Project (ZIP): Remove and upload your own project if needed.",
                        value="project_old.zip",  # Default file
                        interactive=True  # Allow users to remove and upload their own file
                        )                       
                        unzip_output = gr.Textbox(label="Unzip Result")
                        unzip_button = gr.Button("Extract Project")
                        unzip_button.click(unzip_file, inputs=unzip_input, outputs=unzip_output)
                        user_request = gr.Textbox(
                            label="Enter your project request",
                            value="Add logging functionality to all major modules in the project",  # Default message
                            lines=5,  # Number of visible lines
                            placeholder="Enter a description of the feature you want to add to your project. For example:\nAdd logging functionality to all major modules in the project."
                        )
                        pipeline_output = gr.Textbox(label="Pipeline Result")
                        pipeline_button = gr.Button("Generate Feature")
                        pipeline_button.click(run_pipeline, inputs=user_request, outputs=pipeline_output)
                    with gr.Column(scale=5):
                        # Added button and output for displaying the tree
                        tree_output = gr.Textbox(label="New Project Tree")
                        tree_button = gr.Button("Display Results")
                        tree_button.click(display_tree, inputs=None, outputs=tree_output)
                        zip_output = gr.Textbox(label="Zip Result")
                        zip_download = gr.File(label="Download New Project (ZIP)")
                        zip_button = gr.Button("Download New Project")
                        zip_button.click(zip_folder, outputs=[zip_output, zip_download])

            with gr.TabItem("Settings"):
                with gr.Column():
                    api_key = gr.Textbox(label="API Key", type="password")
                    project_id = gr.Textbox(label="Project ID")
                    watsonx_url = gr.Textbox(label="Watsonx URL")
                    settings_output = gr.Textbox(label="Settings Result")
                    submit_button = gr.Button("Submit Settings")
                    submit_button.click(submit_settings, 
                                        inputs=[api_key, project_id, watsonx_url], 
                                        outputs=settings_output)

    demo.queue(max_size=10)
    demo.launch(debug=True)