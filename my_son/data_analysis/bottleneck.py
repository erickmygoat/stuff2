from collections import defaultdict

def find_critical_path(tasks):
    """
    Implements a Critical Path Analysis algorithm to identify bottlenecks.

    This algorithm models a user's workflow as a directed acyclic graph (DAG),
    where tasks are nodes and dependencies are edges. It calculates the
    critical path—the longest path through the graph—which represents the
    bottleneck in the user's system.

    Args:
        tasks (dict): A dictionary of tasks, where each key is a task name and
                      the value is a dict with 'duration' and 'dependencies'.
                      Example: {
                          'A': {'duration': 5, 'dependencies': []},
                          'B': {'duration': 7, 'dependencies': ['A']},
                          'C': {'duration': 3, 'dependencies': ['A']},
                          'D': {'duration': 4, 'dependencies': ['B', 'C']}
                      }

    Returns:
        list: The sequence of tasks that form the critical path.
        int: The total duration of the critical path.
    """
    # Build a graph and find nodes with no incoming edges (start nodes)
    graph = defaultdict(list)
    in_degree = {task: 0 for task in tasks}
    for task, details in tasks.items():
        for dep in details['dependencies']:
            graph[dep].append(task)
            in_degree[task] += 1

    # Calculate earliest start and finish times (ES, EF)
    es = {task: 0 for task in tasks}
    ef = {task: 0 for task in tasks}

    # Using topological sort to process tasks in order
    queue = [task for task, degree in in_degree.items() if degree == 0]

    while queue:
        u = queue.pop(0)
        ef[u] = es[u] + tasks[u]['duration']

        for v in graph[u]:
            es[v] = max(es[v], ef[u])
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    # Find project finish time
    project_finish_time = max(ef.values())

    # Calculate latest start and finish times (LS, LF)
    lf = {task: project_finish_time for task in tasks}
    ls = {task: 0 for task in tasks}

    # Reverse topological sort order
    queue = [task for task in tasks if not graph[task]]
    processed = set()

    while queue:
        u = queue.pop(0)
        processed.add(u)

        if not graph[u]: # if it's an end node
             lf[u] = project_finish_time

        ls[u] = lf[u] - tasks[u]['duration']

        for dep in tasks[u]['dependencies']:
            lf[dep] = min(lf[dep], ls[u])
            # Check if all successors of dep are processed
            all_successors_processed = True
            for successor in graph[dep]:
                if successor not in processed:
                    all_successors_processed = False
                    break
            if all_successors_processed and dep not in queue:
                 queue.append(dep)

    # Identify critical path (where slack is zero)
    critical_path = [task for task in tasks if ls[task] == es[task]]

    # Sort the critical path by earliest start time for logical flow
    critical_path.sort(key=lambda task: es[task])

    return critical_path, project_finish_time

# Example Usage:
if __name__ == '__main__':
    # Simulating a user's project workflow
    user_tasks = {
        'A': {'duration': 5, 'dependencies': []},
        'B': {'duration': 7, 'dependencies': ['A']},
        'C': {'duration': 3, 'dependencies': ['A']},
        'D': {'duration': 4, 'dependencies': ['B', 'C']},
        'E': {'duration': 6, 'dependencies': ['D']}
    }

    path, duration = find_critical_path(user_tasks)

    print("--- Bottleneck Detector ---")
    print(f"The user's bottleneck (critical path) is: {' -> '.join(path)}")
    print(f"Total project duration: {duration} days")
    print(f"Addressing tasks on this path will have the greatest impact on project timelines.")
