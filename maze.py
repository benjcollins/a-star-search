import random
import pygame
import math

square_size = 15
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

def draw_cell(window, coord, color):
    pygame.draw.rect(window, color, (coord.x * square_size, coord.y * square_size, square_size, square_size))

class Grid:

    def __init__(self, dims, window):
        self.window = window
        self.dims = dims//2*2
        self.grid = [[black for _ in range(dims.y)] for _ in range(dims.x)]

    def get_cell(self, coord):
        return self.grid[coord.x][coord.y]

    def set_cell(self, coord, color):
        self.grid[coord.x][coord.y] = color
        draw_cell(self.window, coord, color)

    def __iter__(self):
        cells = []
        for x in range(self.dims.x):
            for y in range(self.dims.y):
                coord = Vec2(x, y)
                cells.append((coord, self.get_cell(coord)))
        return iter(cells)

class MazeGenerator:

    def __init__(self, grid):
        self.grid = grid
        self.cells = [Vec2(0, 0)]

    def finished(self):
        return len(self.cells) == 0

    def current_cell(self):
        return self.cells[-1]

    def get_unvisited(self):
        unvisited = []
        current = self.current_cell()
        for direction in [Vec2(2, 0), Vec2(0, 2), Vec2(-2, 0), Vec2(0, -2)]:
            if current + direction < self.grid.dims and current + direction >= Vec2(0, 0):
                if self.grid.get_cell(current + direction) == black:
                    unvisited.append(direction)
        return unvisited

    def step(self):
        if not self.finished():
            current = self.current_cell()
            self.grid.set_cell(current, white)

            unvisited = self.get_unvisited()
            if len(unvisited) > 0:
                direction = random.choice(unvisited)
                self.grid.set_cell(current+direction//2, white)
                self.cells.append(current+direction)
            else:
                self.cells.pop()

class Vec2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __div__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __floordiv__(self, other):
        return Vec2(self.x // other, self.y // other)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Initial:

    def __init__(self):
        self.gcost = 0

    def is_start(self):
        return True

class CellData:

    def __init__(self, coord, end, parent):
        self.parent = parent
        self.coord = coord
        self.gcost = parent.gcost + 1
        self.hcost = coord.dist(end)
        self.fcost = self.gcost + self.hcost

    def is_start(self):
        return False

class AStar:

    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.current = CellData(start, end, Initial())
        self.open = []
        self.solution = None

    def finished(self):
        return self.current.coord == self.end

    def get_cells(self):
        for direction in [Vec2(1, 0), Vec2(0, 1), Vec2(-1, 0), Vec2(0, -1)]:
            test = self.current.coord + direction
            if test >= self.grid.dims and test < Vec2(0, 0):
                continue
            if not self.grid.get_cell(test) in [white, green]:
                continue
            self.grid.set_cell(test, green)
            self.open.append(CellData(test, self.end, self.current))

    def step(self):
        if self.finished():
            if self.solution == None:
                self.solution = self.current
            else:
                if not self.solution.parent.is_start():
                    self.solution = self.solution.parent
                
            self.grid.set_cell(self.solution.coord, blue)
        else:
            if len(self.open) > 0:
                lowest = self.open[0]
                for open_cell in self.open[1:]:
                    if open_cell.fcost <= lowest.fcost:
                        if open_cell.hcost < lowest.hcost:
                            lowest = open_cell
                self.current = lowest
                self.open.remove(lowest)
                self.grid.set_cell(lowest.coord, red)

            self.get_cells()

def main():
    pygame.init()
    dims = Vec2(30, 20)
    window = pygame.display.set_mode((dims.x * square_size, dims.y * square_size))
    grid = Grid(dims, window)
    pygame.display.set_caption("Maze")
    maze_generator = MazeGenerator(grid)
    astar = AStar(grid, Vec2(0, 0), grid.dims - Vec2(2, 2))
    running = True
    clock = pygame.time.Clock()

    while running:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    astar.step()

        if not maze_generator.finished():
            maze_generator.step()

        if maze_generator.finished():
            astar.step()

        if not maze_generator.finished():
            draw_cell(window, maze_generator.current_cell(), red)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

main()