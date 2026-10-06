import copy
import hashlib
from datetime import datetime
import html
import json
import re
import tempfile
import uuid
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="UI Builder",
    page_icon=":material/widgets:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Konfigurasi dasar
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# 20 komponen bar (navigasi, aksi, informasi, data)
# ---------------------------------------------------------------------------
GROUP_ORDER = ["Dasar", "Navigasi", "Aksi", "Informasi", "Data"]
STATUS_KINDS = {"info": "Info", "success": "Sukses", "warning": "Peringatan", "error": "Galat"}
STATUS_ICONS = {"info": "info", "success": "check_circle", "warning": "warning", "error": "error"}
ICON_HINT = "Nama ikon mengikuti Material Symbols (contoh: home, search, person). Daftar lengkap: fonts.google.com/icons"

BAR_SPECS = {
    # ---- Navigasi ----
    "bottomnav": {
        "label": "Navigasi bawah", "icon": "bottom_navigation", "group": "Navigasi", "hint": True,
        "defaults": {"items": "Beranda|home\nCari|search\nSimpan|favorite\nProfil|person", "active": 1},
        "fields": [("items", "Item (label|ikon, satu per baris)", "area"),
                   ("active", "Item aktif (urutan)", "int", (1, 6))],
    },
    "tabbar": {
        "label": "Tab bar", "icon": "tab", "group": "Navigasi",
        "defaults": {"items": "Ringkasan\nAktivitas\nPengaturan", "active": 1},
        "fields": [("items", "Tab (satu per baris)", "area"), ("active", "Tab aktif (urutan)", "int", (1, 8))],
    },
    "breadcrumb": {
        "label": "Breadcrumb", "icon": "chevron_right", "group": "Navigasi",
        "defaults": {"items": "Beranda\nProduk\nDetail"},
        "fields": [("items", "Jalur (satu per baris)", "area")],
    },
    "sidemenu": {
        "label": "Menu samping", "icon": "side_navigation", "group": "Navigasi", "hint": True,
        "defaults": {"title": "Menu", "active": 1,
                     "items": "Dasbor|dashboard\nPesanan|shopping_bag\nPelanggan|group\nLaporan|bar_chart\nPengaturan|settings"},
        "fields": [("title", "Judul menu", "text"), ("items", "Item (label|ikon, satu per baris)", "area"),
                   ("active", "Item aktif (urutan)", "int", (1, 10))],
    },
    "pagination": {
        "label": "Paginasi", "icon": "format_list_numbered", "group": "Navigasi",
        "defaults": {"pages": 10, "current": 3},
        "fields": [("pages", "Jumlah halaman", "int", (1, 99)), ("current", "Halaman aktif", "int", (1, 99))],
    },
    # ---- Aksi ----
    "toolbar": {
        "label": "Toolbar aksi", "icon": "construction", "group": "Aksi", "hint": True,
        "defaults": {"items": "Baru|add\nSalin|content_copy\nBagikan|share\nHapus|delete"},
        "fields": [("items", "Aksi (label|ikon, satu per baris)", "area")],
    },
    "searchbar": {
        "label": "Bar pencarian", "icon": "search", "group": "Aksi",
        "defaults": {"placeholder": "Cari sesuatu…", "button": "Cari"},
        "fields": [("placeholder", "Placeholder", "text"), ("button", "Label tombol", "text")],
    },
    "filterbar": {
        "label": "Bar filter", "icon": "filter_list", "group": "Aksi",
        "defaults": {"items": "Semua\nBaru\nPopuler\nDiskon", "active": 1},
        "fields": [("items", "Filter (satu per baris)", "area"), ("active", "Filter aktif (urutan)", "int", (1, 10))],
    },
    "fab": {
        "label": "Tombol melayang", "icon": "add_circle", "group": "Aksi", "hint": True,
        "defaults": {"icon": "add", "text": "Tambah", "align": "right"},
        "fields": [("icon", "Ikon", "text"), ("text", "Label (boleh kosong)", "text"),
                   ("align", "Posisi", "sel", {"left": "Kiri", "center": "Tengah", "right": "Kanan"})],
    },
    "socialbar": {
        "label": "Bar sosial", "icon": "share", "group": "Aksi", "hint": True,
        "defaults": {"items": "Instagram|#|photo_camera\nWhatsApp|#|chat\nEmail|#|mail\nWebsite|#|public"},
        "fields": [("items", "Tautan (label|url|ikon, satu per baris)", "area")],
    },
    # ---- Informasi ----
    "announcement": {
        "label": "Bar pengumuman", "icon": "campaign", "group": "Informasi",
        "defaults": {"text": "Diskon 20% sampai akhir bulan.", "link_text": "Lihat promo", "link": "#"},
        "fields": [("text", "Teks", "text"), ("link_text", "Label tautan", "text"), ("link", "URL tautan", "text")],
    },
    "statusbar": {
        "label": "Bar status", "icon": "info", "group": "Informasi",
        "defaults": {"kind": "info", "title": "Pemberitahuan", "text": "Pemeliharaan sistem dijadwalkan malam ini pukul 23.00."},
        "fields": [("kind", "Jenis", "sel", STATUS_KINDS), ("title", "Judul", "text"), ("text", "Isi", "text")],
    },
    "progressbar": {
        "label": "Bar progres", "icon": "linear_scale", "group": "Informasi",
        "defaults": {"label": "Kapasitas penyimpanan", "value": 65},
        "fields": [("label", "Label", "text"), ("value", "Nilai (%)", "int", (0, 100))],
    },
    "stepper": {
        "label": "Bar langkah", "icon": "timeline", "group": "Informasi",
        "defaults": {"steps": "Keranjang\nAlamat\nPembayaran\nSelesai", "current": 2},
        "fields": [("steps", "Langkah (satu per baris)", "area"), ("current", "Langkah saat ini", "int", (1, 8))],
    },
    "ratingbar": {
        "label": "Bar rating", "icon": "star", "group": "Informasi",
        "defaults": {"label": "Ulasan pelanggan", "value": 4.5, "count": "(128 ulasan)"},
        "fields": [("label", "Label", "text"), ("value", "Nilai bintang", "float", (0.0, 5.0, 0.5)),
                   ("count", "Keterangan jumlah", "text")],
    },
    # ---- Data ----
    "statsbar": {
        "label": "Bar statistik", "icon": "monitoring", "group": "Data",
        "defaults": {"items": "12 rb|Pengguna\n98%|Puas\n24/7|Dukungan"},
        "fields": [("items", "Angka (angka|label, satu per baris)", "area")],
    },
    "pricebar": {
        "label": "Bar harga", "icon": "payments", "group": "Data",
        "defaults": {"price": "Rp 149.000", "caption": "Sudah termasuk pajak", "button": "Beli sekarang", "link": "#"},
        "fields": [("price", "Harga", "text"), ("caption", "Keterangan", "text"),
                   ("button", "Label tombol", "text"), ("link", "URL tombol", "text")],
    },
    "categorybar": {
        "label": "Bar kategori", "icon": "category", "group": "Data", "hint": True,
        "defaults": {"items": "Makanan|restaurant\nMinuman|local_cafe\nBelanja|shopping_bag\nTransport|directions_car\nLainnya|apps"},
        "fields": [("items", "Kategori (label|ikon, satu per baris)", "area")],
    },
    "profilebar": {
        "label": "Bar profil", "icon": "account_circle", "group": "Data",
        "defaults": {"name": "Nama Lengkap", "role": "Jabatan", "avatar": "", "action": "Hubungi"},
        "fields": [("name", "Nama", "text"), ("role", "Jabatan / keterangan", "text"),
                   ("avatar", "URL foto (kosongkan untuk inisial)", "text"), ("action", "Label tombol (boleh kosong)", "text")],
    },
    "cookiebar": {
        "label": "Bar persetujuan", "icon": "cookie", "group": "Data",
        "defaults": {"text": "Kami memakai cookie untuk meningkatkan pengalamanmu.", "accept": "Terima", "decline": "Tolak"},
        "fields": [("text", "Teks", "text"), ("accept", "Tombol setuju", "text"), ("decline", "Tombol tolak (boleh kosong)", "text")],
    },
}

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


def mi(name):
    """Ikon Material Symbols untuk HTML hasil (nama dibersihkan)."""
    name = re.sub(r"[^a-z0-9_]", "", str(name or "").lower()) or "circle"
    return f'<span class="mi" aria-hidden="true">{name}</span>'


def clamp_int(value, lo, hi, default):
    try:
        n = int(float(value))
    except (TypeError, ValueError):
        n = default
    return max(lo, min(hi, n))


def parts_of(value, n):
    """Pecah tiap baris 'a|b|c' menjadi daftar n kolom (dilengkapi string kosong)."""
    rows = []
    for ln in lines_of(value):
        cols = [c.strip() for c in ln.split("|")]
        cols += [""] * (n - len(cols))
        rows.append(cols[:n])
    return rows


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


def page_numbers(total, current):
    keep = sorted({1, total, current - 1, current, current + 1})
    result, prev = [], 0
    for n in keep:
        if n < 1 or n > total:
            continue
        if prev and n - prev > 1:
            result.append(None)
        result.append(n)
        prev = n
    return result


def render_bar(el):
    t = el["type"]
    css = soft_style(el)
    sa = f' style="{css}"' if css else ""
    g = el.get

    if t == "bottomnav":
        rows = parts_of(g("items"), 2)
        act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
        inner = "".join(
            f'<a class="bn-item{" on" if i == act else ""}" href="#">'
            f'{mi(ic)}<span>{esc(lb)}</span></a>' for i, (lb, ic) in enumerate(rows))
        return f'<nav class="bar bottomnav" aria-label="Navigasi bawah"{sa}>{inner}</nav>'
    if t == "tabbar":
        rows = lines_of(g("items"))
        act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
        inner = "".join(f'<a class="tab{" on" if i == act else ""}" href="#" role="tab">{esc(lb)}</a>' for i, lb in enumerate(rows))
        return f'<div class="bar tabbar" role="tablist"{sa}>{inner}</div>'
    if t == "breadcrumb":
        rows = lines_of(g("items"))
        bits = []
        for i, lb in enumerate(rows):
            if i == len(rows) - 1:
                bits.append(f'<span class="cur" aria-current="page">{esc(lb)}</span>')
            else:
                bits.append(f'<a href="#">{esc(lb)}</a>{mi("chevron_right")}')
        return f'<nav class="bar crumbs" aria-label="Breadcrumb"{sa}>{"".join(bits)}</nav>'
    if t == "sidemenu":
        rows = parts_of(g("items"), 2)
        act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
        inner = "".join(
            f'<a class="sm-item{" on" if i == act else ""}" href="#">{mi(ic)}<span>{esc(lb)}</span></a>'
            for i, (lb, ic) in enumerate(rows))
        title = f'<div class="sm-title">{esc(g("title", ""))}</div>' if g("title") else ""
        return f'<nav class="bar sidemenu"{sa}>{title}{inner}</nav>'
    if t == "pagination":
        total = clamp_int(g("pages"), 1, 99, 10)
        cur = clamp_int(g("current"), 1, total, 1)
        bits = [f'<a href="#" aria-label="Sebelumnya">{mi("chevron_left")}</a>']
        for n in page_numbers(total, cur):
            bits.append('<span class="dots">…</span>' if n is None else
                        f'<a href="#" class="{"on" if n == cur else ""}">{n}</a>')
        bits.append(f'<a href="#" aria-label="Berikutnya">{mi("chevron_right")}</a>')
        return f'<nav class="bar pager" aria-label="Paginasi"{sa}>{"".join(bits)}</nav>'
    if t == "toolbar":
        rows = parts_of(g("items"), 2)
        inner = "".join(f'<button type="button" class="tb-btn">{mi(ic)}<span>{esc(lb)}</span></button>' for lb, ic in rows)
        return f'<div class="bar toolbar" role="toolbar"{sa}>{inner}</div>'
    if t == "searchbar":
        return (f'<div class="bar searchbar"{sa}>{mi("search")}'
                f'<input type="search" placeholder="{esc(g("placeholder", ""))}" aria-label="Pencarian">'
                f'<button type="button" class="btn">{esc(g("button", ""))}</button></div>')
    if t == "filterbar":
        rows = lines_of(g("items"))
        act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
        inner = "".join(f'<a class="fchip{" on" if i == act else ""}" href="#">{esc(lb)}</a>' for i, lb in enumerate(rows))
        return f'<div class="bar chips"{sa}>{inner}</div>'
    if t == "fab":
        align = g("align") if g("align") in ALIGNS else "right"
        label = f'<span>{esc(g("text", ""))}</span>' if g("text") else ""
        return (f'<div class="fabwrap" style="text-align:{align}"><a class="fab" href="#" '
                f'aria-label="{esc(g("text") or "Aksi")}"{sa}>{mi(g("icon"))}{label}</a></div>')
    if t == "socialbar":
        rows = parts_of(g("items"), 3)
        inner = "".join(f'<a href="{esc(safe_url(u))}">{mi(ic or "link")}<span>{esc(lb)}</span></a>' for lb, u, ic in rows)
        return f'<div class="bar social"{sa}>{inner}</div>'
    if t == "announcement":
        link = ""
        if g("link_text"):
            link = f'<a href="{esc(safe_url(g("link", "#")))}">{esc(g("link_text"))}</a>'
        return f'<div class="bar announce"{sa}>{esc(g("text", ""))}{link}</div>'
    if t == "statusbar":
        kind = g("kind") if g("kind") in STATUS_KINDS else "info"
        title = f'<strong>{esc(g("title", ""))}</strong> ' if g("title") else ""
        return (f'<div class="bar status {kind}" role="status"{sa}>{mi(STATUS_ICONS[kind])}'
                f'<div>{title}{esc(g("text", ""))}</div></div>')
    if t == "progressbar":
        v = clamp_int(g("value"), 0, 100, 0)
        return (f'<div class="bar progress"{sa}><div class="pg-head"><span>{esc(g("label", ""))}</span><span>{v}%</span></div>'
                f'<div class="pg-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{v}">'
                f'<div class="pg-fill" style="width:{v}%"></div></div></div>')
    if t == "stepper":
        rows = lines_of(g("steps"))
        cur = clamp_int(g("current"), 1, max(1, len(rows)), 1)
        inner = []
        for i, lb in enumerate(rows, start=1):
            state = "done" if i < cur else ("now" if i == cur else "")
            dot = mi("check") if i < cur else str(i)
            inner.append(f'<div class="st-step {state}"><div class="st-dot">{dot}</div>{esc(lb)}</div>')
        return f'<div class="bar stepper"{sa}>{"".join(inner)}</div>'
    if t == "ratingbar":
        try:
            val = max(0.0, min(5.0, float(g("value", 0) or 0)))
        except (TypeError, ValueError):
            val = 0.0
        stars = ""
        for i in range(1, 6):
            if val >= i - 0.25:
                stars += mi("star")
            elif val >= i - 0.75:
                stars += mi("star_half")
            else:
                stars += f'<span class="off">{mi("star")}</span>'
        lab = f'<strong>{val:g}</strong>'
        return (f'<div class="bar rating"{sa}><span class="stars" role="img" aria-label="{val:g} dari 5">{stars}</span>'
                f'{lab}<span>{esc(g("label", ""))}</span><small>{esc(g("count", ""))}</small></div>')
    if t == "statsbar":
        rows = parts_of(g("items"), 2)
        inner = "".join(f'<div class="stat"><strong>{esc(n)}</strong><span>{esc(lb)}</span></div>' for n, lb in rows)
        return f'<div class="bar stats"{sa}>{inner}</div>'
    if t == "pricebar":
        btn = f'<a class="btn" href="{esc(safe_url(g("link", "#")))}">{esc(g("button", ""))}</a>' if g("button") else ""
        return (f'<div class="bar pricebar"{sa}><div><strong>{esc(g("price", ""))}</strong>'
                f'<small>{esc(g("caption", ""))}</small></div>{btn}</div>')
    if t == "categorybar":
        rows = parts_of(g("items"), 2)
        inner = "".join(f'<a class="cat" href="#"><span class="cat-ico">{mi(ic)}</span>{esc(lb)}</a>' for lb, ic in rows)
        return f'<div class="bar cats"{sa}>{inner}</div>'
    if t == "profilebar":
        name = str(g("name", "") or "")
        if g("avatar"):
            av = f'<img src="{esc(safe_url(g("avatar")))}" alt="">'
        else:
            av = esc((name.strip()[:1] or "?").upper())
        btn = f'<a class="btn sm" href="#">{esc(g("action"))}</a>' if g("action") else ""
        return (f'<div class="bar profilebar"{sa}><div class="avatar">{av}</div>'
                f'<div class="pf-text"><strong>{esc(name)}</strong><small>{esc(g("role", ""))}</small></div>{btn}</div>')
    if t == "cookiebar":
        no = f'<button type="button" class="btn ghost sm">{esc(g("decline"))}</button>' if g("decline") else ""
        return (f'<div class="bar cookie" role="dialog" aria-label="Persetujuan cookie"{sa}><p>{esc(g("text", ""))}</p>'
                f'{no}<button type="button" class="btn sm">{esc(g("accept", ""))}</button></div>')
    return ""


