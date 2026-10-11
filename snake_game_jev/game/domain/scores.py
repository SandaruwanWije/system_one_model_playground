class Scores:
    def __init__(self):
        self.you_best = 0
        self.jev_best = 0

    def save_run(self, mode, score):
        if mode == "you":
            self.you_best = max(self.you_best, score)
        else:
            self.jev_best = max(self.jev_best, score)

    def best(self, mode):
        return self.you_best if mode == "you" else self.jev_best
