def map_features_to_components(project_data, feature_request):
    """
    Maps feature requests to specific project components.

    Args:
        project_data: Parsed project data.
        feature_request: User-provided feature request.

    Returns:
        Mapping of features to components.
    """
    component_mapping = []

    for item in project_data:
        if feature_request.lower() in item["content"].lower():
            component_mapping.append(item["path"])

    return component_mapping
