from vector import Vec2
import colors
from draw import draw_cell

class Grid:

    def __init__(self, dims, window):
        self.window = window
        self.dims = dims//2*2
        self.grid = [[colors.black for _ in range(dims.y)] for _ in range(dims.x)]

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