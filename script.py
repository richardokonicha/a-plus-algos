import random 
from queue import PriorityQueue
import math
import copy

def create_tile_puzzle(rows, cols):
    board = []
    num = 1
    for r in range(rows):
        newRow = []
        for c in range(cols):
            if (num == rows * cols):
                num = 0
            newRow.append(num)
            num += 1
        board.append(newRow)
    return TilePuzzle(board)

class TilePuzzle(object):

    def __init__(self, board):
        self.board = board
        self.nrows = len(board)
        self.ncols = len(board[0])
        self.emptyTileLoc = self.returnZero(self.board)
        self.solution = self.solutionBoard()
        self.h = 0  # heuristic
        self.f = 0  # evaluation function f = g + h
        self.g = 0  # path cost
        self.path = []
    
    def solutionBoard(self):
        board = []
        num = 1
        for r in range(self.nrows):
            newRow = []
            for c in range(self.ncols):
                if (num == self.nrows * self.ncols):
                    num = 0
                newRow.append(num)
                num += 1
            board.append(newRow)
        return board

    """returns the row, col of the emptyTile"""
    def returnZero(self, board):
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] == 0:
                    return [r, c]

    def get_board(self):
        #print("number of rows " + str(self.nrows))
        #print("number of cols " + str(self.ncols))
        #print("empty tile " + str(self.emptyTileLoc))
        return self.board

    def perform_move(self, direction):
        self.emptyTileLoc = self.returnZero(self.board)
        if(direction == "up"):  # go up a row, same col
            if(self.emptyTileLoc[0] - 1 >= 0):
                swapVal = self.board[self.emptyTileLoc[0] - 1][self.emptyTileLoc[1]]
                self.board[self.emptyTileLoc[0] - 1][self.emptyTileLoc[1]] = 0
                self.board[self.emptyTileLoc[0]][self.emptyTileLoc[1]] = swapVal
                self.emptyTileLoc = self.returnZero(self.board)  #relocate empty Tile
                return True
        if(direction == "down"):  # go down a row, same col
            if(self.emptyTileLoc[0] + 1 < self.nrows):
                swapVal = self.board[self.emptyTileLoc[0] + 1][self.emptyTileLoc[1]]
                self.board[self.emptyTileLoc[0] + 1][self.emptyTileLoc[1]] = 0
                self.board[self.emptyTileLoc[0]][self.emptyTileLoc[1]] = swapVal
                self.emptyTileLoc = self.returnZero(self.board)  #relocate empty Tile
                return True
        if(direction == "left"):  # go left a col, same row
            if(self.emptyTileLoc[1] - 1 >= 0):
                swapVal = self.board[self.emptyTileLoc[0]][self.emptyTileLoc[1] - 1]
                self.board[self.emptyTileLoc[0]][self.emptyTileLoc[1] - 1] = 0
                self.board[self.emptyTileLoc[0]][self.emptyTileLoc[1]] = swapVal
                self.emptyTileLoc = self.returnZero(self.board)  #relocate empty Tile
                return True
        if(direction == "right"):  # go right a col, same row
            if(self.emptyTileLoc[1] + 1 < self.ncols):
                swapVal = self.board[self.emptyTileLoc[0]][self.emptyTileLoc[1] + 1]
                self.board[self.emptyTileLoc[0]][self.emptyTileLoc[1] + 1] = 0
                self.board[self.emptyTileLoc[0]][self.emptyTileLoc[1]] = swapVal
                self.emptyTileLoc = self.returnZero(self.board)  #relocate empty Tile
                return True
        return False

    def scramble(self, num_moves):
        moves = ["up", "down", "left", "right"]
        for n in range(num_moves):
            self.perform_move(random.choice(moves))

    def is_solved(self):
        sample = create_tile_puzzle(self.nrows, self.ncols)
        for r in range(self.nrows):
            for c in range(self.ncols):
                if self.board[r][c] != sample.board[r][c]:
                    return False
        return True

    def copy(self):
        copy = []
        for r in range(self.nrows):
            currentRow = []
            for c in range(self.ncols):
                currentRow.append(self.board[r][c])
            copy.append(currentRow)
        return TilePuzzle(copy)

    def successors(self):
        moves = ["up", "down", "left", "right"]
        successors = []
        for m in moves:
            copy = self.copy()
            if(copy.perform_move(m) == True):
                successors.append((m, copy))
        return successors

    def find_solutions_iddfs(self):
        found_sol = False
        limit = 0
        while not found_sol:
            for move in self.iddfs_helper(limit, []):
                yield move
                found_sol = True
            limit += 1

    def iddfs_helper(self, limit, moves):
        if self.board == self.solution:
            yield moves
        elif len(moves) < limit:
            for move, config in self.successors():
                for sol in config.iddfs_helper(limit, moves + [move]):
                    yield sol

    def find_solution_a_star(self):
        incomplete = set()  # set of unsolved board configs to evaluate #priortyque
        finished = set() # map cost so far
        incomplete.add(self)
        self.h = self.manhattan(self.solution)
        self.path = []
        cost_so_far = {}

        while incomplete: #while pq is not empty
            # find the board with the least f value
            # projected closest to solution
            current = min(incomplete, key=lambda b: b.f)
            
            if current.board == self.solution:
                return current.path  # this is optimal solution
            incomplete.remove(current) # remove from tbd list

            for move, puzzle in current.successors():
                if puzzle.board == self.solution:
                    puzzle.path = current.path + [move]
                    return puzzle.path

                # update heuristic values
                puzzle.g = current.g + current.manhattan(puzzle.board)
                # g is the updated path cost to a particular successor
                puzzle.h = puzzle.manhattan(self.solution)
                # h is the successor's remaining cost to the solution
                puzzle.f = puzzle.g + puzzle.h

                proceed = True
                for config in incomplete:
                    if config.board == puzzle.board and config.f < puzzle.f:
                        proceed = False
                        #continue
                for config in finished:
                    if config.board == puzzle.board and config.f < puzzle.f:
                        proceed = False
                        #continue
                if proceed:
                    incomplete.add(puzzle)
                    puzzle.path = current.path + [move]

            finished.add(current)

    # finds manhattan distance between current board to target config
    def manhattan(self, target):
        distance = 0
        correctCoord = {}
        # put correct coordinates for each tile in a dictionary
        for r in range(self.nrows):
            for c in range(self.ncols):
                correctCoord[target[r][c]] = (r,c)

        for r in range(self.nrows):
            for c in range(self.ncols):
                tileValue = self.board[r][c]
                correct = correctCoord[tileValue]
                distance += abs(r - correct[0]) + abs(c - correct[1])
        return distance


