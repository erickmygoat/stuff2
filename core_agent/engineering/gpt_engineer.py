"""
This module provides code generation and improvement functions for the "My Son" agent, inspired by the techniques used in GPT-Engineer.
"""

import inspect
import io
import re
import sys
import traceback

from pathlib import Path
from typing import List, MutableMapping, Union

from langchain_core.messages import HumanMessage, SystemMessage
from termcolor import colored

from core_agent.ai import AI
from core_agent.memory import BaseMemory
from .chat_to_files import apply_diffs, chat_to_files_dict, parse_diffs
from ..prompting.gpt_engineer import GptEngineerPromptGenerator
from ..files_dict import FilesDict, file_to_lines_dict

def curr_fn() -> str:
    """
    Returns the name of the current function.
    """
    return inspect.stack()[1].function


def setup_sys_prompt(preprompts: MutableMapping[Union[str, Path], str]) -> str:
    """
    Sets up the system prompt for generating code.
    """
    return (
        preprompts["roadmap"]
        + preprompts["generate"].replace("FILE_FORMAT", preprompts["file_format"])
        + "\nUseful to know:\n"
        + preprompts["philosophy"]
    )


def setup_sys_prompt_existing_code(
    preprompts: MutableMapping[Union[str, Path], str]
) -> str:
    """
    Sets up the system prompt for improving existing code.
    """
    return (
        preprompts["roadmap"]
        + preprompts["improve"].replace("FILE_FORMAT", preprompts["file_format_diff"])
        + "\nUseful to know:\n"
        + preprompts["philosophy"]
    )


def gen_code(
    ai: AI, prompt: str, memory: BaseMemory, preprompts_holder: GptEngineerPromptGenerator
) -> FilesDict:
    """
    Generates code from a prompt using AI and returns the generated files.
    """
    preprompts = preprompts_holder.get_preprompts()
    messages = ai.start(
        setup_sys_prompt(preprompts), prompt, step_name=curr_fn()
    )
    chat = messages[-1].content.strip()
    memory.log("code_gen.log", "\n\n".join(x.pretty_repr() for x in messages))
    files_dict = chat_to_files_dict(chat)
    return files_dict


def gen_entrypoint(
    ai: AI,
    prompt: str,
    files_dict: FilesDict,
    memory: BaseMemory,
    preprompts_holder: GptEngineerPromptGenerator,
) -> FilesDict:
    """
    Generates an entrypoint for the codebase and returns the entrypoint files.
    """
    user_prompt = prompt
    if not user_prompt:
        user_prompt = """
        Make a unix script that
        a) installs dependencies
        b) runs all necessary parts of the codebase (in parallel if necessary)
        """
    preprompts = preprompts_holder.get_preprompts()
    messages = ai.start(
        system=(preprompts["entrypoint"]),
        user=user_prompt
        + "\nInformation about the codebase:\n\n"
        + files_dict.to_chat(),
        step_name=curr_fn(),
    )
    print()
    chat = messages[-1].content.strip()
    regex = r"```\S*\n(.+?)```"
    matches = re.finditer(regex, chat, re.DOTALL)
    entrypoint_code = FilesDict(
        {"run.sh": "\n".join(match.group(1) for match in matches)}
    )
    memory.log("entrypoint.log", "\n\n".join(x.pretty_repr() for x in messages))
    return entrypoint_code


def improve_fn(
    ai: AI,
    prompt: str,
    files_dict: FilesDict,
    memory: BaseMemory,
    preprompts_holder: GptEngineerPromptGenerator,
) -> FilesDict:
    """
    Improves the code based on user input and returns the updated files.
    """
    preprompts = preprompts_holder.get_preprompts()
    messages = [
        SystemMessage(content=setup_sys_prompt_existing_code(preprompts)),
    ]

    # Add files as input
    messages.append(HumanMessage(content=f"{files_dict.to_chat()}"))
    messages.append(HumanMessage(content=prompt))
    memory.log(
        "debug.log",
        "UPLOADED FILES:\n" + files_dict.to_log() + "\nPROMPT:\n" + prompt,
    )
    return _improve_loop(ai, files_dict, memory, messages)


def _improve_loop(
    ai: AI, files_dict: FilesDict, memory: BaseMemory, messages: List
) -> FilesDict:
    messages = ai.next(messages, step_name=curr_fn())
    files_dict, errors = salvage_correct_hunks(
        messages, files_dict, memory
    )

    retries = 0
    while errors and retries < 3:
        messages.append(
            HumanMessage(
                content="Some previously produced diffs were not on the requested format, or the code part was not found in the code. Details:\n"
                + "\n".join(errors)
                + "\n Only rewrite the problematic diffs, making sure that the failing ones are now on the correct format and can be found in the code. Make sure to not repeat past mistakes. \n"
            )
        )
        messages = ai.next(messages, step_name=curr_fn())
        files_dict, errors = salvage_correct_hunks(
            messages, files_dict, memory
        )
        retries += 1

    return files_dict


def salvage_correct_hunks(
    messages: List, files_dict: FilesDict, memory: BaseMemory
) -> tuple[FilesDict, List[str]]:
    error_messages = []
    ai_response = messages[-1].content.strip()

    diffs = parse_diffs(ai_response)
    # validate and correct diffs

    for _, diff in diffs.items():
        # if diff is a new file, validation and correction is unnecessary
        if not diff.is_new_file():
            problems = diff.validate_and_correct(
                file_to_lines_dict(files_dict[diff.filename_pre])
            )
            error_messages.extend(problems)
    files_dict = apply_diffs(diffs, files_dict)
    memory.log("improve.log", "\n\n".join(x.pretty_repr() for x in messages))
    memory.log("diff.log", "\n\n".join(error_messages))
    return files_dict, error_messages
