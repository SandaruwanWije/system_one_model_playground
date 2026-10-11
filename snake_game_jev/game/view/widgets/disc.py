import time

import pygame

from game.core.config import BLUE, SOFT, WHITE
from game.view import primitives as draw


class Disc:
    def paint(self, screen, fonts, layout, mode, busy, latency_ms, fade, pulse, raw_open=False):
        x, y = layout.jev
        radius = layout.jev_radius
        draw.blit_center(screen, draw.glow(radius * 2, BLUE, 0.48 + 0.18 * pulse), (x, y))
        spin = time.time()
        for rad, ang, sweep, alpha in (
            (radius * 1.22, spin, 1.3, 180),
            (radius * 1.42, -spin * 0.7, 0.95, 110),
        ):
            draw.blit_center(screen, draw.arc(int(rad), (*BLUE, alpha), ang, sweep, 2), (x, y))
        draw.blit_center(screen, draw.circle(radius, (16, 18, 24)), (x, y))
        draw.blit_center(screen, draw.ring(radius, (214, 226, 255, 220), 2), (x, y))

        title = draw.text(fonts["big"], "JEV" if mode == "jev" else "YOU", WHITE, int(255 * fade))
        screen.blit(title, title.get_rect(center=(x, y - 8)))
        tip = ("…" if busy else f"{latency_ms:.0f} ms") if mode == "jev" else "arrows · WASD"
        sub = draw.text(fonts["tiny"], tip, BLUE, int(255 * fade))
        screen.blit(sub, sub.get_rect(center=(x, y + 11)))

        layout.expand_btn = pygame.Rect(0, 0, 0, 0)
        if mode == "jev" and not raw_open:
            self._expand_button(screen, fonts, layout, x, y, radius)

    def _expand_button(self, screen, fonts, layout, x, y, radius):
        words = draw.text(fonts["tiny"], "Raw view", WHITE)
        height = 34
        box = pygame.Rect(0, 0, 10 + 16 + 8 + words.get_width() + 14, height)
        box.midleft = (int(x + radius * 1.42 + 12), int(y))
        layout.expand_btn = box.inflate(8, 8)

        hover = layout.expand_btn.collidepoint(pygame.mouse.get_pos())
        draw.blit_center(screen, draw.glow(height, BLUE, 0.5 if hover else 0.28), box.center)
        fill = (140, 180, 255, 72 if hover else 40)
        border = (214, 226, 255, 235 if hover else 160)
        draw.soft_rect(screen, box, fill, border, 999, 1)
        ink = WHITE if hover else SOFT
        self._expand_arrow(screen, (box.x + 18, box.centery), ink)
        label = draw.text(fonts["tiny"], "Raw view", ink)
        screen.blit(label, label.get_rect(midleft=(box.x + 34, box.centery)))

    def _expand_arrow(self, screen, center, color):
        scale = 4
        surf = pygame.Surface((16 * scale, 16 * scale), pygame.SRCALPHA)

        def at(pt):
            return (pt[0] * scale, pt[1] * scale)

        pygame.draw.line(surf, color, at((3, 12)), at((12, 3)), scale * 2)
        pygame.draw.lines(surf, color, False, [at((7, 3)), at((12, 3)), at((12, 8))], scale * 2)
        icon = pygame.transform.smoothscale(surf, (16, 16))
        screen.blit(icon, icon.get_rect(center=(int(center[0]), int(center[1]))))
