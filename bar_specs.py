"""Spesifikasi 20 komponen bar (navigasi, aksi, informasi, data).

Hanya data murni, tanpa Streamlit. Untuk menambah bar baru: tambahkan satu entri
di BAR_SPECS, lalu tulis cabang render-nya di bars.py (fungsi render_bar).
"""

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
