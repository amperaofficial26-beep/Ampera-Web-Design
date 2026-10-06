"""Template desain siap pakai.

Untuk menambah template: tambahkan satu entri di TEMPLATES memakai fungsi
pembantu (H, P, B, IMG, GAL, LST, INP, CARD, DIV, SPC, NAV, FOOT, BAR).
"""
import copy
import uuid

from config import ELEMENT_DEFAULTS, ELEMENT_STYLE_DEFAULTS
from design import default_design, theme_of
from styles import ensure_element_style


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
