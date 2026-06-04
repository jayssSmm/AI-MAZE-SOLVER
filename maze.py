import argparse
import random
import heapq

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class stackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)
    
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)   

    def is_empty(self):
        return len(self.frontier) == 0 
    
    def remove(self):
        if self.is_empty():
            raise Exception("empty frontier")
        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return node
    
class QueueFrontier(stackFrontier):
    def remove(self):
        if self.is_empty():
            raise Exception("empty frontier")
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return  node
    
class HeuristicFrontier(stackFrontier):
    def __init__(self, goal):
        self.goal = goal
        self.frontier = []

    def heuristic(self, state):
        goal_x, goal_y = self.goal
        x, y = state

        return abs(x - goal_x) + abs(y - goal_y)

    def add(self, node):
        heapq.heappush(self.frontier, (self.heuristic(node.state)))

    def remove(self):
        return heapq.heappop(self.frontier)
    
    def contains_state(self, state):
        return any(node.state == state for _, node in self.frontier)
    
class Maze():

    def __init__(self, filename):
        
        with open(filename) as f:
            contents = f.read()
        
        if contents.count("A") != 1:
            raise Exception("maze must have exact 1 start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exact 1 goal")
        
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == 'A':
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == 'B':
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)

            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end='')
                elif (i, j) == self.start:
                    print("A", end='')
                elif (i, j) == self.goal:
                    print("B", end='')
                elif solution is not None and (i, j) in solution:
                    print("*", end='')
                else:
                    print(" ", end='')
            print()

    def neighbors(self, state):
        row, col = state

        candidates = [
            ('left', (row, col-1)),
            ('right', (row, col+1)),
            ('up', (row+1, col)),
            ('down', (row-1, col)),
        ]

        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r,c)))
            except IndexError:
                continue
        return result
    
    def solve(self):
        self.num_explored = 0

        start = Node(state=self.start, parent=None, action=None)
        frontier = HeuristicFrontier(self.goal)
        frontier.add(start)

        self.explored = set()

        while True:
            if frontier.is_empty():
                raise Exception("no solution")
            
            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent 
                
                actions.reverse()
                cells.reverse()
                self.solution = actions, cells
                return
            
            self.explored.add(node.state)

            neighbors = self.neighbors(node.state)
            random.shuffle(neighbors)
            for action, state in neighbors:
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)       

    def output_image(self, filename = 'solved_maze1.png', show_explored=False):
        from PIL import Image, ImageDraw     

        img = Image.new("RGB", (self.width * 100, self.height * 100))

        wall = Image.new("RGB", (100, 100), '#282828')
        stop = Image.new("RGB", (100, 100), '#467846')
        visited = Image.new("RGB", (100, 100), '#8C4646')
        start = Image.new("RGB", (100, 100), '#DC3C3C')
        path = Image.new("RGB", (100, 100), '#D2D2D2')
        solution = Image.new("RGB", (100, 100), '#DCBE3C')
        square_size = 100

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row): 
                if col:
                    square = wall
                elif (i, j) == self.start:
                    square = start
                elif (i, j) == self.goal:
                    square = stop
                elif (i, j) in self.solution[1]:
                    square = solution
                elif show_explored and (i, j) in self.explored:
                    square = visited
                else:
                    square = path
        
                draw = ImageDraw.Draw(square)

                draw.rectangle(
                    [(0, 0), (99, 99)],
                    outline="white",
                    width=1
                )

                x1 = j * square_size
                y1 = i * square_size

                img.paste(square, (x1, y1))

        img.save(filename)
        img.show()


if __name__=='__main__':

    print("program started")
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    maze = Maze(args.filename)

    print("Maze:")
    maze.print()
    
    maze.solve()

    print("\nstates explored : ", maze.num_explored)

    print("\nSolution:")
    maze.print()

    maze.output_image(show_explored=False)