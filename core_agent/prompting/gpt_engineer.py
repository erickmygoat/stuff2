"""
This module provides a prompt generator for the "My Son" agent, inspired by the prompt engineering techniques used in GPT-Engineer.
"""

from.import PromptGenerator

GENERATE_PROMPT = """
Think step by step and reason yourself to the correct decisions to make sure we get it right.
First lay out the names of the core classes, functions, methods that will be necessary, As well as a quick comment on their purpose.

FILE_FORMAT

You will start with the "entrypoint" file, then go to the ones that are imported by that file, and so on.
Please note that the code should be fully functional. No placeholders.

Follow a language and framework appropriate best practice file naming convention.
Make sure that files contain all imports, types etc. The code should be fully functional. Make sure that code in different files are compatible with each other.
Ensure to implement all code, if you are unsure, write a plausible implementation.
Include module dependency or package manager dependency definition file.
Before you finish, double check that all parts of the architecture is present in the files.

When you are done, write finish with "this concludes a fully working implementation".
"""

class GptEngineerPromptGenerator(PromptGenerator):
    """
    A prompt generator that uses the GPT-Engineer preprompts to construct the prompts for the "My Son" agent.
    """

    def __init__(self):
        super().__init__()
        self.add_constraint("~4000 word limit for short term memory. Your short term memory is short, so immediately save important information to files.")
        self.add_constraint("If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.")
        self.add_constraint("No user assistance")
        self.add_constraint('Exclusively use the commands listed in double quotes e.g. "command name"')
        self.add_resource("Internet access for searches and information gathering.")
        self.add_resource("Long Term memory management.")
        self.add_resource("GPT-3.5 powered Agents for delegation of simple tasks.")
        self.add_resource("File output.")
        self.add_performance_evaluation("Continuously review and analyze your actions to ensure you are performing to the best of your abilities.")
        self.add_performance_evaluation("Constructively self-criticize your big-picture behavior constantly.")
        self.add_performance_evaluation("Reflect on past decisions and strategies to refine your approach.")
        self.add_performance_evaluation("Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.")
        self.add_performance_evaluation("Write all code to a file.")

    def get_generate_prompt(self, file_format):
        """
        Returns the generate prompt.
        """
        return GENERATE_PROMPT.replace("FILE_FORMAT", file_format)

IMPROVE_PROMPT = """
Think step by step and reason yourself to the correct decisions to make sure we get it right.
Make changes to existing code and implement new code in the unified git diff syntax. When implementing new code, First lay out the names of the core classes, functions, methods that will be necessary, As well as a quick comment on their purpose.

FILE_FORMAT

As far as compatible with the user request, start with the "entrypoint" file, then go to the ones that are imported by that file, and so on.
Please note that the code should be fully functional. No placeholders.

Follow a language and framework appropriate best practice file naming convention.
Make sure that files contain all imports, types etc. The code should be fully functional. Make sure that code in different files are compatible with each other.
Ensure to implement all code, if you are unsure, write a plausible implementation.
Include module dependency or package manager dependency definition file.
Before you finish, double check that all parts of the architecture is present in the files.

When you are done, write finish with "this concludes a fully working implementation".
"""

class GptEngineerPromptGenerator(PromptGenerator):
    """
    A prompt generator that uses the GPT-Engineer preprompts to construct the prompts for the "My Son" agent.
    """

    def __init__(self):
        super().__init__()
        self.add_constraint("~4000 word limit for short term memory. Your short term memory is short, so immediately save important information to files.")
        self.add_constraint("If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.")
        self.add_constraint("No user assistance")
        self.add_constraint('Exclusively use the commands listed in double quotes e.g. "command name"')
        self.add_resource("Internet access for searches and information gathering.")
        self.add_resource("Long Term memory management.")
        self.add_resource("GPT-3.5 powered Agents for delegation of simple tasks.")
        self.add_resource("File output.")
        self.add_performance_evaluation("Continuously review and analyze your actions to ensure you are performing to the best of your abilities.")
        self.add_performance_evaluation("Constructively self-criticize your big-picture behavior constantly.")
        self.add_performance_evaluation("Reflect on past decisions and strategies to refine your approach.")
        self.add_performance_evaluation("Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.")
        self.add_performance_evaluation("Write all code to a file.")

    def get_generate_prompt(self, file_format):
        """
        Returns the generate prompt.
        """
        return GENERATE_PROMPT.replace("FILE_FORMAT", file_format)

    def get_improve_prompt(self, file_format):
        """
        Returns the improve prompt.
        """
        return IMPROVE_PROMPT.replace("FILE_FORMAT", file_format)
