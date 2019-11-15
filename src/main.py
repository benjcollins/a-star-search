import random
import pygame
import math
import colors
from draw import draw_cell, square_size
from vector import Vec2
from astar import AStar
from grid import Grid
from maze_generator import MazeGenerator

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
            draw_cell(window, maze_generator.current_cell(), colors.red)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

main()