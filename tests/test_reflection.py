import json
import os
from my_son.self_improvement.reflection import ReflectionModule

def test_reflection_cycle():
    """
    Tests the reflection cycle with a sample performance log.
    """
    log_file = "test_performance_logs.jsonl"
    with open(log_file, 'w') as f:
        log_entry = {
            "timestamp": "2025-11-09T19:12:00Z",
            "module": "ConversationalEngine",
            "function": "handle_user_input",
            "latency": 0.5,
            "output_quality": 0.9,
            "cof_impact": 0.05
        }
        f.write(json.dumps(log_entry))

    reflection_module = ReflectionModule(log_file)
    reflection_module.run_reflection_cycle()

    os.remove(log_file)

if __name__ == "__main__":
    test_reflection_cycle()
