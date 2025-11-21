from abc import ABC, abstractmethod

class OSINTClient(ABC):
    """
    Abstract base class for all OSINT clients.
    """

    @abstractmethod
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def query(self, query: str, options: dict = None) -> dict:
        """
        Execute a query against the OSINT tool.

        :param query: The search query (e.g., a username, email, IP address).
        :param options: A dictionary of tool-specific options.
        :return: A dictionary containing the results.
        """
        pass
