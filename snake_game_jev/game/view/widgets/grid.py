import pygame

from game.view import primitives as draw


class Grid:
    def paint(self, screen, fonts, layout, board):
        ox, oy = layout.grid_origin
        cell = layout.cell
        draw.soft_rect(screen, layout.frame, (8, 10, 16, 255), (255, 255, 255, 28), 18, 1)
        for r in range(board.rows + 1):
            y = oy + r * cell
            pygame.draw.aaline(screen, (42, 46, 60), (ox, y), (ox + board.cols * cell, y))
        for c in range(board.cols + 1):
            x = ox + c * cell
            pygame.draw.aaline(screen, (42, 46, 60), (x, oy), (x, oy + board.rows * cell))
        for r in range(board.rows):
            for c in range(board.cols):
                label = draw.text(fonts["tiny"], board.cell(c, r), (158, 166, 184), 145)
                screen.blit(label, (ox + c * cell + 4, oy + r * cell + 3))
