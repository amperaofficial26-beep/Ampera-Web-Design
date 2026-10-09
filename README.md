# UI Builder (versi modular)

Aplikasi Streamlit untuk menyusun halaman dengan seret-lepas, dilengkapi preview langsung, ekspor HTML, dan teks **Prompt Master AI**.

Jalankan dari root repo:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Struktur folder

```
Ampera-Web-Design/
├── app.py                        # titik masuk aplikasi (hanya tata letak halaman)
├── README.md                     # dokumen ini
├── requirements.txt
├── docs/
│   └── FEATURES_PLAN.md          # rencana fitur dan catatan status
├── .streamlit/config.toml        # tema dasar widget Streamlit
├── .devcontainer/                # pengaturan Dev Container / Codespaces
└── ui_builder/                   # seluruh kode aplikasi, dikelompokkan per fitur
    ├── core/                     # fondasi tanpa tampilan
    │   ├── config.py             # label, nilai bawaan, font, perangkat, grup, folder proyek
    │   ├── design.py             # struktur desain bawaan dan validasi
    │   ├── element_style.py      # gaya visual per elemen (garis, bayangan, padding)
    │   └── utils.py              # fungsi bantu (escape HTML, URL aman, warna)
    ├── editor/                   # layar editor Streamlit
    │   ├── actions.py            # callback tombol: elemen, halaman, template, gaya
    │   ├── dnd_components.py     # Susunan seret-lepas dan preview interaktif
    │   ├── projects.py           # simpan/muat proyek, autosave, state sesi
    │   └── properties.py         # panel Properti
    ├── components/               # katalog 182 komponen
    │   ├── specs/                # data: label, grup, nilai bawaan, field
    │   ├── render/               # HTML tiap komponen bar
    │   └── css/                  # gaya CSS tiap komponen bar
    ├── templates/                # 84 template desain siap pakai
    │   ├── catalog.py            # katalog utama (54) + penggabungan galeri
    │   └── gallery.py            # 30 template galeri tambahan
    ├── themes/                   # tema dan gaya
    │   ├── css.py                # penyusun CSS gabungan (preview, ekspor, editor)
    │   ├── glass.py              # lapisan glassmorphism
    │   ├── style_refs.py         # daftar 56 referensi gaya
    │   └── style_refs_extra.py   # 30 referensi gaya tambahan
    └── export/                   # hasil akhir
        ├── html_builder.py       # HTML untuk preview dan unduhan
        └── prompt_builder.py     # teks Prompt Master AI
```

Aturan singkat:

- **Root hanya berisi titik masuk, dokumentasi, dan konfigurasi.** Semua kode aplikasi ada di `ui_builder/`.
- **Satu folder = satu fitur.** Folderlah yang memberi konteks, jadi nama berkas tidak perlu awalan seperti `bars_` atau `css_`.
- **Folder `projects/`** dibuat otomatis saat aplikasi berjalan (di root, diabaikan Git). Lokasinya diatur di `ui_builder/core/config.py`.

## Peta fitur

| Fitur | Lokasi | Ubah kalau mau... |
|---|---|---|
| Layar utama: bagian judul, panel Halaman, tab Preview / Kode HTML / Prompt AI, panel kanan, pustaka | `app.py` | mengubah susunan panel, tab, dan tombol |
| Susunan elemen dan preview interaktif | `ui_builder/editor/dnd_components.py` | mengubah seret-lepas atau klik di preview |
| Panel Properti (isi, gaya, naik/turun, gandakan, hapus) | `ui_builder/editor/properties.py` | mengubah field setiap elemen |
| Aksi tombol: tambah, hapus, gandakan, halaman, template, gaya | `ui_builder/editor/actions.py` | mengubah perilaku tombol |
| Proyek: simpan, muat, autosave, daftar proyek | `ui_builder/editor/projects.py` | mengubah penyimpanan proyek |
| Katalog 182 komponen | `ui_builder/components/` | menambah atau mengubah komponen |
| Template desain (84) | `ui_builder/templates/` | menambah template siap pakai |
| Referensi gaya (56) | `ui_builder/themes/style_refs*.py` | menambah palet dan bentuk gaya |
| Tema dan efek kaca | `ui_builder/themes/glass.py`, `css.py` | mengubah blur, warna kaca, bayangan |
| HTML preview dan ekspor | `ui_builder/export/html_builder.py` | mengubah hasil HTML |
| Prompt Master AI | `ui_builder/export/prompt_builder.py` | mengubah format prompt |
| Konfigurasi: label, font, perangkat, grup | `ui_builder/core/config.py` | menambah font atau ukuran perangkat |
| Struktur desain dan validasi | `ui_builder/core/design.py` | mengubah format desain |
| Gaya visual per elemen | `ui_builder/core/element_style.py` | mengubah penerapan gaya elemen |
| Tema dasar widget Streamlit | `.streamlit/config.toml` | mengubah warna dasar widget |

