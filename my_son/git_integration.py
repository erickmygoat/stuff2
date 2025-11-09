from git import Repo
import os

class GitIntegration:
    """
    A module to allow the agent to interact with the local Git repository.
    """
    def __init__(self, repo_path='.'):
        """
        Initializes the GitIntegration module.

        Args:
            repo_path (str): The path to the local Git repository.
        """
        try:
            self.repo = Repo(repo_path, search_parent_directories=True)
        except Exception as e:
            print(f"Error initializing Git repository: {e}")
            self.repo = None

    def commit_changes(self, file_list, commit_message):
        """
        Adds and commits a list of files.

        Args:
            file_list (list): A list of file paths to add and commit.
            commit_message (str): The commit message.

        Returns:
            bool: True if the commit was successful, False otherwise.
        """
        if not self.repo:
            return False

        try:
            self.repo.index.add(file_list)
            self.repo.index.commit(commit_message)
            print("Successfully committed changes.")
            return True
        except Exception as e:
            print(f"An error occurred during commit: {e}")
            return False

    def push_changes(self, remote_name='origin', branch_name='main'):
        """
        Pushes changes to a remote repository.

        Args:
            remote_name (str): The name of the remote to push to.
            branch_name (str): The name of the branch to push.

        Returns:
            bool: True if the push was successful, False otherwise.
        """
        if not self.repo:
            return False

        try:
            origin = self.repo.remote(name=remote_name)
            origin.push(refspec=f'{branch_name}:{branch_name}')
            print("Successfully pushed changes.")
            return True
        except Exception as e:
            print(f"An error occurred during push: {e}")
            return False

# Example Usage:
if __name__ == '__main__':
    # This is a demonstration and will not actually commit/push unless
    # this script is run in a real Git repository with changes.

    # Create a dummy file to commit
    dummy_file = "self_improvement_log.txt"
    with open(dummy_file, "w") as f:
        f.write("Agent self-improved its codebase.\\n")

    git_integration = GitIntegration()

    # In a real scenario, the agent would call these methods after a successful self-modification.
    commit_success = git_integration.commit_changes(
        [dummy_file],
        "Agent Self-Improvement: Optimized a module."
    )

    if commit_success:
        # push_success = git_integration.push_changes()
        print("Push step skipped for this demonstration.")

    # Clean up the dummy file
    os.remove(dummy_file)
