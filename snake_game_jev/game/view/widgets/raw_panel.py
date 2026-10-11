import json
import math
import time

import pygame

from game.core.config import AMBER, BLUE, MUTED, WHITE
from game.view import primitives as draw

INK = {
    "punct": (118, 126, 146),
    "key": (176, 206, 255),
    "str": (255, 198, 140),
    "num": (166, 224, 196),
    "bool": (140, 180, 255),
    "choice": (245, 245, 247),
}


class RawPanel:
    def __init__(self):
        self.scrolls = {"input": 0, "output": 0}
        self.max_scroll = {"input": 0, "output": 0}
        self.viewports = {}
        self.close_btn = pygame.Rect(0, 0, 0, 0)
        self.panel = pygame.Rect(0, 0, 0, 0)
        self._pages = {}
        self._seen = {}
        self._flash = {"input": 0.0, "output": 0.0}
        self._drag = None

    def paint(self, screen, fonts, layout, session):
        shell = layout.shell
        top = layout.frame.bottom + 8
        self.panel = pygame.Rect(shell.x + 12, top, shell.w - 24, shell.bottom - top - 12)
        screen.fill((10, 12, 18), pygame.Rect(0, self.panel.y, screen.get_width(), screen.get_height() - self.panel.y))
        draw.soft_rect(screen, self.panel, (16, 18, 26, 255), (140, 180, 255, 70), 22, 1)
        self._header(screen, fonts, session)

        gap = 10
        body = pygame.Rect(self.panel.x + 12, self.panel.y + 50, self.panel.w - 24, self.panel.h - 62)
        input_h = int((body.h - gap) * 0.54)
        incoming = self._read(session.jev.last_input)
        outgoing = self._read(session.jev.last_output)
        self._column(
            screen, fonts,
            pygame.Rect(body.x, body.y, body.w, input_h),
            "input", "Input", AMBER,
            self._input_meta(incoming),
            session.jev.last_input,
            "Waiting for the first request",
        )
        self._column(
            screen, fonts,
            pygame.Rect(body.x, body.y + input_h + gap, body.w, body.h - input_h - gap),
            "output", "Output", BLUE,
            self._output_meta(outgoing, session),
            session.jev.last_output,
            "Waiting for the first response",
        )

    def on_wheel(self, pos, dy):
        for key, rect in self.viewports.items():
            if rect.collidepoint(pos):
                cap = self.max_scroll.get(key, 0)
                self.scrolls[key] = max(0, min(cap, self.scrolls[key] - dy * 48))
                return

    def begin_drag(self, pos):
        for key, rect in self.viewports.items():
            if rect.collidepoint(pos):
                self._drag = (key, pos[1], self.scrolls[key])
                return True
        return False

    def drag_to(self, pos):
        if not self._drag:
            return
        key, origin, start = self._drag
        cap = self.max_scroll.get(key, 0)
        self.scrolls[key] = max(0, min(cap, start - (pos[1] - origin)))

    def end_drag(self):
        self._drag = None

    def _header(self, screen, fonts, session):
        pulse = 0.55 + 0.45 * abs(math.sin(time.time() * 3.2))
        dot = AMBER if session.busy else (120, 214, 168)
        cx, cy = self.panel.x + 26, self.panel.y + 26
        draw.blit_center(screen, draw.glow(14, dot, 0.35 * pulse), (cx, cy))
        draw.blit_center(screen, draw.circle(4, (*dot, int(160 + 90 * pulse))), (cx, cy))
        title = draw.text(fonts["font"], "Updating" if session.busy else "Live", WHITE)
        screen.blit(title, title.get_rect(midleft=(cx + 12, cy)))

        self.close_btn = pygame.Rect(self.panel.right - 46, self.panel.y + 10, 32, 32)
        hover = self.close_btn.collidepoint(pygame.mouse.get_pos())
        draw.soft_rect(
            screen, self.close_btn,
            (255, 255, 255, 28) if hover else (255, 255, 255, 12),
            (255, 255, 255, 70) if hover else (255, 255, 255, 32),
            999, 1,
        )
        x, y = self.close_btn.center
        pygame.draw.line(screen, WHITE, (x - 4, y - 4), (x + 4, y + 4), 2)
        pygame.draw.line(screen, WHITE, (x + 4, y - 4), (x - 4, y + 4), 2)

        if session.jev.latency_ms:
            chip = draw.text(fonts["tiny"], f"{session.jev.latency_ms:.0f} ms", BLUE)
            pad = pygame.Rect(0, 0, chip.get_width() + 16, 24)
            pad.midright = (self.close_btn.left - 8, self.close_btn.centery)
            draw.soft_rect(screen, pad, (140, 180, 255, 28), (140, 180, 255, 90), 999, 1)
            screen.blit(chip, chip.get_rect(center=pad.center))

    def _column(self, screen, fonts, box, key, title, accent, meta, payload, empty):
        if payload != self._seen.get(key):
            self._seen[key] = payload
            self._flash[key] = time.time()
            self.scrolls[key] = 0
        flashed = max(0.0, 1 - (time.time() - self._flash.get(key, 0)) / 0.65)
        border = draw.mix(accent, WHITE, flashed * 0.45)
        draw.soft_rect(screen, box, (12, 14, 20, 255), (*border, int(46 + 160 * flashed)), 16, 1)
        rail = pygame.Rect(box.x + 14, box.y + 14, 3, 14)
        draw.soft_rect(screen, rail, accent, None, 2)
        head = draw.text(fonts["label"], title, WHITE)
        screen.blit(head, (box.x + 24, box.y + 10))

        well_top = box.y + (64 if meta else 38)
        if meta:
            self._meta_row(screen, fonts, meta, (box.x + 14, box.y + 34), box.right - 14)
        well = pygame.Rect(box.x + 8, well_top, box.w - 16, max(24, box.bottom - 8 - well_top))
        draw.soft_rect(screen, well, (8, 10, 16, 255), None, 12)

        if not payload:
            note = draw.text(fonts["tiny"], empty, MUTED)
            screen.blit(note, note.get_rect(center=well.center))
            self.viewports[key] = well
            self.max_scroll[key] = 0
            return

        gutter = 10
        clip = pygame.Rect(well.x + 10, well.y + 8, well.w - 20 - gutter, well.h - 16)
        page = self._page(key, payload, clip.w, fonts["mono"])
        cap = max(0, page.get_height() - clip.h)
        self.max_scroll[key] = cap
        self.scrolls[key] = max(0, min(cap, self.scrolls[key]))
        self.viewports[key] = clip
        screen.set_clip(clip)
        screen.blit(page, (clip.x, clip.y - self.scrolls[key]))
        screen.set_clip(None)
        if cap:
            self._scrollbar(screen, well, clip, page.get_height(), self.scrolls[key])

    def _meta_row(self, screen, fonts, items, origin, limit):
        x, y = origin
        for text, color, kind in items:
            if kind == "pill":
                label = draw.text(fonts["tiny"], text, WHITE)
                pad = pygame.Rect(x, y, label.get_width() + 16, 22)
                if pad.right > limit:
                    break
                draw.soft_rect(screen, pad, (*color, 42), (*color, 120), 999, 1)
                screen.blit(label, label.get_rect(center=pad.center))
                x = pad.right + 6
                continue
            surf = draw.text(fonts["tiny"], text, color)
            if x + surf.get_width() > limit:
                break
            screen.blit(surf, surf.get_rect(midleft=(x, y + 11)))
            x += surf.get_width() + 10

    def _scrollbar(self, screen, box, clip, content_h, scroll):
        track = pygame.Rect(box.right - 12, clip.y, 3, clip.h)
        draw.soft_rect(screen, track, (255, 255, 255, 16), None, 2)
        thumb_h = max(22, int(track.h * clip.h / content_h))
        span = max(1, track.h - thumb_h)
        cap = max(1, content_h - clip.h)
        thumb = pygame.Rect(track.x, track.y + int(span * (scroll / cap)), 3, thumb_h)
        draw.soft_rect(screen, thumb, (176, 206, 255, 200), None, 2)

    def _page(self, key, payload, width, font):
        cached = self._pages.get(key)
        if cached and cached[0] == payload and cached[1] == width:
            return cached[2]
        lines = self._wrap(self._tokens(payload), font, width)
        line_h = font.get_linesize() + 1
        surf = pygame.Surface((width, max(line_h, line_h * len(lines))), pygame.SRCALPHA)
        for i, runs in enumerate(lines):
            x = 0
            y = i * line_h
            for text, kind in runs:
                piece = font.render(text, True, INK[kind])
                surf.blit(piece, (x, y))
                x += piece.get_width()
        self._pages[key] = (payload, width, surf)
        return surf

    def _tokens(self, payload):
        rows = []
        for line in payload.splitlines() or [""]:
            rows.append(self._tokenize_line(line))
        return rows

    def _tokenize_line(self, line):
        runs = []
        last_key = ""
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == '"':
                j = i + 1
                while j < len(line):
                    if line[j] == "\\":
                        j += 2
                        continue
                    if line[j] == '"':
                        j += 1
                        break
                    j += 1
                word = line[i:j]
                k = j
                while k < len(line) and line[k] == " ":
                    k += 1
                if k < len(line) and line[k] == ":":
                    last_key = word.strip('"')
                    kind = "key"
                elif last_key == "choice":
                    kind = "choice"
                else:
                    kind = "str"
                runs.append((word, kind))
                i = j
                continue
            if ch.isdigit() or (ch == "-" and i + 1 < len(line) and line[i + 1].isdigit()):
                j = i + 1
                while j < len(line) and line[j] in "0123456789.eE+-":
                    j += 1
                runs.append((line[i:j], "num"))
                i = j
                continue
            for word, kind in (("true", "bool"), ("false", "bool"), ("null", "bool")):
                if line.startswith(word, i):
                    runs.append((word, kind))
                    i += len(word)
                    break
            else:
                runs.append((ch, "punct"))
                i += 1
                continue
            continue
        return runs

    def _wrap(self, rows, font, width):
        wrapped = []
        for runs in rows:
            line, used = [], 0
            for text, kind in runs:
                for part in self._chunks(text):
                    if part == " " and used + font.size(part)[0] > width:
                        continue
                    size = font.size(part)[0]
                    if line and used + size > width:
                        wrapped.append(line)
                        line, used = [], 0
                        if part == " ":
                            continue
                    if size > width:
                        rest = part
                        while rest:
                            piece, rest = self._fit(font, rest, width if not line else width - used)
                            if not piece:
                                if line:
                                    wrapped.append(line)
                                    line, used = [], 0
                                    continue
                                piece, rest = rest[0], rest[1:]
                            line.append((piece, kind))
                            used += font.size(piece)[0]
                            if rest:
                                wrapped.append(line)
                                line, used = [], 0
                        continue
                    line.append((part, kind))
                    used += size
            wrapped.append(line or [("", "punct")])
        return wrapped or [[("", "punct")]]

    def _chunks(self, text):
        if " " not in text:
            return [text] if text else []
        parts, buf = [], ""
        for ch in text:
            if ch == " ":
                if buf:
                    parts.append(buf)
                    buf = ""
                parts.append(" ")
            else:
                buf += ch
        if buf:
            parts.append(buf)
        return parts

    def _fit(self, font, text, width):
        if width <= 0:
            return "", text
        if font.size(text)[0] <= width:
            return text, ""
        lo, hi = 0, len(text)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if font.size(text[:mid])[0] <= width:
                lo = mid
            else:
                hi = mid - 1
        if lo <= 0:
            return "", text
        return text[:lo], text[lo:]

    def _read(self, payload):
        if not payload:
            return None
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return None

    def _input_meta(self, data):
        legal = (data or {}).get("state", {}).get("legal") or []
        return [(name, AMBER, "pill") for name in legal]

    def _output_meta(self, data, session):
        move = ((data or {}).get("answers") or {}).get("move") or {}
        choice = move.get("choice")
        if not choice:
            return []
        conf = float(move.get("confidence", session.jev.probs.get(choice, 0)))
        model = (data or {}).get("model") or session.jev.last_model
        return [(choice, BLUE, "pill"), (f"{conf:.0%}", BLUE, "text"), (model, MUTED, "text")]