## Katalog komponen

Ada **170 komponen bar** dan **12 elemen dasar**, total **182 komponen**. Penambahan terbaru tidak mengganti komponen lama.

| Grup | Jumlah | Contoh |
|---|---:|---|
| Navigasi | 23 | navigasi bawah, tab kategori berikon, menu akun, langkah, daftar tautan |
| Aksi | 21 | toolbar pilihan, pencarian perintah, bagikan tautan, urungkan perubahan |
| Informasi | 21 | peringatan, kartu acara, status koneksi, pengingat, catatan rilis |
| Data | 23 | KPI, aktivitas, progres tujuan, perbandingan kanal |
| Formulir | 17 | alamat, checklist, antrean unggahan, preferensi persetujuan |
| Media | 15 | album, kontrol audio, antrean putar, foto dengan kredit, status rekaman |
| Sosial | 13 | jajak pendapat, komunitas, kutipan anggota, profil kreator |
| Toko | 14 | item keranjang, estimasi pengiriman, varian, diskon, status retur |
| Keuangan | 10 | dompet, rincian pengeluaran, arus kas, siklus tagihan, target tabungan |
| Konten | 10 | daftar isi, pengantar cerita, profil penulis, mode membaca, kutipan sumber |
| Peta & Lokasi | 4 | lokasi, rute, tempat terdekat, absensi |
| Dasar | 11 | judul, paragraf, tombol, gambar, galeri, kartu, formulir, footer |

### Empat paket komponen bar

Setiap paket punya tiga berkas dengan nama yang sama di folder `specs/`, `render/`, dan `css/`:

| Paket | Jumlah | Spesifikasi | Renderer HTML | CSS |
|---|---:|---|---|---|
| Inti | 20 | `specs/core.py` | `render/core.py` (juga dispatcher) | `css/core.py` |
| Tambahan lama | 50 | `specs/extra.py` | `render/extra.py` | `css/extra.py` |
| Pro | 50 | `specs/pro.py` | `render/pro.py` | `css/pro.py` |
| Tambahan terbaru | 50 | `specs/addons.py` | `render/addons.py` | `css/addons.py` |

`specs/__init__.py` menggabungkan keempat paket menjadi satu `BAR_SPECS` berisi 170 entri. Dari sana, panel Properti, preview, dan Prompt Master AI membaca data yang sama.

## Template dan referensi gaya

- **84 template** total, termasuk **50 template kategori Galeri** (20 yang sudah ada + 30 tambahan).
- **56 referensi gaya** yang dapat langsung diterapkan (26 yang sudah ada + 30 tambahan).
- Setiap preset gaya mengatur palet warna, font, lebar konten, radius, garis, permukaan, dan bayangan.
- Template dan gaya bisa dicari; galeri katalog dibatasi area scroll agar panel kanan tetap ringkas.
- Panel halaman dan panel editor dibuat lebih lapang, dengan hierarki dan ringkasan yang lebih jelas.

## Tampilan glassmorphism

Seluruh editor dan halaman hasil memakai bahasa desain kaca (*glassmorphism*):

- **Editor Streamlit**: latar aurora berwarna dengan panel, kartu, tombol, tab, kolom isian, dan dropdown berbahan kaca (`backdrop-filter`, garis tepi putih tipis, kilau tepi, bayangan lembut). Semua warna kaca diatur lewat token `--g-*` di `ui_builder/themes/glass.py`, dan warna dasar widget diselaraskan melalui `.streamlit/config.toml`.
- **Halaman hasil (preview & ekspor)**: aktifkan di **Tema → Efek kaca** atau dengan menerapkan preset **Glassmorphism** / **Kaca samudra**. Lapisan kaca menambahkan latar gradien berwarna, bulatan cahaya blur yang bergerak halus, serta efek buram pada kartu, menu navigasi, tombol, dan kolom isian. Kekuatan blur diatur `theme["glass_blur"]` (4–40 px) dan dikirim ke HTML sebagai variabel `--glass-blur`.
- Kompatibilitas dijaga: `@supports not (backdrop-filter)` menyediakan permukaan lebih pekat, animasi dinonaktifkan saat perangkat memakai `prefers-reduced-motion`, dan desain tanpa `glass: True` tetap tampil persis seperti sebelumnya.
- Prompt Master AI ikut menyebutkan efek kaca beserta nilai blur-nya saat fitur ini aktif.

