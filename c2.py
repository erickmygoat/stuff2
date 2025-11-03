import sys
import os

# Use absolute paths for all files to ensure consistency
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PID_FILE = os.path.join(APP_DIR, 'my_son.pid')
LOG_FILE = os.path.join(APP_DIR, 'my_son.log')
CMD_FILE = os.path.join(APP_DIR, 'my_son.cmd')

def get_status():
    """Checks if the agent is running and prints its PID."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE) as f:
            pid = f.read().strip()
        print(f"Agent is running with PID: {pid}")
    else:
        print("Agent is not running.")

def view_log():
    """Prints the latest entries from the agent's log file."""
    if not os.path.exists(LOG_FILE):
        print("Log file not found.")
        return

    with open(LOG_FILE, 'r') as f:
        # Print the last 20 lines of the log
        lines = f.readlines()
        for line in lines[-20:]:
            print(line, end='')

def send_command(command):
    """Sends a command to the agent by writing to the command file."""
    try:
        with open(CMD_FILE, 'w') as f:
            f.write(command)
        print(f"Command '{command}' sent to the agent.")
    except IOError as e:
        print(f"Error sending command: {e}")

def main():
    """Main function for the C2 interface."""
    if len(sys.argv) < 2:
        print("Usage: python c2.py [status|log|pause|resume|reflect|snapshot|learn <topic>|master_language <language>]")
        sys.exit(1)

    action = sys.argv[1]

    if action == 'status':
        get_status()
    elif action == 'log':
        view_log()
    elif action in ['pause', 'resume', 'reflect', 'snapshot']:
        send_command(action)
    elif action == 'learn':
        if len(sys.argv) < 3:
            print("Usage: python c2.py learn <topic>")
            sys.exit(1)
        topic = " ".join(sys.argv[2:])
        send_command(f"learn {topic}")
    elif action == 'master_language':
        if len(sys.argv) < 3:
            print("Usage: python c2.py master_language <language>")
            sys.exit(1)
        language = sys.argv[2]
        send_command(f"master_language {language}")
    else:
        print(f"Unknown command: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