def describe_bar(el):
    spec = BAR_SPECS[el["type"]]
    bits = []
    for field in spec["fields"]:
        k, label = field[0], field[1]
        val = str(el.get(k, "")).replace("\n", " / ")
        bits.append(f'{label}: "{val}"')
    note = "; item ber-format label|ikon memakai nama ikon Material Symbols" if spec.get("hint") else ""
    return "; ".join(bits) + note


def edit_bar_fields(el, key):
    spec = BAR_SPECS[el["type"]]
    for field in spec["fields"]:
        k, label, kind = field[0], field[1], field[2]
        extra = field[3] if len(field) > 3 else None
        wk = f"{key}_{k}"
        if kind == "text":
            el[k] = st.text_input(label, str(el.get(k, "")), key=wk)
        elif kind == "area":
            el[k] = st.text_area(label, str(el.get(k, "")), key=wk, height=120)
        elif kind == "int":
            lo, hi = extra
            el[k] = st.slider(label, lo, hi, clamp_int(el.get(k), lo, hi, lo), key=wk)
        elif kind == "float":
            lo, hi, step = extra
            try:
                cur = max(lo, min(hi, float(el.get(k, lo))))
            except (TypeError, ValueError):
                cur = lo
            el[k] = st.slider(label, float(lo), float(hi), float(cur), step=float(step), key=wk)
        elif kind == "sel":
            keys = list(extra)
            cur = el.get(k) if el.get(k) in keys else keys[0]
            el[k] = st.selectbox(label, keys, keys.index(cur), format_func=lambda v, e=extra: e[v], key=wk)
    if spec.get("hint"):
        st.caption(ICON_HINT)


ICON_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:'
    'opsz,wght,FILL,GRAD@24,400,0..1,0">'
)

BAR_CSS = """
  .mi { font-family: 'Material Symbols Rounded'; font-weight: 400; font-style: normal; font-size: 20px;
    line-height: 1; display: inline-block; width: 1em; overflow: hidden; white-space: nowrap;
    vertical-align: middle; font-feature-settings: 'liga'; -webkit-font-smoothing: antialiased; flex: none; }
  .bar { border-radius: 12px; }
  .bar a { color: inherit; text-decoration: none; }
  .bar .btn { color: var(--on-primary); }
  .bar .btn.sm { padding: 8px 14px; font-size: 14px; }
  .bar .btn.ghost { background: transparent; color: var(--text); border: 1px solid rgba(128,128,128,.5); }
  .bottomnav { display: flex; justify-content: space-around; position: sticky; bottom: 0; z-index: 5;
    background: var(--bg); border: 1px solid rgba(128,128,128,.3); padding: 8px 4px; box-shadow: 0 -4px 16px rgba(0,0,0,.08); }
  .bn-item { display: flex; flex-direction: column; align-items: center; gap: 2px; font-size: 12px;
    padding: 4px 12px; border-radius: 12px; opacity: .65; }
  .bn-item.on { color: var(--primary); opacity: 1; font-weight: 600; }
  .tabbar { display: flex; gap: 4px; overflow-x: auto; border-bottom: 2px solid rgba(128,128,128,.25); border-radius: 0; }
  .tabbar .tab { padding: 10px 16px; margin-bottom: -2px; border-bottom: 2px solid transparent; opacity: .7; white-space: nowrap; }
  .tabbar .tab.on { border-color: var(--primary); color: var(--primary); opacity: 1; font-weight: 600; }
  .crumbs { display: flex; align-items: center; flex-wrap: wrap; gap: 2px; font-size: 14px; }
  .crumbs a { opacity: .7; }
  .crumbs .cur { font-weight: 600; }
  .crumbs .mi { font-size: 18px; opacity: .45; }
  .sidemenu { display: flex; flex-direction: column; gap: 2px; padding: 8px; border: 1px solid rgba(128,128,128,.3); }
  .sm-title { font-size: 13px; opacity: .6; padding: 6px 12px; }
  .sm-item { display: flex; align-items: center; gap: 10px; padding: 9px 12px; border-radius: 10px; }
  .sm-item:hover { background: rgba(128,128,128,.12); }
  .sm-item.on { background: var(--primary); color: var(--on-primary); }
  .pager { display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; }
  .pager a { min-width: 36px; height: 36px; display: inline-flex; align-items: center; justify-content: center;
    border: 1px solid rgba(128,128,128,.35); border-radius: 10px; padding: 0 8px; }
  .pager a.on { background: var(--primary); border-color: var(--primary); color: var(--on-primary); font-weight: 600; }
  .pager .dots { display: inline-flex; align-items: center; opacity: .6; }
  .toolbar { display: flex; gap: 6px; flex-wrap: wrap; padding: 6px; border: 1px solid rgba(128,128,128,.3); }
  .tb-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 12px; border-radius: 10px; border: 0;
    background: transparent; color: inherit; font: inherit; font-size: 14px; cursor: pointer; }
  .tb-btn:hover { background: rgba(128,128,128,.15); }
  .searchbar { display: flex; align-items: center; gap: 8px; padding: 6px 6px 6px 14px; border: 1px solid rgba(128,128,128,.4); border-radius: 999px; }
  .searchbar input { flex: 1; min-width: 0; border: 0; outline: 0; background: transparent; color: inherit; font: inherit; padding: 6px 0; }
  .searchbar .btn { padding: 8px 18px; border-radius: 999px; }
  .chips { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 2px; }
  .fchip { white-space: nowrap; padding: 7px 14px; border: 1px solid rgba(128,128,128,.4); border-radius: 999px; font-size: 14px; }
  .fchip.on { background: var(--primary); border-color: var(--primary); color: var(--on-primary); font-weight: 600; }
  .fabwrap { position: sticky; bottom: 16px; z-index: 5; pointer-events: none; }
  .fab { pointer-events: auto; display: inline-flex; align-items: center; gap: 8px; background: var(--primary);
    color: var(--on-primary) !important; padding: 14px 20px; border-radius: 999px; box-shadow: 0 8px 20px rgba(0,0,0,.25); font-weight: 600; }
  .social { display: flex; gap: 8px; flex-wrap: wrap; }
  .social a { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; border: 1px solid rgba(128,128,128,.35); border-radius: 999px; font-size: 14px; }
  .announce { background: var(--primary); color: var(--on-primary); text-align: center; padding: 10px 16px; font-size: 14px; border-radius: 0; }
  .announce a { color: var(--on-primary); text-decoration: underline; font-weight: 600; margin-left: 8px; }
  .status { display: flex; gap: 10px; align-items: flex-start; padding: 12px 14px; border: 1px solid; border-left-width: 4px; font-size: 14px; }
  .status.info { background: #eff6ff; border-color: #3b82f6; color: #1e3a8a; }
  .status.success { background: #f0fdf4; border-color: #22c55e; color: #14532d; }
  .status.warning { background: #fffbeb; border-color: #f59e0b; color: #78350f; }
  .status.error { background: #fef2f2; border-color: #ef4444; color: #7f1d1d; }
  .pg-head { display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 6px; }
  .pg-track { height: 10px; border-radius: 999px; background: rgba(128,128,128,.25); overflow: hidden; }
  .pg-fill { height: 100%; background: var(--primary); border-radius: 999px; }
  .stepper { display: flex; align-items: flex-start; }
  .st-step { flex: 1; text-align: center; position: relative; font-size: 13px; }
  .st-step::before { content: ""; position: absolute; top: 15px; left: -50%; width: 100%; height: 2px; background: rgba(128,128,128,.35); }
  .st-step:first-child::before { display: none; }
  .st-dot { position: relative; z-index: 1; width: 32px; height: 32px; margin: 0 auto 6px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; background: var(--bg); border: 2px solid rgba(128,128,128,.5); font-weight: 600; font-size: 14px; }
  .st-dot .mi { font-size: 18px; }
  .st-step.done .st-dot, .st-step.now .st-dot { border-color: var(--primary); }
  .st-step.done .st-dot { background: var(--primary); color: var(--on-primary); }
  .st-step.done::before, .st-step.now::before { background: var(--primary); }
  .st-step.now { color: var(--primary); font-weight: 600; }
  .rating { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
  .rating .stars { display: inline-flex; color: #f59e0b; }
  .rating .mi { font-size: 22px; font-variation-settings: 'FILL' 1; }
  .rating .off { opacity: .3; display: inline-flex; }
  .rating small { opacity: .65; }
  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 12px; }
  .stat { text-align: center; padding: 14px 8px; border: 1px solid rgba(128,128,128,.3); border-radius: 12px; }
  .stat strong { display: block; font-size: 24px; color: var(--primary); }
  .stat span { font-size: 13px; opacity: .7; }
  .pricebar { position: sticky; bottom: 0; z-index: 5; display: flex; align-items: center; justify-content: space-between;
    gap: 12px; padding: 12px 16px; background: var(--bg); border: 1px solid rgba(128,128,128,.3); box-shadow: 0 -4px 16px rgba(0,0,0,.08); }
  .pricebar strong { font-size: 20px; }
  .pricebar small { display: block; opacity: .65; }
  .cats { display: flex; gap: 14px; overflow-x: auto; padding: 4px; }
  .cat { display: flex; flex-direction: column; align-items: center; gap: 6px; font-size: 12px; min-width: 64px; }
  .cat-ico { width: 52px; height: 52px; border-radius: 16px; display: flex; align-items: center; justify-content: center;
    background: rgba(128,128,128,.14); color: var(--primary); }
  .cat-ico .mi { font-size: 26px; }
  .profilebar { display: flex; align-items: center; gap: 12px; padding: 12px; border: 1px solid rgba(128,128,128,.3); }
  .avatar { width: 48px; height: 48px; border-radius: 50%; background: var(--primary); color: var(--on-primary); display: flex;
    align-items: center; justify-content: center; font-weight: 700; overflow: hidden; flex: none; }
  .avatar img { width: 100%; height: 100%; object-fit: cover; }
  .pf-text { flex: 1; min-width: 0; }
  .pf-text small { display: block; opacity: .65; }
  .cookie { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; padding: 14px 16px;
    border: 1px solid rgba(128,128,128,.3); box-shadow: 0 8px 24px rgba(0,0,0,.12); }
  .cookie p { flex: 1; min-width: 180px; margin: 0; font-size: 14px; }
"""


def ensure_element_style(el):
    # Visual styling uses a separate key so semantic element properties
    # such as the list's `style` (bullet/number) are never overwritten.
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


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
def default_design():
    return {
        "title": "Aplikasi Saya",
        "theme": {
            "primary": "#4f46e5",
            "bg": "#ffffff",
            "text": "#1f2937",
            "font": "Sans-serif modern",
            "width": 720,
        },
        "pages": [{"id": uuid.uuid4().hex[:8], "name": "Beranda", "elements": []}],
    }


def project_file(project_id):
    return PROJECTS_DIR / f"{project_id}.json"


def project_timestamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def project_digest(design):
    payload = json.dumps(design, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def list_projects():
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    projects = []
    for path in PROJECTS_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("design"), dict):
                projects.append({
                    "id": str(data.get("id") or path.stem),
                    "name": str(data.get("name") or data["design"].get("title") or "Proyek tanpa nama"),
                    "updated_at": str(data.get("updated_at") or ""),
                })
        except (OSError, json.JSONDecodeError, TypeError):
            continue
    projects.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
    return projects


def save_project(project_id, name, design):
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": project_id,
        "name": name.strip() or "Proyek tanpa nama",
        "updated_at": project_timestamp(),
        "design": copy.deepcopy(design),
    }
    project_file(project_id).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return payload


def read_project(project_id):
    try:
        data = json.loads(project_file(project_id).read_text(encoding="utf-8"))
        design = data.get("design")
        if not isinstance(data, dict) or not valid_design(design):
            return None
        return data
    except (OSError, json.JSONDecodeError, TypeError):
        return None


def set_active_project(project_id, data):
    st.session_state.project_id = project_id
    st.session_state.project_name = str(data.get("name") or data["design"].get("title") or "Proyek tanpa nama")
    st.session_state.design = data["design"]
    st.session_state.page_idx = 0
    st.session_state.selected_id = None
    st.session_state.last_saved_hash = project_digest(st.session_state.design)
    st.session_state.last_saved_at = str(data.get("updated_at") or "")
    st.session_state.autosave_status = "saved"


def create_project(name=None, design=None):
    project_id = uuid.uuid4().hex
    design = copy.deepcopy(design or default_design())
    project_name = (name or design.get("title") or "Proyek Baru").strip() or "Proyek Baru"
    payload = save_project(project_id, project_name, design)
    set_active_project(project_id, payload)


def switch_project():
    project_id = st.session_state.get("project_selector_topbar")
    if not project_id or project_id == st.session_state.get("project_id"):
        return
    data = read_project(project_id)
    if data is not None:
        set_active_project(project_id, data)


def new_project():
    create_project("Proyek Baru")


def rename_project():
    project_id = st.session_state.get("project_id")
    name = str(st.session_state.get("project_rename", "")).strip()
    if not project_id or not name:
        return
    st.session_state.project_name = name
    payload = save_project(project_id, name, st.session_state.design)
    st.session_state.last_saved_hash = project_digest(st.session_state.design)
    st.session_state.last_saved_at = payload["updated_at"]
    st.session_state.autosave_status = "saved"


def delete_project():
    project_id = st.session_state.get("project_id")
    projects = list_projects()
    if not project_id or len(projects) <= 1:
        return
    try:
        project_file(project_id).unlink(missing_ok=True)
    except OSError:
        return
    remaining = [p for p in list_projects() if p["id"] != project_id]
    if remaining:
        data = read_project(remaining[0]["id"])
        if data is not None:
            set_active_project(remaining[0]["id"], data)


def autosave_project():
    project_id = st.session_state.get("project_id")
    if not project_id or "design" not in st.session_state:
        return
    digest = project_digest(st.session_state.design)
    if digest == st.session_state.get("last_saved_hash"):
        return
    st.session_state.autosave_status = "saving"
    try:
        payload = save_project(project_id, st.session_state.get("project_name", "Proyek Baru"), st.session_state.design)
        st.session_state.last_saved_hash = digest
        st.session_state.last_saved_at = payload["updated_at"]
        st.session_state.autosave_status = "saved"
    except OSError:
        st.session_state.autosave_status = "error"


def init_state():
    if "design" not in st.session_state:
        projects = list_projects()
        if projects:
            data = read_project(projects[0]["id"])
            if data is not None:
                set_active_project(projects[0]["id"], data)
            else:
                create_project()
        else:
            create_project()
    if "page_idx" not in st.session_state:
        st.session_state.page_idx = 0
    if "selected_id" not in st.session_state:
        st.session_state.selected_id = None
    if "project_id" not in st.session_state:
        create_project()
    if "project_name" not in st.session_state:
        st.session_state.project_name = st.session_state.design.get("title", "Proyek Baru")
    if "last_saved_hash" not in st.session_state:
        st.session_state.last_saved_hash = project_digest(st.session_state.design)
    if "last_saved_at" not in st.session_state:
        st.session_state.last_saved_at = ""
    if "autosave_status" not in st.session_state:
        st.session_state.autosave_status = "saved"


def current_page():
    pages = st.session_state.design["pages"]
    idx = min(st.session_state.page_idx, len(pages) - 1)
    return pages[idx]


def selected_element():
    sid = st.session_state.get("selected_id")
    for i, el in enumerate(current_page()["elements"]):
        if el["id"] == sid:
            return i, el
    return None, None


# ---------------------------------------------------------------------------
# Callback (dijalankan sebelum rerun, jadi aman mengubah state)
# ---------------------------------------------------------------------------
def select_element(eid):
    st.session_state.selected_id = eid


