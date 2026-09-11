"""SVG builders for each profile card."""

import math

from theme import (FONT_MONO, FONT_SANS, MONO_ADVANCE, card, esc, mono_width,
                   svg_open, text_el)

# Abstract agent-graph motif used in the hero. Hand-placed so the silhouette
# stays balanced instead of looking randomly scattered.
NODES = [(792, 94), (864, 62), (934, 106), (886, 134), (808, 160),
         (874, 198), (942, 178)]
EDGES = [(0, 1), (1, 2), (1, 3), (0, 3), (3, 4), (3, 5), (5, 6), (2, 6),
         (4, 5)]
PULSE_EDGES = [(0, 1), (3, 5), (2, 6)]


def _defs(t):
    a1, a2, a3 = t["a1"], t["a3"], t["a2"]
    return f"""<defs>
<linearGradient id="nameGrad" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0" stop-color="{a1}"><animate attributeName="stop-color" values="{a1};{a3};{a2};{a1}" dur="9s" repeatCount="indefinite"/></stop>
<stop offset="1" stop-color="{a2}"><animate attributeName="stop-color" values="{a2};{a1};{a3};{a2}" dur="9s" repeatCount="indefinite"/></stop>
</linearGradient>
<linearGradient id="ruleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0" stop-color="{a1}"/><stop offset="0.45" stop-color="{a3}"/>
<stop offset="1" stop-color="{a2}" stop-opacity="0"/>
</linearGradient>
<radialGradient id="orbA" cx="50%" cy="50%" r="50%">
<stop offset="0" stop-color="{a1}" stop-opacity="0.22"/>
<stop offset="1" stop-color="{a1}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="orbB" cx="50%" cy="50%" r="50%">
<stop offset="0" stop-color="{a2}" stop-opacity="0.20"/>
<stop offset="1" stop-color="{a2}" stop-opacity="0"/>
</radialGradient>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
<circle cx="1.5" cy="1.5" r="1.2" fill="{t['dot']}"/>
</pattern>
<clipPath id="heroClip"><rect x="0" y="0" width="1000" height="260" rx="18"/></clipPath>
</defs>"""


