"""
Factory Feature - Gradio Web Interface.

This module provides a user-friendly web interface for the Factory Feature system
using Gradio. Users can upload projects, submit feature requests, and download
the updated projects.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

import os
import zipfile
from pathlib import Path
from typing import Optional, Tuple

import gradio as gr

from main import main as run_pipeline


def generate_tree(path: str, prefix: str = "") -> str:
    """
    Generate a tree-like representation of a directory structure.

    Args:
        path: Root directory path to generate tree from.
        prefix: Prefix string for current level of tree (used for recursion).

    Returns:
        String representation of the directory tree.

    Example:
        >>> tree = generate_tree("/path/to/project")
        >>> print(tree)
        ├── src/
        │   ├── main.py
        │   └── utils.py
    """
    tree_str = ""

    try:
        entries = sorted(os.listdir(path))
    except (PermissionError, FileNotFoundError) as e:
        return f"{prefix}[Error: {e}]\n"

    num_entries = len(entries)

    for i, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        is_last = i == num_entries - 1

        # Determine connectors
        connector = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")

        tree_str += f"{prefix}{connector}{entry}\n"

        # Recurse into directories
        if os.path.isdir(full_path):
            tree_str += generate_tree(full_path, next_prefix)

    return tree_str


def display_tree(dummy_input: Optional[str] = None) -> str:
    """
    Generate and display the directory tree for 'project_new'.

    Args:
        dummy_input: Unused parameter (required by Gradio button callback).

    Returns:
        Directory tree as a string, or error message if directory doesn't exist.

    Example:
        >>> tree = display_tree()
        >>> print(tree[:50])
        project_new/
        ├── app.py
        ├── requirements.txt
    """
    project_path = "project_new"

    if not os.path.exists(project_path):
        return f"❌ The '{project_path}' folder does not exist yet. Generate a feature first."

    return f"📁 {project_path}/\n{generate_tree(project_path)}"


def unzip_file(file_obj: gr.File) -> str:
    """
    Unzip an uploaded ZIP file to the 'project_old' folder.

    This function extracts the uploaded project, flattening the top-level
    directory to avoid nested project folders.

    Args:
        file_obj: Gradio File object containing the uploaded ZIP file.

    Returns:
        Success or error message string.

    Example:
        >>> result = unzip_file(uploaded_file)
        >>> print(result)
        '✅ File unzipped successfully! Extracted 15 files.'
    """
    if not file_obj:
        return "❌ No file uploaded. Please upload a ZIP file."

    try:
        target_dir = Path("project_old")

        # Remove existing project_old if it exists
        if target_dir.exists():
            import shutil

            shutil.rmtree(target_dir)

        target_dir.mkdir(parents=True, exist_ok=True)

        file_count = 0

        with zipfile.ZipFile(file_obj.name, "r") as zip_ref:
            for member in zip_ref.namelist():
                # Skip macOS metadata files
                if "__MACOSX" in member or member.startswith("."):
                    continue

                # Flatten top-level directory
                member_path = member.split("/", 1)[-1] if "/" in member else member

                if not member_path:  # Skip empty paths
                    continue

                target_path = target_dir / member_path

                # Handle directories
                if member.endswith("/"):
                    target_path.mkdir(parents=True, exist_ok=True)
                else:
                    # Ensure parent directory exists
                    target_path.parent.mkdir(parents=True, exist_ok=True)

                    # Extract file
                    with open(target_path, "wb") as f:
                        f.write(zip_ref.read(member))
                    file_count += 1

        return f"✅ File unzipped successfully! Extracted {file_count} files to '{target_dir}'."

    except zipfile.BadZipFile:
        return "❌ Error: Invalid ZIP file. Please upload a valid ZIP archive."
    except PermissionError:
        return "❌ Error: Permission denied. Check file permissions."
    except Exception as e:
        return f"❌ Error unzipping file: {str(e)}"


def zip_folder() -> Tuple[str, Optional[str]]:
    """
    Create a ZIP archive of the 'project_new' folder.

    Returns:
        Tuple of (status_message, zip_file_path).
        zip_file_path is None if operation fails.

    Example:
        >>> message, zip_path = zip_folder()
        >>> print(message)
        '✅ Project zipped successfully! 25 files archived.'
    """
    project_path = Path("project_new")
    zip_path = "project_new.zip"

    if not project_path.exists():
        return "❌ Folder 'project_new' was not found. Generate a feature first.", None

    try:
        file_count = 0

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_path):
                for filename in files:
                    file_path = Path(root) / filename
                    arc_name = file_path.relative_to(project_path)
                    zipf.write(file_path, arc_name)
                    file_count += 1

        return (
            f"✅ Project zipped successfully! {file_count} files archived to '{zip_path}'.",
            zip_path,
        )

    except Exception as e:
        return f"❌ Error zipping folder: {str(e)}", None


def run_pipeline_wrapper(user_request: str) -> str:
    """
    Execute the Factory Feature pipeline with error handling.

    Args:
        user_request: Natural language description of the feature to integrate.

    Returns:
        Success or error message string.

    Example:
        >>> result = run_pipeline_wrapper("Add logging to all modules")
        >>> print(result)
        '✅ Pipeline executed successfully!'
    """
    if not user_request or not user_request.strip():
        return "❌ Error: Feature request cannot be empty. Please provide a description."

    if not Path("project_old").exists():
        return "❌ Error: 'project_old' folder not found. Please upload a project first."

    try:
        run_pipeline(user_request.strip())
        return "✅ Pipeline executed successfully! The updated project is ready for download."
    except FileNotFoundError as e:
        return f"❌ File not found error: {str(e)}"
    except ValueError as e:
        return f"❌ Invalid input: {str(e)}"
    except Exception as e:
        return f"❌ Error during pipeline execution: {str(e)}"


def submit_settings(api_key: str, project_id: str, watsonx_url: str) -> str:
    """
    Set environment variables with provided IBM WatsonX.ai credentials.

    Args:
        api_key: IBM WatsonX API key.
        project_id: IBM WatsonX project ID.
        watsonx_url: IBM WatsonX API URL.

    Returns:
        Success or error message string.

    Example:
        >>> result = submit_settings("api_key_123", "proj_456", "https://...")
        >>> print(result)
        '✅ Environment variables loaded successfully!'
    """
    if not all([api_key, project_id, watsonx_url]):
        return "❌ Error: All fields are required. Please fill in all credentials."

    try:
        os.environ["WATSONX_APIKEY"] = api_key.strip()
        os.environ["PROJECT_ID"] = project_id.strip()
        os.environ["WATSONX_URL"] = watsonx_url.strip()
        return "✅ Environment variables loaded successfully!"
    except Exception as e:
        return f"❌ Error setting environment variables: {str(e)}"


# Application constants
_TITLE = "Factory Feature"
_DESCRIPTION = """
<div style="text-align: center; margin-bottom: 20px;">
<h2>🏭 AI-Powered Feature Integration System</h2>
<p>
Factory Feature leverages <strong>IBM WatsonX.ai</strong> and <strong>Vector Databases</strong>
to analyze existing projects and automatically integrate new features based on your requests.
</p>
<p>
The system uses <strong>Retrieval-Augmented Generation (RAG)</strong> with Meta Llama 3 70B
to understand your codebase and generate context-aware modifications.
</p>
</div>
"""

_INSTRUCTIONS = """
## 📋 Instructions:

