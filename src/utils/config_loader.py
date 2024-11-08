import yaml

def load_config(config_path):
    """
    Loads configuration from a YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Dictionary containing configuration data.
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
