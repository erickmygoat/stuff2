"""
This module provides Long-Term Memory capabilities using a Vector Database (ChromaDB).
"""
import logging
import time

try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

class Memory:
    """
    The agent's long-term memory system.
    Stores observations, conversations, and facts.
    """

    def __init__(self, persist_directory="./brain_memory"):
        self.logger = logging.getLogger(__name__)
        self.client = None
        self.collection = None

        if CHROMA_AVAILABLE:
            try:
                self.client = chromadb.PersistentClient(path=persist_directory)
                self.collection = self.client.get_or_create_collection(name="episodic_memory")
                print("Memory: Long-term memory initialized.")
            except Exception as e:
                self.logger.error(f"Failed to init ChromaDB: {e}")
                self.client = None
        else:
            self.logger.warning("ChromaDB not installed. Memory will be transient/disabled.")

    def save_context(self, input_text, output_text):
        """
        Stores an interaction pair into memory.
        """
        if not input_text and not output_text:
            return

        text_to_store = ""
        if input_text:
             text_to_store += f"User: {input_text}\n"
        if output_text:
             text_to_store += f"Agent: {output_text}\n"

        self.store_memory(text_to_store.strip())

    def store_memory(self, text, metadata=None):
        """
        Stores a text snippet into memory.
        """
        if not CHROMA_AVAILABLE or not self.collection or not text:
            return

        if metadata is None:
            metadata = {}

        metadata["timestamp"] = time.time()

        try:
            mem_id = f"mem_{int(time.time() * 1000)}"
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[mem_id]
            )
        except Exception as e:
            self.logger.error(f"Failed to store memory: {e}")

    def retrieve_context(self, query, n_results=3):
        """
        Retrieves relevant memories for a given query.
        """
        if not CHROMA_AVAILABLE or not self.collection or not query:
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            if results and results['documents']:
                return results['documents'][0]
            return []
        except Exception as e:
            self.logger.error(f"Failed to retrieve memory: {e}")
            return []
