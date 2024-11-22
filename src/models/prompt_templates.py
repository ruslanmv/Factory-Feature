def get_prompt_template_feature():
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

def get_prompt_template_old(stage: str):
    """
    Returns a template for prompts based on the stage of the FACTACON algorithm.

    Args:
        stage (str): The stage of the algorithm.

    Returns:
        str: Prompt template for the specified stage.
    """
    prompts = {
        "feature_analysis_nodes": (
            "Analyze the project context and identify the nodes (files or components) impacted by the following feature request:\n\n"
            "Feature Request: {feature_request}\n\n"
            "Project Context: {project_context}\n\n"
            "Provide a list of impacted nodes and their roles in the project."
        ),
        "feature_analysis_edges": (
            "Analyze the project context and determine the dependencies (edges) impacted by the following feature request:\n\n"
            "Feature Request: {feature_request}\n\n"
            "Project Context: {project_context}\n\n"
            "Provide a list of impacted dependencies and their significance."
        ),
        "feature_impact_report": (
            "Generate a detailed report on the impact of the following feature request on the project:\n\n"
            "Feature Request: {feature_request}\n\n"
            "Project Context: {project_context}\n\n"
            "Include risks, suggestions for modular implementation, and expected changes."
        ),
        "task_generation": (
            "Generate a list of tasks required to integrate the following feature into the project:\n\n"
            "Feature Request: {feature_request}\n\n"
            "Project Context: {project_context}\n\n"
            "Provide a detailed task list, including operations on files, dependencies, and testing."
        ),
        "agent_creation": (
            "For the following tasks, create specialized agents to handle them:\n\n"
            "Tasks: {tasks}\n\n"
            "Specify how each agent will perform its assigned task using fine-tuned models, tools, or scripts."
        ),
        "weight_translation": (
            "Translate the project elements into weight factors for prioritization. Use the following metrics:\n\n"
            "Project Elements: {project_elements}\n\n"
            "Provide weight factors for nodes (based on size, role, modification frequency) and edges (based on criticality)."
        ),
        "task_assignment": (
            "Assign tasks to suitable agents based on specialization. Evaluate costs and balance workloads:\n\n"
            "Tasks: {tasks}\n\n"
            "Agent Details: {agent_details}\n\n"
            "Provide a mapping of tasks to agents, estimated costs, and workload balance."
        ),
        "task_optimization": (
            "Optimize the allocation of tasks to agents to minimize total cost and prevent bottlenecks:\n\n"
            "Task Assignments: {task_assignments}\n\n"
            "Predict potential issues and suggest dynamic reallocation to improve efficiency."
        ),
        "consistency_validation": (
            "Validate the consistency of the updated project tree after integrating the feature:\n\n"
            "Updated Project Tree: {project_tree}\n\n"
            "Identify and suggest corrections for unmet dependencies, and iterate until consistency is achieved."
        )
    }
    return prompts.get(stage, "Stage not found.")

def get_prompt_template(stage: str):
    """
    Returns a template for prompts based on the stage of the FACTACON algorithm.

    Args:
        stage (str): The stage of the algorithm.

    Returns:
        str: Prompt template for the specified stage.
    """
    prompts = {
        "feature_analysis_nodes": (
            "Analyze the project context and identify the nodes (files or components) impacted by the following feature request:\n\n"
            "Feature Request: {feature_request}\n\n"
            "Project Context: {project_context}\n\n"
            "Provide a list of impacted nodes and their roles in the project."
        ),
        "feature_analysis_edges": (
            "Analyze the project context and determine the dependencies (edges) impacted by the following feature request:\n\n"
            "Feature Request: {feature_request}\n\n"
            "Project Context: {project_context}\n\n"
            "Provide a list of impacted dependencies and their significance."
        ),
        "feature_impact_report": (
            "Generate a detailed report on the impact of the following feature request on the project:\n\n"
            "Feature Request: {feature_request}\n\n"
            "Project Context: {project_context}\n\n"
            "Include risks, suggestions for modular implementation, and expected changes."
        ),
        "preprocessing_step": (
            "Using the results of the feature analysis, identify the specific files to be handled for the following feature request:\n\n"
            "Feature Request: {feature_request}\n\n"
            "Feature Analysis Results:\n{analysis_results}\n\n"
            "For each impacted file:\n"
            "- Provide the file path.\n"
            "- Specify the task to be performed on the file (e.g., modify, add functionality).\n\n"
            "For any new file required:\n"
            "- Specify the file path.\n"
            "- Provide a brief description of its purpose.\n"
            "- Suggest the initial content or structure the file should include.\n\n"
            "Ensure the output clearly separates existing files and new files to be created."
        ),
        "task_generation": (
            "Generate a list of tasks required to integrate the following feature into the project:\n\n"
            "Feature Request: {feature_request}\n\n"
            "Project Context: {project_context}\n\n"
            "Provide a detailed task list, including operations on files, dependencies, and testing."
        ),
        "agent_creation": (
            "For the following tasks, create specialized agents to handle them:\n\n"
            "Tasks: {tasks}\n\n"
            "Specify how each agent will perform its assigned task using fine-tuned models, tools, or scripts."
        ),
        "weight_translation": (
            "Translate the project elements into weight factors for prioritization. Use the following metrics:\n\n"
            "Project Elements: {project_elements}\n\n"
            "Provide weight factors for nodes (based on size, role, modification frequency) and edges (based on criticality)."
        ),
        "task_assignment": (
            "Assign tasks to suitable agents based on specialization. Evaluate costs and balance workloads:\n\n"
            "Tasks: {tasks}\n\n"
            "Agent Details: {agent_details}\n\n"
            "Provide a mapping of tasks to agents, estimated costs, and workload balance."
        ),
        "task_optimization": (
            "Optimize the allocation of tasks to agents to minimize total cost and prevent bottlenecks:\n\n"
            "Task Assignments: {task_assignments}\n\n"
            "Predict potential issues and suggest dynamic reallocation to improve efficiency."
        ),
        "consistency_validation": (
            "Validate the consistency of the updated project tree after integrating the feature:\n\n"
            "Updated Project Tree: {project_tree}\n\n"
            "Identify and suggest corrections for unmet dependencies, and iterate until consistency is achieved."
        )
    }
    return prompts.get(stage, "Stage not found.")