1. **⚙️ Configure Settings** (First-time setup):
   - Navigate to the **Settings** tab
   - Enter your IBM WatsonX.ai credentials
   - Click **Submit Settings**

2. **📦 Upload Project**:
   - Go to the **Project** tab
   - Upload your existing project as a ZIP file
   - Click **Extract Project**

3. **✍️ Enter Feature Request**:
   - Describe the feature you want in natural language
   - Example: *"Add logging functionality to all major modules"*

4. **🚀 Generate Feature**:
   - Click **Generate Feature**
   - Wait for the AI to analyze and modify your project

5. **💾 Download Result**:
   - Click **Display Results** to preview the updated structure
   - Click **Download New Project** to get the ZIP file

---

**Pro Tips:**
- Be specific in your feature requests for better results
- Ensure your project has clear structure and dependencies
- Check the logs for detailed pipeline execution info
"""

_DUPLICATE = """
[![Duplicate this Space](https://huggingface.co/datasets/huggingface/badges/resolve/main/duplicate-this-space-md.svg)](https://huggingface.co/spaces/ruslanmv/FactoryFeature?duplicate=true)
"""

# Build Gradio interface
with gr.Blocks(title=_TITLE, theme=gr.themes.Soft()) as demo:
    # Header
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown(f"# {_TITLE}")
            gr.Image(
                "./assets/logos.jpg",
                label="Logo",
                elem_id="logo-image",
                show_label=False,
                height=200,
            )
        with gr.Column(scale=0):
            gr.Markdown(_DUPLICATE)

    gr.Markdown(_DESCRIPTION)
    gr.Markdown(_INSTRUCTIONS)

    # Main tabs
    with gr.Tabs():
        # Project Tab
        with gr.TabItem("📁 Project"):
            with gr.Row(variant="panel"):
                with gr.Column(scale=5):
                    # File upload section
                    unzip_input = gr.File(
                        file_types=[".zip"],
                        label="Upload Project (ZIP)",
                        value="project_old.zip",  # Default file
                        interactive=True,
                    )
                    unzip_output = gr.Textbox(label="📤 Upload Status", interactive=False)
                    unzip_button = gr.Button("📂 Extract Project", variant="primary")

                    # Feature request section
                    gr.Markdown("---")
                    user_request = gr.Textbox(
                        label="✍️ Feature Request",
                        value="Add logging functionality to all major modules in the project",
                        lines=5,
                        placeholder="Describe the feature you want to add...",
                    )
                    pipeline_output = gr.Textbox(label="🔄 Pipeline Status", interactive=False)
                    pipeline_button = gr.Button("🚀 Generate Feature", variant="primary")

                with gr.Column(scale=5):
                    # Results section
                    tree_output = gr.Textbox(
                        label="📁 Updated Project Structure", lines=15, interactive=False
                    )
                    tree_button = gr.Button("👁️ Display Results", variant="secondary")

                    gr.Markdown("---")

                    # Download section
                    zip_output = gr.Textbox(label="📦 Archive Status", interactive=False)
                    zip_download = gr.File(label="💾 Download Project ZIP")
                    zip_button = gr.Button("⬇️ Download New Project", variant="primary")

        # Settings Tab
        with gr.TabItem("⚙️ Settings"):
            with gr.Column():
                gr.Markdown(
                    """
                ### IBM WatsonX.ai Configuration

                Enter your credentials below. Get them from the
                [IBM Cloud Dashboard](https://cloud.ibm.com/).
                """
                )

                api_key = gr.Textbox(
                    label="🔑 API Key",
                    type="password",
                    placeholder="Enter your WatsonX API key...",
                )
                project_id = gr.Textbox(
                    label="🆔 Project ID", placeholder="Enter your Project ID..."
                )
                watsonx_url = gr.Textbox(
                    label="🌐 WatsonX URL",
                    value="https://eu-gb.ml.cloud.ibm.com",
                    placeholder="Enter WatsonX URL...",
                )

                settings_output = gr.Textbox(label="⚙️ Settings Status", interactive=False)
                submit_button = gr.Button("✅ Submit Settings", variant="primary")

    # Event handlers
    unzip_button.click(unzip_file, inputs=unzip_input, outputs=unzip_output)
    pipeline_button.click(run_pipeline_wrapper, inputs=user_request, outputs=pipeline_output)
    tree_button.click(display_tree, inputs=None, outputs=tree_output)
    zip_button.click(zip_folder, outputs=[zip_output, zip_download])
    submit_button.click(
        submit_settings, inputs=[api_key, project_id, watsonx_url], outputs=settings_output
    )

# Launch application
if __name__ == "__main__":
    demo.queue(max_size=10)
    demo.launch(
        server_name=os.getenv("GRADIO_SERVER_NAME", "0.0.0.0"),
        server_port=int(os.getenv("GRADIO_PORT", "7860")),
        show_error=True,
        debug=True,
    )
