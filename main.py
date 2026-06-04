import random,time,heapq
from operator import add
from collections import deque
import pygame

ROW = 33
COL = 33
CELL_SIZE = 7
ALGO = "prim"
PATH_COLOR = "green"
VISITED_COLOR = "grey"
FOUND_COLOR = "red"
WALL_COLOR = "black"

class TerminalViewer:
    def __init__(self, maze):
        self.maze = maze

    def draw(self):
        print("\033[H\033[J", end="")

        for row in self.maze.maze:
            for cell in row:
                if cell == 1:
                    print("\033[31m██", end="")
                elif cell == "v":
                    print("\033[33m██", end="")
                elif cell == "*":
                    print("\033[35m██", end="")
                else:
                    print("  ", end="")
            print()
        time.sleep(0.05)


class GuiViewer:
    def __init__(self, maze, cell_size=CELL_SIZE):
        self.maze = maze
        self.cell_size = cell_size

        pygame.init()

        self.screen = pygame.display.set_mode(
            (
                maze.col * cell_size,
                maze.row * cell_size
            )
        )

        pygame.display.set_caption("Maze Generator")

    def draw(self):
        for row in range(self.maze.row):
            for col in range(self.maze.col):

                color = pygame.Color(PATH_COLOR)

                if self.maze.maze[row][col] == 1:
                    color = pygame.Color(WALL_COLOR)
                elif self.maze.maze[row][col] == "*":
                    color = pygame.Color(FOUND_COLOR)
                elif self.maze.maze[row][col] == "v":
                    color = pygame.Color(VISITED_COLOR)

                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        col * self.cell_size,
                        row * self.cell_size,
                        self.cell_size,
                        self.cell_size
                    )
                )

        pygame.display.flip()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

class Maze:
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.entry = (0,1)
        self.exit = (self.row-1,self.col-2)
        self.neighbour = [(0,2),(2,0),(0,-2),(-2,0)]
        self.maze = [[0 for _ in range(col)] for _ in range(row)]
        self.visit_status = [[False for _ in range(col)] for _ in range(row)]
        self.generate_empty_maze()

    def create_entrance_and_exit(self):
        self.carve(self.entry)
        self.carve(self.exit)

    def generate_empty_maze(self):
        for i in range(self.row):
            for j in range(self.col):
                    self.maze[i][j] = 1
    def show(self):
        print("\033[H\033[2J", end="")
        for i in range(self.row):
            for j in range(self.col):
                 print(self.maze[i][j],end=" ")
            print()

    def is_border(self,i,j):
        if i == 0 or i == self.row-1 or j == self.col-1 or j == 0:
            return True
        return False
    def mark_visited(self,cell):
        self.visit_status[cell[0]][cell[1]] = not self.visit_status[cell[0]][cell[1]]
    def is_visited(self,cell):
        try:
            return self.visit_status[cell[0]][cell[1]]
        except:
            return False
    def carve(self,loc):
        x,y = loc
        self.maze[x][y] = 0
    def clear_path(self,a,b):
        r1,c1 = a
        r2,c2 = b
        if r1 == r2:
            start = min(c1,c2)
            end = max(c1,c2)
            for c in range(start,end+1):
                self.carve((r1,c))
        elif c1 == c2:
            start = min(r1,r2)
            end = max(r1,r2)
            for r in range(start,end+1):
                self.carve((r,c1))
    def is_carved(self,cell):
        x,y = cell
        return self.maze[x][y] == 0
    def find_neighbours(self,curr):
        neigh = []
        for val in self.neighbour:
            c = (curr[0] + val[0], curr[1] + val[1])
            if 0 <= c[0] < self.row and 0<= c[1] < self.col and not self.is_visited(c): 
                neigh.append(c)
        return neigh



class Backtracking(Maze):
    def __init__(self,row,col):
        super().__init__(row,col)
        self.viewer = TerminalViewer(self)
    def generate_maze(self):
        self.stack = []
        cell = (1,1)
        self.mark_visited(cell)
        self.stack.append(cell)
        while self.stack:
            curr = self.stack[-1]
            neigh = self.find_neighbours(curr)
            if not neigh:
                self.stack.pop(-1)
                continue
            nxt = random.choice(neigh)
            self.clear_path(curr,nxt)
            self.viewer.draw()
            self.mark_visited(nxt)
            self.stack.append(nxt)
        self.create_entrance_and_exit()
        self.viewer.draw()

