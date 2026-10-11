import math
import time

from game.view import primitives as draw

BLUE, WHITE = (160, 190, 255), (245, 245, 247)


def rim(x, y, radius, angle):
    return (x + math.cos(angle) * radius, y + math.sin(angle) * radius)


def bezier(a, c1, c2, b, t):
    u = 1 - t
    return (
        u * u * u * a[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t * t * t * b[0],
        u * u * u * a[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t * t * t * b[1],
    )


def curve(a, c1, c2, b):
    return a, c1, c2, b


def inbound(frame, jev, radius):
    start = (frame.centerx, frame.bottom)
    end = rim(jev[0], jev[1], radius * 2.15, -math.pi / 2)
    drop = max(20, end[1] - start[1])
    return curve(start, (start[0], start[1] + drop * 0.45), (end[0], start[1] + drop * 0.75), end)


def outbound(jev, radius, box, key):
    start = rim(jev[0], jev[1], radius * 2.15, math.pi / 2)
    offset = {"left": -28, "up": 0, "right": 28, "down": 14}[key]
    origin = (start[0] + offset, start[1])
    end = (box.centerx, box.top - 18)
    return curve(origin, (end[0], origin[1] + 22), (end[0], max(origin[1] + 36, end[1] - 28)), end)


def down_routes(jev, radius, up, down):
    # Leave from the bottom of JEV, drift right, then lane around the up pad.
    start = rim(jev[0], jev[1], radius * 2.15, math.pi / 2)
    origin = (start[0] + 16, start[1])
    lane = up.right + 18
    above = min(origin[1] + 16, up.top - 14)
    side_top = (lane, up.top - 2)
    side_low = (lane, up.bottom + 8)
    resume = (down.centerx, side_low[1] + 10)
    end = (down.centerx, down.top - 8)
    return [
        curve(origin, (origin[0], above), (lane, above), side_top),
        curve(side_top, (lane, up.top + up.h * 0.45), (lane, up.top + up.h * 0.75), side_low),
        curve(side_low, (lane, resume[1]), (resume[0], resume[1]), resume),
        curve(resume, (end[0], resume[1] + (end[1] - resume[1]) * 0.4), (end[0], resume[1] + (end[1] - resume[1]) * 0.75), end),
    ]


def paint_dots(screen, route, emphasis, flow, joined=False):
    count = 14 if joined else 18
    for index in range(count):
        t = (index / count + flow) % 1
        if not joined and (t < 0.04 or t > 0.98):
            continue
        point = bezier(*route, t)
        edge = 1 if joined else min((t - 0.03) / 0.12, (1 - t) / 0.1, 1)
        fade = max(0.0, edge) * (0.45 + emphasis * 0.55)
        outer = 4 if emphasis > 0.8 else 3
        inner = 1.2 if emphasis > 0.8 else 0.9
        draw.blit_center(screen, draw.circle(outer, (*BLUE, int(90 * fade))), point)
        draw.blit_center(screen, draw.circle(inner, (*WHITE, int(230 * fade))), point)


def paint(screen, frame, jev, radius, pads, pick, heat):
    flow = (time.time() * 1000 / 900) % 1
    paint_dots(screen, inbound(frame, jev, radius), 1.0, flow)
    for key, box in pads.items():
        emphasis = 1.0 if key == pick else 0.55 + 0.35 * heat.get(key, 0)
        routes = down_routes(jev, radius, pads["up"], pads["down"]) if key == "down" else [outbound(jev, radius, box, key)]
        for route in routes:
            paint_dots(screen, route, emphasis, flow, joined=(key == "down"))
