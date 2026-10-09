"""50 spesifikasi komponen baru yang melengkapi katalog bar yang sudah ada."""


def _spec(label, icon, group, renderer, defaults, fields, hint=False):
    return {
        "label": label,
        "icon": icon,
        "group": group,
        "renderer": renderer,
        "defaults": defaults,
        "fields": fields,
        "hint": hint,
    }


COMPONENT_BAR_SPECS = {
    # --------------------------- Navigasi (5) ---------------------------
    "workspacebar": _spec(
        "Header ruang kerja", "workspaces", "Navigasi", "workspace",
        {"brand": "Studio Utama", "subtitle": "Ruang kerja tim", "badge": "PRO", "action": "Undang"},
        [("brand", "Nama ruang kerja", "text"), ("subtitle", "Keterangan", "text"),
         ("badge", "Lencana (boleh kosong)", "text"), ("action", "Label tombol", "text")],
    ),
    "stepnavpanelbar": _spec(
        "Navigasi langkah", "linear_scale", "Navigasi", "steps",
        {"title": "Buat proyek", "items": "Ringkasan\nDetail\nAnggota\nSelesai", "current": 2},
        [("title", "Judul", "text"), ("items", "Langkah (satu per baris)", "area"),
         ("current", "Langkah aktif", "int", (1, 10))],
    ),
    "sectiontabsbar": _spec(
        "Tab kategori berikon", "category", "Navigasi", "tabs",
        {"items": "Semua|apps\nDesain|palette\nFoto|photo_library\nDokumen|description", "active": 1},
        [("items", "Tab (label|ikon, satu per baris)", "area"), ("active", "Tab aktif", "int", (1, 10))], True,
    ),
    "sectionlinksbar": _spec(
        "Daftar tautan bagian", "list_alt", "Navigasi", "links",
        {"title": "Pengaturan akun", "items": "Profil|Informasi dasar|person\nKeamanan|Kata sandi & akses|lock\nNotifikasi|Preferensi pesan|notifications"},
        [("title", "Judul daftar", "text"), ("items", "Tautan (judul|keterangan|ikon)", "area")], True,
    ),
    "accountmenubar": _spec(
        "Menu akun", "manage_accounts", "Navigasi", "profile_nav",
        {"name": "Nadia Putri", "role": "Admin ruang kerja", "avatar": "", "items": "Profil|person\nTim saya|group\nPreferensi|settings", "active": 1},
        [("name", "Nama", "text"), ("role", "Peran", "text"), ("avatar", "URL foto (opsional)", "text"),
         ("items", "Menu (label|ikon, satu per baris)", "area"), ("active", "Menu aktif", "int", (1, 8))], True,
    ),
    # ----------------------------- Aksi (5) -----------------------------
    "commandpalettebar": _spec(
        "Pencarian perintah", "terminal", "Aksi", "command",
        {"placeholder": "Cari halaman, orang, atau aksi…", "shortcut": "⌘ K", "icon": "search"},
        [("placeholder", "Placeholder", "text"), ("shortcut", "Pintasan", "text"), ("icon", "Ikon", "text")], True,
    ),
    "undoqueuebar": _spec(
        "Bar urungkan perubahan", "undo", "Aksi", "undo",
        {"title": "Perubahan terakhir tersimpan", "note": "2 menit lalu · versi 12", "undo": "Urungkan", "redo": "Ulangi"},
        [("title", "Pesan", "text"), ("note", "Waktu / versi", "text"), ("undo", "Label urungkan", "text"), ("redo", "Label ulangi", "text")],
    ),
    "sharelinkbar": _spec(
        "Bar tautan berbagi", "link", "Aksi", "share_link",
        {"title": "Bagikan halaman ini", "url": "https://contoh.id/halaman", "button": "Salin tautan", "note": "Siapa pun dengan tautan dapat melihat."},
        [("title", "Judul", "text"), ("url", "Tautan", "text"), ("button", "Label tombol", "text"), ("note", "Keterangan", "text")],
    ),
    "selectiontoolbarbar": _spec(
        "Toolbar pilihan massal", "checklist", "Aksi", "selection",
        {"count": 3, "items": "Pindahkan|drive_file_move\nArsipkan|archive\nHapus|delete"},
        [("count", "Jumlah pilihan", "int", (0, 999)), ("items", "Aksi (label|ikon)", "area")], True,
    ),
    "createactionbar": _spec(
        "Bar aksi utama", "add_task", "Aksi", "create_action",
        {"title": "Siap melanjutkan?", "note": "Semua perubahan tersimpan otomatis.", "primary": "Simpan", "secondary": "Batal"},
        [("title", "Judul", "text"), ("note", "Keterangan", "text"), ("primary", "Aksi utama", "text"), ("secondary", "Aksi sekunder", "text")],
    ),
    # -------------------------- Informasi (5) ---------------------------
    "alertlistbar": _spec(
        "Daftar peringatan", "notifications_active", "Informasi", "alert_list",
        {"title": "Perlu perhatian", "items": "warning|Sinkronisasi tertunda|Periksa koneksi internet\ninfo|Pembaruan tersedia|Versi 2.6 siap dipasang\nsuccess|Cadangan selesai|Data aman tersimpan"},
        [("title", "Judul daftar", "text"), ("items", "Pesan (jenis|judul|keterangan)", "area")],
    ),
    "eventcardbar": _spec(
        "Kartu acara", "event_available", "Informasi", "event",
        {"title": "Lokakarya desain produk", "date": "Jumat, 24 Oktober · 10.00", "place": "Ruang Serbaguna, Jakarta", "note": "12 kursi tersisa", "button": "Daftar"},
        [("title", "Nama acara", "text"), ("date", "Tanggal dan waktu", "text"), ("place", "Lokasi", "text"), ("note", "Keterangan", "text"), ("button", "Label tombol", "text")],
    ),
    "connectionstatusbar": _spec(
        "Status koneksi", "wifi_tethering", "Informasi", "connection",
        {"status": "online", "title": "Semua layanan tersambung", "note": "Sinkronisasi terakhir 09.42", "action": "Periksa"},
        [("status", "Status (online / offline / sync)", "text"), ("title", "Judul status", "text"), ("note", "Keterangan", "text"), ("action", "Label tindakan", "text")],
    ),
    "reminderbar": _spec(
        "Pengingat tugas", "alarm", "Informasi", "reminder",
        {"title": "Kirim revisi beranda", "deadline": "Hari ini · 16.30", "owner": "Ditugaskan kepada Sari", "note": "Proyek: Peluncuran Musim Baru", "button": "Buka tugas"},
        [("title", "Tugas", "text"), ("deadline", "Batas waktu", "text"), ("owner", "Penanggung jawab", "text"), ("note", "Keterangan", "text"), ("button", "Label tombol", "text")],
    ),
    "releasecardbar": _spec(
        "Kartu catatan rilis", "new_releases", "Informasi", "release",
        {"version": "Versi 2.6", "title": "Mode fokus sudah hadir", "note": "Sembunyikan panel samping dan rapikan ruang kerja.", "date": "6 Okt 2026", "button": "Lihat pembaruan"},
        [("version", "Versi", "text"), ("title", "Fitur", "text"), ("note", "Ringkasan", "text"), ("date", "Tanggal", "text"), ("button", "Label tombol", "text")],
    ),
    # ------------------------------ Data (5) -----------------------------
    "kpicardbar": _spec(
        "Kartu indikator KPI", "query_stats", "Data", "metric",
        {"label": "Pengunjung aktif", "value": "12.840", "delta": "+12,8%", "note": "dibanding periode sebelumnya", "icon": "groups"},
        [("label", "Label", "text"), ("value", "Nilai", "text"), ("delta", "Perubahan", "text"), ("note", "Keterangan", "text"), ("icon", "Ikon", "text")], True,
    ),
    "progresslistbar": _spec(
        "Daftar progres tujuan", "checklist_rtl", "Data", "progress_list",
        {"title": "Target kuartal", "items": "Akuisisi pengguna|72\nRetensi pelanggan|58\nPenerbitan konten|90"},
        [("title", "Judul", "text"), ("items", "Target (nama|progres persen)", "area")],
    ),
    "activityfeedbar": _spec(
        "Linimasa aktivitas", "history", "Data", "activity",
        {"title": "Aktivitas terbaru", "items": "09.42|Nadia memperbarui beranda|Halaman utama\n09.18|Raka mengunggah gambar|Koleksi musim\nKemarin|Sari memberi komentar|Tombol ajakan"},
        [("title", "Judul", "text"), ("items", "Aktivitas (waktu|judul|keterangan)", "area")],
    ),
    "comparisoncardbar": _spec(
        "Kartu perbandingan metrik", "compare_arrows", "Data", "comparison",
        {"title": "Performa kanal", "items": "Organik|1.240|+14%\nSosial|860|+8%\nEmail|420|-2%", "left_label": "Kunjungan", "right_label": "Tren"},
        [("title", "Judul", "text"), ("items", "Baris (nama|nilai|perubahan)", "area"), ("left_label", "Kolom nilai", "text"), ("right_label", "Kolom tren", "text")],
    ),
    "goaltrackingbar": _spec(
        "Kartu pencapaian target", "track_changes", "Data", "goal",
        {"title": "Target pembaca bulanan", "value": "8.420", "target": "10.000", "progress": 84, "note": "1.580 kunjungan lagi", "button": "Lihat laporan"},
        [("title", "Target", "text"), ("value", "Pencapaian", "text"), ("target", "Nilai sasaran", "text"), ("progress", "Progres (%)", "int", (0, 100)), ("note", "Keterangan", "text"), ("button", "Label tombol", "text")],
    ),
    # --------------------------- Formulir (5) ----------------------------
    "addressformbar": _spec(
        "Ringkasan alamat", "location_on", "Formulir", "address",
        {"label": "Alamat pengiriman", "address": "Jl. Melati No. 24, Bandung, Jawa Barat", "note": "Rumah · atas nama Nadia", "button": "Ubah alamat"},
        [("label", "Label", "text"), ("address", "Alamat lengkap", "area"), ("note", "Keterangan", "text"), ("button", "Label tombol", "text")],
    ),
    "checklistformbar": _spec(
        "Checklist formulir", "fact_check", "Formulir", "checklist",
        {"title": "Sebelum mengirim", "items": "done|Informasi sudah benar\ndone|Dokumen pendukung terlampir\ntodo|Saya menyetujui ketentuan layanan"},
        [("title", "Judul", "text"), ("items", "Pengecekan (done/todo|teks)", "area")],
    ),
    "uploadqueuebar": _spec(
        "Antrean unggahan", "drive_folder_upload", "Formulir", "upload",
        {"title": "Dokumen terlampir", "items": "kontrak-proyek.pdf|2,4 MB|100\nreferensi-warna.png|840 KB|68", "button": "Tambah berkas"},
        [("title", "Judul", "text"), ("items", "Berkas (nama|ukuran|progres %)", "area"), ("button", "Label tombol", "text")],
    ),
    "contactformbar": _spec(
        "Formulir kontak ringkas", "contact_mail", "Formulir", "contact_form",
        {"title": "Minta informasi lebih lanjut", "label": "Alamat email", "placeholder": "nama@contoh.com", "button": "Kirim permintaan", "note": "Tim kami membalas dalam satu hari kerja."},
        [("title", "Judul", "text"), ("label", "Label isian", "text"), ("placeholder", "Placeholder", "text"), ("button", "Label tombol", "text"), ("note", "Keterangan", "text")],
    ),
    "consentpreferencesbar": _spec(
        "Preferensi persetujuan", "tune", "Formulir", "consent",
        {"title": "Preferensi privasi", "items": "Wajib|on\nAnalitik|on\nPersonalisasi|off", "note": "Preferensi dapat diubah kapan saja.", "button": "Simpan pilihan"},
        [("title", "Judul", "text"), ("items", "Preferensi (label|on/off)", "area"), ("note", "Keterangan", "text"), ("button", "Label tombol", "text")],
    ),
    # ----------------------------- Media (5) ----------------------------
    "albumfeaturebar": _spec(
        "Kartu album foto", "photo_album", "Media", "media_card",
        {"image": "https://picsum.photos/seed/album-feature/480/320", "title": "Akhir pekan di Ubud", "meta": "18 foto · 12 Sep 2026", "button": "Buka album"},
        [("image", "URL sampul", "text"), ("title", "Judul album", "text"), ("meta", "Jumlah / tanggal", "text"), ("button", "Label tombol", "text")],
    ),
    "audiocontrolbar": _spec(
        "Kartu kontrol audio", "headphones", "Media", "audio",
        {"title": "Ruang untuk berpikir", "artist": "Sore Sore Podcast", "current": "08:42", "duration": "24:10", "progress": 36},
        [("title", "Judul audio", "text"), ("artist", "Artis / kanal", "text"), ("current", "Waktu berjalan", "text"), ("duration", "Durasi", "text"), ("progress", "Progres (%)", "int", (0, 100))],
    ),
    "playlistqueuebar": _spec(
        "Antrean daftar putar", "queue_music", "Media", "playlist",
        {"title": "Putar berikutnya", "items": "Jalan Pulang|03:42|now\nMusim Baru|04:12|next\nRumah Kecil|02:58|next", "active": 1},
        [("title", "Judul daftar", "text"), ("items", "Lagu (judul|durasi|status)", "area"), ("active", "Item aktif", "int", (1, 12))],
    ),
    "photocaptionbar": _spec(
        "Foto dengan kredit", "image", "Media", "photo_credit",
        {"image": "https://picsum.photos/seed/photo-credit/900/520", "caption": "Cahaya sore di tepi sawah", "credit": "Foto oleh Raka Pratama · Garut, 2026", "alt": "Lanskap sawah saat matahari terbenam"},
        [("image", "URL foto", "text"), ("caption", "Takarir", "text"), ("credit", "Kredit foto", "text"), ("alt", "Teks alternatif", "text")],
    ),
    "recordingsessionbar": _spec(
        "Status sesi rekaman", "radio_button_checked", "Media", "recording",
        {"label": "Rekaman sedang berjalan", "time": "00:42", "status": "Mikrofon aktif", "wave": "4,8,14,9,18,11,6,16,10,20,7,12,5,17", "button": "Selesaikan"},
        [("label", "Judul sesi", "text"), ("time", "Durasi", "text"), ("status", "Keterangan", "text"), ("wave", "Gelombang (angka dipisah koma)", "text"), ("button", "Label tombol", "text")],
    ),
    # ----------------------------- Sosial (5) ----------------------------
    "pollresultbar": _spec(
        "Hasil jajak pendapat", "how_to_vote", "Sosial", "poll",
        {"title": "Format acara pilihan komunitas", "items": "Diskusi panel|48\nLokakarya|72\nSesi tanya jawab|31", "note": "151 suara · ditutup besok"},
        [("title", "Pertanyaan", "text"), ("items", "Pilihan (label|jumlah suara)", "area"), ("note", "Keterangan", "text")],
    ),
    "communitycardbar": _spec(
        "Kartu komunitas", "diversity_3", "Sosial", "community",
        {"name": "Ruang Desain Indonesia", "members": "4.820 anggota", "avatar": "", "note": "Tempat berbagi karya dan bertanya.", "button": "Gabung"},
        [("name", "Nama komunitas", "text"), ("members", "Jumlah anggota", "text"), ("avatar", "URL gambar (opsional)", "text"), ("note", "Keterangan", "text"), ("button", "Label tombol", "text")],
    ),
    "socialproofbar": _spec(
        "Kutipan anggota", "format_quote", "Sosial", "social_proof",
        {"quote": "Saya menemukan kolaborator pertama saya di komunitas ini.", "name": "Mira Anindya", "role": "Anggota sejak 2024", "avatar": ""},
        [("quote", "Kutipan", "area"), ("name", "Nama", "text"), ("role", "Peran / keterangan", "text"), ("avatar", "URL foto (opsional)", "text")],
    ),
    "creatorprofilebar": _spec(
        "Kartu profil kreator", "badge", "Sosial", "creator",
        {"name": "Ardi Saputra", "handle": "@ardibuat", "followers": "18,2 rb pengikut", "avatar": "", "button": "Ikuti"},
        [("name", "Nama", "text"), ("handle", "Nama pengguna", "text"), ("followers", "Jumlah pengikut", "text"), ("avatar", "URL foto (opsional)", "text"), ("button", "Label tombol", "text")],
    ),
    "reactionsummarybar": _spec(
        "Ringkasan reaksi", "emoji_emotions", "Sosial", "reactions",
        {"title": "Respons pembaca", "items": "Suka|thumb_up|128\nApresiasi|favorite|46\nIde|lightbulb|18"},
        [("title", "Judul", "text"), ("items", "Reaksi (label|ikon|jumlah)", "area")], True,
    ),
    # ------------------------------ Toko (5) -----------------------------
    "cartitemdetailbar": _spec(
        "Ringkasan item keranjang", "shopping_bag", "Toko", "cart_item",
        {"image": "https://picsum.photos/seed/cart-item/180/180", "name": "Tas selempang kanvas", "variant": "Hijau zaitun · Ukuran M", "quantity": 1, "price": "Rp 289.000"},
        [("image", "URL foto produk", "text"), ("name", "Nama produk", "text"), ("variant", "Varian", "text"), ("quantity", "Jumlah", "int", (1, 99)), ("price", "Harga", "text")],
    ),
    "deliveryestimatebar": _spec(
        "Estimasi pengiriman", "local_shipping", "Toko", "delivery",
        {"status": "Dalam perjalanan", "date": "Tiba Selasa, 13 Oktober", "note": "Kurir: SiCepat · Nomor resi SC482913", "step": 2},
        [("status", "Status pesanan", "text"), ("date", "Estimasi tiba", "text"), ("note", "Informasi kurir", "text"), ("step", "Tahap (1-3)", "int", (1, 3))],
    ),
    "productvariantbar": _spec(
        "Pemilih varian produk", "palette", "Toko", "variant",
        {"title": "Pilih warna", "items": "Arang\nKrem\nHijau zaitun\nBata", "active": 3, "note": "Ukuran tersedia: XS, S, M, L"},
        [("title", "Judul pilihan", "text"), ("items", "Varian (satu per baris)", "area"), ("active", "Varian aktif", "int", (1, 12)), ("note", "Keterangan", "text")],
    ),
    "discountprogressbar": _spec(
        "Progres diskon", "local_offer", "Toko", "discount",
        {"title": "Diskon bertingkat", "code": "BELANJA20", "progress": 65, "note": "Belanja Rp 35.000 lagi untuk diskon 20%", "button": "Pakai kode"},
        [("title", "Judul promo", "text"), ("code", "Kode", "text"), ("progress", "Progres (%)", "int", (0, 100)), ("note", "Keterangan", "text"), ("button", "Label tombol", "text")],
    ),
    "returnstatusbar": _spec(
        "Status retur pesanan", "assignment_return", "Toko", "return",
        {"code": "RET-2026-0842", "status": "Pemeriksaan barang", "title": "Retur sedang diproses", "date": "Diajukan 4 Oktober", "note": "Pengembalian dana ke metode pembayaran awal", "amount": "Rp 289.000"},
        [("code", "Nomor retur", "text"), ("status", "Tahap", "text"), ("title", "Judul status", "text"), ("date", "Tanggal", "text"), ("note", "Keterangan", "text"), ("amount", "Nilai pengembalian", "text")],
    ),
    # ---------------------------- Keuangan (5) --------------------------
    "walletsummarybar": _spec(
        "Ringkasan dompet", "account_balance_wallet", "Keuangan", "wallet",
        {"label": "Total dana tersedia", "balance": "Rp 8.450.000", "income": "+ Rp 2.150.000", "expense": "− Rp 1.240.000", "button": "Lihat dompet"},
        [("label", "Label", "text"), ("balance", "Saldo", "text"), ("income", "Pemasukan", "text"), ("expense", "Pengeluaran", "text"), ("button", "Label tombol", "text")],
    ),
    "expensebreakdownbar": _spec(
        "Rincian pengeluaran", "pie_chart", "Keuangan", "expense",
        {"title": "Pengeluaran bulan ini", "items": "Hunian|Rp 1.200.000|48\nMakanan|Rp 680.000|27\nTransportasi|Rp 420.000|17\nLainnya|Rp 200.000|8", "total": "Rp 2.500.000"},
        [("title", "Judul", "text"), ("items", "Kategori (nama|jumlah|persen)", "area"), ("total", "Jumlah total", "text")],
    ),
    "cashflowforecastbar": _spec(
        "Prakiraan arus kas", "show_chart", "Keuangan", "cashflow",
        {"title": "Arus kas 3 bulan", "items": "Okt|8,4 jt|6,2 jt\nNov|9,1 jt|6,7 jt\nDes|10,2 jt|7,4 jt", "note": "Proyeksi berdasarkan 6 bulan terakhir"},
        [("title", "Judul", "text"), ("items", "Periode (nama|masuk|keluar)", "area"), ("note", "Keterangan", "text")],
    ),
    "billcyclebar": _spec(
        "Ringkasan siklus tagihan", "receipt_long", "Keuangan", "bill",
        {"title": "Langganan Ruang Kerja", "amount": "Rp 129.000", "cycle": "Bulanan · berikutnya 18 Okt", "status": "Aktif", "button": "Kelola"},
        [("title", "Nama layanan", "text"), ("amount", "Jumlah", "text"), ("cycle", "Siklus", "text"), ("status", "Status", "text"), ("button", "Label tombol", "text")],
    ),
    "savingsmilestonebar": _spec(
        "Target tabungan bertahap", "savings", "Keuangan", "savings",
        {"title": "Dana darurat", "value": "Rp 12.600.000", "target": "Rp 20.000.000", "progress": 63, "next": "Tahap berikutnya: Rp 15 juta", "button": "Tambah tabungan"},
        [("title", "Nama target", "text"), ("value", "Terkumpul", "text"), ("target", "Target", "text"), ("progress", "Progres (%)", "int", (0, 100)), ("next", "Tahap berikutnya", "text"), ("button", "Label tombol", "text")],
    ),
    # ------------------------------ Konten (5) ---------------------------
    "toccompactbar": _spec(
        "Daftar isi ringkas", "format_list_numbered", "Konten", "toc",
        {"title": "Dalam artikel ini", "items": "Awal mula\nPrinsip desain\nSistem warna\nKesimpulan", "active": 2},
        [("title", "Judul", "text"), ("items", "Bagian (satu per baris)", "area"), ("active", "Bagian aktif", "int", (1, 12))],
    ),
    "storyteaserbar": _spec(
        "Kartu pengantar cerita", "auto_stories", "Konten", "story",
        {"image": "https://picsum.photos/seed/story-teaser/480/320", "category": "Di balik layar", "title": "Membangun merek dari ruang kecil", "summary": "Catatan tentang kebiasaan, eksperimen, dan keputusan sederhana.", "read_time": "6 menit baca"},
        [("image", "URL sampul", "text"), ("category", "Kategori", "text"), ("title", "Judul", "text"), ("summary", "Ringkasan", "area"), ("read_time", "Waktu baca", "text")],
    ),
    "authorbylinecardbar": _spec(
        "Kartu profil penulis", "edit_note", "Konten", "byline",
        {"name": "Sari Wulandari", "role": "Penulis & peneliti UX", "avatar": "", "published": "6 Okt 2026", "posts": "48 tulisan"},
        [("name", "Nama", "text"), ("role", "Peran", "text"), ("avatar", "URL foto (opsional)", "text"), ("published", "Tanggal terbit", "text"), ("posts", "Jumlah tulisan", "text")],
    ),
    "readingmodebar": _spec(
        "Kontrol mode membaca", "chrome_reader_mode", "Konten", "reading",
        {"title": "Panduan menyusun halaman", "current": 12, "total": 28, "progress": 43, "note": "Sisa sekitar 16 menit", "button": "Lanjutkan"},
        [("title", "Judul bacaan", "text"), ("current", "Halaman saat ini", "int", (1, 999)), ("total", "Jumlah halaman", "int", (1, 999)), ("progress", "Progres (%)", "int", (0, 100)), ("note", "Keterangan", "text"), ("button", "Label tombol", "text")],
    ),
    "quoteattributionbar": _spec(
        "Kutipan sumber", "format_quote", "Konten", "attributed_quote",
        {"quote": "Desain yang baik membuat hal penting terasa mudah ditemukan.", "author": "Dieter Rams", "source": "Wawancara tentang prinsip desain"},
        [("quote", "Kutipan", "area"), ("author", "Nama sumber", "text"), ("source", "Sumber / konteks", "text")],
    ),
}
