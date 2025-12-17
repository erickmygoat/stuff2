"""
This module manages the acquisition and registration of external tools.
"""
import os
import logging
try:
    import git
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False

TOOLS_DIR = "tools"

class ToolLibrary:
    """
    Manages a local library of external tools cloned from Git.
    """

    def __init__(self, tools_dir=TOOLS_DIR):
        self.logger = logging.getLogger(__name__)
        self.tools_dir = tools_dir
        if not os.path.exists(self.tools_dir):
            os.makedirs(self.tools_dir)

    def install_from_github(self, repo_url):
        """
        Clones a GitHub repository into the tools directory.
        Returns the path to the cloned tool.
        """
        if not GIT_AVAILABLE:
            self.logger.error("GitPython not installed. Cannot clone tools.")
            return None

        repo_name = repo_url.rstrip("/").split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        target_path = os.path.join(self.tools_dir, repo_name)

        if os.path.exists(target_path):
            self.logger.info(f"Tool {repo_name} already exists at {target_path}.")
            return target_path

        print(f"ToolLibrary: Cloning {repo_url}...")
        try:
            git.Repo.clone_from(repo_url, target_path)
            print(f"ToolLibrary: Successfully installed {repo_name}.")
            return target_path
        except Exception as e:
            self.logger.error(f"Failed to clone {repo_url}: {e}")
            return None

    def list_tools(self):
        """
        Returns a list of available tool paths.
        """
        tools = []
        if os.path.exists(self.tools_dir):
            for name in os.listdir(self.tools_dir):
                path = os.path.join(self.tools_dir, name)
                if os.path.isdir(path):
                    tools.append(path)
        return tools
