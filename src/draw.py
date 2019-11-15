import pygame

square_size = 3

def draw_cell(window, coord, color):
    pygame.draw.rect(window, color, (coord.x * square_size, coord.y * square_size, square_size, square_size))