import yaml


def load_data(config_file):
    """
    Loads data from a YAML configuration file.

    Args:
        config_file (str): Path to the YAML configuration file.

    Returns:
        dict: The data loaded from the YAML file, parsed into a Python dictionary.

    Raises:
        Exception: If there is an error reading or parsing the YAML file.
    """
    with open(config_file, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            raise Exception(f"Error in configuration file: {exc}")
