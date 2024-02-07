import numpy as np
from queue import PriorityQueue
import itertools
import random

class TilePuzzleOptimized:
    def __init__(self, board):
        self.board = np.array(board)
        self.size = self.board.shape[0]
        self.blank_pos = self.find_blank_pos()

    def find_blank_pos(self):
        return tuple(np.argwhere(self.board == 0)[0])

    def is_solved(self):
        return np.array_equal(self.board, np.arange(self.size**2).reshape(self.size, self.size))

    def scramble(self, moves=100):
        for _ in range(moves):
            try:
                self.move(random.choice(["up", "down", "left", "right"]))
            except ValueError as e:
                print(f"Invalid move attempted during scramble: {e}")

    def move(self, direction):
        directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        if direction not in directions:
            raise ValueError(f"Invalid move direction: {direction}")
        dx, dy = directions[direction]
        x, y = self.blank_pos
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.size and 0 <= ny < self.size:
            self.board[x, y], self.board[nx, ny] = self.board[nx, ny], self.board[x, y]
            self.blank_pos = (nx, ny)
            print(f"After moving {direction}, board is now:\n{self.board}\n")
            return True
        return False

    def successors(self):
        for direction in ["up", "down", "left", "right"]:
            new_puzzle = TilePuzzleOptimized(self.board.copy())
            if new_puzzle.move(direction):
                yield (direction, new_puzzle)

    def a_star_solution(self):
        open_set = PriorityQueue()
        counter = itertools.count()
        open_set.put((0, next(counter), self))
        came_from = {str(self.board): None}
        g_score = {str(self.board): 0}

        while not open_set.empty():
            _, _, current = open_set.get()

            if current.is_solved():
                return self.reconstruct_path(came_from, current), g_score[str(current.board)]

            for move, next_state in current.successors():
                new_cost = g_score[str(current.board)] + 1
                if str(next_state.board) not in g_score or new_cost < g_score[str(next_state.board)]:
                    g_score[str(next_state.board)] = new_cost
                    priority = new_cost + self.heuristic(next_state)
                    open_set.put((priority, next(counter), next_state))
                    came_from[str(next_state.board)] = (current, move)
        return [], 0

    def heuristic(self, node):
        goal = np.arange(node.size**2).reshape(node.size, node.size)
        return sum(abs((val % node.size) - (goal_pos % node.size)) + abs((val // node.size) - (goal_pos // node.size))
                   for val, goal_pos in enumerate(node.board.flat) if val != 0)

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from and came_from[str(current.board)] is not None:
            current, move = came_from[str(current.board)]
            path.append(move)
        path.reverse()
        return path

# Testing the updated TilePuzzleOptimized class
board = [[4, 1, 3], [2, 0, 5], [7, 8, 6]]  # Initial board state
puzzle = TilePuzzleOptimized(board)
print("Initial board:\n", puzzle.board)

try:
    solution_path, steps = puzzle.a_star_solution()
    if len(solution_path) > 0:
        print(f"Solved in {len(solution_path)} steps.")
        for step in solution_path:
            print(f"Move: {step}")
    else:
        print("No solution found.")
except ValueError as e:
    print(f"Error: {e}")