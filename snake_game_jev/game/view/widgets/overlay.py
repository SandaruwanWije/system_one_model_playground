import pygame

from game.core.config import BLUE, WHITE
from game.view import primitives as draw


class PauseOverlay:
    def paint(self, screen, fonts, width, height):
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((8, 10, 16, 120))
        screen.blit(overlay, (0, 0))
        label = draw.text(fonts["big"], "Paused", WHITE)
        hint = draw.text(fonts["tiny"], "click Resume or press Space", BLUE)
        screen.blit(label, label.get_rect(center=(width / 2, height / 2 - 10)))
        screen.blit(hint, hint.get_rect(center=(width / 2, height / 2 + 16)))
