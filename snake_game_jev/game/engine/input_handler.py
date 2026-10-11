import pygame

from game.core.config import KEYS


class InputHandler:
    def __init__(self, session, layout):
        self.session = session
        self.layout = layout

    def handle(self, event):
        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_p):
                self.session.toggle_pause()
            elif event.key in KEYS:
                self.session.queue_move(KEYS[event.key])
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.layout.pause_btn.collidepoint(event.pos):
                self.session.toggle_pause()
            elif not self.session.clock.paused:
                mode = self.layout.hit(event.pos, self.layout.mode_btns)
                if mode:
                    self.session.set_mode(mode)
                else:
                    pad = self.layout.hit(event.pos, self.layout.pads)
                    if pad:
                        self.session.queue_move(pad)
        return None
