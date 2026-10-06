"""Spesifikasi 50 komponen bar tambahan (paket "Pro").

Berisi data murni tanpa Streamlit, sengaja tidak mengimpor bar_specs.py agar
tidak ada impor melingkar (bar_specs.py yang menggabungkan PRO_BAR_SPECS ke
BAR_SPECS di bagian bawah file). Renderer HTML-nya ada di bars_pro.py,
CSS-nya di css_pro.py.

Grup baru yang dipakai di sini harus didaftarkan lewat PRO_GROUP_ORDER.
"""
import copy

PRO_GROUP_ORDER = ["Konten", "Keuangan", "Peta & Lokasi"]

STATUS_KINDS = {"info": "Info", "success": "Sukses", "warning": "Peringatan", "error": "Galat"}
ICON_HINT = "Nama ikon mengikuti Material Symbols (contoh: home, search, person). Daftar lengkap: fonts.google.com/icons"

ALIGN_KINDS = {"left": "Kiri", "center": "Tengah", "right": "Kanan"}
TREND_KINDS = {"up": "Naik", "down": "Turun", "flat": "Datar"}
HEALTH_KINDS = {"safe": "Aman", "warning": "Perlu perhatian", "danger": "Kritis"}
ORDER_KINDS = {"pending": "Menunggu bayar", "packed": "Dikemas", "shipped": "Dikirim", "done": "Selesai"}
BUDGET_KINDS = {"safe": "Aman", "warning": "Mendekati batas", "over": "Melebihi anggaran"}
MONEY_KINDS = {"in": "Masuk", "out": "Keluar"}
BILL_KINDS = {"due": "Belum dibayar", "paid": "Lunas", "late": "Terlambat"}
ATTEND_KINDS = {"in": "Sudah masuk", "out": "Sudah pulang", "late": "Terlambat"}
OPEN_KINDS = {"open": "Buka", "closed": "Tutup", "busy": "Ramai"}
STOCK_KINDS = {"ready": "Tersedia", "low": "Terbatas", "out": "Habis"}

