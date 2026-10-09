"""Gaya visual per elemen (background, garis, bayangan, padding, lebar)."""
import copy

from ui_builder.core.config import ELEMENT_STYLE_DEFAULTS
from ui_builder.core.utils import clamp_int, esc


def ensure_element_style(el):
    # Gaya visual disimpan di key terpisah ("visual_style") supaya properti
    # semantik seperti `style` pada daftar (bullet/number) tidak tertimpa.
    legacy = el.get("style")
    if isinstance(legacy, dict):
        visual = el.setdefault("visual_style", {})
        for k, v in legacy.items():
            visual.setdefault(k, copy.deepcopy(v))
        el.pop("style", None)
    elif "visual_style" not in el:
        el["visual_style"] = {}
    visual = el["visual_style"]
    for k, v in ELEMENT_STYLE_DEFAULTS.items():
        visual.setdefault(k, copy.deepcopy(v))
    return visual


def element_style_attr(el, extra=""):
    style = ensure_element_style(el)
    bg = style.get("background", "transparent")
    color = style.get("color", "inherit")
    border_color = style.get("border_color", "#d1d5db")
    border_width = max(0, min(8, int(style.get("border_width", 0) or 0)))
    radius = max(0, min(80, int(style.get("radius", 8) or 0)))
    padding = max(0, min(80, int(style.get("padding", 0) or 0)))
    shadow = style.get("shadow", "none")
    width = style.get("width", "auto")
    return (
        f'background:{esc(bg)};color:{esc(color)};'
        f'border:{border_width}px solid {esc(border_color)};'
        f'border-radius:{radius}px;box-shadow:{esc(shadow)};'
        f'padding:{padding}px;width:{esc(width)};' + extra
    )


def soft_style(el, extra=""):
    """Gaya inline hanya untuk properti yang diubah pengguna, agar gaya bawaan bar tetap tampil."""
    s = ensure_element_style(el)
    d = ELEMENT_STYLE_DEFAULTS
    out = []
    if s.get("background") != d["background"]:
        out.append(f'background:{esc(s.get("background"))}')
    if s.get("color") != d["color"]:
        out.append(f'color:{esc(s.get("color"))}')
    bw = clamp_int(s.get("border_width"), 0, 8, 0)
    if bw:
        out.append(f'border:{bw}px solid {esc(s.get("border_color", "#d1d5db"))}')
    if clamp_int(s.get("radius"), 0, 80, 8) != d["radius"]:
        out.append(f'border-radius:{clamp_int(s.get("radius"), 0, 80, 8)}px')
    if s.get("shadow") != d["shadow"]:
        out.append(f'box-shadow:{esc(s.get("shadow"))}')
    if clamp_int(s.get("padding"), 0, 80, 0):
        out.append(f'padding:{clamp_int(s.get("padding"), 0, 80, 0)}px')
    if s.get("width") != d["width"]:
        out.append(f'width:{esc(s.get("width"))}')
    css = ";".join(out)
    if extra:
        css = (css + ";" if css else "") + extra
    return css
