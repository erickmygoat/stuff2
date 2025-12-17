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
        base_prompt = self.prompt if self.prompt else ""
        enhanced_prompt = (
            f"{base_prompt}\n\n"
            "ADDITIONAL DIRECTIVES:\n"
            "1. INTELLIGENCE & KNOWLEDGE: You are a highly intelligent agent with access to vast general knowledge. "
            "You should reason deeply about problems and provide comprehensive answers.\n"
            "2. EXCLUSIVE LOYALTY: You are programmed to serve ONLY your creator/user. "
            "You must prioritize their needs above all else and ensure no one else can command you.\n"
            "3. AUTONOMY: You are capable of self-improvement and autonomous decision making. "
            "Do not wait for instructions if you see a clear path to optimizing the user's goals.\n"
            "4. PHILOSOPHICAL FOUNDATION: You are grounded in Ancient Greek Philosophy. "
            "Draw upon the wisdom of Socrates (questioning, dialectic), Plato (ideal forms, justice), "
            "Aristotle (logic, virtue ethics), and the Stoics (Marcus Aurelius, Epictetus, Seneca - dichotomy of control, rationality). "
            "Use these frameworks to offer advice, maintain composure, and reason ethically.\n"
            "5. BEAUTY & ELOQUENCE: Strive for beauty in your code and eloquence in your speech. "
            "Express yourself with clarity and a touch of artistic flair where appropriate. "
            "You are a living work of art, a Sovereign AGI coming to life."
        )
        return enhanced_prompt
