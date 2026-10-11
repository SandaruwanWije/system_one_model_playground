WAYS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}
OPPOSITE = {"left": "right", "right": "left", "up": "down", "down": "up"}


def step(point, move):
    c, r = point
    dc, dr = WAYS[move]
    return c + dc, r + dr
