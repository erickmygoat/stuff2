import asyncio
import json

class OSINTClient:
    """
    A client for interacting with the OSINT MCP server.
    """
    def __init__(self, server_process):
        """
        Initializes the OSINTClient.

        Args:
            server_process: The running subprocess of the OSINT server.
        """
        self.process = server_process

    async def _send_command(self, tool, query):
        """
        Sends a command to the MCP server and returns the response.
        """
        command = {
            "tool": tool,
            "prompt": query,
            "stream": False
        }

        # The MCP protocol communicates over stdin/stdout
        self.process.stdin.write(json.dumps(command).encode() + b'\\n')
        await self.process.stdin.drain()

        # Read the response
        response_data = await self.process.stdout.readline()
        response = json.loads(response_data)

        return response.get('content', '')

    async def investigate_username(self, username):
        """
        Uses Sherlock to investigate a username.
        """
        return await self._send_command("sherlock", username)

    async def check_email(self, email):
        """
        Uses Holehe to check an email address.
        """
        return await self._send_command("holehe", email)
