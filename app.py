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
    page_icon="🧩",
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
}

ALIGNS = ["left", "center", "right"]

DEVICES = {
    "Ponsel (390 px)": 390,
    "Tablet (768 px)": 768,
    "Desktop (penuh)": None,
}

PANEL_HEIGHT = 780
PROJECTS_DIR = Path(__file__).resolve().parent / "projects"

ICONS = {
    "navbar": "🧭",
    "heading": "🔠",
    "text": "📝",
    "button": "🔘",
    "image": "🖼️",
    "gallery": "🎞️",
    "list": "📋",
    "input": "⌨️",
    "card": "🗂️",
    "divider": "➖",
    "spacer": "↕️",
    "footer": "🔻",
}

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
}

WIDTH_OPTIONS = {
    "Auto": "auto",
    "100%": "100%",
    "90%": "90%",
    "75%": "75%",
    "50%": "50%",
}


def ensure_element_style(el):
    style = el.setdefault("style", {})
    for k, v in ELEMENT_STYLE_DEFAULTS.items():
        style.setdefault(k, copy.deepcopy(v))
    return style


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
    el["style"] = copy.deepcopy(ELEMENT_STYLE_DEFAULTS)
    els = current_page()["elements"]
    if index is None or not isinstance(index, int):
        index = len(els)
    els.insert(min(max(index, 0), len(els)), el)
    st.session_state.selected_id = el["id"]


def add_element(el_type):
    insert_element(el_type)


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
    el["style"] = copy.deepcopy(ELEMENT_STYLE_DEFAULTS)
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
    return ""


def mark_selected(rendered):
    """Beri penanda pada tag pertama supaya elemen terpilih tersorot di preview."""
    return re.sub(r"^<(\w+)", r'<\1 data-sel="1"', rendered, count=1)


