"""
Data Loaders Module
DS 3500 - MP1 Part 2
Functions for loading CSV, JSON, and YAML files.
"""

import json
import logging
from pathlib import Path

import pandas as pd
import yaml

# Do not call logging.basicConfig() here.
# Use the logging configuration from Part 1.
logger = logging.getLogger(__name__)


def load_csv(filepath):
    """Load a CSV file into a DataFrame.

    filepath is a Path object.
    """
    df = pd.read_csv(filepath)
    logger.info("Loaded CSV file: %s (%d rows)", filepath, len(df))
    return df


def load_json(filepath):
    """Load a JSON file into a Python object (dict or list).

    filepath is a Path object.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    logger.info("Loaded JSON file: %s", filepath)
    return data


def load_yaml(filepath):
    """Load a YAML file into a Python object.

    filepath is a Path object.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    logger.info("Loaded YAML file: %s", filepath)
    return data


def load_data(filepath):
    """Load a file based on its extension.

    filepath is a string, such as 'fixtures/sample.csv'
    """
    path = Path(filepath)
    extension = path.suffix.lower()

    if extension == ".csv":
        return load_csv(path)
    elif extension == ".json":
        return load_json(path)
    elif extension == ".yaml":
        return load_yaml(path)
    else:
        logger.error("Unsupported file format: %s", extension)
        raise ValueError(f"Unsupported file format: {extension}")