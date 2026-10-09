"""Fungsi bantu umum (tanpa Streamlit)."""
import html
import re

from ui_builder.core.config import ALIGNS, INPUT_KINDS


def esc(value):
    return html.escape(str(value), quote=True)


def mi(name):
    """Ikon Material Symbols untuk HTML hasil (nama dibersihkan)."""
    name = re.sub(r"[^a-z0-9_]", "", str(name or "").lower()) or "circle"
    return f'<span class="mi" aria-hidden="true">{name}</span>'


def safe_url(url):
    url = str(url).strip()
    if url.lower().startswith(("http://", "https://", "mailto:", "#", "data:image/")):
        return url
    return "#"


def num(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def clamp_int(value, lo, hi, default):
    try:
        n = int(float(value))
    except (TypeError, ValueError):
        n = default
    return max(lo, min(hi, n))


def lines_of(value):
    return [ln.strip() for ln in str(value or "").splitlines() if ln.strip()]


def parts_of(value, n):
    """Pecah tiap baris 'a|b|c' menjadi daftar n kolom (dilengkapi string kosong)."""
    rows = []
    for ln in lines_of(value):
        cols = [c.strip() for c in ln.split("|")]
        cols += [""] * (n - len(cols))
        rows.append(cols[:n])
    return rows


def parse_links(value):
    result = []
    for ln in lines_of(value):
        if "|" in ln:
            label, url = ln.split("|", 1)
        else:
            label, url = ln, "#"
        result.append((label.strip(), url.strip() or "#"))
    return result


def input_kind(el):
    return el.get("kind") if el.get("kind") in INPUT_KINDS else "text"


def align_of(el):
    return el.get("align", "left") if el.get("align") in ALIGNS else "left"


def with_alpha(hex_color, alpha):
    """Ubah warna heksadesimal menjadi rgba() agar bisa ditumpuk sebagai lapisan kaca."""
    h = str(hex_color).strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    try:
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return f"rgba(99, 102, 241, {alpha})"
    return f"rgba({r}, {g}, {b}, {alpha})"


def on_color(hex_color):
    """Pilih teks gelap atau terang agar terbaca di atas warna utama."""
    h = str(hex_color).strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    try:
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return "#ffffff"
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#111827" if lum > 0.62 else "#ffffff"
