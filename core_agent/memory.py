"""
This module provides a base class for memory.
"""

from pathlib import Path
from typing import MutableMapping, Union

class BaseMemory(MutableMapping[Union[str, Path], str]):
    """
    A base class for memory.
    """

    def __init__(self, *args, **kwargs):
        self._storage = dict(*args, **kwargs)

    def __getitem__(self, key):
        return self._storage[key]

    def __setitem__(self, key, value):
        self._storage[key] = value

    def __delitem__(self, key):
        del self._storage[key]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)

    def log(self, file_path, content):
        """
        Logs the content to a file.
        """
        # In a real implementation, this would write to a file.
        # For now, we'll just print it.
        print(f"--- LOGGING TO {file_path} ---")
        print(content)
        print("--- END LOG ---")
