import copy
import html
import json
import re
import uuid

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

INPUT_KINDS = {
    "text": "Teks",
    "email": "Email",
    "password": "Kata sandi",
    "number": "Angka",
    "tel": "Telepon",
}


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


def init_state():
    if "design" not in st.session_state:
        st.session_state.design = default_design()
    if "page_idx" not in st.session_state:
        st.session_state.page_idx = 0
    if "selected_id" not in st.session_state:
        st.session_state.selected_id = None


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


def add_element(el_type):
    el = {"id": uuid.uuid4().hex[:8], "type": el_type}
    el.update(copy.deepcopy(ELEMENT_DEFAULTS[el_type]))
    current_page()["elements"].append(el)
    st.session_state.selected_id = el["id"]


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
    el.update(props)
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
    if t == "navbar":
        links = "".join(
            f'<a href="{esc(safe_url(url))}">{esc(label)}</a>'
            for label, url in parse_links(el.get("links"))
        )
        return (
            f'<header class="topbar"><strong>{esc(el.get("brand", ""))}</strong>'
            f"<nav>{links}</nav></header>"
        )
    if t == "heading":
        return (
            f'<h1 style="font-size:{num(el.get("size"), 36)}px;'
            f'text-align:{align_of(el)}">{esc(el.get("text", ""))}</h1>'
        )
    if t == "text":
        return f'<p style="text-align:{align_of(el)}">{esc(el.get("text", ""))}</p>'
    if t == "button":
        label = esc(el.get("text", ""))
        link = (el.get("link") or "").strip()
        inner = (
            f'<a class="btn" href="{esc(safe_url(link))}">{label}</a>'
            if link
            else f'<button class="btn" type="button">{label}</button>'
        )
        return f'<div style="text-align:{align_of(el)}">{inner}</div>'
    if t == "image":
        return (
            f'<img src="{esc(safe_url(el.get("url", "")))}" alt="{esc(el.get("alt", ""))}" '
            f'style="border-radius:{num(el.get("radius"), 0)}px">'
        )
    if t == "gallery":
        cols = min(max(num(el.get("columns"), 3), 1), 4)
        imgs = "".join(
            f'<img src="{esc(safe_url(u))}" alt="Gambar galeri {n}" '
            f'style="border-radius:{num(el.get("radius"), 0)}px">'
            for n, u in enumerate(lines_of(el.get("urls")), start=1)
        )
        return f'<div class="gallery" style="grid-template-columns:repeat({cols},1fr)">{imgs}</div>'
    if t == "list":
        tag = "ol" if el.get("style") == "number" else "ul"
        items = "".join(f"<li>{esc(i)}</li>" for i in lines_of(el.get("items")))
        return f"<{tag}>{items}</{tag}>"
    if t == "input":
        return (
            f'<label class="field"><span>{esc(el.get("label", ""))}</span>'
            f'<input type="{input_kind(el)}" placeholder="{esc(el.get("placeholder", ""))}"></label>'
        )
    if t == "card":
        return (
            f'<div class="card"><h3>{esc(el.get("title", ""))}</h3>'
            f'<p>{esc(el.get("text", ""))}</p></div>'
        )
    if t == "divider":
        return "<hr>"
    if t == "spacer":
        return f'<div style="height:{num(el.get("height"), 24)}px"></div>'
    if t == "footer":
        return f'<footer class="footer">{esc(el.get("text", ""))}</footer>'
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

    st.divider()
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
        elements = page["elements"]
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

    if view == "Preview":
        tpl_key = st.session_state.get("tpl_choice")
        if st.session_state.get("tpl_preview") and tpl_key in TEMPLATES:
            st.caption(f"Pratinjau template: {TEMPLATES[tpl_key]['name']} (belum diterapkan ke desainmu)")
            inner = build_html(template_design(tpl_key))
        else:
            _, sel_el = selected_element()
            inner = build_html(
                design,
                highlight_id=sel_el["id"] if sel_el else None,
                active=st.session_state.page_idx,
            )
        framed = device_frame(inner, DEVICES[device])
        if hasattr(st, "iframe"):
            st.iframe(framed, height=PANEL_HEIGHT - 50)
        else:  # Streamlit versi lama
            components.html(framed, height=PANEL_HEIGHT - 50, scrolling=False)

    elif view == "Kode HTML":
        output = build_html(design)
        st.download_button("⬇️ Unduh index.html", output, file_name="index.html", mime="text/html")
        with st.container(height=PANEL_HEIGHT - 110, border=True):
            st.code(output, language="html")

    else:
        target = st.selectbox(
            "Target pembuatan",
            [
                "HTML/CSS/JavaScript satu file",
                "React dengan Tailwind CSS",
                "Streamlit (Python)",
                "Flutter (Dart)",
            ],
        )
        output = build_prompt(design, target)
        st.download_button(
            "⬇️ Unduh prompt_master.txt", output, file_name="prompt_master.txt", mime="text/plain"
        )
        with st.container(height=PANEL_HEIGHT - 160, border=True):
            st.code(output, language="markdown")

# ---------------------------- PANEL KANAN ---------------------------------
with col_right:
    with st.container(height=PANEL_HEIGHT, border=True):
        tab_prop, tab_tpl, tab_theme, tab_file = st.tabs(["Properti", "Template", "Tema", "Berkas"])

        with tab_prop:
            idx, sel = selected_element()
            if sel is None:
                st.info("Pilih elemen di panel kiri (bagian Susunan) untuk mengubah propertinya.")
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
