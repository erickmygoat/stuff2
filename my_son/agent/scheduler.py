"""
This module provides a background scheduler for recurring tasks.
"""
import threading
import time
import logging

class Scheduler:
    """
    Manages recurring tasks in a background thread.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tasks = []
        self.running = False
        self.thread = None

    def add_recurring_task(self, interval_minutes, task_func, *args, **kwargs):
        """
        Adds a task to be executed every `interval_minutes`.
        """
        self.tasks.append({
            "interval": interval_minutes * 60, # Convert to seconds
            "func": task_func,
            "args": args,
            "kwargs": kwargs,
            "last_run": time.time()
        })
        print(f"Scheduler: Added task {task_func.__name__} every {interval_minutes} minutes.")

    def start(self):
        """
        Starts the scheduler loop.
        """
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print("Scheduler: Started.")

    def stop(self):
        """
        Stops the scheduler loop.
        """
        self.running = False
        if self.thread:
            self.thread.join()
        print("Scheduler: Stopped.")

    def _run_loop(self):
        """
        The main loop checking for due tasks.
        """
        while self.running:
            now = time.time()
            for task in self.tasks:
                if now - task["last_run"] >= task["interval"]:
                    try:
                        print(f"Scheduler: Running task {task['func'].__name__}...")
                        task["func"](*task["args"], **task["kwargs"])
                        task["last_run"] = time.time()
                    except Exception as e:
                        self.logger.error(f"Scheduler Task Failed: {e}")

            time.sleep(5) # Check every 5 seconds
