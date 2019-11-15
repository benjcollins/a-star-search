from vector import Vec2
import colors
import random
from draw import draw_cell

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
                if self.grid.get_cell(current + direction) == colors.black:
                    unvisited.append(direction)
        return unvisited

    def step(self):
        if not self.finished():
            current = self.current_cell()
            self.grid.set_cell(current, colors.white)

            unvisited = self.get_unvisited()
            if len(unvisited) > 0:
                direction = random.choice(unvisited)
                self.grid.set_cell(current+direction//2, colors.white)
                self.cells.append(current+direction)
            else:
                self.cells.pop()