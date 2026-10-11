import threading

from game.ai import Jev
from game.audio import Audio
from game.core.directions import OPPOSITE, WAYS
from game.domain import Board, Scores
from game.engine.clock import StepClock


class Session:
    """Owns game state and applies one move at a time."""

    def __init__(self):
        self.board = Board()
        self.jev = Jev()
        self.audio = Audio()
        self.scores = Scores()
        self.clock = StepClock()
        self.mode = "jev"
        self.queued = self.board.facing
        self.pick = self.board.facing
        self.next_pick = self.board.facing
        self.from_snake = list(self.board.snake)
        self.busy = False
        self.ready = False
        self.mode_fade = 1.0
        self.heat = {name: 0.0 for name in WAYS}
        self.raw_open = False

    def start(self):
        self.clock.begin()
        self._ask_async()

    def set_mode(self, mode):
        if mode == self.mode:
            return
        self.mode = mode
        self.raw_open = False
        self.clock.paused = False
        self.mode_fade = 0.0
        self._reset_run()
        self.clock.begin()
        if mode == "jev":
            self._ask_async()

    def queue_move(self, move):
        if self.mode == "you" and not self.clock.paused:
            self.queued = move

    def toggle_pause(self):
        self.clock.toggle_pause()

    def toggle_raw(self):
        self.raw_open = not self.raw_open

    def update(self, dt, lerp):
        self._update_heat(dt, lerp)
        self.mode_fade = lerp(self.mode_fade, 1.0, min(1.0, dt * 4.5))
        if self.clock.tick():
            if self.mode == "jev" and self.ready:
                self._apply_jev()
            elif self.mode == "you":
                self._apply_you()

    def _ask_async(self):
        self.busy = True
        self.ready = False
        threading.Thread(target=self._ask, daemon=True).start()

    def _ask(self):
        if self.mode != "jev":
            self.busy = False
            return
        self.next_pick = self.jev.ask(self.board)
        if self.mode == "jev":
            self.ready = True
            self.busy = False

    def _apply_jev(self):
        self._commit(self.next_pick)
        self.clock.restart_step()
        self._ask_async()

    def _apply_you(self):
        move = self.board.facing if self.queued == OPPOSITE[self.board.facing] else self.queued
        self._commit(move)
        self.clock.restart_step()

    def _commit(self, move):
        self.pick = move
        self.from_snake = list(self.board.snake)
        result = self.board.step(move)
        if result == "eat":
            self.audio.play_eat()
        elif result == "die":
            self.scores.save_run(self.mode, self.board.score)
            self._reset_run()

    def _reset_run(self):
        self.board.reset()
        self.from_snake = list(self.board.snake)
        self.pick = self.next_pick = self.queued = self.board.facing
        self.ready = False
        self.busy = False
        self.jev.clear()
        self.heat = {name: 0.0 for name in WAYS}

    def _update_heat(self, dt, lerp):
        for name in WAYS:
            if self.mode == "jev":
                target = self.jev.probs.get(name, 0.0)
                if name == self.pick:
                    target = max(target, 0.55)
            else:
                target = 1.0 if name == self.queued else (0.4 if name == self.pick else 0.08)
            self.heat[name] = lerp(self.heat[name], target, min(1.0, dt * 7))
