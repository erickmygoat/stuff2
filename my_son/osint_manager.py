import asyncio
import os
import signal

class OSINTServiceManager:
    """
    Manages the lifecycle of the OSINT MCP server.
    """
    def __init__(self, server_path='tools/osint-tools-mcp-server/src/osint_tools_mcp_server.py', pid_file='/tmp/osint_server.pid'):
        """
        Initializes the OSINTServiceManager.

        Args:
            server_path (str): The path to the OSINT server script.
            pid_file (str): The file to store the process ID of the server.
        """
        self.server_path = server_path
        self.pid_file = pid_file
        self.process = None

    async def start_server(self):
        """
        Starts the OSINT server as a background subprocess.
        """
        if os.path.exists(self.pid_file):
            print("OSINT server may already be running.")
            return

        try:
            log_file = '/tmp/osint_server.log'
            with open(log_file, 'w') as log:
                self.process = await asyncio.create_subprocess_exec(
                    'python', self.server_path,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=log,
                    preexec_fn=os.setsid
                )

            with open(self.pid_file, 'w') as f:
                f.write(str(self.process.pid))

            print(f"OSINT server started with PID {self.process.pid}.")
            return self.process
        except Exception as e:
            print(f"Error starting OSINT server: {e}")
            return None

    def stop_server(self):
        """
        Stops the OSINT server.
        """
        if not os.path.exists(self.pid_file):
            print("OSINT server does not appear to be running.")
            return

        with open(self.pid_file, 'r') as f:
            pid = int(f.read().strip())

        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
            print(f"OSINT server with PID {pid} stopped.")
        except ProcessLookupError:
            print(f"No process with PID {pid} found.")
        finally:
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
