from game.view import primitives as draw

RED = (220, 64, 72)
DEEP = (170, 36, 48)
LEAF = (90, 190, 110)
STEM = (110, 78, 48)
SHINE = (255, 230, 220)


def paint(screen, pos, cell, pulse=0.0):
    x, y = pos
    r = cell * 0.28
    draw.blit_center(screen, draw.glow(int(r * 3.2), RED, 0.38 + 0.14 * pulse), (x, y))
    draw.blit_center(screen, draw.glow(int(r * 2.1), (255, 120, 110), 0.22 + 0.08 * pulse), (x, y - r * 0.1))

    # Apple body: two lobes + lower fill for a soft fruit silhouette.
    draw.blit_center(screen, draw.circle(int(r * 0.95), (*DEEP, 230)), (x - r * 0.22, y + r * 0.05))
    draw.blit_center(screen, draw.circle(int(r * 0.95), (*DEEP, 230)), (x + r * 0.22, y + r * 0.05))
    draw.blit_center(screen, draw.circle(int(r * 1.05), (*RED, 235)), (x, y + r * 0.12))
    draw.blit_center(screen, draw.circle(int(r * 0.82), (*RED, 240)), (x - r * 0.18, y - r * 0.05))
    draw.blit_center(screen, draw.circle(int(r * 0.82), (*RED, 240)), (x + r * 0.18, y - r * 0.05))

    # Specular shine
    draw.blit_center(screen, draw.circle(int(r * 0.28), (*SHINE, 140)), (x - r * 0.28, y - r * 0.22))
    draw.blit_center(screen, draw.circle(int(r * 0.14), (255, 255, 255, 120)), (x - r * 0.32, y - r * 0.28))

    # Stem
    stem_top = (x + r * 0.02, y - r * 1.05)
    stem_bot = (x - r * 0.02, y - r * 0.55)
    for i in range(5):
        u = i / 4
        px = draw.lerp(stem_bot[0], stem_top[0], u)
        py = draw.lerp(stem_bot[1], stem_top[1], u)
        draw.blit_center(screen, draw.circle(max(1, int(r * 0.1)), (*STEM, 230)), (px, py))

    # Leaf
    lx, ly = x + r * 0.28, y - r * 0.85
    draw.blit_center(screen, draw.circle(int(r * 0.28), (*LEAF, 220)), (lx, ly))
    draw.blit_center(screen, draw.circle(int(r * 0.18), (160, 230, 150, 160)), (lx + r * 0.05, ly - r * 0.05))
