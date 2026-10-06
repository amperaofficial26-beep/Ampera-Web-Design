"""Paket template galeri tambahan (ditambahkan tanpa mengganti template lama)."""
import copy

from config import ELEMENT_DEFAULTS, ELEMENT_STYLE_DEFAULTS
from design import theme_of
from styles import ensure_element_style


def _element(kind, **props):
    element = {"type": kind, **copy.deepcopy(ELEMENT_DEFAULTS[kind])}
    element["visual_style"] = copy.deepcopy(ELEMENT_STYLE_DEFAULTS)
    element.update(props)
    ensure_element_style(element)
    return element


def _pic(seed, width=900, height=520):
    return f"https://picsum.photos/seed/{seed}/{width}/{height}"


def _heading(text, size=32, align="left"):
    return _element("heading", text=text, size=size, align=align)


def _text(text, align="left"):
    return _element("text", text=text, align=align)


def _bar(kind, **props):
    return _element(kind, **props)


def _gallery(seeds, columns=3, radius=12):
    return _element(
        "gallery",
        urls="\n".join(_pic(seed, 480, 360) for seed in seeds),
        columns=columns,
        radius=radius,
    )


def _image(seed, alt, radius=16):
    return _element("image", url=_pic(seed), alt=alt, radius=radius)


