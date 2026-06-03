import random,time
from operator import add
import pygame


class TerminalViewer:
    def __init__(self, maze):
        self.maze = maze

    def draw(self):
        print("\033[H\033[J", end="")

        for row in self.maze.maze:
            for cell in row:
                if cell == 1:
                    print("██", end="")
                else:
                    print("  ", end="")
            print()
        time.sleep(.05)


class GuiViewer:
    def __init__(self, maze, cell_size=10):
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

                color = (255, 255, 255)

                if self.maze.maze[row][col] == 1:
                    color = (0, 0, 0)

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
        pygame.time.delay(10)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

class Maze:
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.neighbour = [(0,2),(2,0),(0,-2),(-2,0)]
        self.maze = [[0 for _ in range(col)] for _ in range(row)]
        self.visit_status = [[False for _ in range(col)] for _ in range(row)]
        self.generate_empty_maze()

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
    def clear_path(self,a,b):
        r1,c1 = a
        r2,c2 = b
        if r1 == r2:
            start = min(c1,c2)
            end = max(c1,c2)
            for c in range(start,end+1):
                self.maze[r1][c] = 0
        elif c1 == c2:
            start = min(r1,r2)
            end = max(r1,r2)
            for r in range(start,end+1):
                self.maze[r][c1] = 0


class Backtracking(Maze):
    def __init__(self,row,col):
        super().__init__(row,col)
        self.viewer = GuiViewer(self)
    def generate_maze(self):
        self.stack = []
        cell = (1,1)
        self.mark_visited(cell)
        self.stack.append(cell)
        while self.stack:
            curr = self.stack[-1]
            neigh = []
            for val in self.neighbour:
                c = (curr[0] + val[0], curr[1] + val[1])
                if  not self.is_visited(c) and 0 <= c[0] < self.row and 0<= c[1] < self.col: 
                    neigh.append(c)
            if not neigh:
                self.stack.pop(-1)
                continue
            nxt = random.choice(neigh)
            self.clear_path(curr,nxt)
            self.viewer.draw()
            self.mark_visited(nxt)
            self.stack.append(nxt)

def main():
    maze = Backtracking(35,75)
    maze.generate_maze()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        maze.viewer.draw()
    pygame.quit()

if __name__ == "__main__":
    main()
