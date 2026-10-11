import pygame

from game.core.config import KEYS


class InputHandler:
    def __init__(self, session, layout, raw_panel):
        self.session = session
        self.layout = layout
        self.raw_panel = raw_panel

    def handle(self, event):
        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.session.raw_open:
                self.session.raw_open = False
                return None
            if event.key in (pygame.K_SPACE, pygame.K_p):
                self.session.toggle_pause()
            elif event.key in KEYS:
                self.session.queue_move(KEYS[event.key])
            return None

        if event.type == pygame.MOUSEWHEEL and self.session.raw_open:
            self.raw_panel.on_wheel(pygame.mouse.get_pos(), event.y)
            return None

        if event.type == pygame.MOUSEMOTION:
            self.raw_panel.drag_to(event.pos)
            return None

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.raw_panel.end_drag()
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.session.raw_open and self.raw_panel.panel.collidepoint(event.pos):
                if self.raw_panel.close_btn.collidepoint(event.pos):
                    self.session.raw_open = False
                else:
                    self.raw_panel.begin_drag(event.pos)
                return None

            if self.layout.expand_btn.width and self.layout.expand_btn.collidepoint(event.pos):
                self.session.toggle_raw()
                return None

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
