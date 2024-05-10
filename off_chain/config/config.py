import os
import yaml

"""
Load configuration settings from a YAML file.

Returns:
    dict: Configuration settings loaded from the YAML file.
"""

# Obtain absolute path from config.py
current_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(current_dir, 'configuration.yml')

# Load config file
with open(config_file, 'r') as file:
    config = yaml.safe_load(file)
