"""Spesifikasi gabungan 170 komponen bar (inti, tambahan, Pro, dan katalog baru).

Hanya data murni, tanpa Streamlit. Spesifikasi bar inti dan paket lama disimpan
pada berkas ini; komponen Pro dan komponen tambahan dimuat dari modul spesifiknya.
"""

GROUP_ORDER = [
    "Dasar", "Navigasi", "Aksi", "Informasi", "Data",
    "Formulir", "Media", "Sosial", "Toko",
]
STATUS_KINDS = {"info": "Info", "success": "Sukses", "warning": "Peringatan", "error": "Galat"}
STATUS_ICONS = {"info": "info", "success": "check_circle", "warning": "warning", "error": "error"}
ICON_HINT = "Nama ikon mengikuti Material Symbols (contoh: home, search, person). Daftar lengkap: fonts.google.com/icons"
# Daftar jenis isian untuk komponen formulir (dipakai bar_specs & bars_extra).
INPUT_KIND_LIST = {"text": "Teks", "email": "Email", "password": "Kata sandi", "number": "Angka", "tel": "Telepon"}
VIEW_KINDS = {"grid": "Grid", "list": "Daftar"}
STOCK_KINDS = {"ready": "Tersedia", "low": "Terbatas", "out": "Habis"}
PLAY_KINDS = {"pause": "Sedang diputar", "play": "Berhenti"}  # status pemutar
ALIGN_KINDS = {"left": "Kiri", "center": "Tengah", "right": "Kanan"}

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

    # ======================= 50 KOMPONEN TAMBAHAN =======================
    # ---- Navigasi (7) ----
    "menubar": {
        "label": "Bilah menu", "icon": "menu_open", "group": "Navigasi",
        "defaults": {"items": "Berkas\nUbah\nTampilan\nBantuan", "active": 1, "action": "Masuk"},
        "fields": [("items", "Menu (satu per baris)", "area"), ("active", "Menu aktif (urutan)", "int", (1, 8)),
                   ("action", "Tombol kanan (boleh kosong)", "text")],
    },
    "pilltabs": {
        "label": "Tab pil", "icon": "tab_unselected", "group": "Navigasi",
        "defaults": {"items": "Semua\nTerbaru\nPopuler\nDiskon", "active": 1},
        "fields": [("items", "Tab (satu per baris)", "area"), ("active", "Tab aktif (urutan)", "int", (1, 10))],
    },
    "railnav": {
        "label": "Rail ikon", "icon": "view_sidebar", "group": "Navigasi", "hint": True,
        "defaults": {"items": "Beranda|home\nTelusuri|explore\nNotifikasi|notifications|3\nPesan|mail|12\nProfil|account_circle",
                     "active": 1},
        "fields": [("items", "Item (label|ikon|badge, satu per baris)", "area"),
                   ("active", "Item aktif (urutan)", "int", (1, 8))],
    },
    "backbar": {
        "label": "Bar kembali", "icon": "arrow_back", "group": "Navigasi",
        "defaults": {"title": "Detail produk", "back": "Kembali", "action": "Bagikan", "icon": "share"},
        "fields": [("title", "Judul", "text"), ("back", "Label kembali", "text"),
                   ("action", "Label aksi kanan (boleh kosong)", "text"), ("icon", "Ikon aksi kanan", "text")],
    },
    "anchorlinks": {
        "label": "Navigasi anchor", "icon": "toc", "group": "Navigasi",
        "defaults": {"items": "Ringkasan|#ringkasan\nFitur|#fitur\nHarga|#harga\nFAQ|#faq", "active": 1},
        "fields": [("items", "Tautan (label|url, satu per baris)", "area"),
                   ("active", "Tautan aktif (urutan)", "int", (1, 10))],
    },
    "prevnext": {
        "label": "Bar sebelumnya/berikutnya", "icon": "swap_horiz", "group": "Navigasi",
        "defaults": {"prev": "Artikel sebelumnya", "prev_note": "Dasar Desain", "next": "Artikel berikutnya",
                     "next_note": "Panduan Warna"},
        "fields": [("prev", "Tombol kiri", "text"), ("prev_note", "Keterangan kiri", "text"),
                   ("next", "Tombol kanan", "text"), ("next_note", "Keterangan kanan", "text")],
    },
    "meganav": {
        "label": "Menu mega", "icon": "apps", "group": "Navigasi", "hint": True,
        "defaults": {"title": "Jelajahi",
                     "items": "Analitik|Pantau performa aplikasimu|insights\nOtomasi|Jalankan alur kerja otomatis|bolt\n"
                              "Laporan|Bagikan hasil ke tim|description\nIntegrasi|Hubungkan alat favoritmu|extension"},
        "fields": [("title", "Judul grup", "text"), ("items", "Item (judul|keterangan|ikon, satu per baris)", "area")],
    },

    # ---- Aksi (7) ----
    "actionbar": {
        "label": "Bar aksi", "icon": "bolt", "group": "Aksi",
        "defaults": {"primary": "Simpan perubahan", "secondary": "Batal", "note": "Perubahan tersimpan otomatis"},
        "fields": [("primary", "Tombol utama", "text"), ("secondary", "Tombol kedua (boleh kosong)", "text"),
                   ("note", "Keterangan kiri (boleh kosong)", "text")],
    },
    "commandbar": {
        "label": "Bar perintah", "icon": "keyboard_command_key", "group": "Aksi",
        "defaults": {"placeholder": "Ketik perintah atau cari…", "hint": "Ctrl K", "icon": "search"},
        "fields": [("placeholder", "Placeholder", "text"), ("hint", "Pintasan keyboard", "text"),
                   ("icon", "Ikon kiri", "text")],
    },
    "sortbar": {
        "label": "Bar urutan", "icon": "sort", "group": "Aksi",
        "defaults": {"label": "Urutkan", "options": "Terbaru\nTermurah\nTermahal\nTerpopuler", "active": 1, "view": "grid"},
        "fields": [("label", "Label", "text"), ("options", "Pilihan (satu per baris)", "area"),
                   ("active", "Pilihan aktif (urutan)", "int", (1, 8)), ("view", "Tampilan aktif", "sel", VIEW_KINDS)],
    },
    "sharebar": {
        "label": "Bar bagikan", "icon": "ios_share", "group": "Aksi", "hint": True,
        "defaults": {"label": "Bagikan ke", "items": "Salin tautan|link\nWhatsApp|chat\nX|tag\nLainnya|more_horiz"},
        "fields": [("label", "Label (boleh kosong)", "text"), ("items", "Tujuan (label|ikon, satu per baris)", "area")],
    },
    "commentbar": {
        "label": "Bar komentar", "icon": "chat_bubble", "group": "Aksi",
        "defaults": {"placeholder": "Tulis komentar…", "button": "Kirim", "hint": "Tekan Enter untuk mengirim", "avatar": ""},
        "fields": [("placeholder", "Placeholder", "text"), ("button", "Label tombol", "text"),
                   ("hint", "Keterangan bawah (boleh kosong)", "text"), ("avatar", "URL foto (kosongkan untuk inisial)", "text")],
    },
    "quickactions": {
        "label": "Aksi cepat", "icon": "grid_view", "group": "Aksi", "hint": True,
        "defaults": {"items": "Transfer|swap_horiz\nTop up|add_card\nBayar|receipt_long\nRiwayat|history\nLainnya|apps"},
        "fields": [("items", "Aksi (label|ikon, satu per baris)", "area")],
    },
    "linkbar": {
        "label": "Bar tautan", "icon": "link", "group": "Aksi",
        "defaults": {"items": "Syarat & ketentuan|#\nKebijakan privasi|#\nBantuan|#\nKarier|#", "align": "center"},
        "fields": [("items", "Tautan (label|url, satu per baris)", "area"), ("align", "Posisi", "sel", ALIGN_KINDS)],
    },

    # ---- Informasi (7) ----
    "infobanner": {
        "label": "Banner info", "icon": "article", "group": "Informasi",
        "defaults": {"kind": "info", "title": "Pembaruan 2.0", "text": "Mode gelap dan pintasan keyboard sudah tersedia.",
                     "link_text": "Lihat pembaruan", "link": "#"},
        "fields": [("kind", "Jenis", "sel", STATUS_KINDS), ("title", "Judul", "text"), ("text", "Isi", "text"),
                   ("link_text", "Label tautan (boleh kosong)", "text"), ("link", "URL tautan", "text")],
    },
    "tipbar": {
        "label": "Bar tips", "icon": "lightbulb", "group": "Informasi",
        "defaults": {"title": "Tips", "text": "Tekan Ctrl + K untuk membuka daftar perintah cepat.", "dismiss": "Mengerti"},
        "fields": [("title", "Label kecil", "text"), ("text", "Isi tips", "text"),
                   ("dismiss", "Tombol tutup (boleh kosong)", "text")],
    },
    "quotebar": {
        "label": "Bar kutipan", "icon": "format_quote", "group": "Informasi",
        "defaults": {"text": "Desain yang baik terasa sederhana, bukan sepi.", "author": "Rani Kusuma", "role": "Perancang Produk"},
        "fields": [("text", "Kutipan", "area"), ("author", "Nama", "text"), ("role", "Keterangan", "text")],
    },
    "totalbar": {
        "label": "Bar ringkasan total", "icon": "receipt_long", "group": "Informasi",
        "defaults": {"items": "Subtotal|Rp 240.000\nOngkir|Rp 18.000\nDiskon|- Rp 20.000",
                     "total_label": "Total", "total": "Rp 238.000"},
        "fields": [("items", "Baris (label|nilai, satu per baris)", "area"), ("total_label", "Label total", "text"),
                   ("total", "Nilai total", "text")],
    },
    "countdownbar": {
        "label": "Bar hitung mundur", "icon": "timer", "group": "Informasi",
        "defaults": {"label": "Promo berakhir dalam", "items": "02|Jam\n45|Menit\n10|Detik"},
        "fields": [("label", "Label", "text"), ("items", "Angka (nilai|satuan, satu per baris)", "area")],
    },
    "stockbar": {
        "label": "Bar ketersediaan", "icon": "inventory_2", "group": "Informasi",
        "defaults": {"label": "Stok tersisa 8 dari 40", "note": "Dikirim hari ini juga", "status": "low", "value": 20},
        "fields": [("label", "Label", "text"), ("note", "Keterangan (boleh kosong)", "text"),
                   ("status", "Status", "sel", STOCK_KINDS), ("value", "Nilai bar (%)", "int", (0, 100))],
    },
    "livebar": {
        "label": "Bar siaran langsung", "icon": "sensors", "group": "Informasi",
        "defaults": {"title": "Kelas daring: Dasar UI", "viewers": "1.240 menonton", "button": "Tonton"},
        "fields": [("title", "Judul", "text"), ("viewers", "Jumlah penonton", "text"),
                   ("button", "Label tombol (boleh kosong)", "text")],
    },

    # ---- Data (7) ----
    "tablebar": {
        "label": "Bar tabel", "icon": "table_chart", "group": "Data",
        "defaults": {"columns": "Produk|45\nHarga|25\nStatus|30", "row": "Kaos Polos|Rp 89.000|Aktif"},
        "fields": [("columns", "Kolom (judul|lebar %, satu per baris)", "area"),
                   ("row", "Baris data (dipisah |)", "text")],
    },
    "comparebar": {
        "label": "Bar perbandingan", "icon": "balance", "group": "Data",
        "defaults": {"title": "Penjualan", "items": "Tahun ini|78\nTahun lalu|54",
                     "caption": "Naik 24% dibanding tahun lalu"},
        "fields": [("title", "Judul", "text"), ("items", "Data (label|nilai 0-100, satu per baris)", "area"),
                   ("caption", "Keterangan bawah (boleh kosong)", "text")],
    },
    "sparkbar": {
        "label": "Bar grafik mini", "icon": "bar_chart", "group": "Data",
        "defaults": {"label": "Kunjungan 7 hari", "values": "12, 18, 9, 22, 30, 26, 34", "caption": "34 hari ini"},
        "fields": [("label", "Label", "text"), ("values", "Angka (dipisah koma)", "text"),
                   ("caption", "Keterangan bawah (boleh kosong)", "text")],
    },
    "legendbar": {
        "label": "Bar legenda", "icon": "legend_toggle", "group": "Data",
        "defaults": {"title": "Status", "items": "Selesai|#22c55e\nBerjalan|#f59e0b\nGagal|#ef4444"},
        "fields": [("title", "Judul (boleh kosong)", "text"), ("items", "Legenda (label|warna, satu per baris)", "area")],
    },
    "timelinebar": {
        "label": "Bar lini masa", "icon": "history", "group": "Data",
        "defaults": {"items": "Pesanan dibuat|09:12\nDikemas|11:40\nDikirim|16:05", "current": 3},
        "fields": [("items", "Tahap (label|waktu, satu per baris)", "area"),
                   ("current", "Tahap saat ini", "int", (1, 8))],
    },
    "rangebar": {
        "label": "Bar rentang nilai", "icon": "straighten", "group": "Data",
        "defaults": {"label": "Rentang harga", "min_label": "Rp 0", "max_label": "Rp 1.000.000", "low": 20, "high": 70},
        "fields": [("label", "Label", "text"), ("min_label", "Label kiri", "text"), ("max_label", "Label kanan", "text"),
                   ("low", "Batas bawah (%)", "int", (0, 100)), ("high", "Batas atas (%)", "int", (0, 100))],
    },
    "calendarstrip": {
        "label": "Strip tanggal", "icon": "calendar_month", "group": "Data",
        "defaults": {"items": "Sen|12\nSel|13\nRab|14\nKam|15\nJum|16\nSab|17", "active": 3},
        "fields": [("items", "Tanggal (hari|tanggal, satu per baris)", "area"),
                   ("active", "Tanggal aktif (urutan)", "int", (1, 14))],
    },

    # ---- Formulir (7) ----
    "formbar": {
        "label": "Bar formulir", "icon": "assignment", "group": "Formulir",
        "defaults": {"label": "Nama lengkap", "placeholder": "Ketik nama…", "kind": "text", "button": "Kirim"},
        "fields": [("label", "Label", "text"), ("placeholder", "Placeholder", "text"),
                   ("kind", "Jenis isian", "sel", INPUT_KIND_LIST), ("button", "Label tombol", "text")],
    },
    "newsletterbar": {
        "label": "Bar buletin", "icon": "mark_email_read", "group": "Formulir",
        "defaults": {"title": "Kabar terbaru tiap minggu", "placeholder": "email@contoh.com", "button": "Langganan",
                     "note": "Tanpa spam. Bisa berhenti kapan saja."},
        "fields": [("title", "Judul", "text"), ("placeholder", "Placeholder email", "text"),
                   ("button", "Label tombol", "text"), ("note", "Keterangan (boleh kosong)", "text")],
    },
    "otpbar": {
        "label": "Bar kode OTP", "icon": "pin", "group": "Formulir",
        "defaults": {"label": "Masukkan kode verifikasi", "digits": 6, "note": "Kode dikirim ke nama@email.com"},
        "fields": [("label", "Label", "text"), ("digits", "Jumlah kotak", "int", (4, 8)),
                   ("note", "Keterangan (boleh kosong)", "text")],
    },
    "tagsinputbar": {
        "label": "Bar input tag", "icon": "new_label", "group": "Formulir",
        "defaults": {"placeholder": "Tambah tag…", "tags": "desain\nantarmuka\nmobile", "button": "Tambah"},
        "fields": [("placeholder", "Placeholder", "text"), ("tags", "Tag (satu per baris)", "area"),
                   ("button", "Label tombol (boleh kosong)", "text")],
    },
    "sliderbar": {
        "label": "Bar penggeser", "icon": "tune", "group": "Formulir",
        "defaults": {"label": "Volume", "value": 60, "min_label": "0", "max_label": "100", "unit": "%"},
        "fields": [("label", "Label", "text"), ("value", "Nilai (%)", "int", (0, 100)),
                   ("min_label", "Label kiri", "text"), ("max_label", "Label kanan", "text"), ("unit", "Satuan", "text")],
    },
    "switchbar": {
        "label": "Bar sakelar", "icon": "toggle_on", "group": "Formulir",
        "defaults": {"items": "Notifikasi email|on\nPromo mingguan|off\nMode gelap|on"},
        "fields": [("items", "Pengaturan (label|on/off, satu per baris)", "area")],
    },
    "loginbar": {
        "label": "Bar masuk cepat", "icon": "login", "group": "Formulir",
        "defaults": {"title": "Masuk ke akunmu", "user": "nama@email.com", "placeholder": "Kata sandi",
                     "button": "Masuk", "note": "Lupa kata sandi?"},
        "fields": [("title", "Judul", "text"), ("user", "Email terisi", "text"), ("placeholder", "Placeholder sandi", "text"),
                   ("button", "Label tombol", "text"), ("note", "Tautan bawah (boleh kosong)", "text")],
    },

    # ---- Media (5) ----
    "playbar": {
        "label": "Bar pemutar", "icon": "play_circle", "group": "Media",
        "defaults": {"title": "Judul lagu", "artist": "Nama artis", "value": 32, "current": "1:12",
                     "duration": "3:48", "playing": "pause"},
        "fields": [("title", "Judul", "text"), ("artist", "Artis", "text"), ("value", "Posisi (%)", "int", (0, 100)),
                   ("current", "Waktu berjalan", "text"), ("duration", "Durasi", "text"),
                   ("playing", "Status", "sel", PLAY_KINDS)],
    },
    "storiesbar": {
        "label": "Bar cerita", "icon": "amp_stories", "group": "Media", "hint": True,
        "defaults": {"items": "Ceritamu||add\nRani|https://i.pravatar.cc/96?img=5\nBudi|https://i.pravatar.cc/96?img=12\n"
                              "Sari|https://i.pravatar.cc/96?img=32\nDewi|"},
        "fields": [("items", "Item (nama|url foto|ikon badge, satu per baris)", "area")],
    },
    "thumbstripbar": {
        "label": "Strip gambar mini", "icon": "view_carousel", "group": "Media",
        "defaults": {"items": "https://picsum.photos/seed/mini1/200/140\nhttps://picsum.photos/seed/mini2/200/140\n"
                              "https://picsum.photos/seed/mini3/200/140\nhttps://picsum.photos/seed/mini4/200/140",
                     "active": 1},
        "fields": [("items", "URL gambar (satu per baris)", "area"), ("active", "Gambar aktif (urutan)", "int", (1, 12))],
    },
    "captionsbar": {
        "label": "Bar takarir", "icon": "subtitles", "group": "Media",
        "defaults": {"text": "Selamat datang di episode kali ini.", "lang": "Bahasa Indonesia", "button": "CC"},
        "fields": [("text", "Teks takarir", "area"), ("lang", "Bahasa", "text"), ("button", "Label tombol", "text")],
    },
    "recordbar": {
        "label": "Bar perekam", "icon": "graphic_eq", "group": "Media",
        "defaults": {"label": "Merekam…", "time": "00:24", "button": "Kirim",
                     "wave": "4,9,14,7,17,11,6,13,8,16,5,10"},
        "fields": [("label", "Label", "text"), ("time", "Durasi", "text"), ("button", "Label tombol", "text"),
                   ("wave", "Tinggi gelombang (angka dipisah koma)", "text")],
    },

    # ---- Sosial (5) ----
    "reactionbar": {
        "label": "Bar reaksi", "icon": "favorite", "group": "Sosial", "hint": True,
        "defaults": {"items": "Suka|thumb_up|128\nCinta|favorite|32\nKomentar|chat_bubble|14"},
        "fields": [("items", "Reaksi (label|ikon|jumlah, satu per baris)", "area")],
    },
    "userstackbar": {
        "label": "Bar pengguna", "icon": "group", "group": "Sosial", "hint": True,
        "defaults": {"items": "Rani|https://i.pravatar.cc/64?img=9\nBudi|https://i.pravatar.cc/64?img=14\nSari|\nDewi|",
                     "count": "+12", "note": "bergabung di kelas ini"},
        "fields": [("items", "Pengguna (nama|url foto, satu per baris)", "area"), ("count", "Jumlah tambahan", "text"),
                   ("note", "Keterangan", "text")],
    },
    "reviewbar": {
        "label": "Bar ulasan", "icon": "rate_review", "group": "Sosial",
        "defaults": {"name": "Budi Santoso", "avatar": "", "rating": 4.5, "time": "2 hari lalu",
                     "text": "Pengiriman cepat, kualitas sesuai deskripsi."},
        "fields": [("name", "Nama", "text"), ("avatar", "URL foto (kosongkan untuk inisial)", "text"),
                   ("rating", "Nilai bintang", "float", (0.0, 5.0, 0.5)), ("time", "Waktu", "text"),
                   ("text", "Isi ulasan", "area")],
    },
    "chatbar": {
        "label": "Bar obrolan", "icon": "forum", "group": "Sosial",
        "defaults": {"name": "Rani Kusuma", "avatar": "https://i.pravatar.cc/64?img=20",
                     "message": "Paketnya sudah sampai, terima kasih!", "time": "09:24", "unread": "3"},
        "fields": [("name", "Nama", "text"), ("avatar", "URL foto (kosongkan untuk inisial)", "text"),
                   ("message", "Pesan terakhir", "text"), ("time", "Waktu", "text"),
                   ("unread", "Jumlah belum dibaca (boleh kosong)", "text")],
    },
    "followbar": {
        "label": "Bar ikuti", "icon": "person_add", "group": "Sosial",
        "defaults": {"name": "Rani Kusuma", "handle": "@ranikusuma · 12,4 rb pengikut", "avatar": "",
                     "button": "Ikuti", "note": "Mengikuti akunmu"},
        "fields": [("name", "Nama", "text"), ("handle", "Akun & pengikut", "text"),
                   ("avatar", "URL foto (kosongkan untuk inisial)", "text"), ("button", "Label tombol", "text"),
                   ("note", "Keterangan tambahan (boleh kosong)", "text")],
    },

    # ---- Toko (5) ----
    "cartbar": {
        "label": "Bar keranjang", "icon": "shopping_cart", "group": "Toko",
        "defaults": {"count": 3, "label": "Keranjang belanja", "total": "Rp 267.000", "button": "Checkout"},
        "fields": [("count", "Jumlah item", "int", (0, 99)), ("label", "Label", "text"),
                   ("total", "Total harga", "text"), ("button", "Label tombol", "text")],
    },
    "couponbar": {
        "label": "Bar kupon", "icon": "confirmation_number", "group": "Toko",
        "defaults": {"code": "HEMAT20", "note": "Diskon 20% maks. Rp 50.000", "expires": "Berlaku sampai 31 Des",
                     "button": "Pakai"},
        "fields": [("code", "Kode kupon", "text"), ("note", "Keterangan", "text"), ("expires", "Masa berlaku", "text"),
                   ("button", "Label tombol", "text")],
    },
    "shippingbar": {
        "label": "Bar gratis ongkir", "icon": "local_shipping", "group": "Toko",
        "defaults": {"label": "Belanja Rp 75.000 lagi untuk gratis ongkir", "value": 62,
                     "min_label": "Rp 0", "max_label": "Gratis ongkir"},
        "fields": [("label", "Label", "text"), ("value", "Progres (%)", "int", (0, 100)),
                   ("min_label", "Label kiri", "text"), ("max_label", "Label kanan", "text")],
    },
    "productbar": {
        "label": "Bar produk", "icon": "sell", "group": "Toko",
        "defaults": {"image": "https://picsum.photos/seed/produk7/160/160", "name": "Kaos Katun Polos",
                     "note": "Ukuran M · Putih", "price": "Rp 89.000", "old_price": "Rp 129.000", "button": "Tambah"},
        "fields": [("image", "URL gambar", "text"), ("name", "Nama produk", "text"), ("note", "Varian", "text"),
                   ("price", "Harga", "text"), ("old_price", "Harga sebelum diskon (boleh kosong)", "text"),
                   ("button", "Label tombol", "text")],
    },
    "paymentbar": {
        "label": "Bar pembayaran", "icon": "credit_card", "group": "Toko", "hint": True,
        "defaults": {"items": "Kartu kredit|•••• 4242|credit_card\nTransfer bank|BCA|account_balance\n"
                              "Dompet digital|Saldo Rp 25.000|wallet",
                     "active": 1, "note": "Pilih satu metode pembayaran"},
        "fields": [("items", "Metode (nama|keterangan|ikon, satu per baris)", "area"),
                   ("active", "Metode aktif (urutan)", "int", (1, 6)), ("note", "Keterangan bawah", "text")],
    },
}

# 50 komponen paket "Pro" (navigasi, aksi, informasi, data, formulir, media, sosial,
# toko, keuangan, peta & lokasi, konten). Spesifikasinya ada di bar_specs_pro.py,
# render HTML-nya di bars_pro.py, CSS-nya di css_pro.py.
from bar_specs_pro import PRO_BAR_SPECS, PRO_GROUP_ORDER  # noqa: E402

BAR_SPECS.update(PRO_BAR_SPECS)
for _group in PRO_GROUP_ORDER:
    if _group not in GROUP_ORDER:
        GROUP_ORDER.append(_group)

# Tambahan baru bersifat aditif: komponen lama dan paket Pro tetap tersedia.
from bar_specs_addons import COMPONENT_BAR_SPECS  # noqa: E402

BAR_SPECS.update(COMPONENT_BAR_SPECS)
del _group
