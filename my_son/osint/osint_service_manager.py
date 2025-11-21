from typing import Dict, Type
from my_son.osint.osint_client import OSINTClient

class OSINTServiceManager:
    """
    Manages the lifecycle of OSINT clients.
    """

    def __init__(self):
        self._clients: Dict[str, OSINTClient] = {}

    def register_client(self, client_class: Type[OSINTClient], name: str, *args, **kwargs):
        """
        Instantiates and registers a new OSINT client.

        :param client_class: The class of the client to register.
        :param name: The name to register the client under.
        """
        if name in self._clients:
            raise ValueError(f"Client with name '{name}' is already registered.")

        client_instance = client_class(name=name, *args, **kwargs)
        self._clients[name] = client_instance
        print(f"Registered OSINT client: {name}")

    def get_client(self, name: str) -> OSINTClient:
        """
        Retrieves a registered OSINT client.

        :param name: The name of the client to retrieve.
        :return: An instance of the OSINT client.
        """
        client = self._clients.get(name)
        if not client:
            raise ValueError(f"No OSINT client registered with the name '{name}'.")
        return client

    def query_all(self, query: str, options: dict = None) -> dict:
        """
        Executes a query against all registered OSINT clients.

        :param query: The search query.
        :param options: A dictionary of tool-specific options.
        :return: A dictionary of results from all clients.
        """
        results = {}
        for name, client in self._clients.items():
            try:
                results[name] = client.query(query, options)
            except Exception as e:
                results[name] = {"error": str(e)}
        return results
