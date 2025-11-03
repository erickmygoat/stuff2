import datetime
import json

class AdherenceTracker:
    """
    Implements a logging mechanism to track user adherence to commands.

    This module records when a Command is issued and tracks user interaction
    with the related task/data to measure the Command Adherence Rate (CAR).
    """
    def __init__(self, log_file='adherence_logs.jsonl'):
        """
        Initializes the AdherenceTracker.

        Args:
            log_file (str): The file to store adherence logs.
        """
        self.log_file = log_file

    def log_command_issuance(self, command, task_id):
        """
        Logs that a command has been issued to the user.

        Args:
            command (str): The command that was issued.
            task_id (str): A unique identifier for the task associated with the command.
        """
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'event_type': 'command_issued',
            'task_id': task_id,
            'command': command
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        print(f"Logged issuance of command for task '{task_id}'.")

    def log_user_action(self, task_id, action_description):
        """
        Logs a user action related to a specific task.

        In a real system, this would be triggered by observing user activity
        in connected apps (e.g., a commit in a repo, a file update in a drive).

        Args:
            task_id (str): The ID of the task the user is working on.
            action_description (str): A description of the user's action.
        """
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'event_type': 'user_action',
            'task_id': task_id,
            'action': action_description
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        print(f"Logged user action for task '{task_id}': {action_description}")

    def calculate_car(self, task_id):
        """
        Calculates the Command Adherence Rate (CAR) for a given task.

        This is a simplified calculation. A more advanced version would analyze
        the quality and timeliness of user actions.

        Returns:
            float: The Command Adherence Rate (0.0 to 1.0).
        """
        with open(self.log_file, 'r') as f:
            logs = [json.loads(line) for line in f]

        issued_logs = [log for log in logs if log['event_type'] == 'command_issued' and log['task_id'] == task_id]
        action_logs = [log for log in logs if log['event_type'] == 'user_action' and log['task_id'] == task_id]

        if not issued_logs:
            return 0.0 # No command was issued for this task

        # Simple adherence metric: Did the user take any action on the task?
        return 1.0 if action_logs else 0.0

# Example Usage:
if __name__ == '__main__':
    tracker = AdherenceTracker()

    # The agent issues a command
    task_id = 'investor_update_q4'
    command = "PRIORITIZED DIRECTIVE: Your primary focus must be 'Draft investor update'. Defer all other tasks until this is complete."
    tracker.log_command_issuance(command, task_id)

    # The user starts working on the task (simulated)
    tracker.log_user_action(task_id, "Opened 'investor_update_draft_v1.docx'")
    tracker.log_user_action(task_id, "Added 500 words to the document")

    # The agent calculates the adherence rate
    car_score = tracker.calculate_car(task_id)

    print("\n--- Adherence Tracking ---")
    print(f"Command Adherence Rate (CAR) for task '{task_id}': {car_score * 100:.1f}%")

    # Example of non-adherence
    non_adherent_task = 'learn_crm'
    tracker.log_command_issuance("PRIORITIZED DIRECTIVE: Learn the new CRM software.", non_adherent_task)
    non_adherent_car = tracker.calculate_car(non_adherent_task)
    print(f"Command Adherence Rate (CAR) for task '{non_adherent_task}': {non_adherent_car * 100:.1f}%")