## Menambah komponen

### Komponen bar baru (paket tambahan terbaru)

1. **Spesifikasi**: tambahkan entri di `ui_builder/components/specs/addons.py` (label, ikon, grup, nilai bawaan, field, dan `renderer` yang menentukan jenis tampilan). Panel Properti dan Prompt Master AI langsung memakai data ini.
2. **Renderer**: pilih jenis tampilan yang sudah ada di `render_catalog_bar()` (`ui_builder/components/render/addons.py`), atau tambahkan cabang baru di fungsi itu.
3. **CSS**: tambahkan gaya di `ui_builder/components/css/addons.py`. Semua selector dibatasi pada `.addonbar`.

Komponen bar baru otomatis masuk ke pustaka, dapat dicari dan difilter berdasarkan grup, serta dapat dipakai pada template atau desain sendiri.

### Paket lain

Paket Pro dan tambahan lama mengikuti pola yang sama: spesifikasi di `specs/pro.py` atau `specs/extra.py`, fungsi render didaftarkan di `PRO_BAR_RENDERERS` (`render/pro.py`) atau `EXTRA_BAR_RENDERERS` (`render/extra.py`), dan CSS di `css/pro.py` atau `css/extra.py`. Grup baru untuk paket Pro didaftarkan di `PRO_GROUP_ORDER`.

### Elemen dasar

Elemen dasar (judul, teks, tombol, dan seterusnya) berjumlah 12. Label, grup, dan nilai bawaannya ada di `ui_builder/core/config.py`, render HTML di `ui_builder/export/html_builder.py`, dan panel Properti di `ui_builder/editor/properties.py`.

### Template dan referensi gaya

- Template baru: tambahkan entri di `ui_builder/templates/catalog.py`, atau di `gallery.py` untuk koleksi galeri.
- Referensi gaya baru: tambahkan di `ui_builder/themes/style_refs_extra.py`.

## Perubahan struktur (dari versi sebelumnya)

Versi sebelumnya menaruh semua modul Python datar di root. Pemetaan berkas lama ke lokasi baru:

| Berkas lama | Lokasi baru |
|---|---|
| `app.py` | `app.py` (tetap di root) |
| `config.py` | `ui_builder/core/config.py` |
| `utils.py` | `ui_builder/core/utils.py` |
| `design.py` | `ui_builder/core/design.py` |
| `styles.py` | `ui_builder/core/element_style.py` |
| `actions.py` | `ui_builder/editor/actions.py` |
| `projects.py` | `ui_builder/editor/projects.py` |
| `properties.py` | `ui_builder/editor/properties.py` |
| `dnd_components.py` | `ui_builder/editor/dnd_components.py` |
| `bar_specs.py` | `ui_builder/components/specs/` (dipecah: `core.py`, `extra.py`, `common.py`; `__init__.py` menggabungkan) |
| `bar_specs_pro.py` | `ui_builder/components/specs/pro.py` |
| `bar_specs_addons.py` | `ui_builder/components/specs/addons.py` |
| `bars.py` | `ui_builder/components/render/core.py` |
| `bars_extra.py` | `ui_builder/components/render/extra.py` |
| `bars_pro.py` | `ui_builder/components/render/pro.py` |
| `bars_addons.py` | `ui_builder/components/render/addons.py` |
| `css.py` | `ui_builder/themes/css.py` (penyusun) dan `ui_builder/components/css/core.py`, `extra.py` |
| `css_pro.py` | `ui_builder/components/css/pro.py` |
| `css_addons.py` | `ui_builder/components/css/addons.py` |
| `css_glass.py` | `ui_builder/themes/glass.py` |
| `templates.py` | `ui_builder/templates/catalog.py` |
| `gallery_templates.py` | `ui_builder/templates/gallery.py` |
| `design_refs.py` | `ui_builder/themes/style_refs.py` |
| `design_refs_extra.py` | `ui_builder/themes/style_refs_extra.py` |
| `html_builder.py` | `ui_builder/export/html_builder.py` |
| `prompt_builder.py` | `ui_builder/export/prompt_builder.py` |
| `FEATURES_PLAN.md` | `docs/FEATURES_PLAN.md` |

Catatan:

- Logika tidak diubah. Yang berubah hanya lokasi berkas, impor (`from ui_builder....`), dan komentar. `bar_specs.py` dan `css.py` dipecah per paket tanpa mengubah isi datanya.
- Modul lama di root tidak lagi tersedia sebagai impor. Jika ada skrip lain yang mengimpornya, perbarui ke jalur baru.
- `.streamlit/config.toml`, `.devcontainer/`, dan perintah `streamlit run app.py` tidak berubah.
