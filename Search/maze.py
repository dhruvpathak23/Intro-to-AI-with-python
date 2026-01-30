# to implement something like DFS or BFS in the context of solving a maze.
import sys


class Node():
    def __init__(self, state, parent, action):
        self.state = state 
        self.parent = parent
        self.action = action 

# to represent a frontier using stack data structure using DFS.
class StackFrontier():

    # intially creates a frontier that i'm going to represent using a list.
    # intially creates an empty list.
    def __init__(self):
        self.frontier = []
    
    # to add something in the list as by appending it to end of the list. 
    def add(self, node):
        self.frontier.append(node)
 
    # to check if the frontier contains a paricular state.
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
 
    # to check if the frontier is empty or not.
    def empty(self):
        return len(self.frontier) == 0 

    # to remove a node from the frontier.
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node   
   
# to represent a frontier using queue data structure using BFS.
class QueueFrontier(StackFrontier):

    #to remove a node from the frontier.
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node 

# to handle the process of taking sequence, a maze like text file, 
# and figuring out how to sove it.
class maze():

    def __init__(self, filename):  

        #Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()    
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
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

    # to print a representation of the maze.
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    # to return the neighbors of a particular state.
    def neighbors(self, state): 
        row, col = state

        # all possible actions.
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        # ensure actions are valid.
        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result     

    # how to actually get from point A to point B.
    def solve(self):
        """Finds a solution to maze, if one exists."""

        #keep track of number of states explored.
        self.num_explored = 0

        #Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)

        # Use either StackFrontier(DFS) or QueueFrontier(BFS).
        frontier = StackFrontier()
        frontier.add(start)

        #Initialize an empty explored set
        self.explored = set()

        #Keep looping until solution found
        while True:

            #If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            #Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            #If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []

                #Follow parent nodes to find solutions.
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            #Mark node as explored
            self.explored.add(node.state)

            #Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
# Pillow library is used to create and save images (PNG here)
from PIL import Image, ImageDraw


# This function converts the solved maze into a PNG image
def save_maze_png(maze, filename="solution.png", cell_size=40):
    """
    maze      : maze object after calling solve()
    filename  : name of the output PNG file
    cell_size : size (in pixels) of each maze cell
    """

    # Maze dimensions
    height = maze.height
    width = maze.width

    # Create a blank white image
    img = Image.new(
        "RGB",
        (width * cell_size, height * cell_size),
        "white"
    )

    # Object used to draw shapes on the image
    draw = ImageDraw.Draw(img)

    # Convert solution path to a set for fast lookup
    solution_cells = set(maze.solution[1]) if maze.solution else set()

    # Iterate over every cell in the maze
    for i in range(height):
        for j in range(width):

            # Calculate pixel boundaries of the cell
            x0 = j * cell_size
            y0 = i * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            # Decide cell color
            if maze.walls[i][j]:
                color = (0, 0, 0)          # Black → Wall
            elif (i, j) == maze.start:
                color = (0, 255, 0)        # Green → Start (A)
            elif (i, j) == maze.goal:
                color = (255, 0, 0)        # Red → Goal (B)
            elif (i, j) in solution_cells:
                color = (0, 0, 255)        # Blue → Solution path
            else:
                color = (255, 255, 255)    # White → Free space

            # Draw the cell rectangle
            draw.rectangle(
                [x0, y0, x1, y1],
                fill=color,
                outline=(200, 200, 200)
            )

    # Save the final image to disk
    img.save(filename)


# Entry point of the program
if __name__ == "__main__":

    # Ensure maze file is provided
    if len(sys.argv) != 2:
        sys.exit("Usage: python maze.py maze.txt")

    # Load maze from text file
    m = maze(sys.argv[1])

    # WORKAROUND:
    # StackFrontier has a typo (__int__ instead of __init__)
    # We initialize the internal list manually WITHOUT changing original code
    frontier_test = StackFrontier()
    frontier_test.frontier = []

    # Solve the maze using DFS (StackFrontier)
    m.solve()

    # Print maze with solution to terminal
    m.print()

    # Save maze solution as PNG image
    save_maze_png(m, "solution.png")

                    