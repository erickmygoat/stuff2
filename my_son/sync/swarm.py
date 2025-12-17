"""
This module handles network discovery and task delegation for the Swarm.
"""
import requests
import socket
import logging
import concurrent.futures
from my_son.config import SWARM_PORT

class SwarmManager:
    """
    Manages discovery of worker nodes and delegation of tasks.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.workers = []
        # In a real scenario, we might cache workers or scan periodically.

    def get_local_ip(self):
        """
        Attempts to determine the local IP address.
        """
        try:
            # Create a dummy socket to connect to an external IP (doesn't send data)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"

    def scan_network(self, timeout=0.5):
        """
        Scans the local subnet for active agents.
        Returns a list of active worker URLs.
        """
        local_ip = self.get_local_ip()
        base_ip = ".".join(local_ip.split(".")[:-1])

        potential_ips = [f"{base_ip}.{i}" for i in range(1, 255)]
        active_workers = []

        print(f"SwarmManager: Scanning network {base_ip}.x on port {SWARM_PORT}...")

        def check_ip(ip):
            if ip == local_ip:
                return None # Don't delegate to self via network loop

            url = f"http://{ip}:{SWARM_PORT}/api/health" # Assuming a health endpoint exists
            # Or we can try the chat endpoint directly if health check isn't strictly defined
            # But the prompt says "find other agents listening on SWARM_PORT".
            # A TCP connect check is faster than a full HTTP request for discovery.

            try:
                # Fast TCP check
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((ip, SWARM_PORT))
                sock.close()
                if result == 0:
                    return f"http://{ip}:{SWARM_PORT}"
            except:
                pass
            return None

        # Use threads for fast scanning
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(check_ip, potential_ips)

        for res in results:
            if res:
                active_workers.append(res)

        self.workers = active_workers
        print(f"SwarmManager: Found {len(self.workers)} active workers.")
        return self.workers

    def delegate_task(self, prompt, system_prompt):
        """
        Delegates a generation task to a worker node.
        Returns the response text if successful, or None.
        """
        if not self.workers:
            # Try a quick scan if we have no known workers
            self.scan_network()

        if not self.workers:
            return None

        # Simple round-robin or pick first for now
        # In a robust system, we would track load/availability
        for worker_url in self.workers:
            print(f"SwarmManager: Delegating task to {worker_url}...")
            endpoint = f"{worker_url}/api/swarm/generate"

            payload = {
                "prompt": prompt,
                "system_prompt": system_prompt
            }

            try:
                response = requests.post(endpoint, json=payload, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    # Assuming standard response format {"response": "text"}
                    return data.get("response")
            except Exception as e:
                self.logger.warning(f"Failed to delegate to {worker_url}: {e}")
                # Remove dead worker?
                continue

        return None