# key, display name, page title, description, visual theme, image prefix,
# intro copy, filters, layout, style signature.
_GALLERIES = [
    ("galeri_lanskap_nusantara", "Galeri lanskap Nusantara", "Rupa Bentang", "Pemandangan gunung, pantai, dan desa dalam koleksi fotografi alam.", "#15803d", "#f5fbf4", "#17351f", "lanskap", "Jejak alam dari pesisir hingga puncak pegunungan.", "Semua\nGunung\nLaut\nHutan", "feature", 14),
    ("galeri_kebun_botani", "Galeri kebun botani", "Daun & Cahaya", "Katalog visual tanaman tropis, bunga, dan ruang hijau kota.", "#4d7c0f", "#f7fee7", "#26351b", "botani", "Catatan visual tentang tanaman yang tumbuh dekat dengan kita.", "Semua\nDaun\nBunga\nRuang", "editorial", 20),
    ("galeri_jelajah_kota", "Galeri jelajah kota", "Kota dalam Bingkai", "Arsip foto jalan, bangunan, dan kehidupan kota dari sudut pandang warga.", "#2563eb", "#f8fafc", "#172554", "kotakota", "Rute kecil, cerita besar, dan detail kota yang sering terlewat.", "Semua\nJalan\nArsitektur\nOrang", "travel", 10),
    ("galeri_kopi_nusantara", "Galeri kopi Nusantara", "Ruang Seduh", "Galeri biji kopi, kebun, dan suasana kedai untuk pencinta kopi.", "#92400e", "#fffbeb", "#422006", "kopi", "Dari kebun ke cangkir—cerita kopi pilihan dari berbagai daerah.", "Semua\nBiji kopi\nSeduhan\nKedai", "shop", 18),
    ("galeri_hidangan_rumah", "Galeri hidangan rumahan", "Meja Makan", "Kumpulan resep visual dan hidangan rumahan yang mudah dibuat.", "#ea580c", "#fff7ed", "#431407", "hidangan", "Menu rumahan penuh warna, disajikan dengan bahan yang mudah ditemukan.", "Semua\nSarapan\nMakan siang\nCamilan", "shop", 16),
    ("galeri_busana_kain", "Galeri busana dan kain", "Benang Cerita", "Lookbook kain lokal, siluet modern, dan detail jahitan pilihan.", "#be185d", "#fff7fb", "#500724", "busana", "Ragam tekstur dan warna yang berangkat dari warisan kain Nusantara.", "Semua\nTenun\nBatik\nKontemporer", "editorial", 22),
    ("galeri_mobil_klasik", "Galeri mobil klasik", "Garasi Klasik", "Arsip mobil klasik lengkap dengan tahun produksi dan catatan kolektor.", "#b91c1c", "#fffafa", "#450a0a", "mobilklasik", "Mesin lama, garis abadi, dan kisah pemilik di balik setiap kendaraan.", "Semua\nSedan\nSport\nUtilitas", "feature", 8),
    ("galeri_penginapan", "Galeri penginapan", "Singgah Sejenak", "Galeri penginapan unik, kamar pilihan, dan pengalaman menginap.", "#0f766e", "#f0fdfa", "#134e4a", "penginapan", "Temukan tempat beristirahat yang membuat perjalanan terasa istimewa.", "Semua\nKabut\nPantai\nKota", "travel", 18),
    ("galeri_satwa_liar", "Galeri satwa liar", "Jejak Satwa", "Potret satwa liar dan habitatnya, dilengkapi cerita konservasi.", "#166534", "#f0fdf4", "#14532d", "satwa", "Mengenal penghuni hutan tanpa mengganggu ruang hidup mereka.", "Semua\nMamalia\nBurung\nReptil", "feature", 24),
    ("galeri_bayi_keluarga", "Galeri potret keluarga", "Hari Kecil", "Koleksi potret keluarga dan momen keseharian dalam gaya hangat.", "#c2410c", "#fff7ed", "#431407", "keluarga", "Potongan hari biasa yang kelak menjadi cerita paling berharga.", "Semua\nKeluarga\nAnak\nPerayaan", "story", 24),
    ("galeri_jalur_pendakian", "Galeri jalur pendakian", "Peta Langkah", "Dokumentasi jalur pendakian, panorama puncak, dan persiapan perjalanan.", "#047857", "#ecfdf5", "#064e3b", "pendakian", "Panduan visual untuk melangkah lebih jauh dengan persiapan matang.", "Semua\nJalur\nPuncak\nPerkemahan", "travel", 14),
    ("galeri_keramik_studio", "Galeri keramik studio", "Tanah Tangan", "Etalase keramik buatan tangan dengan detail glasir dan proses studio.", "#a16207", "#fefce8", "#422006", "keramik", "Objek sehari-hari dibentuk perlahan dari tanah dan api.", "Semua\nMangkuk\nVas\nEksperimen", "shop", 20),
    ("galeri_sampul_buku", "Galeri sampul buku", "Rak Pilihan", "Pameran sampul buku, rekomendasi bacaan, dan catatan pembaca.", "#7c2d12", "#fffaf0", "#3f1d0b", "bukubaca", "Sampul yang menarik perhatian, cerita yang tinggal lebih lama.", "Semua\nFiksi\nEsai\nAnak", "editorial", 12),
    ("galeri_film_independen", "Galeri film independen", "Layar Alternatif", "Koleksi poster dan cuplikan film independen dari sineas lokal.", "#6d28d9", "#faf5ff", "#2e1065", "film", "Cerita yang tumbuh dari ide kecil dan dibuat dengan keberanian besar.", "Semua\nDrama\nDokumenter\nAnimasi", "story", 16),
    ("galeri_skincare_alami", "Galeri perawatan alami", "Ritual Pagi", "Lookbook produk perawatan harian dengan bahan dan cara pakai.", "#0f766e", "#f0fdfa", "#134e4a", "skincare", "Rutinitas sederhana dengan bahan yang terasa dekat dan menenangkan.", "Semua\nPembersih\nSerum\nPelembap", "shop", 16),
    ("galeri_menu_berbasis_tanaman", "Galeri menu berbasis tanaman", "Dapur Hijau", "Galeri hidangan nabati dengan bahan musiman dan resep praktis.", "#16a34a", "#f0fdf4", "#14532d", "nabati", "Makanan berbasis tanaman, kaya rasa, dan mudah dibuat di rumah.", "Semua\nSayur\nProtein\nPencuci mulut", "shop", 18),
    ("galeri_kebun_kota", "Galeri kebun kota", "Tumbuh di Kota", "Cerita kebun komunitas, panen rumahan, dan praktik berkebun di lahan kecil.", "#65a30d", "#f7fee7", "#365314", "kebunkota", "Ruang hijau bisa tumbuh di halaman sempit, balkon, bahkan jendela.", "Semua\nKebun\nPanen\nPanduan", "feature", 20),
    ("galeri_olahraga_lokal", "Galeri olahraga lokal", "Gerak Bersama", "Foto pertandingan komunitas, atlet muda, dan kegiatan olahraga warga.", "#ea580c", "#fff7ed", "#431407", "olahraga", "Momen terbaik olahraga lokal datang dari kerja sama dan semangat.", "Semua\nSepak bola\nLari\nBulu tangkis", "travel", 12),
    ("galeri_sepeda_kustom", "Galeri sepeda kustom", "Roda Bebas", "Koleksi sepeda kustom, komponen, dan rute favorit para pesepeda.", "#0284c7", "#f0f9ff", "#0c4a6e", "sepeda", "Dibangun sesuai kebutuhan, dirawat dengan telaten, dipakai menjelajah.", "Semua\nRoad\nGravel\nKota", "feature", 14),
    ("galeri_fotografi_jalanan", "Galeri fotografi jalanan", "Sudut Jalan", "Esai foto tentang aktivitas sehari-hari dan kehidupan di ruang publik.", "#334155", "#f8fafc", "#0f172a", "street", "Berhenti sejenak untuk melihat cerita yang lewat di hadapan kita.", "Semua\nPagi\nPasar\nMalam", "story", 8),
    ("galeri_langit_malam", "Galeri langit malam", "Ruang Bintang", "Pameran astrofotografi, fase bulan, dan fenomena langit malam.", "#6366f1", "#0b1020", "#e0e7ff", "langit", "Langit malam menyimpan peta yang terus berubah dari waktu ke waktu.", "Semua\nBulan\nBintang\nBima Sakti", "feature", 24),
    ("galeri_furnitur_kayu", "Galeri furnitur kayu", "Serat & Bentuk", "Etalase furnitur buatan pengrajin dengan informasi kayu dan ukuran.", "#a16207", "#faf7f2", "#292524", "furnitur", "Desain sederhana yang menghargai material, fungsi, dan pengerjaan.", "Semua\nKursi\nMeja\nPenyimpanan", "shop", 18),
    ("galeri_museum_kecil", "Galeri museum kecil", "Ruang Temu", "Pameran artefak, arsip, dan karya lokal dengan narasi kuratorial singkat.", "#78350f", "#fffbeb", "#451a03", "museum", "Objek pilihan yang membuka percakapan tentang tempat dan ingatan.", "Semua\nArtefak\nArsip\nKoleksi baru", "editorial", 10),
    ("galeri_ilustrasi_komik", "Galeri ilustrasi dan komik", "Panel Cerita", "Karya ilustrasi editorial, komik pendek, dan sketsa proses kreatif.", "#db2777", "#fdf2f8", "#500724", "ilustrasi", "Satu panel bisa mengundang senyum, satu halaman bisa mengubah sudut pandang.", "Semua\nKomik\nSketsa\nEditorial", "feature", 20),
    ("galeri_desain_produk", "Galeri desain produk", "Benda Berguna", "Portofolio desain produk dengan fokus pada bentuk, bahan, dan fungsi.", "#0f766e", "#f8fafc", "#134e4a", "produkdesain", "Benda sehari-hari yang dipikirkan ulang agar lebih baik digunakan.", "Semua\nRumah\nTeknologi\nAksesori", "editorial", 12),
    ("galeri_pastry_kafe", "Galeri pastry dan kafe", "Pagi Manis", "Menu pastry dan suasana kafe dengan jam buka dan pilihan unggulan.", "#c2410c", "#fff7ed", "#431407", "pastry", "Panggang segar setiap pagi, dinikmati paling nikmat bersama kopi.", "Semua\nRoti\nPastry\nMinuman", "shop", 20),
    ("galeri_gaya_hidup_luar_ruang", "Galeri luar ruang", "Akhir Pekan", "Inspirasi perjalanan singkat, perlengkapan, dan kegiatan luar ruang.", "#15803d", "#f0fdf4", "#14532d", "outdoor", "Ide perjalanan dekat untuk mengisi akhir pekan dengan udara segar.", "Semua\nBerkemah\nPantai\nJalur pendek", "travel", 16),
    ("galeri_motif_tekstil", "Galeri motif tekstil", "Pola Berulang", "Arsip motif tekstil, palet warna, dan kisah perajin dari berbagai daerah.", "#9333ea", "#faf5ff", "#3b0764", "tekstil", "Motif membawa jejak tangan, alam, dan kebudayaan dari generasi ke generasi.", "Semua\nGeometris\nFlora\nTradisional", "editorial", 22),
    ("galeri_arsip_kendaraan", "Galeri arsip kendaraan", "Roda & Waktu", "Arsip kendaraan bersejarah dengan tahun, spesifikasi, dan catatan restorasi.", "#475569", "#f8fafc", "#0f172a", "arsipkendaraan", "Lini masa perkembangan kendaraan dan teknologi yang mengubah perjalanan.", "Semua\nDarat\nLaut\nUdara", "feature", 8),
    ("galeri_kuliner_pasar", "Galeri kuliner pasar", "Rasa Pasar", "Jelajah foto jajanan pasar, bahan lokal, dan kisah pedagang.", "#b45309", "#fffbeb", "#451a03", "kulinerpasar", "Rasa yang akrab, resep yang bertahan, dan cerita dari setiap lapak.", "Semua\nJajanan\nSarapan\nMinuman", "story", 18),
]


