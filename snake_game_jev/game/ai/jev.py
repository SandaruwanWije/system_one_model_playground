import json
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
        self.last_input = ""
        self.last_output = ""
        self.last_model = "jev-latest"

    def clear(self):
        self.probs = {}

    def ask(self, board):
        moves = board.legal()
        if not moves:
            self.choice = board.facing
            self.probs = {}
            self.latency_ms = 0.0
            return self.choice

        state = board.state(moves)
        questions = {
            "move": Choice(
                instructions=RULES,
                criteria={move: board.facts(move) for move in moves},
            )
        }
        self.last_input = json.dumps(
            {
                "state": state,
                "model": "jev-latest",
                "questions": {
                    "move": {
                        "type": "choice",
                        "instructions": RULES,
                        "criteria": {move: board.facts(move) for move in moves},
                    }
                },
            },
            indent=2,
        )

        started = time.perf_counter()
        response = self.client.system_one(state, questions)
        answer = response.choices["move"]
        self.latency_ms = (time.perf_counter() - started) * 1000
        self.last_model = getattr(response, "model", None) or "jev-latest"
        self.choice = answer.choice if answer.choice in moves else moves[0]
        self.probs = {move: float(answer.probabilities.get(move, 0)) for move in moves}
        confidence = float(getattr(answer, "confidence", self.probs.get(self.choice, 0)))
        self.last_output = json.dumps(
            {
                "model": self.last_model,
                "answers": {
                    "move": {
                        "type": "choice",
                        "choice": self.choice,
                        "probabilities": {k: round(v, 4) for k, v in self.probs.items()},
                        "confidence": round(confidence, 4),
                    }
                },
                "latency_ms": round(self.latency_ms, 1),
            },
            indent=2,
        )
        return self.choice
