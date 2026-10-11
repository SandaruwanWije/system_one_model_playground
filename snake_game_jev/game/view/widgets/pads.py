from game.core.config import BLUE, MUTED, WHITE
from game.view import primitives as draw


class Pads:
    def paint(self, screen, fonts, layout, session):
        for name, box in layout.pads.items():
            heat = session.heat[name]
            fill = draw.mix((24, 26, 34), (40, 52, 84), heat)
            border = draw.mix((68, 72, 88), BLUE, heat)
            if heat > 0.15:
                draw.blit_center(screen, draw.glow(int(20 + 18 * heat), BLUE, 0.22 + 0.4 * heat), box.center)
            draw.soft_rect(screen, box, (*fill, 240), (*border, int(90 + 140 * heat)), 20, 1)
            if session.mode == "jev":
                label = draw.text(fonts["tiny"], name, draw.mix(MUTED, WHITE, heat))
                screen.blit(label, label.get_rect(center=(box.centerx, box.centery - 14)))
                prob = session.jev.probs.get(name, 0.0)
                value = draw.text(fonts["big"], f"{prob:.2f}", draw.mix(MUTED, BLUE, max(heat, prob)))
                screen.blit(value, value.get_rect(center=(box.centerx, box.centery + 12)))
            else:
                icon = draw.arrow(36, name, draw.mix((110, 118, 136), WHITE, 0.25 + 0.75 * heat))
                draw.blit_center(screen, icon, box.center)
