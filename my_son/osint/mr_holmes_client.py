"""
This module contains the MrHolmesClient class, which is a wrapper for the Mr.Holmes OSINT tool.
"""

import subprocess
import os

class MrHolmesClient:
    """
    A wrapper for the Mr.Holmes OSINT tool.
    """

    def __init__(self, mr_holmes_path):
        self.mr_holmes_path = mr_holmes_path

    def _run_script(self, script_name, *args):
        """
        Runs a script from the Mr.Holmes Core directory.
        """
        script_path = os.path.join(self.mr_holmes_path, 'Core', script_name)
        cmd = ['python3', script_path] + list(args)

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=self.mr_holmes_path)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error running {script_name}: {e}")
            print(f"Stderr: {e.stderr}")
            return None

    def investigate_domain(self, domain):
        """
        Investigates a domain using Mr.Holmes.
        """
        return self._run_script('Searcher.py', domain)

    def investigate_username(self, username):
        """
        Investigates a username using Mr.Holmes.
        """
        return self._run_script('Searcher_person.py', username)

    def investigate_phone(self, phone_number):
        """
        Investigates a phone number using Mr.Holmes.
        """
        return self._run_script('Searcher_phone.py', phone_number)