print("create_tile_puzzle")
p = create_tile_puzzle(3,3)
print("perform_move")
print(p.perform_move("up"))
print(p.get_board())
p = create_tile_puzzle(3,3)
print(p.perform_move("down"))
print(p.get_board())
p = create_tile_puzzle(3,3)
print(p.perform_move("left"))
print(p.get_board())
p = create_tile_puzzle(3,3)
print(p.perform_move("right"))
print(p.get_board())
p = create_tile_puzzle(2, 4)
print(p.get_board())
print("get_board")
p = TilePuzzle([[1, 2], [3, 0]])
print(p.get_board())
p = TilePuzzle([[0, 1], [3, 2]])
print(p.get_board())
print("scramble")
p = create_tile_puzzle(3,3)
p.scramble(3)
print(p.get_board())
print("is_solved")
p = TilePuzzle([[1, 2], [3, 0]])
print(p.is_solved())
p = TilePuzzle([[0, 1], [3, 2]])
print(p.is_solved())
print("copy")
p = create_tile_puzzle(3,3)
p2 = p.copy()
print(p.get_board() == p2.get_board())
p = create_tile_puzzle(3,3)
p2 = p.copy()
p.perform_move("left")
print(p.get_board() == p2.get_board())
print("successors")
p = create_tile_puzzle(3,3)
for move, new_p in p.successors():
    print(move, new_p.get_board())
b = [[1,2,3], [4,0,5], [6,7,8]]
p = TilePuzzle(b)
for move, new_p in p.successors():
    print(move, new_p.get_board())

print("find_solutions_iddfs")
b = [[4,1,2], [0,5,3], [7,8,6]]
p = TilePuzzle(b)
solutions = p.find_solutions_iddfs()
print(next(solutions))
b = [[1,2,3], [4,0,8], [7,6,5]]
p = TilePuzzle(b)
solutions = p.find_solutions_iddfs()
print(list(p.find_solutions_iddfs()))

print("find_solution_a_star")
b = [[4,1,2], [0,5,3], [7,8,6]]
p = TilePuzzle(b)
print(p.find_solution_a_star())
b =  [[1,2,3], [4,0,5], [6,7,8]]
p = TilePuzzle(b)
print(p.find_solution_a_star())