def clear_selection():
    st.session_state.selected_id = None


def insert_element(el_type, index=None):
    el = {"id": uuid.uuid4().hex[:8], "type": el_type}
    el.update(copy.deepcopy(ELEMENT_DEFAULTS[el_type]))
    el["visual_style"] = copy.deepcopy(ELEMENT_STYLE_DEFAULTS)
    els = current_page()["elements"]
    if index is None or not isinstance(index, int):
        index = len(els)
    els.insert(min(max(index, 0), len(els)), el)
    st.session_state.selected_id = el["id"]


def add_element(el_type):
    """Tambah komponen dari dock bawah setelah elemen yang sedang dipilih."""
    _, selected = selected_element()
    if selected is None:
        insert_element(el_type)
        return
    elements = current_page()["elements"]
    selected_index = next((i for i, el in enumerate(elements) if el["id"] == selected["id"]), len(elements) - 1)
    insert_element(el_type, selected_index + 1)


def move_element(index, delta):
    els = current_page()["elements"]
    new = index + delta
    if 0 <= new < len(els):
        els[index], els[new] = els[new], els[index]


def delete_element(index):
    els = current_page()["elements"]
    if 0 <= index < len(els):
        removed = els.pop(index)
        if st.session_state.selected_id == removed["id"]:
            st.session_state.selected_id = None


def duplicate_element(index):
    els = current_page()["elements"]
    clone = copy.deepcopy(els[index])
    clone["id"] = uuid.uuid4().hex[:8]
    els.insert(index + 1, clone)
    st.session_state.selected_id = clone["id"]


def add_page():
    pages = st.session_state.design["pages"]
    pages.append({"id": uuid.uuid4().hex[:8], "name": f"Halaman {len(pages) + 1}", "elements": []})
    st.session_state.page_idx = len(pages) - 1
    st.session_state.selected_id = None


def delete_page():
    pages = st.session_state.design["pages"]
    if len(pages) > 1:
        pages.pop(st.session_state.page_idx)
        st.session_state.page_idx = max(0, st.session_state.page_idx - 1)
        st.session_state.selected_id = None


def reset_design():
    st.session_state.design = default_design()
    st.session_state.page_idx = 0
    st.session_state.selected_id = None


def load_design(data):
    st.session_state.design = data
    st.session_state.page_idx = 0
    st.session_state.selected_id = None


def valid_design(data):
    try:
        assert isinstance(data["title"], str)
        assert isinstance(data["theme"], dict)
        assert isinstance(data["pages"], list) and data["pages"]
        for page in data["pages"]:
            assert isinstance(page["name"], str)
            page.setdefault("id", uuid.uuid4().hex[:8])
            for el in page["elements"]:
                assert el["type"] in ELEMENT_LABELS
                el.setdefault("id", uuid.uuid4().hex[:8])
                for k, v in ELEMENT_DEFAULTS[el["type"]].items():
                    el.setdefault(k, copy.deepcopy(v))
                ensure_element_style(el)
        for k, v in default_design()["theme"].items():
            data["theme"].setdefault(k, v)
        return True
    except (KeyError, TypeError, AssertionError):
        return False


# ---------------------------------------------------------------------------
# Template desain siap pakai
# ---------------------------------------------------------------------------
def mk(el_type, **props):
    el = {"type": el_type}
    el.update(copy.deepcopy(ELEMENT_DEFAULTS[el_type]))
    el["visual_style"] = copy.deepcopy(ELEMENT_STYLE_DEFAULTS)
    el.update(props)
    ensure_element_style(el)
    return el


def pic(seed, w=800, h=400):
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"


def H(text, size=32, align="left"):
    return mk("heading", text=text, size=size, align=align)


def P(text, align="left"):
    return mk("text", text=text, align=align)


def B(text, link="", align="left"):
    return mk("button", text=text, link=link, align=align)


def IMG(seed, alt, radius=12, w=800, h=400):
    return mk("image", url=pic(seed, w, h), alt=alt, radius=radius)


def GAL(seeds, cols=3, radius=8):
    return mk("gallery", urls="\n".join(pic(s, 400, 300) for s in seeds), columns=cols, radius=radius)


def LST(items, style="bullet"):
    return mk("list", items="\n".join(items), style=style)


def INP(label, placeholder="", kind="text"):
    return mk("input", label=label, placeholder=placeholder, kind=kind)


def CARD(title, text):
    return mk("card", title=title, text=text)


def DIV():
    return mk("divider")


def SPC(height=24):
    return mk("spacer", height=height)


def NAV(brand, links):
    return mk("navbar", brand=brand, links="\n".join(f"{a}|{b}" for a, b in links))


def FOOT(text):
    return mk("footer", text=text)


def BAR(el_type, **props):
    return mk(el_type, **props)


def theme_of(primary, bg, text, font="Sans-serif modern", width=720):
    return {"primary": primary, "bg": bg, "text": text, "font": font, "width": width}