PRO_BAR_SPECS = {
    # ---- Navigasi (5) ----
    "appbar": {
        "label": "Header aplikasi", "icon": "web_asset", "group": "Navigasi", "hint": True,
        "defaults": {"title": "Detail pesanan", "subtitle": "Diperbarui 5 menit lalu",
                     "back": "Kembali", "action": "Simpan", "icon": "more_vert"},
        "fields": [("title", "Judul", "text"), ("subtitle", "Subjudul", "text"),
                   ("back", "Label tombol kembali", "text"), ("action", "Label aksi kanan", "text"),
                   ("icon", "Ikon aksi kanan", "text")],
    },
    "quicknav": {
        "label": "Navigasi cepat", "icon": "apps", "group": "Navigasi", "hint": True,
        "defaults": {"items": "Isi ulang|add_card\nTransfer|swap_horiz\nScan|qr_code_scanner\nRiwayat|history",
                     "active": 1},
        "fields": [("items", "Pintasan (label|ikon, satu per baris)", "area"),
                   ("active", "Pintasan aktif (urutan)", "int", (1, 8))],
    },
    "subnav": {
        "label": "Sub navigasi", "icon": "view_list", "group": "Navigasi",
        "defaults": {"items": "Ringkasan\nDetail\nUlasan\nRekomendasi", "active": 1},
        "fields": [("items", "Menu (satu per baris)", "area"), ("active", "Menu aktif (urutan)", "int", (1, 10))],
    },
    "stepdots": {
        "label": "Titik langkah", "icon": "more_horiz", "group": "Navigasi",
        "defaults": {"total": 5, "current": 2, "label": "Langkah 2 dari 5"},
        "fields": [("total", "Jumlah langkah", "int", (1, 12)), ("current", "Langkah aktif", "int", (1, 12)),
                   ("label", "Keterangan (boleh kosong)", "text")],
    },
    "swipenav": {
        "label": "Navigasi geser", "icon": "swipe", "group": "Navigasi",
        "defaults": {"label": "Kartu 3 dari 8", "prev": "Sebelumnya", "next": "Berikutnya"},
        "fields": [("label", "Keterangan tengah", "text"), ("prev", "Label kiri", "text"),
                   ("next", "Label kanan", "text")],
    },

    # ---- Aksi (4) ----
    "bulkactionbar": {
        "label": "Bar aksi massal", "icon": "checklist", "group": "Aksi", "hint": True,
        "defaults": {"count": 3, "select_all": "Pilih semua",
                     "items": "Hapus|delete\nPindah|drive_file_move\nArsip|archive"},
        "fields": [("count", "Jumlah item terpilih", "int", (0, 99)),
                   ("select_all", "Label pilih semua", "text"),
                   ("items", "Aksi (label|ikon, satu per baris)", "area")],
    },
    "exportbar": {
        "label": "Bar ekspor", "icon": "file_download", "group": "Aksi",
        "defaults": {"label": "Ekspor data", "formats": "CSV\nExcel\nPDF", "active": 1, "button": "Unduh"},
        "fields": [("label", "Label", "text"), ("formats", "Format (satu per baris)", "area"),
                   ("active", "Format aktif (urutan)", "int", (1, 6)), ("button", "Label tombol", "text")],
    },
    "approvalbar": {
        "label": "Bar persetujuan", "icon": "approval", "group": "Aksi",
        "defaults": {"title": "Permintaan cuti", "note": "Diajukan 2 jam lalu oleh Rani",
                     "approve": "Setujui", "reject": "Tolak"},
        "fields": [("title", "Judul pengajuan", "text"), ("note", "Keterangan", "text"),
                   ("approve", "Label tombol setuju", "text"), ("reject", "Label tombol tolak", "text")],
    },
    "printbar": {
        "label": "Bar cetak", "icon": "print", "group": "Aksi",
        "defaults": {"label": "Cetak dokumen", "copies": 2, "size": "A4", "button": "Cetak"},
        "fields": [("label", "Label", "text"), ("copies", "Jumlah salinan", "int", (1, 20)),
                   ("size", "Ukuran kertas", "text"), ("button", "Label tombol", "text")],
    },

    # ---- Informasi (4) ----
    "weatherbar": {
        "label": "Bar cuaca", "icon": "wb_sunny", "group": "Informasi", "hint": True,
        "defaults": {"place": "Jakarta", "temp": "31°C", "note": "Cerah berawan · Lembap 78%",
                     "icon": "wb_sunny", "high": "33°", "low": "26°"},
        "fields": [("place", "Lokasi", "text"), ("temp", "Suhu", "text"), ("note", "Keterangan", "text"),
                   ("icon", "Ikon cuaca", "text"), ("high", "Suhu tertinggi", "text"),
                   ("low", "Suhu terendah", "text")],
    },
    "notificationbar": {
        "label": "Bar notifikasi", "icon": "notifications", "group": "Informasi",
        "defaults": {"app": "Pesan", "title": "Kamu punya 3 pesan baru", "time": "09:12", "unread": "3"},
        "fields": [("app", "Nama pengirim", "text"), ("title", "Isi notifikasi", "text"),
                   ("time", "Waktu", "text"), ("unread", "Jumlah belum dibaca (boleh kosong)", "text")],
    },
    "metricbar": {
        "label": "Bar metrik ambang", "icon": "sensors", "group": "Informasi",
        "defaults": {"label": "Waktu muat rata-rata", "value": "1,8 s", "delta": "+0,3 s",
                     "trend": "up", "status": "warning", "note": "Ambang batas 1,5 s"},
        "fields": [("label", "Label metrik", "text"), ("value", "Nilai", "text"), ("delta", "Perubahan", "text"),
                   ("trend", "Arah tren", "sel", TREND_KINDS), ("status", "Status", "sel", HEALTH_KINDS),
                   ("note", "Keterangan bawah", "text")],
    },
    "updatebar": {
        "label": "Bar pembaruan", "icon": "system_update", "group": "Informasi",
        "defaults": {"version": "Versi 2.4.0", "note": "Perbaikan bug dan mode gelap baru",
                     "size": "18 MB", "button": "Perbarui"},
        "fields": [("version", "Versi", "text"), ("note", "Catatan rilis", "text"),
                   ("size", "Ukuran unduhan", "text"), ("button", "Label tombol", "text")],
    },

    # ---- Data (6) ----
    "donutbar": {
        "label": "Bar donat", "icon": "donut_large", "group": "Data",
        "defaults": {"label": "Komposisi penjualan", "caption": "Total 1.240 pesanan",
                     "items": "Kopi|45|#6366f1\nMakanan|30|#f59e0b\nLainnya|25|#22c55e"},
        "fields": [("label", "Judul", "text"), ("caption", "Keterangan", "text"),
                   ("items", "Segmen (nama|persen|warna, satu per baris)", "area")],
    },
    "gaugebar": {
        "label": "Bar pengukur", "icon": "data_usage", "group": "Data",
        "defaults": {"label": "Kapasitas server", "value": 72, "unit": "%",
                     "min_label": "0", "max_label": "100"},
        "fields": [("label", "Label", "text"), ("value", "Nilai (%)", "int", (0, 100)),
                   ("unit", "Satuan", "text"), ("min_label", "Label minimum", "text"),
                   ("max_label", "Label maksimum", "text")],
    },
    "rankingbar": {
        "label": "Bar peringkat", "icon": "leaderboard", "group": "Data",
        "defaults": {"title": "Produk terlaris", "unit": "terjual",
                     "items": "Kaos Katun Polos|182\nTote Bag Kanvas|140\nTopi Baseball|96"},
        "fields": [("title", "Judul", "text"), ("unit", "Satuan nilai", "text"),
                   ("items", "Peringkat (nama|nilai, satu per baris)", "area")],
    },
    "heatmapbar": {
        "label": "Bar peta panas", "icon": "grid_on", "group": "Data",
        "defaults": {"label": "Kepadatan order per jam", "caption": "Puncak pukul 14.00",
                     "values": "0,1,2,3,5,8,12,15,11,7,4,2"},
        "fields": [("label", "Judul", "text"), ("caption", "Keterangan", "text"),
                   ("values", "Nilai per kolom (dipisah koma)", "text")],
    },
    "distributionbar": {
        "label": "Bar distribusi", "icon": "stacked_bar_chart", "group": "Data",
        "defaults": {"label": "Distribusi jawaban", "caption": "n = 512 responden",
                     "items": "Sangat puas|48|#22c55e\nPuas|30|#3b82f6\nCukup|14|#f59e0b\nKurang|8|#ef4444"},
        "fields": [("label", "Judul", "text"), ("caption", "Keterangan", "text"),
                   ("items", "Bagian (nama|persen|warna, satu per baris)", "area")],
    },
    "funnelbar": {
        "label": "Bar corong", "icon": "filter_alt", "group": "Data",
        "defaults": {"label": "Corong pendaftaran", "caption": "Konversi akhir 16%",
                     "items": "Kunjungan|100\nDaftar|42\nVerifikasi|28\nAktif|16"},
        "fields": [("label", "Judul", "text"), ("caption", "Keterangan", "text"),
                   ("items", "Tahap (nama|nilai, satu per baris)", "area")],
    },

    # ---- Formulir (5) ----
    "uploadinputbar": {
        "label": "Bar unggah berkas", "icon": "upload_file", "group": "Formulir",
        "defaults": {"label": "Unggah dokumen pendukung", "note": "PDF atau JPG, maksimal 5 MB",
                     "button": "Pilih berkas", "file": "ktp.pdf", "progress": 60},
        "fields": [("label", "Label", "text"), ("note", "Keterangan", "text"), ("button", "Label tombol", "text"),
                   ("file", "Nama berkas terpilih (boleh kosong)", "text"),
                   ("progress", "Progres unggah (%)", "int", (0, 100))],
    },
    "datepickerbar": {
        "label": "Bar pemilih tanggal", "icon": "event", "group": "Formulir",
        "defaults": {"label": "Periode laporan", "start": "01 Okt 2026", "end": "31 Okt 2026",
                     "presets": "7 hari\n30 hari\nKustom", "active": 2, "button": "Terapkan"},
        "fields": [("label", "Label", "text"), ("start", "Tanggal mulai", "text"), ("end", "Tanggal selesai", "text"),
                   ("presets", "Pilihan cepat (satu per baris)", "area"),
                   ("active", "Pilihan aktif (urutan)", "int", (1, 6)), ("button", "Label tombol", "text")],
    },
    "ratinginputbar": {
        "label": "Bar masukan rating", "icon": "star_rate", "group": "Formulir",
        "defaults": {"label": "Seberapa puas kamu?", "value": 4,
                     "low_label": "Tidak puas", "high_label": "Sangat puas"},
        "fields": [("label", "Pertanyaan", "text"), ("value", "Nilai terpilih", "int", (0, 5)),
                   ("low_label", "Label kiri", "text"), ("high_label", "Label kanan", "text")],
    },
    "quantitybar": {
        "label": "Bar jumlah", "icon": "calculate", "group": "Formulir",
        "defaults": {"label": "Jumlah", "value": 2, "note": "Maksimal 10 per pesanan", "button": "Tambah"},
        "fields": [("label", "Label", "text"), ("value", "Nilai", "int", (0, 99)),
                   ("note", "Keterangan", "text"), ("button", "Label tombol", "text")],
    },
    "passstrengthbar": {
        "label": "Bar kekuatan sandi", "icon": "password", "group": "Formulir",
        "defaults": {"label": "Kekuatan kata sandi", "value": 3,
                     "levels": "Lemah\nCukup\nKuat\nSangat kuat",
                     "hints": "Minimal 8 karakter\nKombinasi huruf besar & angka\nTambahkan simbol unik"},
        "fields": [("label", "Label", "text"), ("value", "Tingkat kekuatan (1-4)", "int", (1, 4)),
                   ("levels", "Tingkat (satu per baris)", "area"), ("hints", "Syarat (satu per baris)", "area")],
    },

    # ---- Media (5) ----
    "videobar": {
        "label": "Bar video", "icon": "movie", "group": "Media",
        "defaults": {"thumb": "https://picsum.photos/seed/video12/240/140",
                     "title": "Cara menyusun halaman", "channel": "UI Builder",
                     "views": "8,4 rb ditonton", "duration": "12:40", "button": "Putar"},
        "fields": [("thumb", "URL gambar mini", "text"), ("title", "Judul video", "text"),
                   ("channel", "Kanal", "text"), ("views", "Jumlah tontonan", "text"),
                   ("duration", "Durasi", "text"), ("button", "Label tombol", "text")],
    },
    "equalizerbar": {
        "label": "Bar equalizer", "icon": "graphic_eq", "group": "Media",
        "defaults": {"label": "Equalizer", "button": "Reset",
                     "items": "60 Hz|4\n230 Hz|7\n910 Hz|2\n3 kHz|8\n14 kHz|5"},
        "fields": [("label", "Label", "text"), ("button", "Label tombol", "text"),
                   ("items", "Frekuensi (label|nilai 0-10, satu per baris)", "area")],
    },
    "podcastbar": {
        "label": "Bar podcast", "icon": "podcasts", "group": "Media",
        "defaults": {"show": "Sore Sore Podcast", "episode": "Ep. 42: Merancang untuk semua orang",
                     "duration": "38 menit", "button": "Putar"},
        "fields": [("show", "Nama acara", "text"), ("episode", "Judul episode", "text"),
                   ("duration", "Durasi", "text"), ("button", "Label tombol", "text")],
    },
    "camerabar": {
        "label": "Bar kamera", "icon": "photo_camera", "group": "Media", "hint": True,
        "defaults": {"modes": "Video\nFoto\nPotret\nMalam", "active": 2,
                     "note": "Geser untuk ganti mode", "flash": "flash_on"},
        "fields": [("modes", "Mode (satu per baris)", "area"), ("active", "Mode aktif (urutan)", "int", (1, 8)),
                   ("note", "Keterangan", "text"), ("flash", "Ikon lampu", "text")],
    },
    "lyricsbar": {
        "label": "Bar lirik", "icon": "lyrics", "group": "Media",
        "defaults": {"lines": "Reff:\nMelangkah pelan di kota yang tak tidur\nMenghitung bintang dari balik jendela",
                     "active": 2, "note": "Sinkron otomatis"},
        "fields": [("lines", "Baris lirik (satu per baris)", "area"),
                   ("active", "Baris aktif (urutan)", "int", (1, 20)), ("note", "Keterangan", "text")],
    },

    # ---- Sosial (3) ----
    "groupsbar": {
        "label": "Bar komunitas", "icon": "groups", "group": "Sosial",
        "defaults": {"name": "Komunitas Desain Nusantara", "members": "2.840 anggota",
                     "avatar": "https://i.pravatar.cc/96?img=15", "note": "12 post baru minggu ini",
                     "button": "Gabung"},
        "fields": [("name", "Nama komunitas", "text"), ("members", "Jumlah anggota", "text"),
                   ("avatar", "URL foto (kosongkan untuk inisial)", "text"),
                   ("note", "Keterangan", "text"), ("button", "Label tombol", "text")],
    },
    "trendbar": {
        "label": "Bar tren", "icon": "trending_up", "group": "Sosial",
        "defaults": {"title": "Sedang ramai",
                     "items": "#desainantarmuka|12,4 rb\n#buildwithstreamlit|8,1 rb\n#nusantaracreative|5,3 rb"},
        "fields": [("title", "Judul", "text"),
                   ("items", "Tagar (tagar|jumlah post, satu per baris)", "area")],
    },
    "awardbar": {
        "label": "Bar penghargaan", "icon": "emoji_events", "group": "Sosial", "hint": True,
        "defaults": {"badge": "Pengguna Rajin", "note": "Login 30 hari berturut-turut",
                     "points": "+250 poin", "icon": "workspace_premium", "button": "Bagikan"},
        "fields": [("badge", "Nama lencana", "text"), ("note", "Keterangan", "text"),
                   ("points", "Poin", "text"), ("icon", "Ikon lencana", "text"),
                   ("button", "Label tombol", "text")],
    },

    # ---- Toko (4) ----
    "wishlistbar": {
        "label": "Bar daftar keinginan", "icon": "favorite_border", "group": "Toko",
        "defaults": {"image": "https://picsum.photos/seed/wishlist4/160/160", "name": "Sepatu Lari Ringan",
                     "price": "Rp 429.000", "note": "Stok tersisa 4", "button": "Pindah ke keranjang"},
        "fields": [("image", "URL gambar", "text"), ("name", "Nama produk", "text"),
                   ("price", "Harga", "text"), ("note", "Keterangan", "text"),
                   ("button", "Label tombol", "text")],
    },
    "orderbar": {
        "label": "Bar pesanan", "icon": "receipt_long", "group": "Toko",
        "defaults": {"code": "INV-2026-1042", "status": "shipped", "date": "Dikirim 4 Okt",
                     "total": "Rp 267.000", "button": "Lacak"},
        "fields": [("code", "Nomor pesanan", "text"), ("status", "Status", "sel", ORDER_KINDS),
                   ("date", "Keterangan tanggal", "text"), ("total", "Total belanja", "text"),
                   ("button", "Label tombol", "text")],
    },
    "bundlingbar": {
        "label": "Bar paket bundling", "icon": "inventory_2", "group": "Toko",
        "defaults": {"title": "Paket hemat sarapan", "save": "Hemat Rp 8.000", "price": "Rp 32.000",
                     "items": "Kopi Susu|Rp 22.000\nRoti Bakar|Rp 18.000", "button": "Ambil paket"},
        "fields": [("title", "Nama paket", "text"), ("save", "Label hemat", "text"), ("price", "Harga paket", "text"),
                   ("items", "Isi paket (nama|harga, satu per baris)", "area"), ("button", "Label tombol", "text")],
    },
    "loyaltybar": {
        "label": "Bar loyalitas", "icon": "card_giftcard", "group": "Toko",
        "defaults": {"level": "Level Gold", "points": "1.240 poin", "value": 68,
                     "next": "480 poin lagi ke Platinum", "button": "Tukar poin"},
        "fields": [("level", "Level", "text"), ("points", "Poin saat ini", "text"),
                   ("value", "Progres ke level berikutnya (%)", "int", (0, 100)),
                   ("next", "Keterangan berikutnya", "text"), ("button", "Label tombol", "text")],
    },

    # ---- Keuangan (5) ----
    "balancebar": {
        "label": "Bar saldo", "icon": "account_balance_wallet", "group": "Keuangan", "hint": True,
        "defaults": {"label": "Saldo tersedia", "amount": "Rp 3.450.000", "note": "Diperbarui 08:12",
                     "button": "Isi ulang", "icon": "account_balance_wallet"},
        "fields": [("label", "Label", "text"), ("amount", "Jumlah saldo", "text"),
                   ("note", "Keterangan", "text"), ("button", "Label tombol", "text"),
                   ("icon", "Ikon", "text")],
    },
    "transactionbar": {
        "label": "Bar transaksi", "icon": "swap_vert", "group": "Keuangan", "hint": True,
        "defaults": {"title": "Transfer ke Budi", "time": "Hari ini, 09:24", "amount": "- Rp 150.000",
                     "kind": "out", "category": "Transfer", "button": "Detail", "icon": "swap_vert"},
        "fields": [("title", "Judul transaksi", "text"), ("time", "Waktu", "text"), ("amount", "Nominal", "text"),
                   ("kind", "Jenis", "sel", MONEY_KINDS), ("category", "Kategori", "text"),
                   ("button", "Label tombol", "text"), ("icon", "Ikon", "text")],
    },
    "budgetbar": {
        "label": "Bar anggaran", "icon": "pie_chart", "group": "Keuangan",
        "defaults": {"label": "Anggaran bulanan", "spent": "Rp 2,4 jt", "total": "Rp 4 jt", "value": 60,
                     "status": "safe", "note": "Sisa Rp 1,6 juta untuk 12 hari"},
        "fields": [("label", "Label", "text"), ("spent", "Terpakai", "text"), ("total", "Total anggaran", "text"),
                   ("value", "Progres (%)", "int", (0, 100)), ("status", "Status", "sel", BUDGET_KINDS),
                   ("note", "Keterangan", "text")],
    },
    "invoicebar": {
        "label": "Bar tagihan", "icon": "request_quote", "group": "Keuangan",
        "defaults": {"title": "Tagihan listrik", "due": "Jatuh tempo 20 Okt", "amount": "Rp 412.500",
                     "status": "due", "button": "Bayar"},
        "fields": [("title", "Nama tagihan", "text"), ("due", "Jatuh tempo", "text"),
                   ("amount", "Jumlah tagihan", "text"), ("status", "Status", "sel", BILL_KINDS),
                   ("button", "Label tombol", "text")],
    },
    "savingsbar": {
        "label": "Bar target tabungan", "icon": "savings", "group": "Keuangan",
        "defaults": {"title": "Liburan ke Jepang", "value": 45, "collected": "Rp 18 jt",
                     "target": "Rp 40 jt", "note": "Estimasi tercapai Jun 2027", "button": "Tambah dana"},
        "fields": [("title", "Nama target", "text"), ("value", "Progres (%)", "int", (0, 100)),
                   ("collected", "Terkumpul", "text"), ("target", "Target", "text"),
                   ("note", "Keterangan", "text"), ("button", "Label tombol", "text")],
    },

    # ---- Peta & Lokasi (4) ----
    "locationbar": {
        "label": "Bar lokasi", "icon": "location_on", "group": "Peta & Lokasi",
        "defaults": {"label": "Lokasi saat ini", "place": "Jl. Sudirman No. 12, Jakarta",
                     "accuracy": "Akurasi 12 m", "button": "Ubah", "thumb": ""},
        "fields": [("label", "Label", "text"), ("place", "Nama tempat / alamat", "text"),
                   ("accuracy", "Keterangan akurasi", "text"), ("button", "Label tombol", "text"),
                   ("thumb", "URL gambar peta mini (boleh kosong)", "text")],
    },
    "routebar": {
        "label": "Bar rute", "icon": "alt_route", "group": "Peta & Lokasi",
        "defaults": {"start": "Kantor", "end": "Bandara Soekarno-Hatta", "duration": "48 menit",
                     "distance": "24,6 km", "button": "Mulai"},
        "fields": [("start", "Titik awal", "text"), ("end", "Titik tujuan", "text"),
                   ("duration", "Estimasi waktu", "text"), ("distance", "Jarak", "text"),
                   ("button", "Label tombol", "text")],
    },
    "nearbybar": {
        "label": "Bar tempat terdekat", "icon": "near_me", "group": "Peta & Lokasi",
        "defaults": {"thumb": "https://picsum.photos/seed/tempat9/160/160", "name": "Kopi Sudut",
                     "category": "Kafe", "distance": "350 m", "rating": 4.6, "open": "open",
                     "open_note": "Buka sampai 22.00", "button": "Rute"},
        "fields": [("thumb", "URL gambar tempat", "text"), ("name", "Nama tempat", "text"),
                   ("category", "Kategori", "text"), ("distance", "Jarak", "text"),
                   ("rating", "Rating", "float", (0.0, 5.0, 0.5)), ("open", "Status", "sel", OPEN_KINDS),
                   ("open_note", "Keterangan jam", "text"), ("button", "Label tombol", "text")],
    },
    "checkinbar": {
        "label": "Bar absen", "icon": "how_to_reg", "group": "Peta & Lokasi",
        "defaults": {"label": "Absen masuk", "time": "08:02", "place": "Kantor Pusat · Radius 50 m",
                     "status": "in", "button": "Absen pulang"},
        "fields": [("label", "Label", "text"), ("time", "Waktu", "text"), ("place", "Lokasi", "text"),
                   ("status", "Status kehadiran", "sel", ATTEND_KINDS), ("button", "Label tombol", "text")],
    },

    # ---- Konten (5) ----
    "articlebar": {
        "label": "Bar artikel", "icon": "article", "group": "Konten",
        "defaults": {"category": "Panduan", "title": "Merancang tata letak yang mudah dibaca",
                     "meta": "7 menit baca · 4 Okt 2026", "button": "Baca"},
        "fields": [("category", "Kategori", "text"), ("title", "Judul artikel", "text"),
                   ("meta", "Keterangan", "text"), ("button", "Label tombol", "text")],
    },
    "authorbar": {
        "label": "Bar penulis", "icon": "badge", "group": "Konten",
        "defaults": {"name": "Sari Wulandari", "role": "Penulis & Peneliti UX", "avatar": "",
                     "posts": "48 tulisan", "button": "Ikuti"},
        "fields": [("name", "Nama penulis", "text"), ("role", "Peran", "text"),
                   ("avatar", "URL foto (kosongkan untuk inisial)", "text"),
                   ("posts", "Jumlah tulisan", "text"), ("button", "Label tombol", "text")],
    },
    "chaptersbar": {
        "label": "Bar bab", "icon": "menu_book", "group": "Konten",
        "defaults": {"title": "Bab 3: Warna dan Kontras",
                     "items": "3.1 Teori warna\n3.2 Kontras teks\n3.3 Latihan mandiri\n3.4 Ringkasan",
                     "current": 3, "progress": 60},
        "fields": [("title", "Judul bab", "text"), ("items", "Subbab (satu per baris)", "area"),
                   ("current", "Subbab aktif (urutan)", "int", (1, 20)),
                   ("progress", "Progres baca (%)", "int", (0, 100))],
    },
    "readingprogressbar": {
        "label": "Bar progres baca", "icon": "auto_stories", "group": "Konten",
        "defaults": {"label": "Halaman 12 dari 28", "value": 43, "note": "Sisa 16 menit",
                     "button": "Lanjut baca"},
        "fields": [("label", "Label", "text"), ("value", "Progres (%)", "int", (0, 100)),
                   ("note", "Keterangan", "text"), ("button", "Label tombol", "text")],
    },
    "relatedbar": {
        "label": "Bar bacaan terkait", "icon": "library_books", "group": "Konten",
        "defaults": {"title": "Bacaan terkait",
                     "items": "Tipografi untuk pemula|6 menit\nMenata grid 12 kolom|9 menit",
                     "button": "Lihat semua"},
        "fields": [("title", "Judul", "text"),
                   ("items", "Artikel (judul|durasi baca, satu per baris)", "area"),
                   ("button", "Label tombol", "text")],
    },
}


def pro_specs_copy():
    """Salinan dalam dari PRO_BAR_SPECS (untuk pengujian / pemakaian ulang)."""
    return copy.deepcopy(PRO_BAR_SPECS)
