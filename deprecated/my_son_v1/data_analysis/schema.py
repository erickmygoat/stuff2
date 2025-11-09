import json
from datetime import datetime

class UnifiedDataPoint:
    """
    A flexible data model for ingesting time-series data from disparate sources.

    This class provides a unified schema for various types of user data, ensuring
    that all incoming information can be processed and analyzed consistently.
    """
    def __init__(self, source, data_type, timestamp, content, metadata=None):
        """
        Initializes a new UnifiedDataPoint.

        Args:
            source (str): The origin of the data (e.g., 'google_calendar', 'slack').
            data_type (str): The type of data (e.g., 'event', 'message', 'task').
            timestamp (datetime): The timestamp of the data point.
            content (dict): The main content of the data point.
            metadata (dict, optional): Additional metadata. Defaults to None.
        """
        self.source = source
        self.data_type = data_type
        self.timestamp = timestamp
        self.content = content
        self.metadata = metadata or {}

    def to_json(self):
        """
        Serializes the data point to a JSON string.
        """
        return json.dumps({
            'source': self.source,
            'data_type': self.data_type,
            'timestamp': self.timestamp.isoformat(),
            'content': self.content,
            'metadata': self.metadata
        }, indent=2)

    @classmethod
    def from_json(cls, json_string):
        """
        Deserializes a JSON string to a UnifiedDataPoint object.
        """
        data = json.loads(json_string)
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)

# Example Usage:
if __name__ == '__main__':
    # Simulating data ingestion from a calendar and a task manager
    calendar_event = UnifiedDataPoint(
        source='google_calendar',
        data_type='event',
        timestamp=datetime.now(),
        content={'title': 'Project X Stand-up', 'duration_minutes': 15},
        metadata={'attendees': ['user@example.com', 'team@example.com']}
    )

    task = UnifiedDataPoint(
        source='todoist',
        data_type='task',
        timestamp=datetime.now(),
        content={'title': 'Draft Q4 Report', 'priority': 1, 'project': 'Reports'},
        metadata={'status': 'pending'}
    )

    print("--- Unified Calendar Event ---")
    print(calendar_event.to_json())

    print("\n--- Unified Task ---")
    print(task.to_json())