TEMPLATES = {
    "landing_produk": {
        "name": "Landing page produk",
        "category": "Bisnis",
        "desc": "Halaman promosi satu layar: hero, tiga fitur, dan ajakan mendaftar.",
        "title": "Nusa Keuangan",
        "theme": theme_of("#4f46e5", "#ffffff", "#111827", width=760),
        "pages": [{"name": "Beranda", "elements": [
            NAV("Nusa Keuangan", [("Fitur", "#"), ("Harga", "#"), ("Kontak", "#")]),
            SPC(16),
            H("Kelola uang harian dengan lebih tenang", 40, "center"),
            P("Catat pemasukan dan pengeluaran, lihat laporan otomatis, semuanya dari satu aplikasi.", "center"),
            B("Coba gratis", "#", "center"),
            IMG("finance", "Tampilan aplikasi"),
            H("Fitur utama", 28),
            CARD("Catatan cepat", "Tambah transaksi dalam hitungan detik, tanpa formulir panjang."),
            CARD("Laporan otomatis", "Ringkasan mingguan dan bulanan tanpa perlu spreadsheet."),
            CARD("Data aman", "Semua catatan tersimpan terenkripsi di perangkatmu."),
            DIV(),
            H("Siap mulai?", 28, "center"),
            B("Unduh sekarang", "#", "center"),
            FOOT("© 2026 Nusa Keuangan"),
        ]}],
    },
    "faq": {
        "name": "FAQ dan bantuan",
        "category": "Bisnis",
        "desc": "Pertanyaan yang sering diajukan dalam bentuk kartu, lengkap dengan tombol kontak.",
        "title": "Pusat Bantuan",
        "theme": theme_of("#059669", "#ffffff", "#064e3b", width=680),
        "pages": [{"name": "Bantuan", "elements": [
            H("Pertanyaan yang sering diajukan", 34),
            P("Jawaban cepat untuk hal-hal yang paling sering ditanyakan pelanggan."),
            CARD("Bagaimana cara memesan?", "Pilih produk, isi alamat, lalu bayar. Pesanan diproses di hari yang sama."),
            CARD("Berapa lama pengiriman?", "Biasanya 2 sampai 4 hari kerja, tergantung kota tujuan."),
            CARD("Apakah barang bisa dikembalikan?", "Bisa, maksimal 7 hari setelah barang diterima dan dalam kondisi utuh."),
            CARD("Metode pembayaran apa saja?", "Transfer bank, dompet digital, dan bayar di tempat untuk area tertentu."),
            DIV(),
            H("Masih bingung?", 24),
            B("Hubungi kami", "#"),
            FOOT("Layanan pelanggan: setiap hari 08.00 sampai 20.00"),
        ]}],
    },
    "kontak": {
        "name": "Halaman kontak",
        "category": "Bisnis",
        "desc": "Formulir pesan sederhana dan informasi kontak.",
        "title": "Hubungi Kami",
        "theme": theme_of("#2563eb", "#ffffff", "#1e293b", width=560),
        "pages": [{"name": "Kontak", "elements": [
            H("Hubungi kami", 36),
            P("Tulis pesanmu dan tim kami akan membalas dalam 1 x 24 jam."),
            INP("Nama lengkap", "Nama kamu"),
            INP("Email", "nama@email.com", "email"),
            INP("Pesan", "Apa yang ingin kamu tanyakan?"),
            B("Kirim pesan"),
            DIV(),
            H("Informasi lain", 22),
            LST(["Alamat: Jl. Contoh No. 10", "Telepon: 0812-0000-0000", "Email: halo@contoh.id"]),
            FOOT("© 2026 Contoh Usaha"),
        ]}],
    },
    "promo_app": {
        "name": "Promosi aplikasi mobile",
        "category": "Aplikasi",
        "desc": "Halaman sempit ala ponsel untuk mempromosikan aplikasi dan tombol unduh.",
        "title": "BelanjaKu",
        "theme": theme_of("#db2777", "#fff1f2", "#4c0519", width=480),
        "pages": [{"name": "Beranda", "elements": [
            H("Belanja hemat di genggaman", 34, "center"),
            IMG("shopping", "Aplikasi BelanjaKu", 24, 600, 400),
            P("Ribuan promo harian, gratis ongkir, dan cashback langsung di ponselmu.", "center"),
            LST(["Voucher baru setiap hari", "Lacak pesanan secara langsung", "Bayar dengan satu ketukan"]),
            B("Unduh di Play Store", "#", "center"),
            B("Unduh di App Store", "#", "center"),
            FOOT("© 2026 BelanjaKu"),
        ]}],
    },
    "login": {
        "name": "Masuk dan daftar",
        "category": "Aplikasi",
        "desc": "Dua halaman: formulir masuk dan formulir pendaftaran.",
        "title": "Akun Saya",
        "theme": theme_of("#4f46e5", "#f9fafb", "#111827", width=420),
        "pages": [
            {"name": "Masuk", "elements": [
                SPC(24),
                H("Selamat datang kembali", 30, "center"),
                P("Masuk untuk melanjutkan.", "center"),
                INP("Email", "nama@email.com", "email"),
                INP("Kata sandi", "Masukkan kata sandi", "password"),
                B("Masuk"),
                P("Belum punya akun? Buka halaman Daftar.", "center"),
            ]},
            {"name": "Daftar", "elements": [
                SPC(24),
                H("Buat akun baru", 30, "center"),
                P("Hanya butuh satu menit.", "center"),
                INP("Nama lengkap", "Nama kamu"),
                INP("Email", "nama@email.com", "email"),
                INP("Kata sandi", "Minimal 8 karakter", "password"),
                B("Daftar"),
            ]},
        ],
    },
    "coming_soon": {
        "name": "Segera hadir",
        "category": "Aplikasi",
        "desc": "Halaman tema gelap untuk mengumpulkan email sebelum peluncuran.",
        "title": "Segera Hadir",
        "theme": theme_of("#0284c7", "#0f172a", "#f8fafc", width=520),
        "pages": [{"name": "Beranda", "elements": [
            SPC(80),
            H("Segera hadir", 52, "center"),
            P("Kami sedang menyiapkan sesuatu yang baru. Tinggalkan emailmu untuk jadi yang pertama tahu.", "center"),
            INP("Email", "nama@email.com", "email"),
            B("Beri tahu saya", "", "center"),
            SPC(40),
            FOOT("Peluncuran: kuartal pertama 2027"),
        ]}],
    },
    "katalog_kopi": {
        "name": "Katalog produk",
        "category": "Toko dan kuliner",
        "desc": "Etalase produk dengan galeri foto, kartu harga, dan tombol pesan.",
        "title": "Kopi Nusantara",
        "theme": theme_of("#ea580c", "#fffbeb", "#292524", width=840),
        "pages": [{"name": "Katalog", "elements": [
            NAV("Kopi Nusantara", [("Katalog", "#"), ("Cara pesan", "#"), ("Kontak", "#")]),
            SPC(8),
            H("Biji kopi pilihan dari berbagai daerah", 36),
            P("Disangrai segar setiap minggu dan dikirim ke seluruh Indonesia."),
            GAL(["coffee1", "coffee2", "coffee3"], 3),
            CARD("Arabika Gayo", "Rp 85.000 per 250 gr. Aroma floral dengan asam yang lembut."),
            CARD("Robusta Lampung", "Rp 60.000 per 250 gr. Pahit tegas dan body tebal."),
            CARD("Toraja Sapan", "Rp 95.000 per 250 gr. Rasa rempah dengan sentuhan cokelat."),
            B("Pesan sekarang", "#", "center"),
            FOOT("Pengiriman setiap Senin dan Kamis"),
        ]}],
    },
    "menu_restoran": {
        "name": "Menu restoran",
        "category": "Toko dan kuliner",
        "desc": "Halaman warung atau restoran: menu favorit, jam buka, dan tombol pesan.",
        "title": "Warung Bu Sari",
        "theme": theme_of("#b45309", "#fff7ed", "#431407", "Serif klasik", 720),
        "pages": [{"name": "Menu", "elements": [
            NAV("Warung Bu Sari", [("Menu", "#"), ("Lokasi", "#"), ("Pesan", "#")]),
            SPC(8),
            H("Masakan rumahan, rasa juara", 40, "center"),
            IMG("food", "Hidangan warung", 12),
            H("Menu favorit", 28),
            LST([
                "Nasi gudeg komplit: Rp 28.000",
                "Ayam bakar madu: Rp 32.000",
                "Soto betawi: Rp 30.000",
                "Es teh manis: Rp 6.000",
            ]),
            DIV(),
            H("Jam buka", 24),
            P("Setiap hari, pukul 08.00 sampai 21.00."),
            B("Pesan sekarang", "#", "center"),
            FOOT("Terima pesanan katering minimal 20 porsi"),
        ]}],
    },
    "harga_umkm": {
        "name": "Daftar harga UMKM",
        "category": "Toko dan kuliner",
        "desc": "Daftar harga dan cara pesan untuk usaha rumahan.",
        "title": "Kue Basah Bu Lina",
        "theme": theme_of("#16a34a", "#f0fdf4", "#14532d", width=640),
        "pages": [{"name": "Harga", "elements": [
            H("Kue basah Bu Lina", 36, "center"),
            P("Dibuat segar setiap pagi tanpa pengawet. Pesan H-1 ya.", "center"),
            IMG("cake", "Aneka kue basah", 16),
            H("Daftar harga", 26),
            LST([
                "Risoles isi ragout: Rp 3.500 per buah",
                "Lemper ayam: Rp 3.000 per buah",
                "Kue lapis: Rp 2.500 per potong",
                "Paket arisan (30 pcs): Rp 90.000",
            ]),
            H("Cara pesan", 26),
            LST(["Pilih kue dan jumlahnya", "Kirim pesanan lewat WhatsApp", "Bayar saat kue diantar"], "number"),
            B("Pesan lewat WhatsApp", "#", "center"),
            FOOT("Antar gratis area dalam kota"),
        ]}],
    },
    "portofolio": {
        "name": "Portofolio pribadi",
        "category": "Pribadi",
        "desc": "Tiga halaman: perkenalan, proyek dengan galeri, dan formulir kontak.",
        "title": "Rani Maharani",
        "theme": theme_of("#0f766e", "#fafaf9", "#1c1917", "Serif klasik", 720),
        "pages": [
            {"name": "Beranda", "elements": [
                SPC(16),
                H("Halo, saya Rani", 44),
                P("Desainer grafis dan ilustrator. Saya membantu merek kecil tampil rapi dan mudah diingat."),
                IMG("portrait", "Foto Rani", 16),
                B("Lihat proyek", "#"),
            ]},
            {"name": "Proyek", "elements": [
                H("Proyek pilihan", 34),
                GAL(["design1", "design2", "design3", "design4"], 2, 10),
                H("Layanan", 24),
                LST(["Desain logo dan identitas merek", "Ilustrasi untuk buku dan kemasan", "Desain media sosial"]),
            ]},
            {"name": "Kontak", "elements": [
                H("Mari berkolaborasi", 34),
                P("Ceritakan kebutuhanmu dan saya balas dalam dua hari kerja."),
                INP("Nama", "Nama kamu"),
                INP("Email", "nama@email.com", "email"),
                INP("Pesan", "Ceritakan proyekmu"),
                B("Kirim pesan"),
                FOOT("© 2026 Rani Maharani"),
            ]},
        ],
    },
    "cv_online": {
        "name": "CV online",
        "category": "Pribadi",
        "desc": "Riwayat kerja, pendidikan, dan keahlian dalam satu halaman rapi.",
        "title": "Budi Santoso",
        "theme": theme_of("#334155", "#ffffff", "#0f172a", "Serif klasik", 700),
        "pages": [{"name": "CV", "elements": [
            H("Budi Santoso", 40),
            P("Analis data. budi@contoh.id"),
            DIV(),
            H("Pengalaman", 26),
            LST([
                "Analis Data, PT Maju Bersama (2023 sampai sekarang)",
                "Staf Riset, Lembaga Survei Nusantara (2021 sampai 2023)",
            ]),
            H("Pendidikan", 26),
            LST(["S1 Statistika, Universitas Contoh (2017 sampai 2021)"]),
            H("Keahlian", 26),
            LST(["SQL dan Python", "Visualisasi data", "Penulisan laporan"]),
            B("Unduh CV", "#"),
        ]}],
    },
    "link_bio": {
        "name": "Link in bio",
        "category": "Pribadi",
        "desc": "Halaman sempit berisi foto profil dan deretan tombol tautan.",
        "title": "Nadia Creates",
        "theme": theme_of("#7c3aed", "#faf5ff", "#2e1065", width=420),
        "pages": [{"name": "Tautan", "elements": [
            SPC(16),
            IMG("avatar", "Foto profil", 48, 400, 400),
            H("@nadia.creates", 28, "center"),
            P("Kreator konten fotografi dan perjalanan.", "center"),
            B("Instagram", "#", "center"),
            B("YouTube", "#", "center"),
            B("Toko preset foto", "#", "center"),
            B("Kerja sama", "#", "center"),
            FOOT("Terima kasih sudah mampir"),
        ]}],
    },
    "blog": {
        "name": "Artikel blog",
        "category": "Konten",
        "desc": "Tata letak artikel dengan gambar sampul, poin penting, dan rekomendasi bacaan.",
        "title": "Catatan Dimas",
        "theme": theme_of("#1d4ed8", "#ffffff", "#1f2937", "Serif klasik", 680),
        "pages": [{"name": "Artikel", "elements": [
            H("Belajar menulis setiap hari", 38),
            P("Oleh Dimas, 5 menit baca"),
            IMG("writing", "Meja menulis", 8),
            P("Menulis bukan soal bakat. Ia kebiasaan kecil yang diulang sampai terasa ringan. Mulailah dari satu paragraf sehari."),
            H("Poin penting", 26),
            LST(["Tetapkan waktu menulis yang sama", "Tulis dulu, rapikan belakangan", "Baca ulang dengan suara keras"], "number"),
            DIV(),
            CARD("Baca juga", "Tiga kebiasaan kecil yang membuat tulisanmu lebih tajam."),
            FOOT("© 2026 Catatan Dimas"),
        ]}],
    },
    "kursus": {
        "name": "Kursus online",
        "category": "Pendidikan",
        "desc": "Halaman pendaftaran kelas: materi, pilihan paket, dan tombol daftar.",
        "title": "Kelas Kode",
        "theme": theme_of("#0369a1", "#f0f9ff", "#0c4a6e", width=760),
        "pages": [{"name": "Kelas", "elements": [
            NAV("Kelas Kode", [("Materi", "#"), ("Paket", "#"), ("Masuk", "#")]),
            SPC(8),
            H("Belajar pemrograman dari nol", 40),
            P("Kelas daring dengan latihan langsung dan mentor yang menjawab pertanyaanmu."),
            B("Daftar kelas", "#"),
            IMG("coding", "Belajar pemrograman", 12),
            H("Yang akan kamu pelajari", 28),
            LST(["Dasar logika pemrograman", "Membuat halaman web", "Mengolah data sederhana", "Membuat aplikasi kecil", "Proyek akhir"], "number"),
            H("Pilih paket", 28),
            CARD("Reguler", "Rp 299.000. Akses materi selama 3 bulan."),
            CARD("Intensif", "Rp 599.000. Akses 1 tahun dan sesi mentoring mingguan."),
            FOOT("Garansi uang kembali 7 hari"),
        ]}],
    },
    "undangan": {
        "name": "Undangan acara",
        "category": "Acara",
        "desc": "Undangan digital dengan waktu, tempat, dan konfirmasi kehadiran.",
        "title": "Ayu dan Bagas",
        "theme": theme_of("#be185d", "#fdf2f8", "#500724", "Serif klasik", 600),
        "pages": [{"name": "Undangan", "elements": [
            SPC(16),
            H("Ayu dan Bagas", 44, "center"),
            P("Dengan hormat mengundang Anda untuk hadir di hari bahagia kami.", "center"),
            IMG("wedding", "Foto pasangan", 24, 600, 400),
            H("Waktu dan tempat", 26, "center"),
            P("Sabtu, 12 Desember 2026, pukul 10.00 WIB", "center"),
            P("Gedung Serbaguna Melati, Jl. Merdeka No. 12", "center"),
            B("Lihat lokasi", "#", "center"),
            DIV(),
            H("Konfirmasi kehadiran", 24, "center"),
            INP("Nama", "Nama Anda"),
            INP("Jumlah tamu", "1", "number"),
            B("Konfirmasi", "", "center"),
            FOOT("Merupakan kehormatan bagi kami atas kehadiran Anda"),
        ]}],
    },
    "konferensi": {
        "name": "Jadwal acara dan pembicara",
        "category": "Acara",
        "desc": "Halaman meetup atau seminar: jadwal, foto pembicara, dan tombol tiket.",
        "title": "Dev Meetup 2026",
        "theme": theme_of("#4338ca", "#eef2ff", "#1e1b4b", width=720),
        "pages": [{"name": "Acara", "elements": [
            H("Dev Meetup 2026", 38, "center"),
            P("Sabtu, 14 November 2026, di Aula Utama. Gratis untuk 200 peserta pertama.", "center"),
            B("Daftar tiket", "#", "center"),
            H("Jadwal", 26),
            LST([
                "09.00 Registrasi",
                "09.30 Pembukaan",
                "10.00 Sesi 1: Membangun aplikasi cepat",
                "13.00 Sesi 2: Data untuk pemula",
                "15.30 Diskusi panel",
            ]),
            H("Pembicara", 26),
            GAL(["speaker1", "speaker2", "speaker3", "speaker4"], 4, 48),
            FOOT("Ditemani kopi dan makan siang"),
        ]}],
    },
    "dashboard": {
        "name": "Ringkasan statistik",
        "category": "Data",
        "desc": "Kartu angka penting, daftar tugas, dan kolom pencarian laporan.",
        "title": "Ringkasan Mingguan",
        "theme": theme_of("#0891b2", "#f8fafc", "#0f172a", width=900),
        "pages": [{"name": "Ringkasan", "elements": [
            H("Ringkasan minggu ini", 34),
            CARD("Pengunjung", "12.480, naik 8% dari minggu lalu."),
            CARD("Pesanan", "342, naik 3% dari minggu lalu."),
            CARD("Pendapatan", "Rp 48,2 juta."),
            DIV(),
            H("Tugas hari ini", 24),
            LST(["Balas ulasan pelanggan", "Perbarui stok produk", "Kirim laporan ke tim"]),
            INP("Cari laporan", "Ketik kata kunci"),
            B("Unduh laporan"),
        ]}],
    },
    # ------------------------------------------------------------------
    # Template tambahan (memakai komponen bar)
    # ------------------------------------------------------------------
    "profil_perusahaan": {
        "name": "Profil perusahaan",
        "category": "Bisnis",
        "desc": "Pengumuman, angka pencapaian, daftar layanan, dan tautan sosial.",
        "title": "Karya Mandiri Teknik",
        "theme": theme_of("#1d4ed8", "#f8fafc", "#0f172a", width=820),
        "pages": [{"name": "Profil", "elements": [
            BAR("announcement", text="Kantor cabang baru kami kini buka di Surabaya.", link_text="Selengkapnya", link="#"),
            NAV("Karya Mandiri", [("Tentang", "#"), ("Layanan", "#"), ("Kontak", "#")]),
            SPC(8),
            H("Mitra teknik tepercaya sejak 2009", 38),
            P("Kami membantu pabrik dan gudang menjaga mesin tetap berjalan, dengan teknisi bersertifikat dan jadwal perawatan yang jelas."),
            IMG("factory", "Tim teknisi di lapangan"),
            BAR("statsbar", items="15 tahun|Pengalaman\n480|Klien aktif\n98%|Tepat waktu"),
            H("Layanan kami", 28),
            CARD("Perawatan berkala", "Pemeriksaan terjadwal supaya mesin tidak berhenti mendadak."),
            CARD("Perbaikan darurat", "Teknisi tiba dalam empat jam untuk area Jawa Timur."),
            CARD("Audit efisiensi", "Laporan tertulis berisi temuan dan saran penghematan energi."),
            BAR("socialbar", items="LinkedIn|#|work\nEmail|#|mail\nTelepon|#|call"),
            FOOT("© 2026 PT Karya Mandiri Teknik"),
        ]}],
    },
    "layanan_jasa": {
        "name": "Layanan jasa rumah",
        "category": "Bisnis",
        "desc": "Kategori layanan dengan ikon, alur kerja bertahap, dan ajakan memesan.",
        "title": "Sigap Rumah",
        "theme": theme_of("#0d9488", "#ffffff", "#134e4a", width=700),
        "pages": [{"name": "Layanan", "elements": [
            NAV("Sigap Rumah", [("Layanan", "#"), ("Harga", "#"), ("Bantuan", "#")]),
            SPC(8),
            H("Masalah rumah beres tanpa repot", 36),
            P("Pilih jenis layanan, tentukan jadwal, dan teknisi kami datang ke rumahmu."),
            BAR("categorybar", items="Servis AC|ac_unit\nListrik|bolt\nPipa|plumbing\nCat|format_paint\nKebersihan|cleaning_services"),
            H("Cara kerja", 26),
            BAR("stepper", steps="Pesan\nTeknisi datang\nPengerjaan\nSelesai", current=2),
            CARD("Garansi 30 hari", "Bila masalah muncul lagi, kami perbaiki tanpa biaya tambahan."),
            CARD("Harga dimuka", "Biaya diberitahukan sebelum pengerjaan dimulai."),
            B("Pesan teknisi", "#", "center"),
            FOOT("Layanan setiap hari, pukul 07.00 sampai 21.00"),
        ]}],
    },
    "tim_kami": {
        "name": "Tim kami",
        "category": "Bisnis",
        "desc": "Perkenalan anggota tim dengan bar profil dan ajakan bergabung.",
        "title": "Studio Lentera",
        "theme": theme_of("#7c3aed", "#faf5ff", "#2e1065", width=640),
        "pages": [{"name": "Tim", "elements": [
            NAV("Studio Lentera", [("Karya", "#"), ("Tim", "#"), ("Kontak", "#")]),
            SPC(8),
            H("Orang-orang di balik Lentera", 34),
            P("Tim kecil dengan latar desain, riset, dan teknologi yang bekerja dari tiga kota."),
            BAR("profilebar", name="Dewi Anggraini", role="Direktur kreatif", action="Profil"),
            BAR("profilebar", name="Bagas Pratama", role="Insinyur utama", action="Profil"),
            BAR("profilebar", name="Citra Lestari", role="Peneliti pengguna", action="Profil"),
            BAR("profilebar", name="Fajar Nugroho", role="Manajer proyek", action="Profil"),
            DIV(),
            H("Ingin bergabung?", 26, "center"),
            B("Lihat lowongan", "#", "center"),
            FOOT("© 2026 Studio Lentera"),
        ]}],
    },
    "dashboard_admin": {
        "name": "Dasbor admin",
        "category": "Data",
        "desc": "Menu samping, angka ringkas, bar progres, peringatan, toolbar, dan paginasi.",
        "title": "Toko Kita Admin",
        "theme": theme_of("#4f46e5", "#f8fafc", "#0f172a", width=920),
        "pages": [{"name": "Dasbor", "elements": [
            BAR("sidemenu", title="Toko Kita", active=1,
                items="Dasbor|dashboard\nPesanan|shopping_bag\nPelanggan|group\nLaporan|bar_chart\nPengaturan|settings"),
            H("Dasbor hari ini", 30),
            BAR("statsbar", items="128|Pesanan\nRp 9,4 jt|Pendapatan\n32|Pelanggan baru\n4,7|Rating"),
            BAR("statusbar", kind="warning", title="Stok menipis", text="Lima produk tersisa kurang dari sepuluh unit."),
            H("Penggunaan sumber daya", 22),
            BAR("progressbar", label="Penyimpanan foto produk", value=72),
            BAR("progressbar", label="Kuota pesan WhatsApp", value=45),
            BAR("progressbar", label="Kuota iklan bulan ini", value=88),
            BAR("toolbar", items="Tambah produk|add\nUnduh laporan|download\nFilter|filter_list\nMuat ulang|refresh"),
            LST(["Konfirmasi 6 pembayaran", "Balas 3 pertanyaan pelanggan", "Cetak 12 label pengiriman"]),
            BAR("pagination", pages=8, current=2),
        ]}],
    },
    "pengaturan": {
        "name": "Halaman pengaturan",
        "category": "Aplikasi",
        "desc": "Breadcrumb, tab pengaturan, isian akun, dan tombol simpan.",
        "title": "Pengaturan Akun",
        "theme": theme_of("#2563eb", "#ffffff", "#111827", width=620),
        "pages": [{"name": "Akun", "elements": [
            BAR("breadcrumb", items="Beranda\nAkun\nPengaturan"),
            H("Pengaturan", 32),
            BAR("tabbar", items="Akun\nNotifikasi\nPrivasi", active=1),
            INP("Nama lengkap", "Nama sesuai KTP"),
            INP("Email", "nama@contoh.com", "email"),
            INP("Nomor telepon", "08xxxxxxxxxx", "tel"),
            INP("Kata sandi baru", "Minimal 8 karakter", "password"),
            BAR("statusbar", kind="info", title="Tips", text="Gunakan kata sandi yang berbeda dari akun lain."),
            B("Simpan perubahan", "", "left"),
        ]}],
    },
    "onboarding": {
        "name": "Onboarding aplikasi",
        "category": "Aplikasi",
        "desc": "Tiga layar pengenalan dengan bar langkah di setiap halaman.",
        "title": "Catatin",
        "theme": theme_of("#f97316", "#fffaf5", "#431407", "Sans-serif modern", 420),
        "pages": [
            {"name": "Mulai", "elements": [
                BAR("stepper", steps="Mulai\nProfil\nSelesai", current=1),
                IMG("onboard1", "Ilustrasi catatan", 20, 600, 420),
                H("Catat apa saja, di mana saja", 30, "center"),
                P("Simpan ide, daftar belanja, dan tugas dalam satu tempat yang rapi.", "center"),
                B("Lanjut", "#", "center"),
            ]},
            {"name": "Profil", "elements": [
                BAR("stepper", steps="Mulai\nProfil\nSelesai", current=2),
                H("Kenalan dulu", 30, "center"),
                INP("Nama panggilan", "Mau dipanggil apa?"),
                INP("Email", "nama@contoh.com", "email"),
                B("Lanjut", "#", "center"),
            ]},
            {"name": "Selesai", "elements": [
                BAR("stepper", steps="Mulai\nProfil\nSelesai", current=3),
                IMG("onboard3", "Ilustrasi selesai", 20, 600, 420),
                H("Semua siap", 30, "center"),
                P("Buat catatan pertamamu sekarang.", "center"),
                B("Mulai mencatat", "#", "center"),
            ]},
        ],
    },
    "detail_produk": {
        "name": "Detail produk",
        "category": "Toko dan kuliner",
        "desc": "Foto produk, rating bintang, spesifikasi, dan bar harga yang menempel di bawah.",
        "title": "Tas Anyaman Lombok",
        "theme": theme_of("#b45309", "#fffbeb", "#451a03", "Serif klasik", 640),
        "pages": [{"name": "Produk", "elements": [
            BAR("breadcrumb", items="Beranda\nTas\nTas Anyaman Lombok"),
            IMG("bag", "Tas anyaman", 16, 800, 560),
            H("Tas Anyaman Lombok", 32),
            BAR("ratingbar", label="Ulasan pembeli", value=4.5, count="(212 ulasan)"),
            P("Dianyam tangan oleh pengrajin Lombok dari serat pandan, ringan dan kuat untuk dipakai sehari-hari."),
            LST(["Bahan: pandan dan kulit sintetis", "Ukuran: 32 x 24 x 12 cm", "Berat: 480 gram", "Warna: cokelat alami"]),
            CARD("Garansi pengrajin", "Jahitan lepas dalam 60 hari kami perbaiki gratis."),
            BAR("pricebar", price="Rp 189.000", caption="Gratis ongkir Jawa dan Bali", button="Beli sekarang", link="#"),
        ]}],
    },
    "checkout": {
        "name": "Keranjang dan checkout",
        "category": "Toko dan kuliner",
        "desc": "Langkah pembayaran, isian alamat, kode promo, dan ringkasan harga.",
        "title": "Checkout",
        "theme": theme_of("#16a34a", "#ffffff", "#14532d", width=620),
        "pages": [{"name": "Alamat", "elements": [
            BAR("breadcrumb", items="Keranjang\nCheckout"),
            BAR("stepper", steps="Keranjang\nAlamat\nPembayaran\nSelesai", current=2),
            H("Alamat pengiriman", 28),
            INP("Nama penerima", "Nama lengkap"),
            INP("Alamat", "Jalan, nomor, kecamatan"),
            INP("Nomor telepon", "08xxxxxxxxxx", "tel"),
            BAR("statusbar", kind="success", title="Promo terpasang", text="Potongan Rp 15.000 untuk pesanan pertama."),
            CARD("Ringkasan pesanan", "2 barang, ongkir Rp 12.000, potongan Rp 15.000."),
            BAR("pricebar", price="Rp 246.000", caption="Total yang dibayar", button="Lanjut bayar", link="#"),
        ]}],
    },
    "galeri_foto": {
        "name": "Galeri foto",
        "category": "Konten",
        "desc": "Pencarian, filter kategori, dua galeri, paginasi, dan tombol unggah melayang.",
        "title": "Galeri Nusantara",
        "theme": theme_of("#e11d48", "#fff1f2", "#4c0519", width=860),
        "pages": [{"name": "Galeri", "elements": [
            H("Galeri Nusantara", 34),
            BAR("searchbar", placeholder="Cari foto atau fotografer", button="Cari"),
            BAR("filterbar", items="Semua\nAlam\nKota\nPotret\nKuliner", active=1),
            GAL(["g1", "g2", "g3", "g4", "g5", "g6"], 3, 12),
            GAL(["g7", "g8", "g9"], 3, 12),
            BAR("pagination", pages=12, current=1),
            BAR("fab", icon="add_a_photo", text="Unggah", align="right"),
        ]}],
    },
    "testimoni": {
        "name": "Testimoni dan ulasan",
        "category": "Konten",
        "desc": "Rating rata-rata, statistik kepuasan, dan kutipan pelanggan.",
        "title": "Kata Mereka",
        "theme": theme_of("#d97706", "#ffffff", "#1f2937", width=680),
        "pages": [{"name": "Ulasan", "elements": [
            H("Kata pelanggan kami", 34, "center"),
            BAR("ratingbar", label="Rata-rata dari semua ulasan", value=4.8, count="(1.204 ulasan)"),
            BAR("statsbar", items="96%|Merekomendasikan\n4,8|Rating\n1,2 rb|Ulasan"),
            CARD("Rina, Bandung", "Pesanan sampai lebih cepat dari perkiraan dan kemasannya rapi."),
            CARD("Yoga, Medan", "Adminnya sabar menjawab semua pertanyaan sebelum saya membeli."),
            CARD("Mega, Makassar", "Sudah tiga kali pesan ulang, kualitasnya konsisten."),
            B("Tulis ulasanmu", "#", "center"),
            FOOT("Ulasan diverifikasi dari pembelian nyata"),
        ]}],
    },
    "pricing": {
        "name": "Paket harga",
        "category": "Bisnis",
        "desc": "Tiga paket langganan, pilihan periode, dan pengumuman diskon tahunan.",
        "title": "Paket Harga",
        "theme": theme_of("#0ea5e9", "#f0f9ff", "#0c4a6e", width=700),
        "pages": [{"name": "Harga", "elements": [
            BAR("announcement", text="Hemat 20% dengan paket tahunan.", link_text="Pilih tahunan", link="#"),
            H("Pilih paket yang pas", 36, "center"),
            P("Mulai gratis, naik paket kapan saja tanpa kehilangan data.", "center"),
            BAR("filterbar", items="Bulanan\nTahunan", active=1),
            CARD("Starter, Rp 0", "Satu proyek, 100 MB penyimpanan, dukungan komunitas."),
            CARD("Pro, Rp 99.000 per bulan", "Proyek tanpa batas, 20 GB penyimpanan, dukungan email."),
            CARD("Bisnis, Rp 299.000 per bulan", "Lima anggota tim, 200 GB penyimpanan, dukungan prioritas."),
            LST(["Semua paket memakai enkripsi data", "Batalkan kapan saja", "Faktur pajak tersedia"]),
            B("Mulai gratis", "#", "center"),
        ]}],
    },
    "halaman_404": {
        "name": "Halaman 404",
        "category": "Utilitas",
        "desc": "Pesan halaman tidak ditemukan dengan pencarian dan tombol kembali.",
        "title": "Tidak ditemukan",
        "theme": theme_of("#6366f1", "#ffffff", "#1e1b4b", width=560),
        "pages": [{"name": "404", "elements": [
            BAR("breadcrumb", items="Beranda\nTidak ditemukan"),
            SPC(40),
            H("404", 72, "center"),
            H("Halaman tidak ditemukan", 26, "center"),
            P("Alamat yang kamu buka mungkin salah ketik atau halamannya sudah dipindahkan. Coba cari dari sini.", "center"),
            BAR("searchbar", placeholder="Cari halaman", button="Cari"),
            B("Kembali ke beranda", "#", "center"),
        ]}],
    },
    "newsletter": {
        "name": "Langganan newsletter",
        "category": "Konten",
        "desc": "Formulir email, tautan sosial, dan bar persetujuan cookie.",
        "title": "Surat Senin",
        "theme": theme_of("#be185d", "#fdf2f8", "#500724", "Serif klasik", 560),
        "pages": [{"name": "Langganan", "elements": [
            BAR("announcement", text="Edisi terbaru terbit setiap Senin pagi.", link_text="Baca arsip", link="#"),
            SPC(16),
            H("Satu surel seminggu, isinya padat", 36, "center"),
            P("Ringkasan kabar teknologi dan desain yang bisa dibaca dalam lima menit.", "center"),
            INP("Alamat email", "nama@contoh.com", "email"),
            B("Berlangganan", "#", "center"),
            BAR("socialbar", items="Instagram|#|photo_camera\nThreads|#|forum\nRSS|#|rss_feed"),
            BAR("cookiebar", text="Kami memakai cookie untuk mengukur jumlah pembaca.", accept="Terima", decline="Tolak"),
            FOOT("Berhenti berlangganan kapan saja"),
        ]}],
    },
    "donasi": {
        "name": "Penggalangan donasi",
        "category": "Sosial",
        "desc": "Progres dana terkumpul, pilihan nominal, dan bar harga untuk donasi.",
        "title": "Perpustakaan Desa",
        "theme": theme_of("#dc2626", "#fff7ed", "#450a0a", width=640),
        "pages": [{"name": "Donasi", "elements": [
            IMG("library", "Anak-anak membaca buku", 16, 800, 440),
            H("Bantu bangun perpustakaan desa", 32),
            P("Dana dipakai untuk rak buku, 1.000 judul buku anak, dan honor pustakawan selama setahun."),
            BAR("progressbar", label="Terkumpul Rp 38 juta dari Rp 50 juta", value=76),
            BAR("statsbar", items="412|Donatur\n12|Hari tersisa\n76%|Tercapai"),
            H("Pilih nominal", 22),
            BAR("filterbar", items="Rp 25.000\nRp 50.000\nRp 100.000\nLainnya", active=2),
            INP("Nama (boleh disamarkan)", "Hamba Allah"),
            BAR("pricebar", price="Rp 50.000", caption="Donasi pilihanmu", button="Donasi sekarang", link="#"),
        ]}],
    },
    "app_navbawah": {
        "name": "Aplikasi mobile dengan navigasi bawah",
        "category": "Aplikasi",
        "desc": "Pencarian, kategori ikon, filter, kartu rekomendasi, dan navigasi bawah.",
        "title": "Jajan Dekat",
        "theme": theme_of("#ea580c", "#ffffff", "#431407", width=420),
        "pages": [{"name": "Beranda", "elements": [
            H("Mau jajan apa hari ini?", 26),
            BAR("searchbar", placeholder="Cari makanan atau warung", button="Cari"),
            BAR("categorybar", items="Nasi|rice_bowl\nMie|ramen_dining\nKopi|local_cafe\nKue|cake\nSemua|apps"),
            BAR("filterbar", items="Terdekat\nTerlaris\nBuka 24 jam", active=1),
            CARD("Warung Bu Tini", "Nasi pecel dan rempeyek, 350 m dari lokasimu."),
            CARD("Kopi Sudut", "Kopi susu gula aren, buka sampai tengah malam."),
            CARD("Mie Ayam Pak Joko", "Porsi besar, antrean cepat saat jam makan siang."),
            BAR("bottomnav", items="Beranda|home\nJelajah|explore\nPesanan|receipt_long\nProfil|person", active=1),
        ]}],
    },
}


