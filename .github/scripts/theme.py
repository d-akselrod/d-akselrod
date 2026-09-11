"""Palettes and shared SVG primitives for the profile card renderer."""

FONT_SANS = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,"
             "Helvetica,Arial,sans-serif")
FONT_MONO = ("ui-monospace,SFMono-Regular,'SF Mono','Cascadia Mono',"
             "Menlo,Consolas,'Liberation Mono',monospace")

THEMES = {
    "dark": {
        "bg": "#0B0F17",
        "surface": "#0F1522",
        "chip": "#121A28",
        "border": "#1E2A3C",
        "grid": "#16213200",
        "dot": "#1B2739",
        "text": "#E8EEF6",
        "muted": "#8A99AD",
        "faint": "#5C6B80",
        "a1": "#22D3EE",
        "a2": "#A78BFA",
        "a3": "#60A5FA",
        "track": "#18222F",
    },
    "light": {
        "bg": "#FFFFFF",
        "surface": "#F7F9FC",
        "chip": "#FFFFFF",
        "border": "#D8E0EA",
        "grid": "#00000000",
        "dot": "#DDE5EF",
        "text": "#0C1420",
        "muted": "#5A6B80",
        "faint": "#8494A6",
        "a1": "#0E9BB8",
        "a2": "#7C3AED",
        "a3": "#2563EB",
        "track": "#E9EEF5",
    },
}

# Monospace advance width as a fraction of font-size. Used to size chips so
# text never overflows its border on platforms with wider mono fonts.
MONO_ADVANCE = 0.62


def mono_width(text, size):
    return len(text) * size * MONO_ADVANCE


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def text_el(x, y, content, size=14, fill="#fff", family=FONT_MONO,
            weight="400", anchor="start", opacity=None, spacing=None):
    attrs = [
        f'x="{x:.1f}"', f'y="{y:.1f}"',
        f'font-family="{family}"', f'font-size="{size}"',
        f'font-weight="{weight}"', f'fill="{fill}"',
    ]
    if anchor != "start":
        attrs.append(f'text-anchor="{anchor}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    if spacing is not None:
        attrs.append(f'letter-spacing="{spacing}"')
    return f'<text {" ".join(attrs)}>{esc(content)}</text>'


def card(w, h, t, radius=16, fill=None):
    """Outer rounded panel every card shares.

    Pass fill="none" when the panel is stroked on top of existing artwork.
    """
    return (f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" '
            f'rx="{radius}" fill="{fill or t["bg"]}" stroke="{t["border"]}" '
            f'stroke-width="1.5"/>')


def svg_open(w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(label)}">')
