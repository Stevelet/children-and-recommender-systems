from pathlib import Path
import re


def project_root():
    return Path(__file__).resolve().parent.parent


def data_root():
    return project_root() / "data"

def make_path_safe(raw_path):
    """
    Parse string to path string for file storage.

    :param raw_path: Path
    :return: Path without special characters
    """
    return re.sub(r'[^a-zA-Z\d()]', '_', raw_path)
