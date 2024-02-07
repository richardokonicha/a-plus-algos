from heapq import heappush, heappop

def euclidean_distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def find_path(start, goal, scene):
    rows, cols = len(scene), len(scene[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: euclidean_distance(start, goal)}

    while open_set:
        current = heappop(open_set)[1]
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and not scene[neighbor[0]][neighbor[1]]:
                tentative_g_score = g_score[current] + euclidean_distance(current, neighbor)
                if neighbor not in g_score or tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + euclidean_distance(neighbor, goal)
                    heappush(open_set, (f_score[neighbor], neighbor))

    return None

# Example usage
scene = [[False, False, False],
         [False, True, False],
         [False, False, False]]

for start, goal in [((0, 0), (2, 1)), ((0, 0), (2, 1)), ((0, 0), (0, 2)), ((0, 1), (2, 1)), ((0, 0), (9, 9))]:
    path = find_path(start, goal, scene)

    if path is None:
        print("No path found")
    else:
        path_steps = " -> ".join([f"({p[0]}, {p[1]})" for p in path])
        print(f"Shortest path from ({start[0]}, {start[1]}) to ({goal[0]}, {goal[1]}):")
        print(path_steps)