def build_html(design, highlight_id=None, active=0):
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
            if highlight_id and el.get("id") == highlight_id:
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
<style>
  :root {{
    --primary: {esc(theme["primary"])};
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
  .nav-btn.active {{ background: var(--primary); color: #fff; }}
  .page > * {{ margin-top: 0; margin-bottom: 16px; }}
  h1, h3 {{ line-height: 1.2; }}
  img {{ max-width: 100%; height: auto; display: block; }}
  hr {{ border: 0; border-top: 1px solid rgba(128,128,128,.35); }}
  ul, ol {{ padding-left: 1.4em; }}
  .btn {{
    display: inline-block;
    background: var(--primary);
    color: #fff;
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
{highlight_css}</style>
</head>
<body>
<main class="app">
<p class="app-title">{esc(design["title"])}</p>
{nav}
{chr(10).join(sections)}
</main>{script}
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
        "- Gunakan HTML semantik dan pastikan fokus keyboard terlihat jelas.",
        "- Jangan menambahkan elemen, teks, atau fitur di luar spesifikasi ini.",
        "- Berikan hasil akhir berupa kode lengkap yang bisa langsung dijalankan.",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Komponen seret dan lepas (HTML5 drag-and-drop, tanpa paket tambahan)
# ---------------------------------------------------------------------------
DND_HTML = r'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<style>
  :root { --fg: #31333f; --bg2: #f0f2f6; --accent: #ff4b4b; --line: rgba(128,128,128,.35); }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: transparent; color: var(--fg);
    font-family: "Source Sans Pro", system-ui, sans-serif; font-size: 14px; }
  .title { font-weight: 600; margin: 4px 0 2px; }
  .hint { opacity: .65; font-size: 12px; margin: 0 0 8px; }
  #palette { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
  .chip { border: 1px solid var(--line); background: var(--bg2); border-radius: 8px;
    padding: 5px 9px; cursor: grab; user-select: none; font-size: 13px; }
  .chip:hover { border-color: var(--accent); }
  #list { list-style: none; margin: 0; padding: 6px 6px 14px; min-height: 64px;
    border: 1px dashed var(--line); border-radius: 8px; }
  #list:empty::before { content: "Seret komponen ke sini"; display: block;
    text-align: center; opacity: .6; padding: 14px 0; }
  #list.ins-empty { border-color: var(--accent); background: var(--bg2); }
  li { display: flex; align-items: center; gap: 8px; padding: 7px 8px; margin: 0 0 6px;
    border: 1px solid var(--line); border-radius: 8px; background: var(--bg2);
    cursor: grab; user-select: none; position: relative; }
  li.sel { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
  li.dragging { opacity: .4; }
  li.ins-before::before, li.ins-after::after { content: ""; position: absolute; left: 0; right: 0;
    height: 3px; background: var(--accent); border-radius: 2px; }
  li.ins-before::before { top: -5px; }
  li.ins-after::after { bottom: -5px; }
  .grip { opacity: .5; }
  .lbl { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .del { border: 0; background: transparent; color: inherit; cursor: pointer;
    opacity: .55; font-size: 14px; padding: 0 4px; }
  .del:hover { opacity: 1; color: var(--accent); }
</style>
</head>
<body>
<div class="title">Komponen</div>
<p class="hint">Seret ke daftar di bawah, atau klik untuk menambah di akhir.</p>
<div id="palette"></div>
<div class="title">Susunan</div>
<p class="hint">Seret baris untuk mengubah urutan. Klik untuk memilih.</p>
<ul id="list"></ul>
<script>
(function () {
  var items = [], palette = [], selected = null, drag = null;
  var listEl = document.getElementById("list");
  var palEl = document.getElementById("palette");

  function post(type, data) {
    window.parent.postMessage(Object.assign({ isStreamlitMessage: true, type: type }, data), "*");
  }
  function send(payload) {
    payload.id = Date.now() + "-" + Math.random().toString(36).slice(2);
    post("streamlit:setComponentValue", { value: payload, dataType: "json" });
  }
  function fit() {
    post("streamlit:setFrameHeight", { height: document.documentElement.scrollHeight + 4 });
  }
  function clearInd() {
    listEl.classList.remove("ins-empty");
    listEl.querySelectorAll("li").forEach(function (li) {
      li.classList.remove("ins-before", "ins-after");
    });
  }
  function indexAt(y) {
    var lis = listEl.querySelectorAll("li"), idx = 0;
    for (var i = 0; i < lis.length; i++) {
      var r = lis[i].getBoundingClientRect();
      if (y > r.top + r.height / 2) idx++; else break;
    }
    return idx;
  }
  function showInd(idx) {
    clearInd();
    var lis = listEl.querySelectorAll("li");
    if (!lis.length) { listEl.classList.add("ins-empty"); return; }
    if (idx < lis.length) lis[idx].classList.add("ins-before");
    else lis[lis.length - 1].classList.add("ins-after");
  }

  function render() {
    palEl.textContent = "";
    palette.forEach(function (p) {
      var c = document.createElement("div");
      c.className = "chip";
      c.draggable = true;
      c.textContent = p.icon + " " + p.label;
      c.addEventListener("dragstart", function (e) {
        drag = { kind: "new", type: p.type };
        e.dataTransfer.setData("text/plain", "new:" + p.type);
        e.dataTransfer.effectAllowed = "copy";
      });
      c.addEventListener("dragend", function () { drag = null; clearInd(); });
      c.addEventListener("click", function () {
        send({ action: "insert", type: p.type, index: items.length });
      });
      palEl.appendChild(c);
    });

    listEl.textContent = "";
    items.forEach(function (it, i) {
      var li = document.createElement("li");
      li.draggable = true;
      li.dataset.id = it.id;
      if (it.id === selected) li.classList.add("sel");
      var grip = document.createElement("span");
      grip.className = "grip";
      grip.textContent = "\u283F";
      var lbl = document.createElement("span");
      lbl.className = "lbl";
      lbl.textContent = (i + 1) + ". " + it.icon + " " + it.label;
      var del = document.createElement("button");
      del.className = "del";
      del.type = "button";
      del.title = "Hapus";
      del.textContent = "\u2715";
      del.addEventListener("click", function (e) {
        e.stopPropagation();
        send({ action: "delete", target: it.id });
      });
      li.appendChild(grip); li.appendChild(lbl); li.appendChild(del);
      li.addEventListener("click", function () { send({ action: "select", target: it.id }); });
      li.addEventListener("dragstart", function (e) {
        drag = { kind: "move", id: it.id };
        li.classList.add("dragging");
        e.dataTransfer.setData("text/plain", "move:" + it.id);
        e.dataTransfer.effectAllowed = "move";
      });
      li.addEventListener("dragend", function () {
        drag = null; li.classList.remove("dragging"); clearInd();
      });
      listEl.appendChild(li);
    });
    fit();
  }

  listEl.addEventListener("dragover", function (e) {
    if (!drag) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = drag.kind === "new" ? "copy" : "move";
    showInd(indexAt(e.clientY));
  });
  listEl.addEventListener("dragleave", function (e) {
    if (!listEl.contains(e.relatedTarget)) clearInd();
  });
  listEl.addEventListener("drop", function (e) {
    e.preventDefault();
    if (!drag) return;
    var idx = indexAt(e.clientY);
    clearInd();
    if (drag.kind === "new") {
      send({ action: "insert", type: drag.type, index: idx });
    } else {
      var ids = items.map(function (x) { return x.id; });
      var from = ids.indexOf(drag.id);
      if (from < 0) { drag = null; return; }
      var to = idx;
      if (from < to) to -= 1;
      if (to === from) { drag = null; return; }
      ids.splice(from, 1);
      ids.splice(to, 0, drag.id);
      var byId = {};
      items.forEach(function (x) { byId[x.id] = x; });
      items = ids.map(function (id) { return byId[id]; });
      selected = drag.id;
      send({ action: "reorder", order: ids, selected: drag.id });
      render();
    }
    drag = null;
  });

  function applyTheme(t) {
    if (!t) return;
    var r = document.documentElement.style;
    if (t.textColor) r.setProperty("--fg", t.textColor);
    if (t.secondaryBackgroundColor) r.setProperty("--bg2", t.secondaryBackgroundColor);
    if (t.primaryColor) r.setProperty("--accent", t.primaryColor);
    if (t.font) document.body.style.fontFamily = t.font;
  }

  window.addEventListener("message", function (e) {
    var d = e.data;
    if (!d || d.type !== "streamlit:render") return;
    var a = d.args || {};
    items = a.items || [];
    palette = a.palette || [];
    selected = a.selected || null;
    applyTheme(d.theme);
    render();
  });
  window.addEventListener("resize", fit);
  post("streamlit:componentReady", { apiVersion: 1 });
})();
</script>
</body>
</html>
'''


@st.cache_resource
def get_dnd_component():
    """Daftarkan komponen kustom dari folder sementara yang dibuat saat dijalankan."""
    digest = hashlib.md5(DND_HTML.encode("utf-8")).hexdigest()[:8]
    folder = Path(tempfile.gettempdir()) / f"ui_builder_dnd_{digest}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(DND_HTML, encoding="utf-8")
    return components.declare_component(f"ui_builder_dnd_{digest}", path=str(folder))


def handle_dnd_event(event):
    """Terapkan event dari komponen seret-lepas. Mengembalikan True jika state berubah."""
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
    if action == "insert":
        if event.get("type") in ELEMENT_LABELS:
            insert_element(event["type"], event.get("index"))
        return True
    if action == "delete":
        target = event.get("target")
        for i, el in enumerate(els):
            if el["id"] == target:
                delete_element(i)
                break
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
    with st.expander("🎨 Tampilan & Bentuk", expanded=False):
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
    else:
        st.caption("Elemen ini tidak punya pengaturan.")

    edit_visual_properties(el, key)
    st.divider()
    total = len(current_page()["elements"])
    m1, m2 = st.columns(2)
    m1.button("⬆️ Naikkan", key=f"{key}_mvup", on_click=move_element, args=(index, -1),
              disabled=index == 0, use_container_width=True)
    m2.button("⬇️ Turunkan", key=f"{key}_mvdn", on_click=move_element, args=(index, 1),
              disabled=index >= total - 1, use_container_width=True)
    c1, c2 = st.columns(2)
    c1.button("📄 Gandakan", key=f"{key}_dup", on_click=duplicate_element, args=(index,), use_container_width=True)
    c2.button("🗑️ Hapus", key=f"{key}_del", on_click=delete_element, args=(index,), use_container_width=True)


# ---------------------------------------------------------------------------
# Tampilan
# ---------------------------------------------------------------------------
init_state()
design = st.session_state.design

st.markdown(
    "<style>.block-container{padding-top:1.2rem;padding-bottom:0.5rem}"
    "h5{margin-bottom:0.2rem}</style>",
    unsafe_allow_html=True,
)
st.markdown("### 🧩 UI Builder")

autosave_project()
project_list = list_projects()
project_ids = [p["id"] for p in project_list]
project_names = {p["id"]: p["name"] for p in project_list}
if st.session_state.get("project_id") not in project_ids:
    project_ids.insert(0, st.session_state.project_id)
    project_names[st.session_state.project_id] = st.session_state.project_name
if st.session_state.get("project_selector_topbar") not in project_ids:
    st.session_state.project_selector_topbar = st.session_state.project_id

with st.container(border=True):
    p1, p2, p3, p4 = st.columns([3.1, 1.15, 1.15, 1.15])
    p1.selectbox(
        "Proyek",
        project_ids,
        format_func=lambda pid: project_names.get(pid, pid),
        key="project_selector_topbar",
        on_change=switch_project,
        label_visibility="collapsed",
    )
    p2.button("➕ Baru", key="new_project_btn", on_click=new_project, use_container_width=True)
    p3.button("✏️ Nama", key="rename_project_btn", on_click=rename_project, use_container_width=True)
    p4.button(
        "🗑️ Hapus", key="delete_project_btn", on_click=delete_project,
        disabled=len(project_ids) <= 1, use_container_width=True,
    )
    r1, r2 = st.columns([3.1, 4.45])
    r1.text_input(
        "Nama proyek", value=st.session_state.project_name, key="project_rename",
        label_visibility="collapsed", placeholder="Nama proyek",
    )
    status = {
        "saved": "🟢 Tersimpan otomatis",
        "saving": "🟡 Menyimpan...",
        "error": "🔴 Gagal menyimpan",
    }.get(st.session_state.get("autosave_status"), "🟢 Tersimpan otomatis")
    saved_at = st.session_state.get("last_saved_at")
    r2.caption(f"{status}" + (f" · {saved_at}" if saved_at else ""))

col_left, col_center, col_right = st.columns([1.15, 2.6, 1.35], gap="medium")

# ---------------------------- PANEL KIRI ----------------------------------
with col_left:
    with st.container(height=PANEL_HEIGHT, border=True):
        st.markdown("##### 📄 Halaman")
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
        b1.button("➕ Tambah", on_click=add_page, use_container_width=True)
        b2.button("🗑️ Hapus", on_click=delete_page, disabled=len(pages) <= 1, use_container_width=True)

        dnd_on = st.checkbox(
            "🖱️ Mode seret dan lepas",
            value=True,
            key="dnd_mode",
            help="Matikan jika komponen seret-lepas tidak tampil di perangkatmu. Daftar tombol akan dipakai sebagai gantinya.",
        )
        elements = page["elements"]

        if dnd_on:
            dnd = get_dnd_component()
            event = dnd(
                items=[
                    {
                        "id": el["id"],
                        "label": ELEMENT_LABELS[el["type"]] + summary_of(el),
                        "icon": ICONS.get(el["type"], "▫️"),
                    }
                    for el in elements
                ],
                palette=[
                    {"type": t, "label": label, "icon": ICONS.get(t, "▫️")}
                    for t, label in ELEMENT_LABELS.items()
                ],
                selected=st.session_state.selected_id,
                key="dnd_list",
                default=None,
            )
            if handle_dnd_event(event):
                st.rerun()
        else:
            st.markdown("##### ➕ Komponen")
            grid = st.columns(2)
            for n, t in enumerate(ELEMENT_LABELS):
                grid[n % 2].button(
                    ELEMENT_LABELS[t],
                    key=f"add_{t}",
                    on_click=add_element,
                    args=(t,),
                    use_container_width=True,
                )

            st.markdown("##### 🌳 Susunan")
            if not elements:
                st.caption("Belum ada elemen. Klik salah satu komponen di atas.")
            for i, el in enumerate(elements):
                is_sel = el["id"] == st.session_state.selected_id
                r1, r2, r3 = st.columns([6, 1.4, 1.4], gap="small")
                r1.button(
                    f"{i + 1}. {ELEMENT_LABELS[el['type']]}{summary_of(el)}",
                    key=f"sel_{el['id']}",
                    on_click=select_element,
                    args=(el["id"],),
                    type="primary" if is_sel else "secondary",
                    use_container_width=True,
                )
                r2.button("↑", key=f"up_{el['id']}", on_click=move_element, args=(i, -1),
                          disabled=i == 0, help="Naikkan", use_container_width=True)
                r3.button("↓", key=f"dn_{el['id']}", on_click=move_element, args=(i, 1),
                          disabled=i == len(elements) - 1, help="Turunkan", use_container_width=True)

# ---------------------------- PANEL TENGAH --------------------------------
with col_center:
    top1, top2 = st.columns([2.2, 1])
    view = top1.radio(
        "Tampilan",
        ["Preview", "Kode HTML", "Prompt Master AI"],
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

    # Output preview/kode/prompt dirender setelah seluruh panel kanan selesai.
    # Ini penting agar perubahan widget properti/tema pada rerun yang sama
    # langsung memakai state terbaru, bukan state sebelum widget diproses.
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
with col_right:
    with st.container(height=PANEL_HEIGHT, border=True):
        tab_prop, tab_tpl, tab_theme, tab_file = st.tabs(["Properti", "Template", "Tema", "Berkas"])

        with tab_prop:
            idx, sel = selected_element()
            if sel is None:
                st.info("Klik salah satu baris di daftar Susunan (panel kiri) untuk mengubah propertinya.")
            else:
                edit_properties(sel, idx)

        with tab_tpl:
            cats = ["Semua"] + sorted({t["category"] for t in TEMPLATES.values()})
            cat = st.selectbox("Kategori", cats, key="tpl_cat")
            keys = [k for k, t in TEMPLATES.items() if cat == "Semua" or t["category"] == cat]
            choice = st.selectbox(
                "Template", keys, format_func=lambda k: TEMPLATES[k]["name"], key="tpl_choice"
            )
            tpl = TEMPLATES[choice]
            n_el = sum(len(p["elements"]) for p in tpl["pages"])
            st.caption(f"{tpl['desc']} ({len(tpl['pages'])} halaman, {n_el} elemen)")
            st.checkbox("Pratinjau di panel tengah", key="tpl_preview")
            st.radio(
                "Cara menerapkan",
                ["Ganti seluruh desain", "Tambahkan sebagai halaman baru"],
                key="tpl_mode",
            )
            st.button("✨ Pakai template", on_click=apply_template, use_container_width=True)
            st.caption("Mode ganti akan menimpa desain yang sedang dikerjakan. Unduh dulu lewat tab Berkas bila perlu.")

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
                "💾 Unduh desain (.json)",
                json.dumps(design, ensure_ascii=False, indent=2),
                file_name="desain.json",
                mime="application/json",
                use_container_width=True,
            )
            uploaded = st.file_uploader("Muat desain (.json)", type=["json"])
            if uploaded is not None and st.button("📂 Terapkan file", use_container_width=True):
                try:
                    data = json.loads(uploaded.getvalue().decode("utf-8"))
                    if valid_design(data):
                        load_design(data)
                        st.rerun()
                    else:
                        st.error("Struktur file tidak sesuai format desain.")
                except (json.JSONDecodeError, UnicodeDecodeError):
                    st.error("File bukan JSON yang valid.")
            st.button("♻️ Reset desain", on_click=reset_design, use_container_width=True)

# ---------------------- RENDER OUTPUT TERBARU ------------------------------
# Diletakkan setelah panel kanan supaya preview selalu memakai design yang sudah
# diperbarui oleh widget pada rerun Streamlit saat ini.
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
            )
        framed = device_frame(inner, DEVICES[device])
        if hasattr(st, "iframe"):
            st.iframe(framed, height=PANEL_HEIGHT - 50)
        else:
            components.html(framed, height=PANEL_HEIGHT - 50, scrolling=False)

    elif view == "Kode HTML":
        output = build_html(st.session_state.design)
        st.download_button("⬇️ Unduh index.html", output, file_name="index.html", mime="text/html")
        with st.container(height=PANEL_HEIGHT - 110, border=True):
            st.code(output, language="html")

    else:
        output = build_prompt(st.session_state.design, target)
        st.download_button(
            "⬇️ Unduh prompt_master.txt", output, file_name="prompt_master.txt", mime="text/plain"
        )
        with st.container(height=PANEL_HEIGHT - 160, border=True):
            st.code(output, language="markdown")

# Autosave terakhir dijalankan setelah seluruh widget pada rerun ini menerapkan perubahan.
autosave_project()
