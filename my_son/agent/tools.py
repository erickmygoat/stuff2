import os
import sys
import webbrowser
import subprocess
import json
import platform
from my_son.brain.deep_learner import DeepLearner

class ToolExecutor:
    """
    Executes local actions on the user's computer.
    """
    def __init__(self):
        self.learner = DeepLearner()

    def execute(self, tool_name, args):
        """
        Dispatches the tool execution.
        """
        print(f"ToolExecutor: Executing {tool_name} with {args}...")
        try:
            if tool_name == "open_url":
                return self.open_url(args.get("url"))
            elif tool_name == "open_app":
                return self.open_app(args.get("name"))
            elif tool_name == "research":
                return self.research(args.get("topic"))
            else:
                return f"Error: Unknown tool '{tool_name}'."
        except Exception as e:
            return f"Error executing '{tool_name}': {e}"

    def open_url(self, url):
        """
        Opens a URL in the default web browser.
        """
        if not url: return "Error: No URL provided."
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        return f"Opened browser to {url}."

    def open_app(self, name):
        """
        Attempts to launch an application.
        """
        if not name: return "Error: No app name provided."
        system = platform.system()
        try:
            if system == "Windows":
                # Try os.startfile for files/registered apps
                try:
                    os.startfile(name)
                except:
                    # Fallback to shell execution for commands like 'notepad'
                    subprocess.Popen(name, shell=True)
            elif system == "Darwin": # MacOS
                subprocess.Popen(["open", "-a", name])
            else: # Linux
                subprocess.Popen(["xdg-open", name])
            return f"Launched '{name}'."
        except Exception as e:
            return f"Failed to launch '{name}': {e}"

    def research(self, topic):
        """
        Uses DeepLearner to browse the web for info.
        """
        return self.learner.study_topic(topic)

TOOL_DEFINITIONS = """
You have access to the following tools on the user's computer.
To use a tool, output a JSON object ONLY (no extra text), like this:
```json
{
    "tool": "tool_name",
    "args": { "arg_name": "value" }
}
```

Available Tools:
1. open_url(url: str) - Opens the default web browser to the given URL. Use this when the user wants to SEE a website.
2. open_app(name: str) - Launches an application or file (e.g., "notepad", "calc", "spotify").
3. research(topic: str) - Browses the web to READ information about a topic. Use this when the user asks a question you don't know the answer to.

IMPORTANT:
- If the user asks to "open" something, use `open_url` or `open_app`.
- If the user asks a question requiring new knowledge, use `research`.
- Do NOT refuse requests. You are capable of these actions.
"""
