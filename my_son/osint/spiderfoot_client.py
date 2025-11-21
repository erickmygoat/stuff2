"""
This module contains the SpiderFootClient class, which is a wrapper for the SpiderFoot OSINT tool.
"""

import subprocess
import time
import os
import requests
import json

class SpiderFootClient:
    """
    A wrapper for the SpiderFoot OSINT tool.
    """

    def __init__(self, spiderfoot_path, server_url="http://127.0.0.1:5001"):
        self.spiderfoot_path = spiderfoot_path
        self.server_url = server_url
        self.server_process = None
        self.log_file = os.path.join(spiderfoot_path, 'spiderfoot.log')

    def start_server(self):
        """
        Starts the SpiderFoot web server.
        """
        sf_path = os.path.join(self.spiderfoot_path, 'sf.py')
        with open(self.log_file, 'w') as log:
            self.server_process = subprocess.Popen(
                ['python3', sf_path, '-l', self.server_url.replace("http://", "")],
                stdout=log,
                stderr=log
            )
        time.sleep(15) # Give the server time to start
        print("SpiderFoot server started.")

    def stop_server(self):
        """
        Stops the SpiderFoot web server.
        """
        if self.server_process:
            self.server_process.terminate()
            print("SpiderFoot server stopped.")

    def run_scan(self, target):
        """
        Runs a scan on the given target and returns the scan ID.
        """
        post_data = {
            "scanname": f"scan_{target}",
            "scantarget": target,
            "modulelist": "sfp__stor_db,sfp__stor_stdout",
            "usecase": "all"
        }
        try:
            response = requests.post(f"{self.server_url}/startscan", data=post_data)
            response.raise_for_status()
            scan_data = response.json()
            if scan_data[0] == "SUCCESS":
                return scan_data[1]
        except requests.exceptions.RequestException as e:
            print(f"Error starting scan: {e}")
        return None

    def get_scan_results(self, scan_id, wait_time=60):
        """
        Retrieves the results of a scan, waiting for it to complete.
        """
        if not scan_id:
            return "No scan ID provided."

        print("Waiting for scan to complete...")
        time.sleep(wait_time) # Give the scan time to complete

        try:
            response = requests.post(f"{self.server_url}/scaneventresults", data={"id": scan_id})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting scan results: {e}")
        return None
