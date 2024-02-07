import heapq

def misplaced_tiles_heuristic(config, length, n):
    """Counts the number of disks not in their final positions."""
    misplaced = 0
    for i, disk in enumerate(config):
        if disk != length - n + i:
            misplaced += 1
    return misplaced

def manhattan_distance_heuristic(config, length, n):
    """Calculates the sum of Manhattan distances of disks from their final positions."""
    distance = 0
    for i, disk in enumerate(config):
        distance += abs(disk - (length - n + i))
    return distance

def is_goal_state(config, length, n):
    """Checks if all disks are in reverse order at the end."""
    return config == [length - n + i for i in range(n)]

def generate_successors(config, length, n):
    """Generates all valid moves (jumping over disks when possible)."""
    successors = []
    for i, disk in enumerate(config):
        # Move left one space
        if i > 0 and config[i-1] == -1:
            new_config = config[:]
            new_config[i], new_config[i-1] = new_config[i-1], new_config[i]
            successors.append(new_config)
        # Move left two spaces (jumping over a disk)
        if i > 1 and config[i-1] == -1 and config[i-2] != -1:
            new_config = config[:]
            new_config[i], new_config[i-2] = new_config[i-2], new_config[i]
            successors.append(new_config)
        # Move right one space
        if i < n-1 and config[i+1] == -1:
            new_config = config[:]
            new_config[i], new_config[i+1] = new_config[i+1], new_config[i]
            successors.append(new_config)
        # Move right two spaces (jumping over a disk)
        if i < n-2 and config[i+1] == -1 and config[i+2] != -1:
            new_config = config[:]
            new_config[i], new_config[i+2] = new_config[i+2], new_config[i]
            successors.append(new_config)
    return successors

def reconstruct_path(state):
    """Backtracks from goal state to reconstruct the move sequence."""
    path = []
    while state[0] != [0] * n:
        for successor in generate_successors(state[0], length, n):
            if successor == state[1]:
                path.append("Move disk {} {} spaces".format(state[0][state[0].index(-1)],
                                                          abs(state[0].index(-1) - successor.index(-1))))
                state = (successor, state[2])
                break
    return path[::-1]  # Reverse path for chronological order

def solve_distinct_disks(length, n, heuristic="misplaced_tiles"):
    """Solves the Linear Disk Movement problem using A* search.

    Args:
        length: The length of the row.
        n: The number of distinct disks.
        heuristic (optional): The heuristic to use. Can be "misplaced_tiles" or "manhattan_distance".

    Returns:
        A list of moves required to reach the goal state, or None if no solution exists.
    """

    # Initial state representation
    initial_state = ([i for i in range(n)], 0, eval(heuristic)(initial_state[0], length, n))

    # Priority queue for A* search
    pq = [(initial_state[2], initial_state)]

    # Visited states to prevent loops
    visited = set()

    while pq:
        # Get state with lowest f_score
        f_score, state = heapq.heappop(pq)

        # Check for goal state
        if is_goal_state(state[0], length, n):
            return reconstruct_path(state)

        # Check if already visited
        if state in visited:
            continue

        # Add to visited set
        visited.add(state)

        # Generate successor states
        
