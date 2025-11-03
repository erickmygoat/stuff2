import pytest
from unittest.mock import MagicMock
from my_son.agent.agent import Agent

def test_agent_initialization_and_state_check_success():
    """
    Tests that the agent initializes successfully and the state check passes
    when the Firebase configuration is valid.
    """
    # Arrange: Create a mock Firebase client that returns a valid config.
    mock_firebase_client = MagicMock()
    mock_firebase_client.get_config.return_value = {
        'baseCodeSnippet': 'def main():\n    print("Hello, World!")',
        'prompt': "Your mission is to assist the user."
    }

    # Act: Initialize the Agent with the mock client.
    agent = Agent(user_id='test_user', firebase_client=mock_firebase_client)

    # Assert: Verify that the configuration was loaded correctly and the state check passes.
    assert agent.base_code_snippet is not None
    assert agent.prompt is not None
    assert agent.state_check() is True

def test_agent_state_check_failure():
    """
    Tests that the state check fails when the Firebase configuration is missing.
    """
    # Arrange: Create a mock Firebase client that returns None.
    mock_firebase_client = MagicMock()
    mock_firebase_client.get_config.return_value = None

    # Act: Initialize the Agent.
    agent = Agent(user_id='test_user', firebase_client=mock_firebase_client)

    # Assert: Verify that the state is not loaded and the state check fails.
    assert agent.base_code_snippet is None
    assert agent.prompt is None
    assert agent.state_check() is False
