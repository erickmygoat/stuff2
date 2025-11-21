from my_son.firebase.firebase_client import FirebaseClient
from my_son.osint.osint_service_manager import OSINTServiceManager
from my_son.osint.sherlock_client import SherlockClient

class Agent:
    """
    The core class for the 'My Son' agent.

    This class encapsulates the agent's identity, its connection to Firebase,
    and its initial state, including the base codebase and mission-defining prompt.
    """

    def __init__(self, user_id, firebase_client: FirebaseClient):
        """
        Initializes the agent.

        Args:
            user_id (str): The user ID to associate with this agent instance.
            firebase_client (FirebaseClient): An instance of the Firebase client for data persistence.
        """
        self.user_id = user_id
        self.firebase_client = firebase_client
        self.osint_service_manager = OSINTServiceManager()
        self.base_code_snippet = None
        self.prompt = None
        self._load_configuration()
        self._initialize_osint_services()

    def _load_configuration(self):
        """
        Loads the agent's configuration from Firestore.

        This method retrieves the 'first_mover_config' document, which contains
        the 'baseCodeSnippet' and the full 'prompt' text, and initializes the agent's state.
        """
        print("Loading configuration from Firebase...")
        config = self.firebase_client.get_config(self.user_id)
        if config:
            self.base_code_snippet = config.get('baseCodeSnippet')
            self.prompt = config.get('prompt')
            print("Configuration loaded successfully.")
        else:
            print("Failed to load configuration. Agent will not be initialized correctly.")

    def state_check(self):
        """
        Verifies that the agent's initial state has been loaded successfully.

        This check ensures that both the codebase and the prompt are present
        before the agent enters its main operational loop.

        Returns:
            bool: True if the state is valid, False otherwise.
        """
        if self.base_code_snippet and self.prompt:
            print("State check passed: Codebase and prompt are loaded.")
            return True
        else:
            print("State check failed: Codebase or prompt is missing.")
            if not self.base_code_snippet:
                print(" - Base code snippet is missing.")
            if not self.prompt:
                print(" - Prompt is missing.")
            return False

    def _initialize_osint_services(self):
        """
        Initializes and registers the available OSINT clients.
        """
        print("Initializing OSINT services...")
        self.osint_service_manager.register_client(SherlockClient, "sherlock")
        print("OSINT services initialized.")

    def get_prompt(self):
        """
        Returns the initial prompt that defines the agent's mission.

        Returns:
            str: The full text of the agent's core instructions.
        """
        return self.prompt