def template_design(key):
    """Buat salinan desain dari template, lengkap dengan id baru."""
    tpl = copy.deepcopy(TEMPLATES[key])
    theme = default_design()["theme"]
    theme.update(tpl["theme"])
    pages = tpl["pages"]
    for page in pages:
        page["id"] = uuid.uuid4().hex[:8]
        for el in page["elements"]:
            el["id"] = uuid.uuid4().hex[:8]
    return {"title": tpl["title"], "theme": theme, "pages": pages}


def apply_template():
    key = st.session_state.get("tpl_choice")
    if key not in TEMPLATES:
        return
    new = template_design(key)
    mode = st.session_state.get("tpl_mode", "Ganti seluruh desain")
    if mode == "Ganti seluruh desain":
        load_design(new)
    else:
        pages = st.session_state.design["pages"]
        start = len(pages)
        pages.extend(new["pages"])
        st.session_state.page_idx = start
        st.session_state.selected_id = None
    st.session_state.tpl_preview = False


def preview_template(key):
    if key in TEMPLATES:
        st.session_state.tpl_choice = key
        st.session_state.tpl_preview = True
        st.session_state.view_mode = "Preview"


def close_template_preview():
    st.session_state.tpl_preview = False


def use_template(key):
    if key in TEMPLATES:
        st.session_state.tpl_choice = key
        apply_template()


# Referensi gaya desain: palet, font, dan bentuk elemen siap pakai.
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


def apply_design_ref(name):
    ref = DESIGN_REFS.get(name)
    if not ref:
        return
    design = st.session_state.design
    design["theme"].update(copy.deepcopy(ref["theme"]))
    if st.session_state.get("ref_shape", True):
        for page in design["pages"]:
            for el in page["elements"]:
                if el.get("type") not in SHAPE_TYPES:
                    continue
                style = ensure_element_style(el)
                style.update(ref["shape"])
                if el["type"] in SURFACE_TYPES:
                    style["background"] = ref["surface"]
                    style["color"] = ref["ink"]
                # Hapus state widget lama supaya panel properti memakai nilai terbaru.
                for k in [k for k in st.session_state.keys() if str(k).startswith(f"{el['id']}_")]:
                    del st.session_state[k]


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


# ---------------------------------------------------------------------------
# Generator HTML
# ---------------------------------------------------------------------------
def esc(value):
    return html.escape(str(value), quote=True)


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


def lines_of(value):
    return [ln.strip() for ln in str(value or "").splitlines() if ln.strip()]


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


def render_element(el):
    t = el["type"]
    common = element_style_attr(el)
    if t == "navbar":
        links = "".join(
            f'<a href="{esc(safe_url(url))}">{esc(label)}</a>'
            for label, url in parse_links(el.get("links"))
        )
        return (
            f'<header class="topbar" style="{common}"><strong>{esc(el.get("brand", ""))}</strong>'
            f"<nav>{links}</nav></header>"
        )
    if t == "heading":
        return (
            f'<h1 style="{element_style_attr(el, f"font-size:{num(el.get("size"), 36)}px;text-align:{align_of(el)};")}">'
            f'{esc(el.get("text", ""))}</h1>'
        )
    if t == "text":
        return f'<p style="{element_style_attr(el, f"text-align:{align_of(el)};")}">{esc(el.get("text", ""))}</p>'
    if t == "button":
        label = esc(el.get("text", ""))
        link = (el.get("link") or "").strip()
        button_style = element_style_attr(el, "display:inline-block;font:inherit;text-decoration:none;cursor:pointer;")
        inner = (
            f'<a class="btn" style="{button_style}" href="{esc(safe_url(link))}">{label}</a>'
            if link
            else f'<button class="btn" style="{button_style}" type="button">{label}</button>'
        )
        return f'<div style="text-align:{align_of(el)}">{inner}</div>'
    if t == "image":
        style = element_style_attr(el, "display:block;max-width:100%;height:auto;")
        return f'<img src="{esc(safe_url(el.get("url", "")))}" alt="{esc(el.get("alt", ""))}" style="{style}">'
    if t == "gallery":
        cols = min(max(num(el.get("columns"), 3), 1), 4)
        gallery_style = element_style_attr(el, f"display:grid;gap:10px;grid-template-columns:repeat({cols},1fr);")
        imgs = "".join(
            f'<img src="{esc(safe_url(u))}" alt="Gambar galeri {n}" style="width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:{max(0, int(ensure_element_style(el).get("radius", 8) or 0))}px">'
            for n, u in enumerate(lines_of(el.get("urls")), start=1)
        )
        return f'<div class="gallery" style="{gallery_style}">{imgs}</div>'
    if t == "list":
        tag = "ol" if el.get("style") == "number" else "ul"
        items = "".join(f"<li>{esc(i)}</li>" for i in lines_of(el.get("items")))
        return f'<{tag} style="{element_style_attr(el)}">{items}</{tag}>'
    if t == "input":
        style = ensure_element_style(el)
        input_style = (
            f'width:100%;padding:10px 12px;font:inherit;'
            f'background:{esc(style.get("background", "transparent"))};color:{esc(style.get("color", "inherit"))};'
            f'border:{max(1, int(style.get("border_width", 0) or 0))}px solid {esc(style.get("border_color", "#d1d5db"))};'
            f'border-radius:{max(0, int(style.get("radius", 8) or 0))}px;box-shadow:{esc(style.get("shadow", "none"))};'
        )
        label_style = f'color:{esc(style.get("color", "inherit"))};'
        return (
            f'<label class="field" style="width:{esc(style.get("width", "auto"))};padding:{max(0, int(style.get("padding", 0) or 0))}px;">'
            f'<span style="{label_style}">{esc(el.get("label", ""))}</span>'
            f'<input type="{input_kind(el)}" placeholder="{esc(el.get("placeholder", ""))}" style="{input_style}"></label>'
        )
    if t == "card":
        return (
            f'<div class="card" style="{common}"><h3>{esc(el.get("title", ""))}</h3>'
            f'<p>{esc(el.get("text", ""))}</p></div>'
        )
    if t == "divider":
        style = ensure_element_style(el)
        bw = max(1, int(style.get("border_width", 1) or 1))
        return f'<hr style="border:0;border-top:{bw}px solid {esc(style.get("border_color", "#d1d5db"))};margin:0 0 16px;box-shadow:{esc(style.get("shadow", "none"))};width:{esc(style.get("width", "100%"))}">'
    if t == "spacer":
        return f'<div style="height:{num(el.get("height"), 24)}px;background:{esc(ensure_element_style(el).get("background", "transparent"))};border-radius:{max(0, int(ensure_element_style(el).get("radius", 8) or 0))}px;"></div>'
    if t == "footer":
        return f'<footer class="footer" style="{common}">{esc(el.get("text", ""))}</footer>'
    if t in BAR_SPECS:
        return render_bar(el)
    return ""


def mark_selected(rendered):
    """Beri penanda pada tag pertama supaya elemen terpilih tersorot di preview."""
    return re.sub(r"^<(\w+)", r'<\1 data-sel="1"', rendered, count=1)


