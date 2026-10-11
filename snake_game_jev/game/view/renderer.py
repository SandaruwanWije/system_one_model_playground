import math
import time

import pygame

from game.core.config import AMBER, BLUE, INK, PANEL, WINDOW
from game.view import primitives as draw
from game.view.layout import Layout
from game.view.sprites import apple, routes, snake
from game.view.widgets import Disc, Grid, Pads, PauseOverlay, TopBar


class Renderer:
    def __init__(self):
        self.width, self.height = WINDOW
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED)
        pygame.display.set_caption("JEV Snake")
        self.fonts = {
            "font": pygame.font.SysFont("segoeui", 15),
            "big": pygame.font.SysFont("segoeui", 20, bold=True),
            "tiny": pygame.font.SysFont("segoeui", 13),
        }
        self.layout = Layout(self.width, self.height)
        self.top_bar = TopBar()
        self.grid = Grid()
        self.pads = Pads()
        self.disc = Disc()
        self.overlay = PauseOverlay()
        self.pulse = 0.0

    def draw(self, session):
        self.pulse = math.sin(time.time() * 2.2) * 0.5 + 0.5
        self._backdrop()
        draw.soft_rect(self.screen, self.layout.shell, (*PANEL, 245), (255, 255, 255, 36), 30, 1)
        board_top = self.top_bar.paint(self.screen, self.fonts, self.layout, session)
        self.layout.place_board(board_top, session.board.cols, session.board.rows)
        self.grid.paint(self.screen, self.fonts, self.layout, session.board)

        food = self.layout.cell_center(*session.board.food)
        apple.paint(self.screen, food, self.layout.cell, self.pulse)
        snake.paint(
            self.screen,
            session.from_snake,
            session.pick,
            session.clock.along,
            self.layout.cell,
            self.layout.cell_center,
            self.pulse,
        )
        routes.paint(
            self.screen,
            self.layout.frame,
            self.layout.jev,
            self.layout.jev_radius,
            self.layout.pads,
            session.pick,
            session.heat,
        )
        self.disc.paint(
            self.screen,
            self.fonts,
            self.layout.jev,
            self.layout.jev_radius,
            session.mode,
            session.busy,
            session.jev.latency_ms,
            session.mode_fade,
            self.pulse,
        )
        self.pads.paint(self.screen, self.fonts, self.layout, session)
        if session.clock.paused:
            self.overlay.paint(self.screen, self.fonts, self.width, self.height)
        pygame.display.flip()

    def _backdrop(self):
        self.screen.fill(INK)
        draw.blit_center(self.screen, draw.glow(240, BLUE, 0.11 + 0.04 * self.pulse), (self.width * 0.5, self.height * 0.26))
        draw.blit_center(self.screen, draw.glow(170, AMBER, 0.05), (self.width * 0.78, self.height * 0.16))
        self.screen.blit(draw.vignette((self.width, self.height), INK, 0.64), (0, 0))
