"""
This module contains a simple test script to verify the MrHolmesClient.
"""

import os
import sys

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_son.osint.mr_holmes_client import MrHolmesClient

def main():
    """
    Instantiates the MrHolmesClient and runs an investigation.
    """
    mr_holmes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Mr.Holmes')
    client = MrHolmesClient(mr_holmes_path)

    print("--- Investigating Domain: example.com ---")
    domain_results = client.investigate_domain("example.com")
    if domain_results:
        print(domain_results)
    else:
        print("No results found.")

    print("\n--- Investigating Username: jules ---")
    username_results = client.investigate_username("jules")
    if username_results:
        print(username_results)
    else:
        print("No results found.")

    print("\n--- Investigating Phone: 1234567890 ---")
    phone_results = client.investigate_phone("1234567890")
    if phone_results:
        print(phone_results)
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
