import math

import pygame

_cache: dict = {}


def clamp(value, lo=0.0, hi=1.0):
    return max(lo, min(hi, value))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    t = ease(t)
    return a + (b - a) * t


def mix(c1, c2, t):
    t = clamp(t)
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


def with_alpha(color, alpha):
    return (*color[:3], int(clamp(alpha, 0, 255)))


def glow(radius, color, strength=0.55):
    key = ("glow", int(radius), color, round(strength, 2))
    if key in _cache:
        return _cache[key]
    size = max(16, int(radius) * 2)
    sample = 56
    tiny = pygame.Surface((sample, sample), pygame.SRCALPHA)
    cx = cy = sample / 2 - 0.5
    reach = sample / 2
    r, g, b = color[:3]
    for y in range(sample):
        for x in range(sample):
            d = math.hypot(x - cx, y - cy) / reach
            if d >= 1:
                continue
            a = int(255 * strength * (1 - d) ** 2.4)
            if a:
                tiny.set_at((x, y), (r, g, b, a))
    surf = pygame.transform.smoothscale(tiny, (size, size))
    _cache[key] = surf
    return surf


def circle(radius, color, scale=4):
    rgb = color[:3]
    alpha = color[3] if len(color) > 3 else 255
    key = ("circle", int(radius), rgb, alpha, scale)
    if key in _cache:
        return _cache[key]
    r = max(2, int(radius))
    big = r * scale
    pad = 2
    surf = pygame.Surface((big * 2 + pad * 2, big * 2 + pad * 2), pygame.SRCALPHA)
    pygame.draw.circle(surf, (*rgb, alpha), (big + pad, big + pad), big)
    out = pygame.transform.smoothscale(surf, (r * 2, r * 2))
    _cache[key] = out
    return out


def ring(radius, color, width=2, scale=4):
    rgb = color[:3]
    alpha = color[3] if len(color) > 3 else 255
    key = ("ring", int(radius), rgb, alpha, width, scale)
    if key in _cache:
        return _cache[key]
    r = max(3, int(radius))
    big_r, big_w = r * scale, max(1, int(width * scale))
    pad = big_w + 2
    size = big_r * 2 + pad * 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, (*rgb, alpha), (size // 2, size // 2), big_r, big_w)
    out = pygame.transform.smoothscale(surf, (r * 2 + 4, r * 2 + 4))
    _cache[key] = out
    return out


def arc(radius, color, start, sweep, width=2, scale=4):
    rgb = color[:3]
    alpha = color[3] if len(color) > 3 else 255
    r = max(4, int(radius))
    big_r, big_w = r * scale, max(1, int(width * scale))
    pad = big_w + 2
    size = big_r * 2 + pad * 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    rect = pygame.Rect(pad, pad, big_r * 2, big_r * 2)
    pygame.draw.arc(surf, (*rgb, alpha), rect, start, start + sweep, big_w)
    return pygame.transform.smoothscale(surf, (r * 2 + 4, r * 2 + 4))


def arrow(size, direction, color):
    key = ("arrow", int(size), direction, color)
    if key in _cache:
        return _cache[key]
    s = max(10, int(size))
    scale = 4
    big = s * scale
    surf = pygame.Surface((big, big), pygame.SRCALPHA)
    cx = cy = big / 2
    arm = big * 0.28
    tip = big * 0.34
    dirs = {
        "up": (0, -1),
        "down": (0, 1),
        "left": (-1, 0),
        "right": (1, 0),
    }
    dx, dy = dirs[direction]
    px, py = -dy, dx
    points = [
        (cx + dx * tip, cy + dy * tip),
        (cx - dx * arm + px * arm, cy - dy * arm + py * arm),
        (cx - dx * arm * 0.2 + px * arm * 0.35, cy - dy * arm * 0.2 + py * arm * 0.35),
        (cx - dx * tip * 0.85 + px * arm * 0.35, cy - dy * tip * 0.85 + py * arm * 0.35),
        (cx - dx * tip * 0.85 - px * arm * 0.35, cy - dy * tip * 0.85 - py * arm * 0.35),
        (cx - dx * arm * 0.2 - px * arm * 0.35, cy - dy * arm * 0.2 - py * arm * 0.35),
        (cx - dx * arm - px * arm, cy - dy * arm - py * arm),
    ]
    pygame.draw.polygon(surf, color, points)
    out = pygame.transform.smoothscale(surf, (s, s))
    _cache[key] = out
    return out


def panel(size, radius, fill, border=None, border_width=1):
    key = ("panel", size, radius, fill, border, border_width)
    if key in _cache:
        return _cache[key]
    w, h = size
    scale = 3
    surf = pygame.Surface((w * scale, h * scale), pygame.SRCALPHA)
    rect = pygame.Rect(0, 0, w * scale, h * scale)
    pygame.draw.rect(surf, fill, rect, border_radius=radius * scale)
    if border:
        pygame.draw.rect(surf, border, rect, border_width * scale, border_radius=radius * scale)
    out = pygame.transform.smoothscale(surf, (w, h))
    _cache[key] = out
    return out


def soft_rect(screen, rect, fill, border=None, radius=18, width=1):
    surf = panel((rect.w, rect.h), radius, fill, border, width)
    screen.blit(surf, rect.topleft)


def vignette(size, color=(8, 10, 16), strength=0.55):
    key = ("vig", size, color, round(strength, 2))
    if key in _cache:
        return _cache[key]
    w, h = size
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    sample = pygame.Surface((64, 64), pygame.SRCALPHA)
    cx, cy = 31.5, 31.5
    r, g, b = color
    for y in range(64):
        for x in range(64):
            dx = abs(x - cx) / 32
            dy = abs(y - cy) / 32
            d = max(dx, dy)
            a = int(255 * strength * clamp((d - 0.45) / 0.55) ** 1.6)
            if a:
                sample.set_at((x, y), (r, g, b, a))
    surf.blit(pygame.transform.smoothscale(sample, (w, h)), (0, 0))
    _cache[key] = surf
    return surf


def text(font, value, color, alpha=255):
    surf = font.render(str(value), True, color[:3])
    if alpha >= 255:
        return surf
    surf = surf.convert_alpha()
    surf.set_alpha(int(clamp(alpha, 0, 255)))
    return surf


def blit_center(screen, surf, pos):
    screen.blit(surf, surf.get_rect(center=(int(pos[0]), int(pos[1]))))


def blit_alpha(screen, surf, pos, alpha):
    if alpha >= 254:
        screen.blit(surf, pos)
        return
    copy = surf.copy()
    copy.set_alpha(int(clamp(alpha, 0, 255)))
    screen.blit(copy, pos)
