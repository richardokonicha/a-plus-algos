import copy
from math import sqrt
from queue import PriorityQueue


class TilePuzzle:
    """Represents a sliding tile puzzle of any size."""

    def __init__(self, board):
        """Initializes the puzzle with a given board layout.

        Args:
            board: A 2D list of integers representing the puzzle's tile configuration.
                   Empty space is denoted by 0.
        """
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.empty_row, self.empty_col = self.find_empty()

    def get_board(self):
        """Returns a deep copy of the current board configuration."""
        return copy.deepcopy(self.board)

    def perform_move(self, direction):
        """Attempts to swap the empty tile with its neighbor in the given direction.

        Args:
            direction: String indicating the direction ("up", "down", "left", or "right").

        Returns:
            True if the move was successful, False otherwise.
        """
        if direction not in ("up", "down", "left", "right"):
            return False

        new_row, new_col = self.get_neighbor(direction)
        if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
            self.board[self.empty_row][self.empty_col], self.board[new_row][new_col] = \
                self.board[new_row][new_col], self.board[self.empty_row][self.empty_col]
            self.empty_row, self.empty_col = new_row, new_col
            return True
        return False

    def scramble(self, num_moves):
        """Scrambles the puzzle by performing random moves."""
        import random
        for _ in range(num_moves):
            self.perform_move(random.choice(["up", "down", "left", "right"]))

    def is_solved(self):
        """Checks if the puzzle is in its solved state."""
        start_tile = 1
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != start_tile:
                    return False
                start_tile += 1
        return True

    def copy(self):
        """Returns a deep copy of the current puzzle."""
        return copy.deepcopy(self)

    def find_neighbors(self):
        """Yields all valid (direction, new_puzzle) tuples for potential moves."""
        for direction in ("up", "down", "left", "right"):
            new_row, new_col = self.get_neighbor(direction)
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                new_puzzle = self.copy()
                new_puzzle.perform_move(direction)
                yield direction, new_puzzle

    def find_empty(self):
        """Finds the row and column of the empty tile."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 0:
                    return row, col

    def get_neighbor(self, direction):
        """Calculates the row and column of the neighbor in the given direction."""
        row, col = self.empty_row, self.empty_col
        if direction == "up":
            row -= 1
        elif direction == "down":
            row += 1
        elif direction == "left":
            col -= 1
        elif direction == "right":
            col += 1
        return row, col

    def manhattan_distance(self, tile, goal_row, goal_col):
        """Calculates the Manhattan distance between a tile and its goal position."""
        return abs(tile[0] - goal_row) + abs(tile[1] - goal_col)

    def find_solutions_iddfs(self):
        """Yields all optimal solutions using iterative deepening depth-first search."""
        for limit in range(1, self.rows * self.cols):
            for solution in self.iddfs_helper(limit):
                yield solution


# board = [[4, 1, 3], [2, 0, 5], [7, 8, 6]] 