"""
This module provides Long-Term Memory capabilities using a Vector Database (ChromaDB).
"""
import logging
import time

# Handle missing dependencies for MVP/CI environments
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
                # Use persistent client to save to disk (the "own file" requirement)
                self.client = chromadb.PersistentClient(path=persist_directory)
                self.collection = self.client.get_or_create_collection(name="episodic_memory")
                print("Memory: Long-term memory initialized.")
            except Exception as e:
                self.logger.error(f"Failed to init ChromaDB: {e}")
                # We can't change the global CHROMA_AVAILABLE here easily if we want to avoid UnboundLocalError
                # Instead, just log and set client to None
                self.client = None
        else:
            self.logger.warning("ChromaDB not installed. Memory will be transient/disabled.")

    def store_memory(self, text, metadata=None):
        """
        Stores a text snippet into memory.
        """
        if not CHROMA_AVAILABLE or not self.collection:
            return

        if metadata is None:
            metadata = {}

        metadata["timestamp"] = time.time()

        try:
            # We use a simple ID generation based on timestamp
            mem_id = f"mem_{int(time.time() * 1000)}"
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[mem_id]
            )
            print(f"Memory: Stored '{text[:30]}...'")
        except Exception as e:
            self.logger.error(f"Failed to store memory: {e}")

    def retrieve_context(self, query, n_results=3):
        """
        Retrieves relevant memories for a given query.
        """
        if not CHROMA_AVAILABLE or not self.collection:
            return []

        try:
            # ChromaDB handles embedding generation automatically by default (using all-MiniLM-L6-v2)
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )

            # results['documents'] is a list of lists
            if results and results['documents']:
                return results['documents'][0]
            return []
        except Exception as e:
            self.logger.error(f"Failed to retrieve memory: {e}")
            return []
