"""
This module provides a base class for prompt generators.
"""

class PromptGenerator:
    """
    A base class for prompt generators.
    """

    def __init__(self):
        self.constraints = []
        self.resources = []
        self.performance_evaluations = []

    def add_constraint(self, constraint):
        """
        Adds a constraint to the prompt.
        """
        self.constraints.append(constraint)

    def add_resource(self, resource):
        """
        Adds a resource to the prompt.
        """
        self.resources.append(resource)

    def add_performance_evaluation(self, performance_evaluation):
        """
        Adds a performance evaluation to the prompt.
        """
        self.performance_evaluations.append(performance_evaluation)

    def get_prompt(self, **kwargs):
        """
        Returns the prompt.
        """
        raise NotImplementedError
