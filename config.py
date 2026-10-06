"""Konstanta dan konfigurasi dasar UI Builder."""
import copy
from pathlib import Path

from bar_specs import BAR_SPECS

ELEMENT_LABELS = {
    "navbar": "Menu navigasi",
    "heading": "Judul",
    "text": "Paragraf",
    "button": "Tombol",
    "image": "Gambar",
    "gallery": "Galeri",
    "list": "Daftar",
    "input": "Kolom isian",
    "card": "Kartu",
    "divider": "Garis",
    "spacer": "Jarak",
    "footer": "Footer",
}

ELEMENT_DEFAULTS = {
    "navbar": {
        "brand": "Merek Saya",
        "links": "Beranda|#\nTentang|#\nKontak|#",
    },
    "heading": {"text": "Judul baru", "size": 36, "align": "left"},
    "text": {"text": "Tulis isi paragraf di sini.", "align": "left"},
    "button": {"text": "Klik di sini", "link": "", "align": "left"},
    "image": {
        "url": "https://picsum.photos/800/400",
        "alt": "Gambar",
        "radius": 12,
    },
    "gallery": {
        "urls": "https://picsum.photos/400/300?random=1\n"
        "https://picsum.photos/400/300?random=2\n"
        "https://picsum.photos/400/300?random=3",
        "columns": 3,
        "radius": 8,
    },
    "list": {"items": "Item pertama\nItem kedua\nItem ketiga", "style": "bullet"},
    "input": {"label": "Nama", "placeholder": "Ketik di sini", "kind": "text"},
    "card": {"title": "Judul kartu", "text": "Isi singkat kartu."},
    "divider": {},
    "spacer": {"height": 24},
    "footer": {"text": "© 2026 Aplikasi Saya"},
}

FONTS = {
    "Sans-serif modern": "'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    "Serif klasik": "Georgia, 'Times New Roman', serif",
    "Monospace": "'Courier New', Consolas, monospace",
    "Humanis": "'Trebuchet MS', 'Segoe UI', Verdana, sans-serif",
    "Serif elegan": "'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif",
}

ALIGNS = ["left", "center", "right"]

DEVICES = {
    "Ponsel (390 px)": 390,
    "Tablet (768 px)": 768,
    "Desktop (penuh)": None,
}

PANEL_HEIGHT = 780
PROJECTS_DIR = Path(__file__).resolve().parent / "projects"

ICONS = {}

INPUT_KINDS = {
    "text": "Teks",
    "email": "Email",
    "password": "Kata sandi",
    "number": "Angka",
    "tel": "Telepon",
}

# Gaya visual umum yang bisa diedit pada setiap elemen.
ELEMENT_STYLE_DEFAULTS = {
    "background": "transparent",
    "color": "inherit",
    "border_color": "#d1d5db",
    "border_width": 0,
    "radius": 8,
    "shadow": "none",
    "padding": 0,
    "width": "auto",
}

SHADOW_OPTIONS = {
    "Tanpa bayangan": "none",
    "Halus": "0 2px 8px rgba(0,0,0,.08)",
    "Sedang": "0 6px 18px rgba(0,0,0,.12)",
    "Kuat": "0 12px 30px rgba(0,0,0,.18)",
    "Kaca": "0 8px 32px rgba(31,38,135,.2)",
    "Gelap": "0 6px 18px rgba(0,0,0,.35)",
    "Brutal": "6px 6px 0 #111111",
}

WIDTH_OPTIONS = {
    "Auto": "auto",
    "100%": "100%",
    "90%": "90%",
    "75%": "75%",
    "50%": "50%",
}

# Gabungkan komponen bar ke daftar elemen utama.
ELEMENT_GROUP = {t: "Dasar" for t in ELEMENT_LABELS}
ELEMENT_GROUP["navbar"] = "Navigasi"
for _t, _s in BAR_SPECS.items():
    ELEMENT_LABELS[_t] = _s["label"]
    ELEMENT_DEFAULTS[_t] = copy.deepcopy(_s["defaults"])
    ICONS[_t] = _s["icon"]
    ELEMENT_GROUP[_t] = _s["group"]
ICONS.update({
    "navbar": "menu", "heading": "title", "text": "notes", "button": "smart_button", "image": "image",
    "gallery": "photo_library", "list": "format_list_bulleted", "input": "edit_note",
    "card": "branding_watermark", "divider": "horizontal_rule", "spacer": "height", "footer": "call_to_action",
})
