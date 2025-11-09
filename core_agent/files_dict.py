"""
This module provides a FilesDict class which is a dictionary-based container for managing code files.
"""
from collections import OrderedDict
from pathlib import Path
from typing import Union


class FilesDict(dict):
    """
    A dictionary-based container for managing code files.
    """

    def __setitem__(self, key: Union[str, Path], value: str):
        """
        Set the code content for the given filename, enforcing type checks on the key and value.
        """
        if not isinstance(key, (str, Path)):
            raise TypeError("Keys must be strings or Path's")
        if not isinstance(value, str):
            raise TypeError("Values must be strings")
        super().__setitem__(key, value)

    def to_chat(self):
        """
        Formats the items of the object (assuming file name and content pairs)
        into a string suitable for chat display.
        """
        chat_str = ""
        for file_name, file_content in self.items():
            lines_dict = file_to_lines_dict(file_content)
            chat_str += f"File: {file_name}\n"
            for line_number, line_content in lines_dict.items():
                chat_str += f"{line_number} {line_content}\n"
            chat_str += "\n"
        return f"```\n{chat_str}```"

    def to_log(self):
        """
        Formats the items of the object (assuming file name and content pairs)
        into a string suitable for log display.
        """
        log_str = ""
        for file_name, file_content in self.items():
            log_str += f"File: {file_name}\n"
            log_str += file_content
            log_str += "\n"
        return log_str


def file_to_lines_dict(file_content: str) -> dict:
    """
    Converts file content into a dictionary where each line number is a key
    and the corresponding line content is the value.
    """
    lines_dict = OrderedDict(
        {
            line_number: line_content
            for line_number, line_content in enumerate(file_content.split("\n"), 1)
        }
    )
    return lines_dict
