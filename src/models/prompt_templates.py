def get_prompt_template():
    """
    Returns a template for feature integration prompts.

    Returns:
        Prompt template string.
    """
    return (
        "Given the context of the project, implement the following feature request. "
        "Ensure the feature integrates seamlessly with existing components:\n\n"
        "Feature Request: {feature_request}\n\n"
        "Project Context: {project_context}"
    )