def _build_gallery(entry):
    key, name, title, desc, primary, bg, ink, seed, intro, filters, layout, radius = entry
    seeds = [f"{seed}-{i}" for i in range(1, 10)]
    elements = [
        _bar("appbar", title=title, subtitle="Koleksi kurasi · diperbarui 2026", back="Beranda",
             action="Bagikan", icon="share"),
        _heading(name, 32),
        _text(intro),
        _bar("filterbar", items=filters, active=1),
    ]
    if layout == "feature":
        elements += [
            _image(f"{seed}-hero", intro, radius),
            _bar("statsbar", items="24|Karya terpilih\n8|Kontributor\n2026|Edisi"),
            _gallery(seeds[:6], 3, radius),
            _bar("quotebar", text="Setiap karya membuka cara baru untuk melihat hal yang dekat.",
                 author="Tim Kurator", role=title),
            _gallery(seeds[6:], 3, radius),
        ]
    elif layout == "editorial":
        elements += [
            _bar("breadcrumb", items=f"Beranda\nKoleksi\n{name}"),
            _gallery(seeds[:4], 2, radius),
            _bar("quotebar", text="Koleksi pilihan kami tumbuh dari detail, proses, dan cerita pembuatnya.",
                 author="Catatan kurator", role=title),
            _heading("Pilihan editor", 24),
            _gallery(seeds[4:], 3, radius),
            _bar("linkbar", items="Lihat arsip|#\nCerita koleksi|#\nHubungi kurator|#", align="left"),
        ]
    elif layout == "shop":
        elements += [
            _bar("searchbar", placeholder=f"Cari di {title.lower()}", button="Cari"),
            _bar("categorybar", items="Unggulan|auto_awesome\nTerbaru|new_releases\nFavorit|favorite\nSemua|apps"),
            _gallery(seeds[:6], 3, radius),
            _bar("productbar", image=_pic(seeds[6], 240, 240), name=f"Pilihan {title}",
                 note="Pilihan kurator · stok terbatas", price="Mulai Rp 89.000", old_price="", button="Lihat"),
            _bar("couponbar", code="KOLEKSI10", note="Potongan khusus untuk koleksi pilihan", expires="Berlaku bulan ini",
                 button="Pakai"),
            _gallery(seeds[7:], 2, radius),
        ]
    elif layout == "travel":
        elements += [
            _image(f"{seed}-cover", f"Sampul {name}", radius),
            _bar("locationbar", label="Lokasi pilihan", place="Indonesia · beragam kota", accuracy="Dikurasi komunitas",
                 button="Jelajahi", thumb=""),
            _bar("filterbar", items="Semua\nTerdekat\nFavorit\nTerbaru", active=1),
            _gallery(seeds[:6], 3, radius),
            _bar("routebar", start="Mulai dari sini", end="Lihat koleksi lengkap", duration="9 pilihan", distance="", button="Buka"),
            _gallery(seeds[6:], 3, radius),
        ]
    else:  # story
        elements += [
            _image(f"{seed}-story", f"Sampul cerita {name}", radius),
            _bar("articlebar", category="Cerita pilihan", title=intro,
                 meta="6 menit baca · 2026", button="Baca"),
            _gallery(seeds[:4], 2, radius),
            _bar("authorbar", name="Redaksi Koleksi", role=f"Cerita di balik {title}", avatar="",
                 posts="12 catatan", button="Ikuti"),
            _gallery(seeds[4:], 3, radius),
            _bar("sharebar", label="Bagikan cerita", items="Salin tautan|link\nWhatsApp|chat\nEmail|mail"),
        ]
    elements.extend([
        _bar("pagination", pages=8, current=2),
        _bar("newsletterbar", title="Dapatkan koleksi terbaru", placeholder="email@contoh.com",
             button="Ikuti", note="Satu kabar pilihan setiap bulan."),
        _bar("socialbar", items="Instagram|#|photo_camera\nPinterest|#|push_pin\nKontak|mailto:halo@example.com|mail"),
        _element("footer", text=f"© 2026 {title} · Dibuat dengan rasa ingin tahu."),
    ])
    return {
        "name": name,
        "category": "Galeri",
        "desc": desc,
        "title": title,
        "theme": theme_of(primary, bg, ink, "Sans-serif modern", 880),
        "pages": [{"name": "Koleksi", "elements": elements}],
    }


GALLERY_TEMPLATES = {entry[0]: _build_gallery(entry) for entry in _GALLERIES}
