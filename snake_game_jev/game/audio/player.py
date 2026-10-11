from pathlib import Path

import pygame

SOUND = Path(__file__).resolve().parents[2] / "sounds" / "eat_sound.mp3"


class Audio:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.eat = pygame.mixer.Sound(SOUND)
        self.eat.set_volume(0.55)

    def play_eat(self):
        self.eat.play()
