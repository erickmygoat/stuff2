import asyncio
from my_son.firebase.firebase_client import FirebaseClient
from my_son.agent.agent import Agent
from my_son.conversational.conversational_engine import ConversationalEngine

async def main():
    """
    The main entry point for the 'My Son' agent.
    """
    print("Starting agent...")

    # Initialize Firebase and Agent
    firebase_client = FirebaseClient()
    # TODO: Get the user_id from a secure source.
    agent = Agent(user_id="test_user", firebase_client=firebase_client)

    # Start the conversational engine
    conversational_engine = ConversationalEngine(agent)
    await conversational_engine.start_conversation()

if __name__ == "__main__":
    asyncio.run(main())
