import time

from game.core.config import BLUE, WHITE
from game.view import primitives as draw


class Disc:
    def paint(self, screen, fonts, center, radius, mode, busy, latency_ms, fade, pulse):
        x, y = center
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