def build_html(design, highlight_id=None, active=0, builder_mode=False):
    theme = design["theme"]
    font = FONTS.get(theme.get("font"), FONTS["Sans-serif modern"])
    pages = design["pages"]
    multi = len(pages) > 1
    active = min(max(active, 0), len(pages) - 1)

    nav = ""
    if multi:
        links = "".join(
            f'<button type="button" class="nav-btn{" active" if i == active else ""}" '
            f'data-target="page-{i}">{esc(p["name"])}</button>'
            for i, p in enumerate(pages)
        )
        nav = f'<nav class="nav">{links}</nav>'

    sections = []
    for i, page in enumerate(pages):
        parts = []
        for el in page["elements"]:
            rendered = render_element(el)
            if builder_mode:
                selected_attr = ' data-sel="1"' if highlight_id and el.get("id") == highlight_id else ""
                rendered = (
                    f'<div class="builder-element" data-element-id="{esc(el.get("id", ""))}"{selected_attr}>'
                    f'{rendered}</div>'
                )
            elif highlight_id and el.get("id") == highlight_id:
                rendered = mark_selected(rendered)
            parts.append(rendered)
        body = "\n".join(parts) or '<p class="empty">Halaman ini masih kosong.</p>'
        hidden = "" if i == active else " hidden"
        sections.append(f'<section id="page-{i}" class="page"{hidden}>\n{body}\n</section>')

    highlight_css = (
        "  [data-sel] { outline: 2px dashed #f59e0b; outline-offset: 4px; }\n"
        if highlight_id
        else ""
    )
    builder_css = ""
    builder_script = ""
    if builder_mode:
        builder_css = """
  .builder-element { position: relative; border: 1px solid transparent; border-radius: 6px; transition: outline .12s, background .12s, border-color .12s; cursor: pointer; }
  .builder-element:hover { border-color: rgba(99,102,241,.42); outline: 2px solid rgba(99,102,241,.12); outline-offset: 2px; }
  .builder-element[data-sel] { border-color: #6366f1; outline: 2px solid rgba(99,102,241,.18); outline-offset: 3px; }
  .builder-element > * { margin-top: 0 !important; margin-bottom: 0 !important; }
"""
        builder_script = """
<script>
  document.addEventListener("click", function (event) {
    var el = event.target.closest ? event.target.closest("[data-element-id]") : null;
    if (!el) return;
    event.preventDefault();
    event.stopPropagation();
    window.parent.postMessage({type:"ui-builder-select", id:el.getAttribute("data-element-id")}, "*");
  }, true);
</script>"""

    script = ""
    if multi:
        script = """
<script>
  document.querySelectorAll('.nav-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.page').forEach(function (p) { p.hidden = true; });
      document.querySelectorAll('.nav-btn').forEach(function (b) { b.classList.remove('active'); });
      document.getElementById(btn.dataset.target).hidden = false;
      btn.classList.add('active');
    });
  });
</script>"""

    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(design["title"])}</title>
{ICON_LINK}
<style>
  :root {{
    --primary: {esc(theme["primary"])};
    --on-primary: {on_color(theme["primary"])};
    --bg: {esc(theme["bg"])};
    --text: {esc(theme["text"])};
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: {font};
    line-height: 1.6;
  }}
  .app {{
    max-width: {num(theme["width"], 720)}px;
    margin: 0 auto;
    padding: 24px 20px 48px;
  }}
  .app-title {{ margin: 0 0 16px; font-size: 14px; opacity: .6; }}
  .nav {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px; }}
  .nav-btn {{
    border: 1px solid var(--primary);
    background: transparent;
    color: var(--primary);
    padding: 6px 14px;
    border-radius: 999px;
    cursor: pointer;
    font: inherit;
  }}
  .nav-btn.active {{ background: var(--primary); color: var(--on-primary); }}
  .page > * {{ margin-top: 0; margin-bottom: 16px; }}
  h1, h3 {{ line-height: 1.2; }}
  img {{ max-width: 100%; height: auto; display: block; }}
  hr {{ border: 0; border-top: 1px solid rgba(128,128,128,.35); }}
  ul, ol {{ padding-left: 1.4em; }}
  .btn {{
    display: inline-block;
    background: var(--primary);
    color: var(--on-primary);
    border: 0;
    padding: 10px 20px;
    border-radius: 8px;
    font: inherit;
    text-decoration: none;
    cursor: pointer;
  }}
  .btn:focus-visible, .nav-btn:focus-visible, input:focus-visible, .topbar a:focus-visible {{
    outline: 3px solid var(--primary);
    outline-offset: 2px;
  }}
  .topbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(128,128,128,.35);
  }}
  .topbar nav {{ display: flex; gap: 16px; flex-wrap: wrap; }}
  .topbar a {{ color: var(--text); text-decoration: none; }}
  .topbar a:hover {{ color: var(--primary); }}
  .gallery {{ display: grid; gap: 10px; }}
  .gallery img {{ width: 100%; aspect-ratio: 4 / 3; object-fit: cover; }}
  .field {{ display: block; }}
  .field span {{ display: block; margin-bottom: 4px; font-size: 14px; }}
  .field input {{
    width: 100%;
    padding: 10px 12px;
    border: 1px solid rgba(128,128,128,.5);
    border-radius: 8px;
    font: inherit;
    background: transparent;
    color: inherit;
  }}
  .card {{
    border: 1px solid rgba(128,128,128,.35);
    border-radius: 12px;
    padding: 16px 18px;
  }}
  .card h3 {{ margin: 0 0 6px; }}
  .card p {{ margin: 0; }}
  .footer {{
    text-align: center;
    font-size: 14px;
    opacity: .65;
    padding-top: 16px;
    border-top: 1px solid rgba(128,128,128,.35);
  }}
  .empty {{ opacity: .5; font-style: italic; }}
{BAR_CSS}{highlight_css}{builder_css}</style>
</head>
<body>
<main class="app">
<p class="app-title">{esc(design["title"])}</p>
{nav}
{chr(10).join(sections)}
</main>{script}{builder_script}
</body>
</html>
"""


def device_frame(inner_html, width):
    """Bungkus preview dalam bingkai perangkat dengan lebar tertentu."""
    w = f"{width}px" if width else "100%"
    return (
        '<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
        "html,body{margin:0;height:100%;background:#e5e7eb}"
        "body{display:flex;justify-content:center;padding:12px;box-sizing:border-box}"
        f"iframe{{width:{w};max-width:100%;height:100%;border:0;background:#fff;"
        "border-radius:10px;box-shadow:0 2px 12px rgba(0,0,0,.18)}}"
        f'</style></head><body><iframe srcdoc="{html.escape(inner_html, quote=True)}">'
        "</iframe></body></html>"
    )


# ---------------------------------------------------------------------------
# Generator Prompt Master AI
# ---------------------------------------------------------------------------
def describe_element(el, number):
    t = el["type"]
    label = ELEMENT_LABELS[t]
    if t == "navbar":
        menu = ", ".join(f"{a} -> {b}" for a, b in parse_links(el.get("links")))
        detail = f'merek "{el.get("brand", "")}", menu: {menu or "-"}'
    elif t == "heading":
        detail = f'teks "{el.get("text", "")}", ukuran {el.get("size")}px, rata {el.get("align")}'
    elif t == "text":
        detail = f'teks "{el.get("text", "")}", rata {el.get("align")}'
    elif t == "button":
        link = el.get("link") or "tanpa tautan"
        detail = f'label "{el.get("text", "")}", tautan: {link}, rata {el.get("align")}'
    elif t == "image":
        detail = (
            f'sumber {el.get("url")}, teks alternatif "{el.get("alt", "")}", '
            f'sudut membulat {el.get("radius")}px'
        )
    elif t == "gallery":
        detail = (
            f'{el.get("columns")} kolom, sudut membulat {el.get("radius")}px, gambar: '
            + ", ".join(lines_of(el.get("urls")))
        )
    elif t == "list":
        gaya = "bernomor" if el.get("style") == "number" else "berpoin"
        detail = f"daftar {gaya} dengan item: " + "; ".join(lines_of(el.get("items")))
    elif t == "input":
        detail = (
            f'label "{el.get("label", "")}", placeholder "{el.get("placeholder", "")}", '
            f'jenis isian: {INPUT_KINDS[input_kind(el)].lower()}'
        )
    elif t == "card":
        detail = f'judul "{el.get("title", "")}", isi "{el.get("text", "")}"'
    elif t == "divider":
        detail = "garis horizontal tipis"
    elif t == "footer":
        detail = f'teks "{el.get("text", "")}", rata tengah'
    elif t in BAR_SPECS:
        detail = describe_bar(el)
    else:
        detail = f'tinggi {el.get("height")}px'
    return f"   {number}. {label}: {detail}"


def build_prompt(design, target="HTML/CSS/JavaScript satu file"):
    theme = design["theme"]
    lines = [
        f'Bangun aplikasi web bernama "{design["title"]}" menggunakan {target}.',
        "Ikuti spesifikasi desain di bawah ini secara persis, termasuk urutan elemen, teks, dan nilai propertinya.",
        "",
        "## Tema visual",
        f'- Warna utama (tombol, aksen): {theme["primary"]}',
        f'- Warna latar: {theme["bg"]}',
        f'- Warna teks: {theme["text"]}',
        f'- Font: {theme["font"]} ({FONTS.get(theme["font"], "")})',
        f'- Lebar maksimum konten: {theme["width"]}px, diletakkan di tengah',
        "",
        f"## Struktur halaman ({len(design['pages'])} halaman)",
    ]
    for i, page in enumerate(design["pages"], start=1):
        lines.append(f'{i}. Halaman "{page["name"]}"')
        if page["elements"]:
            lines.append("   Elemen dari atas ke bawah:")
            for n, el in enumerate(page["elements"], start=1):
                lines.append(describe_element(el, n))
        else:
            lines.append("   (halaman kosong)")
    lines += ["", "## Aturan tambahan"]
    if len(design["pages"]) > 1:
        lines.append("- Sediakan navigasi antar halaman di bagian atas tanpa memuat ulang browser.")
    lines += [
        "- Tampilan harus responsif sampai ukuran layar ponsel.",
        "- Nama ikon pada spesifikasi mengacu ke Material Symbols (Google); pakai ikon yang sama.",
        "- Gunakan HTML semantik dan pastikan fokus keyboard terlihat jelas.",
        "- Jangan menambahkan elemen, teks, atau fitur di luar spesifikasi ini.",
        "- Berikan hasil akhir berupa kode lengkap yang bisa langsung dijalankan.",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Komponen seret dan lepas (HTML5 drag-and-drop, tanpa paket tambahan)
# ---------------------------------------------------------------------------
DND_HTML = r'''
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0">
<style>
  .mi { font-family:'Material Symbols Rounded'; font-size:18px; line-height:1; display:inline-block;
    width:1em; overflow:hidden; white-space:nowrap; vertical-align:middle; font-feature-settings:'liga'; }
  :root { --fg:#31333f; --bg2:#f0f2f6; --accent:#ff4b4b; --line:rgba(128,128,128,.35); }
  *{box-sizing:border-box} html,body{margin:0;padding:0;background:transparent;color:var(--fg);
    font-family:Inter,system-ui,sans-serif;font-size:13px}
  .title{font-weight:700;margin:2px 0 5px}.hint{opacity:.62;font-size:11px;margin:0 0 8px}
  #list{list-style:none;margin:0;padding:6px;min-height:74px;border:1px dashed var(--line);
    border-radius:12px;max-height:280px;overflow:auto}
  #list:empty::before{content:"Tarik komponen ke sini, atau pilih komponen di bawah";
    display:block;text-align:center;opacity:.55;padding:26px 8px}
  #list.ins-empty{border-color:var(--accent);background:var(--bg2)}
  li{display:flex;align-items:center;gap:7px;padding:8px 9px;margin:0 0 6px;border:1px solid var(--line);
    border-radius:9px;background:var(--bg2);cursor:grab;user-select:none;position:relative}
  li.sel{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
  li.dragging{opacity:.4}
  li.ins-before::before,li.ins-after::after{content:"";position:absolute;left:0;right:0;height:3px;
    background:var(--accent);border-radius:2px}
  li.ins-before::before{top:-5px} li.ins-after::after{bottom:-5px}
  .grip{opacity:.45}.lbl{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .del{border:0;background:transparent;color:inherit;cursor:pointer;opacity:.55;padding:0 3px}
  .del:hover{opacity:1;color:var(--accent)}
</style>
</head>
<body>
<div class="title">Susunan halaman</div>
<p class="hint">Klik untuk memilih · seret untuk mengubah urutan · × untuk menghapus</p>
<ul id="list"></ul>
<script>
(function(){
  var items=[],selected=null,drag=null;
  var listEl=document.getElementById("list");
  function post(type,data){window.parent.postMessage(Object.assign({isStreamlitMessage:true,type:type},data),"*");}
  function send(payload){payload.id=Date.now()+"-"+Math.random().toString(36).slice(2);
    post("streamlit:setComponentValue",{value:payload,dataType:"json"});}
  function fit(){post("streamlit:setFrameHeight",{height:Math.min(document.documentElement.scrollHeight+4,360)});}
  function clearInd(){listEl.classList.remove("ins-empty");
    listEl.querySelectorAll("li").forEach(function(li){li.classList.remove("ins-before","ins-after");});}
  function indexAt(y){var lis=listEl.querySelectorAll("li"),idx=0;
    for(var i=0;i<lis.length;i++){var r=lis[i].getBoundingClientRect();if(y>r.top+r.height/2)idx++;else break;}return idx;}
  function showInd(idx){clearInd();var lis=listEl.querySelectorAll("li");
    if(!lis.length){listEl.classList.add("ins-empty");return;}
    if(idx<lis.length)lis[idx].classList.add("ins-before");else lis[lis.length-1].classList.add("ins-after");}
  function icon(name){var s=document.createElement("span");s.className="mi";s.textContent=name;return s;}
  function fit(){post("streamlit:setFrameHeight",{height:78});}
  function render(){
    listEl.textContent="";
    items.forEach(function(it,i){
      var li=document.createElement("li");li.draggable=true;li.dataset.id=it.id;
      if(it.id===selected)li.classList.add("sel");
      var grip=document.createElement("span");grip.className="grip";grip.textContent="⠿";
      var lbl=document.createElement("span");lbl.className="lbl";lbl.appendChild(icon(it.icon));
      lbl.appendChild(document.createTextNode(" "+(i+1)+". "+it.label));
      var del=document.createElement("button");del.className="del";del.type="button";del.title="Hapus";
      del.appendChild(icon("close"));del.addEventListener("click",function(e){e.stopPropagation();send({action:"delete",target:it.id});});
      li.appendChild(grip);li.appendChild(lbl);li.appendChild(del);
      li.addEventListener("click",function(){send({action:"select",target:it.id});});
      li.addEventListener("dragstart",function(e){drag={id:it.id};li.classList.add("dragging");
        e.dataTransfer.setData("text/plain","move:"+it.id);e.dataTransfer.effectAllowed="move";});
      li.addEventListener("dragend",function(){drag=null;li.classList.remove("dragging");clearInd();});
      listEl.appendChild(li);
    });
    fit();
  }
  listEl.addEventListener("dragover",function(e){
    var external=e.dataTransfer.getData("text/plain")||"";
    if(!drag && !external.startsWith("new:"))return;
    e.preventDefault();
    e.dataTransfer.dropEffect=external.startsWith("new:")?"copy":"move";
    showInd(indexAt(e.clientY));
  });
  listEl.addEventListener("dragleave",function(e){if(!listEl.contains(e.relatedTarget))clearInd();});
  listEl.addEventListener("drop",function(e){
    e.preventDefault();
    var external=e.dataTransfer.getData("text/plain")||"";
    var idx=indexAt(e.clientY);clearInd();
    if(external.startsWith("new:")){
      send({action:"insert",type:external.slice(4),index:idx});
      drag=null;
      return;
    }
    if(!drag)return;
    var ids=items.map(function(x){return x.id;});
    var from=ids.indexOf(drag.id);if(from<0){drag=null;return;}var to=idx;if(from<to)to--;
    if(to!==from){ids.splice(from,1);ids.splice(to,0,drag.id);selected=drag.id;send({action:"reorder",order:ids,selected:drag.id});}
    drag=null;
  });
  window.addEventListener("message",function(e){
    var d=e.data;if(!d||d.type!=="streamlit:render")return;
    var a=d.args||{};items=a.items||[];selected=a.selected||null;render();
  });
  window.addEventListener("resize",fit);
  post("streamlit:componentReady",{apiVersion:1});
})();
</script>
</body>
</html>
'''

PALETTE_HTML = r'''
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0">
<style>
  *{box-sizing:border-box}html,body{margin:0;padding:0;background:transparent;font-family:Inter,system-ui,sans-serif;color:#252733}
  .dock{border:1px solid rgba(128,128,128,.28);background:rgba(255,255,255,.72);border-radius:16px;padding:10px 12px;
    box-shadow:0 8px 24px rgba(0,0,0,.06)}
  .head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:8px}
  .title{font-size:13px;font-weight:700}.hint{font-size:11px;opacity:.58}
  .scroll{display:flex;gap:7px;overflow-x:auto;padding:2px 1px 5px;scrollbar-width:thin}
  .chip{flex:0 0 auto;display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(128,128,128,.28);
    background:#f5f6f8;border-radius:10px;padding:8px 11px;font-size:12px;cursor:pointer;white-space:nowrap;
    transition:.12s}
  .chip:hover{transform:translateY(-1px);border-color:#6366f1;background:#eef2ff}
  .chip .mi{font-family:'Material Symbols Rounded';font-size:17px;line-height:1}
  .group{flex:0 0 auto;font-size:10px;font-weight:700;opacity:.55;padding:8px 3px 0}
</style>
</head>
<body>
<div class="dock">
  <div class="head"><div class="title">Komponen</div><div class="hint">Klik komponen untuk menambah ke Susunan</div></div>
  <div id="scroll" class="scroll"></div>
</div>
<script>
(function(){
  var palette=[],root=document.getElementById("scroll");
  function post(type,data){window.parent.postMessage(Object.assign({isStreamlitMessage:true,type:type},data),"*");}
  function send(payload){payload.id=Date.now()+"-"+Math.random().toString(36).slice(2);
    post("streamlit:setComponentValue",{value:payload,dataType:"json"});}
  function fit(){post("streamlit:setFrameHeight",{height:96});}
  function icon(name){var s=document.createElement("span");s.className="mi";s.textContent=name;return s;}
  function render(){
    root.textContent="";var last="";
    palette.forEach(function(p){
      if(p.group!==last){var g=document.createElement("span");g.className="group";g.textContent=p.group;root.appendChild(g);last=p.group;}
      var c=document.createElement("button");c.type="button";c.className="chip";c.draggable=true;
      c.appendChild(icon(p.icon||"widgets"));
      c.appendChild(document.createTextNode(p.label));c.title="Klik atau seret ke Susunan";
      c.addEventListener("dragstart",function(e){
        e.dataTransfer.setData("text/plain","new:"+p.type);
        e.dataTransfer.effectAllowed="copy";
      });
      c.addEventListener("click",function(){send({action:"insert",type:p.type});});
      root.appendChild(c);
    });
    fit();
  }
  window.addEventListener("message",function(e){var d=e.data;if(!d||d.type!=="streamlit:render")return;
    palette=(d.args||{}).palette||[];render();});
  post("streamlit:componentReady",{apiVersion:1});
})();
</script>
</body>
</html>
'''

PREVIEW_HTML = r'''
<!DOCTYPE html>
<html lang="id">
<head><meta charset="utf-8"><style>
html,body{margin:0;width:100%;height:100%;background:#e5e7eb}
body{display:flex;justify-content:center;padding:12px;box-sizing:border-box;overflow:hidden}
iframe{width:100%;height:100%;border:0;background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,.18)}
</style></head>
<body><iframe id="preview"></iframe>
<script>
(function(){
  var frame=document.getElementById("preview");
  function post(type,data){window.parent.postMessage(Object.assign({isStreamlitMessage:true,type:type},data),"*");}
  function send(payload){payload.id=Date.now()+"-"+Math.random().toString(36).slice(2);
    post("streamlit:setComponentValue",{value:payload,dataType:"json"});}
  function fit(){post("streamlit:setFrameHeight",{height:620});}
  window.addEventListener("message",function(e){
    var d=e.data;if(!d)return;
    if(d.type==="streamlit:render"){
      var a=d.args||{};frame.style.width=a.deviceWidth?a.deviceWidth+"px":"100%";frame.style.maxWidth="100%";
      frame.srcdoc=a.html||"";fit();
    }
    if(d.type==="ui-builder-select"&&d.id){send({action:"select",target:d.id});}
  });
  post("streamlit:componentReady",{apiVersion:1});
})();
</script>
</body>
</html>
'''

@st.cache_resource
def get_dnd_component():
    digest = hashlib.md5(DND_HTML.encode("utf-8")).hexdigest()[:8]
    folder = Path(tempfile.gettempdir()) / f"ui_builder_dnd_{digest}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(DND_HTML, encoding="utf-8")
    return components.declare_component(f"ui_builder_dnd_{digest}", path=str(folder))


@st.cache_resource
def get_palette_component():
    digest = hashlib.md5(PALETTE_HTML.encode("utf-8")).hexdigest()[:8]
    folder = Path(tempfile.gettempdir()) / f"ui_builder_palette_{digest}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(PALETTE_HTML, encoding="utf-8")
    return components.declare_component(f"ui_builder_palette_{digest}", path=str(folder))


@st.cache_resource
def get_preview_component():
    digest = hashlib.md5(PREVIEW_HTML.encode("utf-8")).hexdigest()[:8]
    folder = Path(tempfile.gettempdir()) / f"ui_builder_preview_{digest}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(PREVIEW_HTML, encoding="utf-8")
    return components.declare_component(f"ui_builder_preview_{digest}", path=str(folder))


def handle_dnd_event(event):
    'Terapkan event dari panel Susunan.'
    if not isinstance(event, dict):
        return False
    event_id = event.get("id")
    if not event_id or event_id == st.session_state.get("last_dnd_event"):
        return False
    st.session_state.last_dnd_event = event_id

    els = current_page()["elements"]
    by_id = {e["id"]: e for e in els}
    action = event.get("action")

    if action == "select":
        target = event.get("target")
        if target in by_id:
            st.session_state.selected_id = target
        return True
    if action == "reorder":
        order = event.get("order")
        if isinstance(order, list) and sorted(order) == sorted(by_id):
            els[:] = [by_id[i] for i in order]
            if event.get("selected") in by_id:
                st.session_state.selected_id = event["selected"]
        return True
    if action == "delete":
        target = event.get("target")
        for i, el in enumerate(els):
            if el["id"] == target:
                delete_element(i)
                break
        return True
    if action == "insert":
        if event.get("type") in ELEMENT_LABELS:
            insert_element(event["type"], event.get("index"))
        return True
    return False


def handle_palette_event(event):
    if not isinstance(event, dict):
        return False
    event_id = event.get("id")
    if not event_id or event_id == st.session_state.get("last_palette_event"):
        return False
    st.session_state.last_palette_event = event_id
    if event.get("action") == "insert" and event.get("type") in ELEMENT_LABELS:
        add_element(event["type"])
        return True
    return False

def handle_preview_event(event):
    if not isinstance(event, dict):
        return False
    event_id = event.get("id")
    if not event_id or event_id == st.session_state.get("last_preview_event"):
        return False
    st.session_state.last_preview_event = event_id
    if event.get("action") == "select":
        target = event.get("target")
        if any(el.get("id") == target for el in current_page()["elements"]):
            st.session_state.selected_id = target
            return True
    return False



# ---------------------------------------------------------------------------
# Panel properti (kanan)
# ---------------------------------------------------------------------------
def summary_of(el):
    for k in ("text", "title", "label", "brand", "alt"):
        v = str(el.get(k, "")).strip().replace("\n", " ")
        v = re.sub(r"[*_`\[\]]", "", v)
        if v:
            return " – " + (v[:16] + "…" if len(v) > 16 else v)
    return ""


def align_radio(el, key):
    return st.radio("Rata", ALIGNS, ALIGNS.index(align_of(el)), horizontal=True, key=key)


def edit_visual_properties(el, key):
    """Panel gaya umum untuk setiap elemen."""
    style = ensure_element_style(el)
    with st.expander(":material/palette: Tampilan & Bentuk", expanded=False):
        c1, c2 = st.columns(2)
        style["background"] = c1.color_picker(
            "Warna latar", style.get("background", "#ffffff") if style.get("background") != "transparent" else "#ffffff",
            key=f"{key}_bg_color",
        )
        transparent = c2.checkbox("Transparan", style.get("background") == "transparent", key=f"{key}_bg_transparent")
        if transparent:
            style["background"] = "transparent"

        c1, c2 = st.columns(2)
        style["color"] = c1.color_picker(
            "Warna teks", style.get("color", "#1f2937") if style.get("color") != "inherit" else "#1f2937",
            key=f"{key}_text_color",
        )
        style["border_color"] = c2.color_picker(
            "Warna garis", style.get("border_color", "#d1d5db"), key=f"{key}_border_color"
        )

        c1, c2 = st.columns(2)
        style["border_width"] = c1.slider(
            "Ketebalan garis", 0, 6, int(style.get("border_width", 0)), key=f"{key}_border_width"
        )
        style["radius"] = c2.slider(
            "Bentuk / radius", 0, 48, int(style.get("radius", 8)), key=f"{key}_radius_style"
        )

        c1, c2 = st.columns(2)
        shadow_label = next((label for label, value in SHADOW_OPTIONS.items() if value == style.get("shadow")), "Tanpa bayangan")
        selected_shadow = c1.selectbox(
            "Bayangan", list(SHADOW_OPTIONS), index=list(SHADOW_OPTIONS).index(shadow_label), key=f"{key}_shadow"
        )
        style["shadow"] = SHADOW_OPTIONS[selected_shadow]
        style["padding"] = c2.slider(
            "Padding", 0, 48, int(style.get("padding", 0)), key=f"{key}_padding"
        )

        width_label = next((label for label, value in WIDTH_OPTIONS.items() if value == style.get("width")), "Auto")
        style["width"] = WIDTH_OPTIONS[c1.selectbox(
            "Lebar elemen", list(WIDTH_OPTIONS), index=list(WIDTH_OPTIONS).index(width_label), key=f"{key}_width"
        )]


def edit_properties(el, index):
    key = el["id"]
    t = el["type"]
    st.markdown(f"**{ELEMENT_LABELS[t]}** (elemen ke-{index + 1})")

    if t == "navbar":
        el["brand"] = st.text_input("Nama merek", el["brand"], key=f"{key}_brand")
        el["links"] = st.text_area(
            "Menu (satu per baris, format: label|tautan)", el["links"], key=f"{key}_links", height=110
        )
    elif t == "heading":
        el["text"] = st.text_input("Teks", el["text"], key=f"{key}_text")
        el["size"] = st.slider("Ukuran (px)", 16, 72, int(el["size"]), key=f"{key}_size")
        el["align"] = align_radio(el, f"{key}_align")
    elif t == "text":
        el["text"] = st.text_area("Teks", el["text"], key=f"{key}_text")
        el["align"] = align_radio(el, f"{key}_align")
    elif t == "button":
        el["text"] = st.text_input("Label", el["text"], key=f"{key}_text")
        el["link"] = st.text_input("Tautan (opsional)", el["link"], key=f"{key}_link")
        el["align"] = align_radio(el, f"{key}_align")
    elif t == "image":
        el["url"] = st.text_input("URL gambar", el["url"], key=f"{key}_url")
        el["alt"] = st.text_input("Teks alternatif", el["alt"], key=f"{key}_alt")
        el["radius"] = st.slider("Sudut membulat (px)", 0, 48, int(el["radius"]), key=f"{key}_radius")
    elif t == "gallery":
        el["urls"] = st.text_area("URL gambar (satu per baris)", el["urls"], key=f"{key}_urls", height=120)
        el["columns"] = st.slider("Jumlah kolom", 1, 4, int(el["columns"]), key=f"{key}_cols")
        el["radius"] = st.slider("Sudut membulat (px)", 0, 32, int(el["radius"]), key=f"{key}_radius")
    elif t == "list":
        el["items"] = st.text_area("Item (satu per baris)", el["items"], key=f"{key}_items", height=120)
        el["style"] = st.radio(
            "Gaya", ["bullet", "number"], 0 if el["style"] != "number" else 1,
            format_func=lambda s: "Poin" if s == "bullet" else "Bernomor",
            horizontal=True, key=f"{key}_style",
        )
    elif t == "input":
        el["label"] = st.text_input("Label", el["label"], key=f"{key}_label")
        el["placeholder"] = st.text_input("Placeholder", el["placeholder"], key=f"{key}_ph")
        kinds = list(INPUT_KINDS)
        el["kind"] = st.selectbox(
            "Jenis isian", kinds, kinds.index(input_kind(el)),
            format_func=lambda k: INPUT_KINDS[k], key=f"{key}_kind",
        )
    elif t == "card":
        el["title"] = st.text_input("Judul", el["title"], key=f"{key}_title")
        el["text"] = st.text_area("Isi", el["text"], key=f"{key}_text")
    elif t == "spacer":
        el["height"] = st.slider("Tinggi (px)", 4, 200, int(el["height"]), key=f"{key}_h")
    elif t == "footer":
        el["text"] = st.text_input("Teks footer", el["text"], key=f"{key}_text")
    elif t in BAR_SPECS:
        edit_bar_fields(el, key)
    else:
        st.caption("Elemen ini tidak punya pengaturan.")

    edit_visual_properties(el, key)
    st.divider()
    total = len(current_page()["elements"])
    m1, m2 = st.columns(2)
    m1.button("Naikkan", icon=":material/arrow_upward:", key=f"{key}_mvup", on_click=move_element, args=(index, -1),
              disabled=index == 0, use_container_width=True)
    m2.button("Turunkan", icon=":material/arrow_downward:", key=f"{key}_mvdn", on_click=move_element, args=(index, 1),
              disabled=index >= total - 1, use_container_width=True)
    c1, c2 = st.columns(2)
    c1.button("Gandakan", icon=":material/content_copy:", key=f"{key}_dup", on_click=duplicate_element, args=(index,), use_container_width=True)
    c2.button("Hapus", icon=":material/delete:", key=f"{key}_del", on_click=delete_element, args=(index,), use_container_width=True)


# ---------------------------------------------------------------------------
# Tampilan
# ---------------------------------------------------------------------------
init_state()
design = st.session_state.design

APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stAppDeployButton"], [data-testid="stMainMenu"],
.stAppDeployButton, .stDeployButton, [data-testid="stSidebarCollapsedControl"] {
  display: none !important; visibility: hidden !important; height: 0 !important; }
.stApp { font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  background: radial-gradient(900px 420px at 8% -8%, rgba(99,102,241,.16), transparent 62%),
              radial-gradient(800px 380px at 100% 0%, rgba(236,72,153,.12), transparent 60%); }
.stApp button, .stApp input, .stApp textarea, .stApp [data-baseweb="select"] { font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; }
.block-container { padding-top: 1.1rem !important; padding-bottom: 1rem !important; max-width: 1680px; }
h5 { margin-bottom: .2rem; font-weight: 700; }
.st-key-hero { background: linear-gradient(115deg, #3730a3 0%, #6d28d9 50%, #be185d 115%); border-radius: 20px;
  padding: 18px 26px !important; box-shadow: 0 14px 34px rgba(79,70,229,.32); }
.st-key-hero, .st-key-hero * { color: #fff !important; }
.st-key-hero h2 { margin: 0 !important; padding: 0 !important; font-weight: 700; letter-spacing: -.01em; }
.st-key-hero [data-testid="stCaptionContainer"] { opacity: .88; }
.st-key-hero [data-testid="stColumn"]:last-child { text-align: right; }
.st-key-projbar { border-radius: 16px !important; border: 1px solid rgba(128,128,128,.22) !important; background: rgba(128,128,128,.045); }
.st-key-panel_left, .st-key-panel_right { border-radius: 18px !important; border: 1px solid rgba(128,128,128,.22) !important;
  background: rgba(128,128,128,.045); box-shadow: 0 8px 24px rgba(0,0,0,.06); }
.stButton > button, .stDownloadButton > button { border-radius: 10px; font-weight: 600;
  transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease; }
.stButton > button:hover, .stDownloadButton > button:hover { transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(99,102,241,.22); border-color: #6366f1; }
[data-testid="stBaseButton-primary"] { background: linear-gradient(120deg, #6366f1, #8b5cf6) !important; border: 0 !important; color: #fff !important; }
.stTabs [data-baseweb="tab"] { font-weight: 600; }
.stTabs [data-baseweb="tab-highlight"] { background-color: #6366f1 !important; height: 3px; border-radius: 3px; }
.stTabs [aria-selected="true"] { color: #6366f1 !important; }
[data-testid="stExpander"] { border-radius: 14px; border: 1px solid rgba(128,128,128,.25); }
.tpl-sws { display: flex; gap: 4px; margin: 2px 0 4px; }
.tpl-sw { width: 16px; height: 16px; border-radius: 50%; border: 1px solid rgba(128,128,128,.45); }
.ref-prev { display: flex; align-items: center; gap: 10px; padding: 12px; border-radius: 12px;
  border: 1px solid rgba(128,128,128,.25); margin-bottom: 6px; }
.ref-card { flex: 1; padding: 8px 10px; display: flex; flex-direction: column; font-size: 13px; }
.ref-card span { font-size: 12px; opacity: .8; }
.ref-btn { padding: 8px 12px; font-size: 13px; font-weight: 600; }
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-thumb { background: rgba(128,128,128,.35); border-radius: 8px; }
"""
st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)

