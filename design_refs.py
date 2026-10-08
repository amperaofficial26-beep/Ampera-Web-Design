"""Referensi gaya desain (Minimalis, Glassmorphism, dst.) dan pratinjau kecilnya."""
from bar_specs import BAR_SPECS
from config import FONTS
from design import theme_of
from utils import esc, on_color, with_alpha

DESIGN_REFS = {
    "Minimalis": {
        "desc": "Putih bersih, banyak ruang kosong, satu warna aksen tegas.",
        "theme": theme_of("#111827", "#ffffff", "#111827", "Sans-serif modern", 700),
        "shape": {"radius": 6, "border_width": 1, "border_color": "#e5e7eb", "shadow": "none"},
        "surface": "transparent", "ink": "inherit",
    },
    "Glassmorphism": {
        "desc": "Lapisan kaca tembus pandang di atas latar berwarna, sudut lembut dan bayangan halus.",
        "theme": theme_of("#7c3aed", "#e0e7ff", "#1e1b4b", "Humanis", 760, glass=True, glass_blur=20),
        "shape": {"radius": 22, "border_width": 1, "border_color": "#ffffff",
                  "shadow": "0 8px 32px rgba(31,38,135,.2)"},
        "surface": "rgba(255,255,255,.5)", "ink": "inherit",
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
    # ---- 20 referensi gaya tambahan ----
    "Neumorphism": {
        "desc": "Permukaan lembut dengan bayangan ganda, terasa seperti tombol fisik.",
        "theme": theme_of("#4c6ef5", "#e8ecf3", "#3b4252", "Sans-serif modern", 760),
        "shape": {"radius": 18, "border_width": 0, "border_color": "#dbe1ea",
                  "shadow": "8px 8px 16px rgba(0,0,0,.12), -8px -8px 16px rgba(255,255,255,.9)"},
        "surface": "#eef1f6", "ink": "#3b4252",
    },
    "Material You": {
        "desc": "Sudut besar dan warna hangat khas Material 3, lembut untuk aplikasi harian.",
        "theme": theme_of("#6750a4", "#fffbfe", "#1c1b1f", "Sans-serif modern", 780),
        "shape": {"radius": 20, "border_width": 1, "border_color": "#e7e0ec",
                  "shadow": "0 2px 8px rgba(0,0,0,.08)"},
        "surface": "#f3edf7", "ink": "#1c1b1f",
    },
    "Gaya iOS": {
        "desc": "Biru sistem, latar abu terang, dan kartu bulat khas aplikasi iOS.",
        "theme": theme_of("#007aff", "#f2f2f7", "#1c1c1e", "Humanis", 760),
        "shape": {"radius": 16, "border_width": 1, "border_color": "#e5e5ea",
                  "shadow": "0 2px 8px rgba(0,0,0,.08)"},
        "surface": "#ffffff", "ink": "inherit",
    },
    "Flat modern": {
        "desc": "Tanpa bayangan, garis tipis rapi, fokus pada tipografi dan jarak.",
        "theme": theme_of("#2563eb", "#f8fafc", "#0f172a", "Sans-serif modern", 800),
        "shape": {"radius": 10, "border_width": 1, "border_color": "#e2e8f0", "shadow": "none"},
        "surface": "#ffffff", "ink": "inherit",
    },
    "Claymorphism": {
        "desc": "Bentuk tebal membulat seperti tanah liat, ceria tapi tetap lembut.",
        "theme": theme_of("#8b5cf6", "#eef2ff", "#312e81", "Humanis", 760),
        "shape": {"radius": 24, "border_width": 2, "border_color": "#ffffff",
                  "shadow": "0 10px 24px rgba(99,102,241,.22)"},
        "surface": "#ffffff", "ink": "#312e81",
    },
    "Aurora gradien": {
        "desc": "Latar gelap dengan aksen sian keunguan seperti cahaya aurora.",
        "theme": theme_of("#06b6d4", "#0f172a", "#e2e8f0", "Humanis", 780),
        "shape": {"radius": 20, "border_width": 1, "border_color": "#1e3a5f",
                  "shadow": "0 12px 30px rgba(6,182,212,.28)"},
        "surface": "#1e293b", "ink": "#e2e8f0",
    },
    "Neo-Memphis": {
        "desc": "Warna ceria, garis hitam tebal, dan bayangan keras ala Memphis baru.",
        "theme": theme_of("#f43f5e", "#fef9c3", "#111827", "Humanis", 740),
        "shape": {"radius": 16, "border_width": 2, "border_color": "#111827", "shadow": "5px 5px 0 #111827"},
        "surface": "#ffffff", "ink": "#111827",
    },
    "Swiss tipografi": {
        "desc": "Grid ketat, satu warna aksen, hierarki jelas khas gaya tipografi Swiss.",
        "theme": theme_of("#e11d48", "#ffffff", "#111111", "Sans-serif modern", 720),
        "shape": {"radius": 2, "border_width": 1, "border_color": "#111111", "shadow": "none"},
        "surface": "#ffffff", "ink": "#111111",
    },
    "Brutalisme lembut": {
        "desc": "Garis tegas dan sudut kaku, tapi warnanya hangat dan mudah dibaca.",
        "theme": theme_of("#f97316", "#fff7ed", "#1f2937", "Humanis", 760),
        "shape": {"radius": 12, "border_width": 2, "border_color": "#1f2937", "shadow": "4px 4px 0 #1f2937"},
        "surface": "#ffffff", "ink": "#1f2937",
    },
    "Editorial majalah": {
        "desc": "Serif klasik, margin lega, dan aksen merah seperti rubrik majalah cetak.",
        "theme": theme_of("#b91c1c", "#fffdf7", "#1c1917", "Serif klasik", 700),
        "shape": {"radius": 2, "border_width": 1, "border_color": "#d6d3d1", "shadow": "none"},
        "surface": "#ffffff", "ink": "#1c1917",
    },
    "Monokrom kontras": {
        "desc": "Hitam putih tanpa warna pengganggu, fokus penuh pada bentuk dan kontras.",
        "theme": theme_of("#111827", "#f5f5f5", "#0a0a0a", "Sans-serif modern", 760),
        "shape": {"radius": 4, "border_width": 2, "border_color": "#111827", "shadow": "none"},
        "surface": "#ffffff", "ink": "#0a0a0a",
    },
    "Retro terminal": {
        "desc": "Hijau fosfor di atas hitam, huruf monospace, nuansa layar terminal lama.",
        "theme": theme_of("#22c55e", "#0b0f0c", "#a7f3d0", "Monospace", 780),
        "shape": {"radius": 4, "border_width": 1, "border_color": "#166534",
                  "shadow": "0 6px 18px rgba(0,0,0,.45)"},
        "surface": "#052e16", "ink": "#86efac",
    },
    "Y2K nostalgia": {
        "desc": "Gradien pastel, kilau lembut, dan sudut bulat khas antarmuka tahun 2000-an.",
        "theme": theme_of("#a855f7", "#e0f2fe", "#312e81", "Humanis", 760),
        "shape": {"radius": 22, "border_width": 2, "border_color": "#c4b5fd",
                  "shadow": "0 6px 18px rgba(168,85,247,.28)"},
        "surface": "#ffffff", "ink": "#312e81",
    },
    "Neon cyberpunk": {
        "desc": "Ungu gelap dengan garis neon menyala, terasa futuristik dan malam.",
        "theme": theme_of("#ec4899", "#0b0616", "#f5d0fe", "Monospace", 780),
        "shape": {"radius": 6, "border_width": 1, "border_color": "#7c3aed",
                  "shadow": "0 0 22px rgba(236,72,153,.45)"},
        "surface": "#1b0f2e", "ink": "#f5d0fe",
    },
    "Zen Jepang": {
        "desc": "Warna kertas dan batu, ruang lega, garis tipis, terasa tenang.",
        "theme": theme_of("#78716c", "#faf7f2", "#292524", "Serif elegan", 680),
        "shape": {"radius": 3, "border_width": 1, "border_color": "#d6cfc4", "shadow": "none"},
        "surface": "#f5f1ea", "ink": "#292524",
    },
    "Art Deco": {
        "desc": "Emas dan gelap, garis tegas geometris, berkesan mewah dan klasik.",
        "theme": theme_of("#c9a227", "#101418", "#f5e6c8", "Serif elegan", 780),
        "shape": {"radius": 0, "border_width": 2, "border_color": "#c9a227",
                  "shadow": "0 8px 24px rgba(0,0,0,.35)"},
        "surface": "#1b2028", "ink": "#f5e6c8",
    },
    "Bauhaus": {
        "desc": "Bentuk dasar dan warna primer, sudut siku dengan komposisi tegas.",
        "theme": theme_of("#dc2626", "#f5f0e1", "#1a1a1a", "Sans-serif modern", 780),
        "shape": {"radius": 0, "border_width": 3, "border_color": "#1a1a1a",
                  "shadow": "0 4px 12px rgba(0,0,0,.12)"},
        "surface": "#ffffff", "ink": "#1a1a1a",
    },
    "Skandinavia hangat": {
        "desc": "Kayu terang, warna tanah, dan sudut membulat yang terasa ramah.",
        "theme": theme_of("#b45309", "#fdf6ec", "#3f3a34", "Humanis", 780),
        "shape": {"radius": 14, "border_width": 1, "border_color": "#e7d8c3",
                  "shadow": "0 2px 8px rgba(0,0,0,.08)"},
        "surface": "#ffffff", "ink": "#3f3a34",
    },
    "Bento grid": {
        "desc": "Blok besar membulat seperti kotak bento, rapi untuk dasbor dan galeri.",
        "theme": theme_of("#0ea5e9", "#f1f5f9", "#0f172a", "Sans-serif modern", 860),
        "shape": {"radius": 26, "border_width": 1, "border_color": "#e2e8f0",
                  "shadow": "0 8px 32px rgba(31,38,135,.12)"},
        "surface": "#ffffff", "ink": "inherit",
    },
    "Hijau berkelanjutan": {
        "desc": "Nuansa hijau segar untuk brand ramah lingkungan dan gaya hidup sehat.",
        "theme": theme_of("#15803d", "#f0fdf4", "#14532d", "Humanis", 780),
        "shape": {"radius": 18, "border_width": 1, "border_color": "#bbf7d0",
                  "shadow": "0 2px 8px rgba(21,128,61,.16)"},
        "surface": "#ffffff", "ink": "#14532d",
    },
}

# Tambahkan koleksi gaya baru, sambil mempertahankan semua referensi sebelumnya.
from design_refs_extra import EXTRA_DESIGN_REFS  # noqa: E402

DESIGN_REFS.update(EXTRA_DESIGN_REFS)

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
    # Preset bergaya kaca diberi latar berwarna + blur agar efeknya terlihat.
    if th.get("glass"):
        backdrop = (
            f'background:radial-gradient(240px 140px at 10% -20%, {with_alpha(th["primary"], .55)}, transparent 65%),'
            f'radial-gradient(220px 150px at 98% 120%, {with_alpha("#ec4899", .40)}, transparent 62%),'
            f'{esc(th["bg"])};'
            "-webkit-backdrop-filter:blur(14px) saturate(160%);backdrop-filter:blur(14px) saturate(160%);"
        )
    else:
        backdrop = f'background:{esc(th["bg"])};'
    glass = f'background:{esc(surface)};'
    if th.get("glass"):
        glass += "-webkit-backdrop-filter:blur(14px) saturate(160%);backdrop-filter:blur(14px) saturate(160%);"
    return (
        f'<div class="ref-prev" style="{backdrop}color:{esc(th["text"])};font-family:{esc(font)}">'
        f'<div class="ref-card" style="{glass}color:{esc(ink)};border:{esc(border)};'
        f'border-radius:{sh["radius"]}px;box-shadow:{esc(sh["shadow"])}"><b>Judul kartu</b>'
        f'<span>Contoh teks isi singkat.</span></div>'
        f'<span class="ref-btn" style="background:{esc(th["primary"])};border-radius:{sh["radius"]}px;'
        f'color:{on_color(th["primary"])};border:{esc(border)};box-shadow:{esc(sh["shadow"])}">Tombol</span></div>'
    )