class GridNavigation(object):

    def __init__(self, loc):
        self.coord = loc
        self.g = 0
        self.h = 0
        self.f = 0
        self.path = []

    def successors(self, scene):
        x, y = self.coord
        r = len(scene) - 1
        c = len(scene[0]) - 1
        if x > 0:
            if not scene[x - 1][y]:
                yield GridNavigation((x - 1, y))  # up
        if y > 0:
            if not scene[x][y - 1]:
                yield GridNavigation((x, y - 1))  # left
        if x < r:
            if not scene[x + 1][y]:
                yield GridNavigation((x + 1, y))  # down
        if y < c:
            if not scene[x][y + 1]:
                yield GridNavigation((x, y + 1))  # right
        if x < r and y < c:
            if not scene[x + 1][y + 1]:
                yield GridNavigation((x + 1, y + 1))  # down-right
        if x < r and y > 0:
            if not scene[x + 1][y - 1]:
                yield GridNavigation((x + 1, y - 1))  # down-left
        if x > 0 and y < c:
            if not scene[x - 1][y + 1]:
                yield GridNavigation((x - 1, y + 1))  # up-right
        if x > 0 and y > 0:
            if not scene[x - 1][y - 1]:
                yield GridNavigation((x - 1, y - 1))  # up-left

    def euclidean(self, b):
        x1, y1 = self.coord
        x2, y2 = b
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def find_path(start, goal, scene):
    incomplete = set()
    finished = set()
    a = GridNavigation(start)
    incomplete.add(a)
    a.h = a.euclidean(goal)
    a.path = [start]

    while incomplete:
        current = min(incomplete, key=lambda p: p.f)

        if current.coord == goal:
            return current.path
        incomplete.remove(current)

        for point in current.successors(scene):
            if point.coord == goal:
                point.path = current.path + [point.coord]
                return point.path

            point.g = current.g + current.euclidean(point.coord)
            point.h = point.euclidean(goal)
            point.f = point.g + point.h

            proceed = True
            for loc in incomplete:
                if loc.coord == point.coord and loc.f < point.f:
                    proceed = False
            for loc in finished:
                if loc.coord == point.coord and loc.f < point.f:
                    proceed = False
            if proceed:
                incomplete.add(point)
                point.path = current.path + [point.coord]

        finished.add(current)

print("\nfind_path")
scene = [[False, False, False], [False, True , False], [False, False, False]]
print(find_path((0, 0), (2, 1), scene))
scene = [[False, True, False], [False, True, False], [False, True, False]]
print(find_path((0, 0), (0, 2), scene))

class LinearDiskMovement(object):

    def __init__(self, n, length, disks):
        self.n = n
        self.len = length
        self.disks = list(disks)
        self.g = 0
        self.h = 0
        self.f = 0
        self.path = []

    def successors(self):
        for i in range(len(self.disks)):
            if self.disks[i]:
                if i + 1 < self.len:
                    if self.disks[i + 1] == 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i + 1] = disk
                        yield ((i, i + 1), LinearDiskMovement(self.n, self.len, replace))

                if i + 2 < self.len:
                    if self.disks[i + 2] == 0 and self.disks[i + 1] != 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i + 2] = disk
                        yield ((i, i + 2), LinearDiskMovement(self.n, self.len, replace))

                if i - 1 >= 0:
                    if self.disks[i - 1] == 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i - 1] = disk
                        yield ((i, i - 1), LinearDiskMovement(self.n, self.len, replace))

                if i - 2 >= 0:
                    if self.disks[i - 2] == 0 and self.disks[i - 1] != 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i - 2] = disk
                        yield ((i, i - 2), LinearDiskMovement(self.n, self.len, replace))

    def heuristic(self, b):
        coord = {}
        for i, x in enumerate(b):
            coord[x] = i

        total = 0
        for i, x in enumerate(self.disks):
            total += abs(i - coord[x])

        return total


def solve_distinct_disks(length, n):
    start = [x + 1 for x in range(n)]
    for x in range(length - n):
        start.append(0)
    goal = list(reversed(copy.deepcopy(start)))

    if start == goal:
        return [()]

    incomplete = set()
    a = LinearDiskMovement(n, length, start)
    incomplete.add(a)

    finished = set()
    a.h = a.heuristic(goal)

    while incomplete:
        current = min(incomplete, key=lambda ldm: ldm.f)

        if current.disks == goal:
            return current.path
        incomplete.remove(current)

        for move, disk in current.successors():
            if disk.disks == goal:
                disk.path = current.path + [move]
                return disk.path

            disk.g = current.g + current.heuristic(disk.disks)
            disk.h = disk.heuristic(goal)
            disk.f = disk.g + disk.h

            proceed = True
            for loc in incomplete:
                if loc.disks == disk.disks and loc.f < disk.f:
                    proceed = False
                    continue
            for loc in finished:
                if loc.disks == disk.disks and loc.f < disk.f:
                    proceed = False
                    continue
            if proceed:
                incomplete.add(disk)
                disk.path = current.path + [move]

        finished.add(current)

print("\nlinear_disk")
print(solve_distinct_disks(4,2))
print(solve_distinct_disks(5,2))
print(solve_distinct_disks(4,3))
print(solve_distinct_disks(5,3))