autosave_project()

with st.container(key="hero"):
    hc1, hc2 = st.columns([3, 1.4], vertical_alignment="center")
    hc1.markdown("## :material/dashboard_customize: UI Builder")
    hc1.caption("Susun tampilan aplikasi, lihat hasilnya langsung, lalu ambil kode HTML atau prompt master AI.")
    hc2.markdown(
        f":material/widgets: {len(ELEMENT_LABELS)} komponen &nbsp;·&nbsp; "
        f":material/dashboard: {len(TEMPLATES)} template &nbsp;·&nbsp; :material/palette: {len(DESIGN_REFS)} gaya"
    )

project_list = list_projects()
project_ids = [p["id"] for p in project_list]
project_names = {p["id"]: p["name"] for p in project_list}
if st.session_state.get("project_id") not in project_ids:
    project_ids.insert(0, st.session_state.project_id)
    project_names[st.session_state.project_id] = st.session_state.project_name
if st.session_state.get("project_selector_topbar") not in project_ids:
    st.session_state.project_selector_topbar = st.session_state.project_id

with st.container(border=True, key="projbar"):
    p1, p2, p3, p4 = st.columns([3.1, 1.15, 1.15, 1.15])
    p1.selectbox(
        "Proyek",
        project_ids,
        format_func=lambda pid: project_names.get(pid, pid),
        key="project_selector_topbar",
        on_change=switch_project,
        label_visibility="collapsed",
    )
    p2.button("Baru", icon=":material/add:", key="new_project_btn", on_click=new_project, use_container_width=True)
    p3.button("Nama", icon=":material/edit:", key="rename_project_btn", on_click=rename_project, use_container_width=True)
    p4.button(
        "Hapus", icon=":material/delete:", key="delete_project_btn", on_click=delete_project,
        disabled=len(project_ids) <= 1, use_container_width=True,
    )
    r1, r2 = st.columns([3.1, 4.45])
    r1.text_input(
        "Nama proyek", value=st.session_state.project_name, key="project_rename",
        label_visibility="collapsed", placeholder="Nama proyek",
    )
    status = {
        "saved": ":material/cloud_done: Tersimpan otomatis",
        "saving": ":material/sync: Menyimpan...",
        "error": ":material/error: Gagal menyimpan",
    }.get(st.session_state.get("autosave_status"), ":material/cloud_done: Tersimpan otomatis")
    saved_at = st.session_state.get("last_saved_at")
    r2.caption(f"{status}" + (f" · {saved_at}" if saved_at else ""))

