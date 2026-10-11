import time

import pygame

from game.engine import InputHandler, Session
from game.view import Renderer
from game.view import primitives as draw


class App:
    def __init__(self):
        pygame.init()
        self.session = Session()
        self.renderer = Renderer()
        self.input = InputHandler(self.session, self.renderer.layout)
        self.clock = pygame.time.Clock()

    def run(self):
        self.session.start()
        prev = time.perf_counter()
        while True:
            now = time.perf_counter()
            dt, prev = now - prev, now
            for event in pygame.event.get():
                if self.input.handle(event) == "quit":
                    return
            self.session.update(dt, draw.lerp)
            self.renderer.draw(self.session)
            self.clock.tick(60)
