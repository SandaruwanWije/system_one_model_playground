import pygame

from game.core.config import CELL


class Layout:
    """Computes where every UI piece sits on screen."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell = CELL
        self.shell = pygame.Rect(32, 20, width - 64, height - 40)
        self.frame = pygame.Rect(0, 0, 0, 0)
        self.grid_origin = (0, 0)
        self.jev = (width / 2, 0)
        self.jev_radius = 32
        self.pads = {}
        self.mode_btns = {}
        self.pause_btn = pygame.Rect(0, 0, 0, 0)

    def place_board(self, board_top, cols, rows):
        ox = self.shell.x + (self.shell.w - cols * self.cell) / 2
        oy = board_top + 6
        self.grid_origin = (ox, oy)
        self.frame = pygame.Rect(
            ox - 14, oy - 14, cols * self.cell + 28, rows * self.cell + 28
        )
        jx = self.width / 2
        jy = oy + rows * self.cell + 78
        self.jev = (jx, jy)
        self._place_pads(jx, jy + self.jev_radius * 2.35 + 44)

    def cell_center(self, c, r):
        ox, oy = self.grid_origin
        return ox + c * self.cell + self.cell / 2, oy + r * self.cell + self.cell / 2

    def _place_pads(self, jx, top):
        size, gap = 78, 20
        self.pads = {
            "up": pygame.Rect(jx - size / 2, top, size, size),
            "left": pygame.Rect(jx - size * 1.5 - gap, top + size + gap, size, size),
            "right": pygame.Rect(jx + size / 2 + gap, top + size + gap, size, size),
            "down": pygame.Rect(jx - size / 2, top + (size + gap) * 2, size, size),
        }

    def hit(self, pos, buttons):
        for name, box in buttons.items():
            if box.collidepoint(pos):
                return name
        return None
