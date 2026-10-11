import pygame

from game.core.config import BLUE, MUTED, WHITE
from game.view import primitives as draw


class TopBar:
    def paint(self, screen, fonts, layout, session):
        shell = layout.shell
        y = shell.y + 18

        group = pygame.Rect(shell.x + 20, y, 168, 36)
        draw.soft_rect(screen, group, (255, 255, 255, 14), (255, 255, 255, 28), 999, 1)
        you_btn = pygame.Rect(group.x + 4, group.y + 4, 78, 28)
        jev_btn = pygame.Rect(you_btn.right + 4, group.y + 4, 78, 28)
        layout.mode_btns = {"you": you_btn, "jev": jev_btn}

        for name, box in layout.mode_btns.items():
            on = session.mode == name
            draw.soft_rect(
                screen, box,
                (140, 180, 255, 50) if on else (255, 255, 255, 0),
                (140, 180, 255, 210) if on else None,
                999, 1,
            )
            label = draw.text(fonts["font"], "You" if name == "you" else "Jev", WHITE if on else MUTED)
            screen.blit(label, label.get_rect(center=box.center))

        layout.pause_btn = pygame.Rect(group.right + 10, y, 36, 36)
        self._pause_button(screen, layout.pause_btn, session.clock.paused)

        chip_w, gap = 132, 8
        right = shell.right - 20
        chips = (("You", session.scores.you_best, "you"), ("Jev", session.scores.jev_best, "jev"))
        for i, (title, best, mode) in enumerate(chips):
            chip = pygame.Rect(right - chip_w * (2 - i) - gap * (1 - i), y, chip_w, 36)
            active = session.mode == mode
            draw.soft_rect(
                screen, chip,
                (140, 180, 255, 30) if active else (255, 255, 255, 10),
                (140, 180, 255, 170) if active else (255, 255, 255, 24),
                14, 1,
            )
            current = session.board.score if active else "—"
            line = draw.text(fonts["tiny"], f"{title}  {current} · best {best}", BLUE if active else MUTED)
            screen.blit(line, line.get_rect(center=chip.center))
        return y + 52

    def _pause_button(self, screen, box, paused):
        draw.soft_rect(
            screen, box,
            (140, 180, 255, 45) if paused else (255, 255, 255, 12),
            (140, 180, 255, 200) if paused else (255, 255, 255, 28),
            12, 1,
        )
        cx, cy = box.center
        if paused:
            pygame.draw.polygon(screen, WHITE, [(cx - 5, cy - 7), (cx - 5, cy + 7), (cx + 7, cy)])
        else:
            pygame.draw.rect(screen, WHITE, (cx - 6, cy - 7, 4, 14), border_radius=1)
            pygame.draw.rect(screen, WHITE, (cx + 2, cy - 7, 4, 14), border_radius=1)
