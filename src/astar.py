from vector import Vec2
import colors

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
            if not self.grid.get_cell(test) in [colors.white, colors.green]:
                continue
            self.grid.set_cell(test, colors.green)
            self.open.append(CellData(test, self.end, self.current))

    def step(self):
        if self.finished():
            if self.solution == None:
                self.solution = self.current
            else:
                if not self.solution.parent.is_start():
                    self.solution = self.solution.parent
                
            self.grid.set_cell(self.solution.coord, colors.blue)
        else:
            if len(self.open) > 0:
                lowest = self.open[0]
                for open_cell in self.open[1:]:
                    if open_cell.fcost <= lowest.fcost:
                        if open_cell.hcost < lowest.hcost:
                            lowest = open_cell
                self.current = lowest
                self.open.remove(lowest)
                self.grid.set_cell(lowest.coord, colors.red)

            self.get_cells()