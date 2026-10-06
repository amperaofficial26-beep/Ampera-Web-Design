"""Referensi gaya desain (Minimalis, Glassmorphism, dst.) dan pratinjau kecilnya."""
from bar_specs import BAR_SPECS
from config import FONTS
from design import theme_of
from utils import esc, on_color

DESIGN_REFS = {
    "Minimalis": {
        "desc": "Putih bersih, banyak ruang kosong, satu warna aksen tegas.",
        "theme": theme_of("#111827", "#ffffff", "#111827", "Sans-serif modern", 700),
        "shape": {"radius": 6, "border_width": 1, "border_color": "#e5e7eb", "shadow": "none"},
        "surface": "transparent", "ink": "inherit",
    },
    "Glassmorphism": {
        "desc": "Lapisan kaca tembus pandang dengan sudut lembut dan bayangan halus.",
        "theme": theme_of("#7c3aed", "#e0e7ff", "#1e1b4b", "Humanis", 760),
        "shape": {"radius": 22, "border_width": 1, "border_color": "#ffffff", "shadow": "0 8px 32px rgba(31,38,135,.2)"},
        "surface": "#ffffff99", "ink": "inherit",
    },
    "Neo-brutalism": {
        "desc": "Garis tebal, bayangan keras tanpa blur, warna mencolok.",
        "theme": theme_of("#ff5c00", "#fff7e6", "#111111", "Monospace", 720),
        "shape": {"radius": 0, "border_width": 3, "border_color": "#111111", "shadow": "6px 6px 0 #111111"},
        "surface": "#ffffff", "ink": "#111111",
    },
    "Mode gelap": {
        "desc": "Latar biru malam dengan aksen sian, nyaman untuk dibaca malam hari.",
        "theme": theme_of("#22d3ee", "#0b1220", "#e5e7eb", "Sans-serif modern", 760),
        "shape": {"radius": 14, "border_width": 1, "border_color": "#1f2a44", "shadow": "0 6px 18px rgba(0,0,0,.35)"},
        "surface": "#111a2e", "ink": "#e5e7eb",
    },
    "Pastel": {
        "desc": "Warna lembut, sudut sangat membulat, terasa ramah dan ceria.",
        "theme": theme_of("#f472b6", "#fff1f5", "#4a2c3a", "Humanis", 680),
        "shape": {"radius": 26, "border_width": 2, "border_color": "#fbcfe8", "shadow": "0 2px 8px rgba(0,0,0,.08)"},
        "surface": "#ffffff", "ink": "inherit",
    },
    "Korporat": {
        "desc": "Biru tegas dan sudut rapi, cocok untuk perusahaan dan layanan resmi.",
        "theme": theme_of("#1d4ed8", "#f8fafc", "#0f172a", "Serif elegan", 820),
        "shape": {"radius": 4, "border_width": 1, "border_color": "#cbd5e1", "shadow": "0 2px 8px rgba(0,0,0,.08)"},
        "surface": "#ffffff", "ink": "inherit",
    },
}

SHAPE_TYPES = {"card", "button", "image", "gallery", "input"} | set(BAR_SPECS)
SURFACE_TYPES = {"card"} | (set(BAR_SPECS) - {"announcement", "fab", "progressbar", "stepper", "searchbar"})


def swatches_html(theme):
    dots = "".join(
        f'<span class="tpl-sw" style="background:{esc(theme[k])}"></span>' for k in ("primary", "bg", "text")
    )
    return f'<div class="tpl-sws">{dots}</div>'


def ref_preview_html(ref):
    th, sh = ref["theme"], ref["shape"]
    font = FONTS.get(th["font"], FONTS["Sans-serif modern"])
    surface = ref["surface"]
    ink = ref["ink"] if ref["ink"] != "inherit" else th["text"]
    border = f'{sh["border_width"]}px solid {sh["border_color"]}'
    return (
        f'<div class="ref-prev" style="background:{esc(th["bg"])};color:{esc(th["text"])};font-family:{esc(font)}">'
        f'<div class="ref-card" style="background:{esc(surface)};color:{esc(ink)};border:{esc(border)};'
        f'border-radius:{sh["radius"]}px;box-shadow:{esc(sh["shadow"])}"><b>Judul kartu</b>'
        f'<span>Contoh teks isi singkat.</span></div>'
        f'<span class="ref-btn" style="background:{esc(th["primary"])};border-radius:{sh["radius"]}px;'
        f'color:{on_color(th["primary"])};border:{esc(border)};box-shadow:{esc(sh["shadow"])}">Tombol</span></div>'
    )
