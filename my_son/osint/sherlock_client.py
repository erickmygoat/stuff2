"""
This module contains the SherlockClient class, which is a wrapper for the Sherlock OSINT tool.
"""

import subprocess
import os
import csv
from my_son.osint.osint_client import OSINTClient

class SherlockClient(OSINTClient):
    """
    A wrapper for the Sherlock OSINT tool that conforms to the OSINTClient interface.
    """

    def __init__(self, name: str, sherlock_path: str = "./sherlock"):
        """
        Initializes the SherlockClient.

        :param name: The name of the client.
        :param sherlock_path: The path to the sherlock installation.
        """
        super().__init__(name)
        self.sherlock_path = sherlock_path

    def query(self, query: str, options: dict = None) -> dict:
        """
        Investigates a username using Sherlock.

        :param query: The username to investigate.
        :param options: (Unused) A dictionary of tool-specific options.
        :return: A dictionary containing the results.
        """
        username = query
        sherlock_py_path = os.path.join(self.sherlock_path, 'sherlock', 'sherlock.py')
        output_file = f"{username}.csv"
        # Note: Sherlock's path seems to have changed in some installations.
        # Adjusting the path to be more robust. Original was 'sherlock_project/sherlock.py'
        cmd = f"python3 {sherlock_py_path} --csv -o {output_file} {username}"

        try:
            # Increased timeout for potentially long-running Sherlock scans
            process = subprocess.run(
                cmd,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=300
            )

            results = []
            with open(output_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    results.append(row)

            os.remove(output_file) # Clean up the output file
            return {"results": results}

        except FileNotFoundError:
            error_message = f"Sherlock executable not found at '{sherlock_py_path}'. Please ensure Sherlock is correctly installed and the path is configured."
            print(error_message)
            return {"error": error_message}
        except subprocess.CalledProcessError as e:
            error_message = f"Error running Sherlock for username '{username}': {e.stderr}"
            print(error_message)
            return {"error": error_message}
        except subprocess.TimeoutExpired:
            error_message = f"Sherlock scan for '{username}' timed out after 300 seconds."
            print(error_message)
            return {"error": error_message}
        except Exception as e:
            error_message = f"An unexpected error occurred during the Sherlock scan for '{username}': {str(e)}"
            print(error_message)
            return {"error": error_message}
