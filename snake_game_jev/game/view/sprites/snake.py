from game.core.directions import WAYS
from game.view import primitives as draw

BLUE = (140, 180, 255)
TEAL = (120, 210, 220)
WHITE = (245, 250, 255)
SHADOW = (40, 70, 120)


def _pos(points, index, along, pick, cell_center):
    c, r = points[index]
    goal = (c + WAYS[pick][0], r + WAYS[pick][1]) if index == 0 else points[index - 1]
    x0, y0 = cell_center(c, r)
    x1, y1 = cell_center(*goal)
    return draw.lerp(x0, x1, along), draw.lerp(y0, y1, along)


def _mid(a, b):
    return ((a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5)


def _quad(a, b, c, t):
    u = 1 - t
    return (
        u * u * a[0] + 2 * u * t * b[0] + t * t * c[0],
        u * u * a[1] + 2 * u * t * b[1] + t * t * c[1],
    )


def _smooth_path(anchors, steps=8):
    if len(anchors) == 1:
        return list(anchors)
    if len(anchors) == 2:
        return [
            (
                draw.lerp(anchors[0][0], anchors[1][0], i / steps),
                draw.lerp(anchors[0][1], anchors[1][1], i / steps),
            )
            for i in range(steps + 1)
        ]

    path = [anchors[0]]
    # Straight into the first midpoint, then quadratic through each joint.
    first_mid = _mid(anchors[0], anchors[1])
    for i in range(1, steps + 1):
        path.append((
            draw.lerp(anchors[0][0], first_mid[0], i / steps),
            draw.lerp(anchors[0][1], first_mid[1], i / steps),
        ))

    for i in range(1, len(anchors) - 1):
        start = _mid(anchors[i - 1], anchors[i])
        ctrl = anchors[i]
        end = _mid(anchors[i], anchors[i + 1])
        for s in range(1, steps + 1):
            path.append(_quad(start, ctrl, end, s / steps))

    last = anchors[-1]
    prev_mid = _mid(anchors[-2], last)
    for i in range(1, steps + 1):
        path.append((
            draw.lerp(prev_mid[0], last[0], i / steps),
            draw.lerp(prev_mid[1], last[1], i / steps),
        ))
    return path


def paint(screen, points, pick, along, cell, cell_center, pulse=0.0):
    if not points:
        return
    t = draw.ease(along)
    anchors = [_pos(points, i, t, pick, cell_center) for i in range(len(points))]
    path = _smooth_path(anchors, steps=10)
    total = max(1, len(path) - 1)

    for i in range(total, -1, -1):
        x, y = path[i]
        fade = i / total
        rad = cell * (0.33 - 0.08 * fade)
        color = draw.mix(TEAL, BLUE, 1 - fade * 0.5)
        alpha = int(255 * (0.38 + 0.4 * (1 - fade)))
        if i % 2 == 0:
            draw.blit_center(screen, draw.glow(int(rad * 2.0), color, 0.12 + 0.08 * (1 - fade)), (x, y))
        draw.blit_center(screen, draw.circle(int(rad * 1.05), (*SHADOW, int(34 + 24 * (1 - fade)))), (x, y + 1))
        draw.blit_center(screen, draw.circle(int(rad), (*color, alpha)), (x, y))
        if i % 2 == 0:
            draw.blit_center(
                screen,
                draw.circle(int(rad * 0.58), (*WHITE, int(20 + 26 * (1 - fade)))),
                (x - rad * 0.15, y - rad * 0.18),
            )

    hx, hy = path[0]
    head_r = cell * 0.37
    draw.blit_center(screen, draw.glow(int(head_r * 2.8), BLUE, 0.34 + 0.12 * pulse), (hx, hy))
    draw.blit_center(screen, draw.circle(int(head_r), (*BLUE, 210)), (hx, hy))
    draw.blit_center(screen, draw.circle(int(head_r * 0.78), (170, 210, 255, 90)), (hx, hy))
    draw.blit_center(screen, draw.circle(int(head_r * 0.45), (*WHITE, 55)), (hx - head_r * 0.2, hy - head_r * 0.25))
    draw.blit_center(screen, draw.ring(int(head_r), (220, 235, 255, 120), 1), (hx, hy))

    dx, dy = WAYS[pick]
    eye = head_r * 0.42
    side = head_r * 0.38
    for sign in (-1, 1):
        ex = hx + dx * eye + (-dy) * side * sign * 0.55
        ey = hy + dy * eye + dx * side * sign * 0.55
        draw.blit_center(screen, draw.circle(int(head_r * 0.16), (245, 248, 255, 230)), (ex, ey))
        draw.blit_center(screen, draw.circle(int(head_r * 0.08), (20, 28, 40, 230)), (ex + dx * 1.5, ey + dy * 1.5))
