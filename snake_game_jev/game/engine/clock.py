import pygame

from game.core.config import STEP_MS


class StepClock:
    def __init__(self):
        self.along = 1.0
        self.started = 0
        self.paused = False
        self._pause_at = 0

    def begin(self):
        self.started = pygame.time.get_ticks()
        self.along = 1.0

    def restart_step(self):
        self.along = 0.0
        self.started = pygame.time.get_ticks()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self._pause_at = pygame.time.get_ticks()
        else:
            self.started += pygame.time.get_ticks() - self._pause_at

    def tick(self):
        if self.paused:
            return False
        self.along = min(1.0, (pygame.time.get_ticks() - self.started) / STEP_MS)
        return self.along >= 1.0