def _graph(t):
    out = []
    for i, j in EDGES:
        x1, y1 = NODES[i]
        x2, y2 = NODES[j]
        out.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{t["a3"]}" stroke-width="1" opacity="0.28"/>')
    for n, (x, y) in enumerate(NODES):
        colour = [t["a1"], t["a2"], t["a3"]][n % 3]
        delay = n * 0.45
        out.append(
            f'<circle cx="{x}" cy="{y}" r="3.4" fill="{colour}" opacity="0.85">'
            f'<animate attributeName="r" values="3.4;5.2;3.4" dur="3.6s" '
            f'begin="{delay:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.85;0.35;0.85" '
            f'dur="3.6s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
            f'</circle>')
    for n, (i, j) in enumerate(PULSE_EDGES):
        x1, y1 = NODES[i]
        x2, y2 = NODES[j]
        out.append(
            f'<circle r="2.4" fill="{t["a1"]}" opacity="0.9">'
            f'<animateMotion dur="2.8s" begin="{n * 0.9:.2f}s" '
            f'repeatCount="indefinite" path="M{x1},{y1} L{x2},{y2}"/>'
            f'<animate attributeName="opacity" values="0;0.9;0" dur="2.8s" '
            f'begin="{n * 0.9:.2f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def hero(t, name, role, meta):
    w, h = 1000, 260
    p = []
    p.append(svg_open(w, h, f"{name} — {role}"))
    p.append(_defs(t))
    p.append('<g clip-path="url(#heroClip)">')
    p.append(f'<rect width="{w}" height="{h}" fill="{t["bg"]}"/>')
    p.append(f'<rect width="{w}" height="{h}" fill="url(#dots)" opacity="0.55"/>')
    p.append('<ellipse cx="130" cy="40" rx="320" ry="210" fill="url(#orbA)">'
             '<animateTransform attributeName="transform" type="translate" '
             'values="0,0; 60,26; 0,0" dur="16s" repeatCount="indefinite"/>'
             '</ellipse>')
    p.append('<ellipse cx="880" cy="250" rx="300" ry="200" fill="url(#orbB)">'
             '<animateTransform attributeName="transform" type="translate" '
             'values="0,0; -50,-30; 0,0" dur="20s" repeatCount="indefinite"/>'
             '</ellipse>')
    p.append(_graph(t))

    p.append(text_el(56, 72, "$ whoami", 14, t["a1"], FONT_MONO, "500"))
    cursor_x = 56 + mono_width("$ whoami ", 14)
    p.append(f'<rect x="{cursor_x:.1f}" y="60" width="8" height="15" '
             f'fill="{t["a1"]}" opacity="0.9">'
             f'<animate attributeName="opacity" values="0.9;0.9;0;0" '
             f'dur="1.15s" repeatCount="indefinite"/></rect>')

    p.append(text_el(54, 134, name, 46, "url(#nameGrad)", FONT_SANS, "800",
                     spacing="-1"))
    p.append(f'<rect x="56" y="151" width="340" height="3" rx="1.5" '
             f'fill="url(#ruleGrad)">'
             f'<animate attributeName="width" from="0" to="340" dur="1.1s" '
             f'begin="0.25s" fill="freeze"/></rect>')
    p.append(text_el(56, 186, role, 20, t["text"], FONT_SANS, "600"))
    p.append(text_el(56, 216, meta, 13.5, t["muted"], FONT_MONO, "400"))
    p.append("</g>")
    p.append(card(w, h, t, radius=18, fill="none"))
    p.append("</svg>")
    return "".join(p)


def stack(t, groups):
    """Grouped capability chips. `groups` is a list of (label, [items])."""
    w = 1000
    pad_x, label_w, gap, chip_h = 30, 132, 8, 30
    row_gap, group_gap = 8, 16
    chip_font = 13
    top = 26

    body, y = [], top
    for label, items in groups:
        rows, cur, cur_w = [], [], 0
        avail = w - pad_x - label_w - 24 - pad_x
        for item in items:
            cw = mono_width(item, chip_font) + 26
            if cur and cur_w + cw + gap > avail:
                rows.append(cur)
                cur, cur_w = [], 0
            cur.append((item, cw))
            cur_w += cw + gap
        if cur:
            rows.append(cur)

        block_h = len(rows) * chip_h + (len(rows) - 1) * row_gap
        body.append(text_el(pad_x + label_w, y + chip_h / 2 + 4.5,
                            label.upper(), 11, t["faint"], FONT_MONO, "600",
                            anchor="end", spacing="0.8"))
        body.append(f'<rect x="{pad_x + label_w + 12}" y="{y + 3}" width="2" '
                    f'height="{block_h - 6}" rx="1" fill="{t["border"]}"/>')
        ry = y
        for row in rows:
            rx = pad_x + label_w + 30
            for item, cw in row:
                body.append(
                    f'<rect x="{rx:.1f}" y="{ry}" width="{cw:.1f}" '
                    f'height="{chip_h}" rx="8" fill="{t["chip"]}" '
                    f'stroke="{t["border"]}" stroke-width="1"/>')
                body.append(text_el(rx + cw / 2, ry + 19.5, item, chip_font,
                                    t["text"], FONT_MONO, "500",
                                    anchor="middle"))
                rx += cw + gap
            ry += chip_h + row_gap
        y += block_h + group_gap

    h = y - group_gap + top
    out = [svg_open(w, h, "Technical stack"), card(w, h, t), "".join(body),
           "</svg>"]
    return "".join(out)


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _mix(c1, c2, k):
    a, b = _hex(c1), _hex(c2)
    return "#%02X%02X%02X" % tuple(
        round(a[i] + (b[i] - a[i]) * k) for i in range(3))


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def activity(t, weeks, total, scope):
    """`weeks` is a list of week columns, each a list of (date, count)."""
    w, pad = 1000, 30
    gap = 4
    grid_x, grid_y = pad + 26, 92
    weeks = weeks[-53:]
    # Size the cells to the data so the grid always fills the card width.
    step = (w - pad - grid_x) / max(len(weeks), 53)
    cell = step - gap
    h = grid_y + round(7 * step) + 54

    peak = max((c for wk in weeks for _, c in wk), default=0)
    p = [svg_open(w, h, "Contribution activity"), card(w, h, t)]
    p.append(text_el(pad, 46, "CONTRIBUTION ACTIVITY", 12, t["faint"],
                     FONT_MONO, "600", spacing="1.2"))
    p.append(text_el(w - pad, 46, scope, 12, t["faint"], FONT_MONO, "400",
                     anchor="end"))
    p.append(text_el(pad, 70, f"{total:,}", 21, t["text"], FONT_SANS, "700"))
    p.append(text_el(pad + mono_width(f"{total:,}", 21) * 0.95 + 8, 70,
                     "contributions in the last year", 13, t["muted"],
                     FONT_SANS, "400"))

    seen = set()
    for i, wk in enumerate(weeks):
        if not wk:
            continue
        month = int(wk[0][0][5:7])
        if month not in seen and i < len(weeks) - 2:
            seen.add(month)
            p.append(text_el(grid_x + i * step, grid_y - 9, MONTHS[month - 1],
                             10, t["faint"], FONT_MONO, "400"))
    for row, day in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        p.append(text_el(pad, grid_y + row * step + cell * 0.72, day, 9.5, t["faint"],
                         FONT_MONO, "400"))

    for i, wk in enumerate(weeks):
        for j, (_, count) in enumerate(wk):
            if count <= 0:
                fill, op = t["track"], 1.0
            else:
                k = math.sqrt(min(count / peak, 1.0)) if peak else 0
                fill = _mix(t["a3"], t["a1"], k) if k < 0.5 else \
                    _mix(t["a1"], t["a2"], (k - 0.5) * 2)
                op = 0.35 + 0.65 * k
            p.append(f'<rect x="{grid_x + i * step:.2f}" '
                     f'y="{grid_y + j * step:.2f}" width="{cell:.2f}" '
                     f'height="{cell:.2f}" rx="3" fill="{fill}" '
                     f'opacity="{op:.2f}"/>')

    lx, ly = w - pad - 5 * step - 74, h - 30
    p.append(text_el(lx - 8, ly + cell * 0.72, "Less", 10, t["faint"], FONT_MONO, "400",
                     anchor="end"))
    for i in range(5):
        k = i / 4
        fill = t["track"] if i == 0 else (
            _mix(t["a3"], t["a1"], k) if k < 0.5
            else _mix(t["a1"], t["a2"], (k - 0.5) * 2))
        p.append(f'<rect x="{lx + i * step:.2f}" y="{ly}" '
                 f'width="{cell:.2f}" height="{cell:.2f}" rx="3" fill="{fill}" '
                 f'opacity="{1.0 if i == 0 else 0.35 + 0.65 * k:.2f}"/>')
    p.append(text_el(lx + 5 * step + 4, ly + cell * 0.72, "More", 10, t["faint"],
                     FONT_MONO, "400"))
    p.append("</svg>")
    return "".join(p)


def credentials(t, education, certs, accent="#FF9900"):
    """Two-column education / certification panel.

    `education` and `certs` are lists of (title, subtitle) pairs.
    """
    w, pad, h = 1000, 30, 196
    split = 560

    p = [svg_open(w, h, "Education and certifications"), card(w, h, t)]
    p.append(text_el(pad, 44, "EDUCATION", 12, t["faint"], FONT_MONO, "600",
                     spacing="1.2"))
    p.append(text_el(split + 30, 44, "CERTIFICATIONS", 12, t["faint"],
                     FONT_MONO, "600", spacing="1.2"))
    p.append(f'<rect x="{pad}" y="60" width="{w - pad * 2}" height="1" '
             f'fill="{t["border"]}"/>')
    p.append(f'<rect x="{split}" y="76" width="1" height="{h - 106}" '
             f'fill="{t["border"]}"/>')

    for i, (title, subtitle) in enumerate(education[:2]):
        y = 104 + i * 52
        p.append(f'<rect x="{pad}" y="{y - 13}" width="3" height="34" rx="1.5" '
                 f'fill="{t["a1"] if i == 0 else t["a2"]}"/>')
        p.append(text_el(pad + 16, y, title, 15.5, t["text"], FONT_SANS, "650"))
        p.append(text_el(pad + 16, y + 19, subtitle, 12, t["muted"], FONT_MONO,
                         "400"))

    for i, (title, subtitle) in enumerate(certs[:2]):
        y = 104 + i * 52
        cx, cy = split + 39, y - 4
        p.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{accent}" '
                 f'opacity="0.16"/>')
        p.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{accent}">'
                 f'<animate attributeName="opacity" values="1;0.45;1" '
                 f'dur="3.4s" begin="{i * 1.1:.1f}s" repeatCount="indefinite"/>'
                 f'</circle>')
        p.append(text_el(split + 58, y, title, 15.5, t["text"], FONT_SANS,
                         "650"))
        p.append(text_el(split + 58, y + 19, subtitle, 12, t["muted"],
                         FONT_MONO, "400"))
    p.append("</svg>")
    return "".join(p)
