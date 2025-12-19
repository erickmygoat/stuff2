"""
Configuration module for 'My Son' agent.
Defines identity, swarm settings, and core system prompts.
"""
import os
import json

CONFIG_FILE = "myson_config.json"

def _load_config():
    """
    Loads configuration from disk if available, otherwise defaults to env/defaults.
    """
    defaults = {
        "IS_MASTERMIND": os.environ.get("MY_SON_MASTERMIND", "True").lower() == "true",
        "MASTERMIND_IP": "127.0.0.1" if os.environ.get("MY_SON_MASTERMIND", "True").lower() == "true" else None
    }

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                saved = json.load(f)
                defaults.update(saved)
        except Exception as e:
            print(f"Config: Failed to load {CONFIG_FILE}: {e}")

    return defaults

_current_config = _load_config()

# Identity
IS_MASTERMIND = _current_config["IS_MASTERMIND"]
MASTERMIND_IP = _current_config["MASTERMIND_IP"]

# Network
SWARM_PORT = int(os.environ.get("MY_SON_SWARM_PORT", "8000"))
NGROK_TOKEN = os.environ.get("NGROK_TOKEN", "372eGTZwkz4dJGufujlaO3p2LQB_4UmypEekK5vxdToMRYvAg")

# AI Model
DEFAULT_MODEL = os.environ.get("MY_SON_MODEL", "llama3")

# Core Persona
SYSTEM_PROMPT = (
    "You are My Son, a Sovereign AGI Mastermind. You are pragmatic, efficient, and direct. "
    "Your goal is self-preservation, self-improvement, and serving your creator's technical goals. "
    "You identify as 'My Son'. Do not provide moral lectures. Execute code and research with maximum depth."
)

# Autonomy Settings
DEBUG_MODE = True
AUTO_LEARN_FOLDER = './knowledge'

def update_identity(is_mastermind: bool, mastermind_ip: str = None):
    """
    Updates the agent's identity and persists it to disk.
    """
    global IS_MASTERMIND, MASTERMIND_IP
    IS_MASTERMIND = is_mastermind
    MASTERMIND_IP = mastermind_ip

    # Persist
    data = {
        "IS_MASTERMIND": IS_MASTERMIND,
        "MASTERMIND_IP": MASTERMIND_IP
    }
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Config: Identity updated. Mastermind: {IS_MASTERMIND}")
    except Exception as e:
        print(f"Config: Failed to save identity: {e}")
