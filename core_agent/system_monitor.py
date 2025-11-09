import psutil
import json

class SystemMonitor:
    """
    A module that monitors the host system's resources (CPU, memory, disk).
    """
    def get_cpu_usage(self):
        """
        Returns the system-wide CPU utilization as a percentage.
        """
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self):
        """
        Returns the system's memory usage statistics.
        """
        mem = psutil.virtual_memory()
        return {
            'total_gb': round(mem.total / (1024**3), 2),
            'available_gb': round(mem.available / (1024**3), 2),
            'percent_used': mem.percent
        }

    def get_disk_usage(self, path='/'):
        """
        Returns the disk usage statistics for a given path.
        """
        disk = psutil.disk_usage(path)
        return {
            'total_gb': round(disk.total / (1024**3), 2),
            'used_gb': round(disk.used / (1024**3), 2),
            'free_gb': round(disk.free / (1024**3), 2),
            'percent_used': disk.percent
        }

    def get_snapshot(self):
        """
        Returns a snapshot of all key system metrics.
        """
        return {
            'cpu_percent': self.get_cpu_usage(),
            'memory': self.get_memory_usage(),
            'disk': self.get_disk_usage()
        }

# Example Usage:
if __name__ == '__main__':
    monitor = SystemMonitor()
    system_snapshot = monitor.get_snapshot()

    print("--- System Resource Snapshot ---")
    print(json.dumps(system_snapshot, indent=2))
