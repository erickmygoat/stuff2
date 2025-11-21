"""
This module contains a simple test script to verify the SpiderFootClient.
"""

import os
import sys
import time

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_son.osint.spiderfoot_client import SpiderFootClient

def main():
    """
    Instantiates the SpiderFootClient, starts the server, runs a scan, and prints the results.
    """
    spiderfoot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'spiderfoot')
    client = SpiderFootClient(spiderfoot_path)

    try:
        client.start_server()
        scan_id = client.run_scan("example.com")
        print(f"Scan started with ID: {scan_id}")
        results = client.get_scan_results(scan_id, wait_time=120)
        print("--- SCAN RESULTS ---")
        if results:
            print(f"Found {len(results)} results.")
            for result in results[:5]: # Print the first 5 results
                print(result)
        else:
            print("No results found.")
    finally:
        client.stop_server()

if __name__ == "__main__":
    main()
