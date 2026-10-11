import time

from typesafe_sdk import Choice, TypeSafeClient

RULES = (
    "You are playing Snake. Choose the next head direction. "
    "Every listed direction is safe for this one step; facts are exact. "
    "Avoid DEAD END moves. Prefer food when it does not trap you."
)


class Jev:
    def __init__(self):
        self.client = TypeSafeClient(model="jev-latest")
        self.choice = "right"
        self.probs = {}
        self.latency_ms = 0.0

    def clear(self):
        self.probs = {}

    def ask(self, board):
        moves = board.legal()
        if not moves:
            self.choice = board.facing
            self.probs = {}
            self.latency_ms = 0.0
            return self.choice

        started = time.perf_counter()
        answer = self.client.system_one(
            board.state(moves),
            {
                "move": Choice(
                    instructions=RULES,
                    criteria={move: board.facts(move) for move in moves},
                )
            },
        ).choices["move"]
        self.latency_ms = (time.perf_counter() - started) * 1000
        self.choice = answer.choice if answer.choice in moves else moves[0]
        self.probs = {move: float(answer.probabilities.get(move, 0)) for move in moves}
        return self.choice