with st.expander(":material/lightbulb: Cara pakai singkat", expanded=False):
    g1, g2, g3, g4 = st.columns(4)
    g1.markdown(":material/add_circle: **1. Tambah komponen**\n\nSeret dari daftar Komponen ke Susunan, atau klik untuk menambah di akhir.")
    g2.markdown(":material/tune: **2. Atur properti**\n\nKlik satu baris di Susunan, lalu ubah teks, ikon, dan gaya di tab Properti.")
    g3.markdown(":material/dashboard: **3. Mulai dari template**\n\nTab Template berisi galeri siap pakai dan referensi gaya desain.")
    g4.markdown(":material/code: **4. Ambil hasilnya**\n\nPilih Kode HTML atau Prompt AI di atas preview, lalu unduh.")

col_left, col_center, col_right = st.columns([1.05, 2.7, 1.45], gap="medium")

# ---------------------------- PANEL KIRI ----------------------------------
# Panel kiri sekarang hanya untuk mengelola halaman. Daftar komponen dipindahkan
# ke dock horizontal di bagian paling bawah agar tidak mengganggu area editor.
with col_left:
    with st.container(height=PANEL_HEIGHT, border=True, key="panel_left"):
        st.markdown("##### :material/description: Halaman")
        pages = design["pages"]
        st.selectbox(
            "Halaman aktif",
            options=list(range(len(pages))),
            format_func=lambda i: pages[i]["name"] if i < len(pages) else "",
            key="page_idx",
            on_change=clear_selection,
            label_visibility="collapsed",
        )
        page = current_page()
        page.setdefault("id", uuid.uuid4().hex[:8])
        page["name"] = st.text_input("Nama halaman", page["name"], key=f"pname_{page['id']}")
        b1, b2 = st.columns(2)
        b1.button("Tambah", icon=":material/add:", on_click=add_page, use_container_width=True)
        b2.button(
            "Hapus", icon=":material/delete:", on_click=delete_page,
            disabled=len(pages) <= 1, use_container_width=True
        )

        st.divider()
        st.markdown("##### :material/layers: Ringkasan")
        st.caption(f"{len(page['elements'])} komponen di halaman ini")
        if st.session_state.get("selected_id"):
            _, _sel = selected_element()
            if _sel:
                st.success(
                    f"Terpilih: {ELEMENT_LABELS[_sel['type']]}",
                    icon=":material/touch_app:",
                )
        else:
            st.info(
                "Pilih komponen dari Preview atau panel Susunan di kanan.",
                icon=":material/touch_app:",
            )

        st.divider()
        st.markdown("##### :material/lightbulb: Alur baru")
        st.caption("1. Pilih komponen di dock bawah.")
        st.caption("2. Komponen masuk ke Susunan di kanan.")
        st.caption("3. Klik komponen di Preview atau Susunan.")
        st.caption("4. Edit langsung di panel Properti.")

# ---------------------------- PANEL TENGAH --------------------------------
with col_center:
    top1, top2 = st.columns([2.2, 1])
    VIEW_LABELS = {
        "Preview": ":material/visibility: Preview",
        "Kode HTML": ":material/code: Kode HTML",
        "Prompt Master AI": ":material/auto_awesome: Prompt AI",
    }
    view = top1.radio(
        "Tampilan",
        list(VIEW_LABELS),
        format_func=lambda v: VIEW_LABELS[v],
        horizontal=True,
        label_visibility="collapsed",
        key="view_mode",
    )
    device = top2.selectbox(
        "Ukuran layar",
        list(DEVICES),
        index=0,
        label_visibility="collapsed",
        disabled=view != "Preview",
    )
    center_output = st.empty()
    target = None
    if view == "Prompt Master AI":
        target = st.selectbox(
            "Target pembuatan",
            [
                "HTML/CSS/JavaScript satu file",
                "React dengan Tailwind CSS",
                "Streamlit (Python)",
                "Flutter (Dart)",
            ],
            key="prompt_target",
        )

# ---------------------------- PANEL KANAN ---------------------------------
# Panel kanan sekarang menjadi area utama untuk Susunan + Properti.
with col_right:
    with st.container(height=PANEL_HEIGHT, border=True, key="panel_right"):
        tab_editor, tab_tpl, tab_theme, tab_file = st.tabs([
            ":material/edit_note: Editor",
            ":material/dashboard: Template",
            ":material/palette: Tema",
            ":material/folder: Berkas",
        ])

        with tab_editor:
            elements = current_page()["elements"]
            st.markdown("##### :material/account_tree: Susunan")
            st.caption("Komponen yang kamu tambahkan muncul di sini. Seret untuk mengubah urutan.")

            dnd = get_dnd_component()
            dnd_signature = hashlib.md5(
                "|".join(
                    [
                        str(current_page().get("id", "")),
                        *[f"{el.get('id','')}:{el.get('type','')}" for el in elements],
                    ]
                ).encode("utf-8")
            ).hexdigest()[:10]

            dnd_event = dnd(
                items=[
                    {
                        "id": el["id"],
                        "label": ELEMENT_LABELS[el["type"]] + summary_of(el),
                        "icon": ICONS.get(el["type"], "widgets"),
                    }
                    for el in elements
                ],
                selected=st.session_state.selected_id,
                key=f"layer_list_{dnd_signature}",
                default=None,
            )
            if handle_dnd_event(dnd_event):
                st.rerun()

            st.divider()
            st.markdown("##### :material/tune: Properti")

            idx, sel = selected_element()
            if sel is None:
                st.info(
                    "Belum ada komponen yang dipilih. Klik komponen di Preview atau Susunan.",
                    icon=":material/touch_app:",
                )
            else:
                edit_properties(sel, idx)

        with tab_tpl:
            sub_gal, sub_ref = st.tabs([":material/grid_view: Galeri", ":material/palette: Referensi gaya"])
            with sub_gal:
                st.text_input("Cari template", key="tpl_q", placeholder="Ketik nama, kategori, atau kata kunci")
                cats = ["Semua"] + sorted({t["category"] for t in TEMPLATES.values()})
                st.selectbox("Kategori", cats, key="tpl_cat")
                st.radio(
                    "Cara menerapkan",
                    ["Ganti seluruh desain", "Tambahkan sebagai halaman baru"],
                    key="tpl_mode",
                )
                if st.session_state.get("tpl_preview") and st.session_state.get("tpl_choice") in TEMPLATES:
                    st.info(
                        f"Pratinjau aktif: {TEMPLATES[st.session_state.tpl_choice]['name']}",
                        icon=":material/visibility:",
                    )
                    st.button(
                        "Tutup pratinjau", icon=":material/close:",
                        on_click=close_template_preview, use_container_width=True,
                    )
                q = str(st.session_state.get("tpl_q", "")).strip().lower()
                cat = st.session_state.get("tpl_cat", "Semua")
                shown = [
                    k for k, t in TEMPLATES.items()
                    if (cat == "Semua" or t["category"] == cat)
                    and (not q or q in t["name"].lower() or q in t["category"].lower() or q in t["desc"].lower())
                ]
                st.caption(f"{len(shown)} dari {len(TEMPLATES)} template")
                if not shown:
                    st.info("Tidak ada template yang cocok. Ubah kata kunci atau kategori.", icon=":material/search_off:")
                for k in shown:
                    tpl = TEMPLATES[k]
                    n_el = sum(len(p["elements"]) for p in tpl["pages"])
                    with st.container(border=True):
                        st.markdown(f"**{tpl['name']}**")
                        st.markdown(swatches_html(tpl["theme"]), unsafe_allow_html=True)
                        st.caption(f"{tpl['category']} · {len(tpl['pages'])} halaman · {n_el} elemen")
                        st.caption(tpl["desc"])
                        b1, b2 = st.columns(2)
                        b1.button(
                            "Pratinjau", key=f"tpv_{k}", icon=":material/visibility:",
                            on_click=preview_template, args=(k,), use_container_width=True,
                        )
                        b2.button(
                            "Pakai", key=f"tus_{k}", icon=":material/check:", type="primary",
                            on_click=use_template, args=(k,), use_container_width=True,
                        )
                st.caption("Mode ganti akan menimpa desain yang sedang dikerjakan. Unduh dulu lewat tab Berkas bila perlu.")

            with sub_ref:
                st.caption("Pilih gaya visual sebagai titik awal. Warna, font, dan lebar langsung diterapkan ke tema desainmu.")
                st.checkbox(
                    "Terapkan juga ke bentuk elemen (sudut, garis, bayangan)",
                    value=True, key="ref_shape",
                    help="Matikan bila kamu hanya ingin mengganti warna, font, dan lebar tema.",
                )
                for name, ref in DESIGN_REFS.items():
                    with st.container(border=True):
                        st.markdown(f"**{name}**")
                        st.markdown(ref_preview_html(ref), unsafe_allow_html=True)
                        st.caption(ref["desc"])
                        st.button(
                            "Terapkan gaya", key=f"ref_{name}", icon=":material/palette:",
                            on_click=apply_design_ref, args=(name,), use_container_width=True,
                        )

        with tab_theme:
            design["title"] = st.text_input("Nama aplikasi", design["title"])
            theme = design["theme"]
            theme["primary"] = st.color_picker("Warna utama", theme["primary"])
            theme["bg"] = st.color_picker("Warna latar", theme["bg"])
            theme["text"] = st.color_picker("Warna teks", theme["text"])
            font_names = list(FONTS)
            theme["font"] = st.selectbox(
                "Font", font_names, font_names.index(theme["font"]) if theme["font"] in font_names else 0
            )
            theme["width"] = st.slider("Lebar konten (px)", 360, 1200, int(theme["width"]), step=20)

        with tab_file:
            st.download_button(
                "Unduh desain (.json)",
                json.dumps(design, ensure_ascii=False, indent=2),
                file_name="desain.json",
                mime="application/json",
                icon=":material/download:",
                use_container_width=True,
            )
            uploaded = st.file_uploader("Muat desain (.json)", type=["json"])
            if uploaded is not None and st.button("Terapkan file", icon=":material/upload_file:", use_container_width=True):
                try:
                    data = json.loads(uploaded.getvalue().decode("utf-8"))
                    if valid_design(data):
                        load_design(data)
                        st.rerun()
                    else:
                        st.error("Struktur file tidak sesuai format desain.")
                except (json.JSONDecodeError, UnicodeDecodeError):
                    st.error("File bukan JSON yang valid.")
            st.button("Reset desain", icon=":material/restart_alt:", on_click=reset_design, use_container_width=True)

# ---------------------------- DOCK KOMPONEN --------------------------------
# Semua komponen berada di bagian bawah halaman, di luar tiga kolom editor.
# Klik chip -> masuk ke Susunan dan langsung terpilih. Drag -> lepaskan ke panel Susunan.
st.markdown("### :material/widgets: Komponen")
st.caption("Klik untuk menambahkan. Seret komponen ke panel Susunan di kanan untuk menentukan posisinya.")
palette_component = get_palette_component()
palette_event = palette_component(
    palette=[
        {
            "type": t,
            "label": ELEMENT_LABELS[t],
            "icon": ICONS.get(t, "widgets"),
            "group": ELEMENT_GROUP[t],
        }
        for t in sorted(ELEMENT_LABELS, key=lambda x: (GROUP_ORDER.index(ELEMENT_GROUP[x]), ELEMENT_LABELS[x]))
    ],
    key="component_palette_bottom",
    default=None,
)
if handle_palette_event(palette_event):
    st.rerun()

# ---------------------- RENDER OUTPUT TERBARU ------------------------------
with center_output.container():
    if view == "Preview":
        tpl_key = st.session_state.get("tpl_choice")
        if st.session_state.get("tpl_preview") and tpl_key in TEMPLATES:
            st.caption(f"Pratinjau template: {TEMPLATES[tpl_key]['name']} (belum diterapkan ke desainmu)")
            inner = build_html(template_design(tpl_key))
        else:
            _, sel_el = selected_element()
            inner = build_html(
                st.session_state.design,
                highlight_id=sel_el["id"] if sel_el else None,
                active=st.session_state.page_idx,
                builder_mode=True,
            )

        preview_component = get_preview_component()
        preview_event = preview_component(
            html=inner,
            deviceWidth=DEVICES[device],
            key="builder_live_preview",
            default=None,
        )
        if handle_preview_event(preview_event):
            st.rerun()

    elif view == "Kode HTML":
        output = build_html(st.session_state.design)
        st.download_button(
            "Unduh index.html", output, file_name="index.html",
            mime="text/html", icon=":material/download:"
        )
        with st.container(height=PANEL_HEIGHT - 110, border=True):
            st.code(output, language="html")

    else:
        output = build_prompt(st.session_state.design, target)
        st.download_button(
            "Unduh prompt_master.txt", output, file_name="prompt_master.txt",
            mime="text/plain", icon=":material/download:",
        )
        with st.container(height=PANEL_HEIGHT - 160, border=True):
            st.code(output, language="markdown")

# Autosave terakhir dijalankan setelah seluruh widget pada rerun ini menerapkan perubahan.
autosave_project()