class Prims(Maze):
    def __init__(self,row,col):
        super().__init__(row,col)
        self.viewer = TerminalViewer(self)
    def generate_maze(self):
        cell = (1,1)
        self.carve(cell)
        frontier = set(self.find_neighbours(cell))
        while frontier:
            cell = random.choice(list(frontier))
            frontier.remove(cell)
            neigh = self.find_neighbours(cell)
            carved = [c for c in neigh if self.is_carved(c)]
            if carved:
                parent = random.choice(carved)
                self.clear_path(cell, parent)
            for c in neigh:
                if not self.is_carved(c): 
                    frontier.add(c)
            self.viewer.draw()
        self.create_entrance_and_exit()
        self.viewer.draw()

# Path Finding Algos
class Path:
    def __init__(self,maze):
        self.maze = maze
    def dfs(self):
        maze = self.maze.maze
        start = self.maze.entry
        rows = self.maze.row
        cols = self.maze.col
        goal = self.maze.exit
        stack = [start]
        visited = {start}
        parent = {}
        directions = [
            (-1,0),
            (1,0),
            (0,-1),
            (0,1)
        ]

        while stack:
            row, col = stack.pop()
            self.maze.maze[row][col] = "v"
            self.maze.viewer.draw()
            #time.sleep(0.01)
            if (row, col) == goal:
                break

            for dr, dc in directions:

                nr = row + dr
                nc = col + dc

                if (
                    0 <= nr < rows and
                    0 <= nc < cols and
                    maze[nr][nc] == 0 and
                    (nr, nc) not in visited
                ):

                    visited.add((nr, nc))
                    parent[(nr, nc)] = (row, col)
                    stack.append((nr, nc))

        if goal not in visited:
            return None

        path = []
        node = goal

        while node != start:
            path.append(node)
            node = parent[node]

        path.append(start)

        return path[::-1]
    def bfs(self):
        maze = self.maze.maze
        start = self.maze.entry
        rows = self.maze.row
        cols = self.maze.col
        goal = self.maze.exit
        queue = deque([start])
        visited = {start}
        parent = {}
        directions = [
            (-1,0),
            (1,0),
            (0,-1),
            (0,1)
        ]

        while queue:
            row, col = queue.popleft()
            self.maze.maze[row][col] = "v"
            self.maze.viewer.draw()
            if (row, col) == goal:
                break

            for dr, dc in directions:

                nr = row + dr
                nc = col + dc

                if (
                    0 <= nr < rows and
                    0 <= nc < cols and
                    maze[nr][nc] == 0 and
                    (nr, nc) not in visited
                ):

                    visited.add((nr, nc))
                    parent[(nr, nc)] = (row, col)
                    queue.append((nr, nc))

        if goal not in visited:
            return None

        path = []
        node = goal

        while node != start:
            path.append(node)
            node = parent[node]

        path.append(start)

        return path[::-1]

    def astar(self):
        maze = self.maze.maze
        start = self.maze.entry
        rows = self.maze.row
        cols = self.maze.col
        goal = self.maze.exit

        # Priority queue: (f, g, node)
        open_set = []
        heapq.heappush(open_set, (0, 0, start))

        # Cost from start to node
        g_score = {start: 0}

        # Parent pointers
        came_from = {}

        # Visited nodes
        closed_set = set()

        while open_set:
            _, current_g, current = heapq.heappop(open_set)

            if current in closed_set:
                continue
            
            self.maze.maze[current[0]][current[1]] = "v"
            self.maze.viewer.draw()

            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]

                path.append(start)
                path.reverse()
                return path

            closed_set.add(current)

            x, y = current

            # 4-directional movement
            directions = [
                (-1, 0),  # up
                (1, 0),   # down
                (0, -1),  # left
                (0, 1)    # right
            ]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                # Check bounds
                if not (0 <= nx < rows and 0 <= ny < cols):
                    continue

                # Check wall
                if maze[nx][ny] == 1:
                    continue

                neighbor = (nx, ny)

                if neighbor in closed_set:
                    continue

                tentative_g = current_g + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g

                    h = self.heuristic(neighbor, goal)
                    f = tentative_g + h

                    came_from[neighbor] = current

                    heapq.heappush(
                        open_set,
                        (f, tentative_g, neighbor)
                    )

        return None

    def heuristic(self,start,end):
        a,b = start 
        c,d = end 
        return abs(a - c) + abs(b - d)



def main():
    match ALGO: 
        case "prim":
            maze = Prims(ROW,COL)
        case "backtrack":
            maze = Backtracking(ROW,COL)
        case _:
            maze = Backtracking(ROW,COL)
    maze.generate_maze()
    running = True
    clock = pygame.time.Clock()
    path = Path(maze)
    path = path.dfs()
    for x,y in path:
        maze.maze[x][y] = "*"
    maze.viewer.draw()
    #while running:
    #    for event in pygame.event.get():
    #        if event.type == pygame.QUIT:
    #            running = False
    #    clock.tick(60)
    #pygame.quit()

if __name__ == "__main__":
    main()
