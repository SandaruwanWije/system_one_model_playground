import random
from collections import deque

from game.core.directions import OPPOSITE, WAYS, step


class Board:
    def __init__(self, cols=12, rows=8):
        self.cols, self.rows = cols, rows
        self.reset()

    def reset(self):
        self.snake = [(4, 4), (3, 4), (2, 4), (1, 4)]
        self.facing = "right"
        self.food = (9, 4)
        self.score = 0

    def cell(self, c, r):
        return r * self.cols + c + 1

    def place(self, c, r):
        return f"{self.cell(c, r)}, column {c + 1}, row {r + 1}"

    def inside(self, point):
        c, r = point
        return 0 <= c < self.cols and 0 <= r < self.rows

    def target(self, move):
        return step(self.snake[0], move)

    def legal(self):
        moves = []
        for move in WAYS:
            if move == OPPOSITE[self.facing]:
                continue
            nxt = self.target(move)
            if self.inside(nxt) and nxt not in self.snake[:-1]:
                moves.append(move)
        return moves

    def facts(self, move):
        nxt = self.target(move)
        eats = nxt == self.food
        body = [nxt, *(self.snake if eats else self.snake[:-1])]
        reachable = self._flood(nxt, set(body))
        free = self.cols * self.rows - len(body)
        dist = abs(self.food[0] - nxt[0]) + abs(self.food[1] - nxt[1])
        line = f"head to {self.place(*nxt)}; "
        line += "EATS FOOD now; " if eats else f"food {dist} steps away; "
        line += f"{reachable}/{free} empty cells reachable"
        if reachable < len(body):
            line += "; DEAD END"
        return line

    def ascii(self):
        grid = [["." for _ in range(self.cols)] for _ in range(self.rows)]
        fc, fr = self.food
        grid[fr][fc] = "F"
        for i, (c, r) in enumerate(self.snake):
            grid[r][c] = "H" if i == 0 else "T" if i == len(self.snake) - 1 else "o"
        return ["".join(row) for row in grid]

    def state(self, moves):
        hc, hr = self.snake[0]
        return {
            "board": self.ascii(),
            "legend": "H=head o=body T=tail F=food .=empty. Row 1 is top, column 1 is left.",
            "head": self.place(hc, hr),
            "food": self.place(*self.food),
            "facing": self.facing,
            "length": len(self.snake),
            "grid": {"cols": self.cols, "rows": self.rows},
            "legal": moves,
        }

    def step(self, move):
        nxt = self.target(move)
        if not self.inside(nxt) or nxt in self.snake[:-1]:
            return "die"
        self.snake = [nxt, *self.snake]
        self.facing = move
        if nxt == self.food:
            self.score += 1
            open_ = [
                (c, r)
                for r in range(self.rows)
                for c in range(self.cols)
                if (c, r) not in self.snake
            ]
            self.food = random.choice(open_ or [(0, 0)])
            return "eat"
        self.snake.pop()
        return "ok"

    def _flood(self, start, blocked):
        seen, queue = set(), deque([start])
        while queue:
            c, r = queue.popleft()
            for dc, dr in WAYS.values():
                nxt = (c + dc, r + dr)
                if not self.inside(nxt) or nxt in blocked or nxt in seen:
                    continue
                seen.add(nxt)
                queue.append(nxt)
        return len(seen)
