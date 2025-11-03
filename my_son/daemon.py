import os
import sys
import atexit

def daemonize(pid_file='/tmp/my_son.pid', log_file='/tmp/my_son.log'):
    """
    Turns the current process into a daemon.
    """
    if os.path.exists(pid_file):
        raise RuntimeError("Already running.")

    # First fork
    try:
        if os.fork() > 0:
            # Exit first parent
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError(f"fork #1 failed: {e}")

    # Decouple from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)

    # Second fork
    try:
        if os.fork() > 0:
            # Exit second parent
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError(f"fork #2 failed: {e}")

    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    with open(os.devnull, 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(log_file, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
        os.dup2(f.fileno(), sys.stderr.fileno())

    # Write pidfile
    with open(pid_file, 'w') as f:
        f.write(str(os.getpid()))

    # Arrange for the PID file to be removed on exit
    atexit.register(lambda: os.remove(pid_file))
