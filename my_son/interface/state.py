"""
This module manages the real-time state of the agent and broadcasts updates to connected clients via WebSockets.
"""
import asyncio
import json
import logging
import psutil
import time
from fastapi import WebSocket

class StateManager:
    """
    Holds the state of the agent and manages WebSocket connections.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StateManager, cls).__new__(cls)
            cls._instance.active_connections = []
            cls._instance.state = {
                "status": "Idle",
                "current_task": "Waiting for input...",
                "thought_process": "",
                "system_stats": {},
                "logs": []
            }
            cls._instance.logger = logging.getLogger(__name__)
        return cls._instance

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Send initial state
        await websocket.send_text(json.dumps({"type": "state_update", "data": self.state}))

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message_type: str, data: dict):
        """
        Broadcasts a message to all connected clients.
        """
        message = json.dumps({"type": message_type, "data": data})
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                self.logger.error(f"Broadcasting failed: {e}")
                self.disconnect(connection)

    async def update_state(self, key, value):
        """
        Updates a specific key in the state and broadcasts the change.
        """
        self.state[key] = value
        await self.broadcast("state_update", {key: value})

    async def log_activity(self, message):
        """
        Adds a log entry and broadcasts it.
        """
        entry = f"[{time.strftime('%H:%M:%S')}] {message}"
        self.state["logs"].append(entry)
        # Keep log size manageable
        if len(self.state["logs"]) > 50:
            self.state["logs"].pop(0)

        await self.broadcast("log_update", {"entry": entry})

    def get_system_stats(self):
        """
        Returns current system stats.
        """
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }

# Global instance accessor
state_manager = StateManager()
