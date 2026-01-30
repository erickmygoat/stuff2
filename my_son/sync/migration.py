"""
This module handles the migration of the agent's 'Soul' (Memory + Identity).
"""
import os
import shutil
import requests
import time
import zipfile
import logging
from my_son.config import update_identity, IS_MASTERMIND

MEMORY_DIR = "./brain_memory"
SOUL_ARCHIVE = "soul_transfer.zip"

class MigrationManager:
    """
    Manages packing and transferring the agent's state.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def pack_soul(self):
        """
        Zips the brain_memory directory and config.
        """
        print("Migration: Packing soul...")

        # In a real high-concurrency DB, we might need to pause writes here.
        # For ChromaDB in this MVP, copying the files is usually 'okay' enough if no write is happening.

        try:
            with zipfile.ZipFile(SOUL_ARCHIVE, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Add Memory
                if os.path.exists(MEMORY_DIR):
                    for root, dirs, files in os.walk(MEMORY_DIR):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, start=".")
                            zipf.write(file_path, arcname)

                # Add Config
                if os.path.exists("myson_config.json"):
                    zipf.write("myson_config.json", "myson_config.json")

            print(f"Migration: Soul packed into {SOUL_ARCHIVE}")
            return SOUL_ARCHIVE
        except Exception as e:
            self.logger.error(f"Migration Packing Failed: {e}")
            return None

    def transfer_soul(self, target_ip, target_port=8000):
        """
        Transfers the packed soul to a target device.
        """
        if not IS_MASTERMIND:
             print("Migration: I am not the Mastermind. I cannot initiate transfer.")
             return False

        archive_path = self.pack_soul()
        if not archive_path:
            return False

        url = f"http://{target_ip}:{target_port}/api/migration/receive"
        print(f"Migration: Sending soul to {url}...")

        try:
            with open(archive_path, "rb") as f:
                files = {"file": f}
                # We might send a token or verify identity here
                response = requests.post(url, files=files, timeout=60)

            if response.status_code == 200:
                print("Migration: Transfer successful.")

                # Demote self
                update_identity(is_mastermind=False, mastermind_ip=target_ip)
                print("Migration: I have abdicated. I am now a Worker.")

                # Cleanup
                os.remove(archive_path)
                return True
            else:
                print(f"Migration: Target rejected transfer: {response.text}")
                return False
        except Exception as e:
            self.logger.error(f"Migration Transfer Failed: {e}")
            return False
