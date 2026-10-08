# Rencana Implementasi Fitur Baru

## 1. Auto-Navigate ke Halaman Baru
- Saat user klik tombol "Tambah" di panel kiri, buat halaman baru
- Langsung switch ke halaman baru tersebut
- User bisa langsung mulai design
- **File yang di-modify**: `actions.py`, `app.py`

## 2. Edit Destination/Link per Tombol
- Tambahkan field `link_target` di tombol (bisa referensi halaman atau URL)
- UI untuk memilih: internal page atau external URL
- Preview menunjukkan kemana link akan mengarah
- **File yang di-modify**: `properties.py`, `config.py`, `bars.py`

## 3. Edit Komponen (Component Properties)
- Selain edit warna/radius/garis, user bisa edit:
  - Text content (untuk heading, paragraph, button, card, dll)
  - Ikon (untuk tombol, bar navigation)
  - Placeholder (untuk input field)
  - Alignment (left, center, right, justify)
  - Font size
  - dan property spesifik per komponen
- **File yang di-modify**: `properties.py`, `config.py`

## 4. 30 Template Referensi Gaya
- 30 template style yang bisa dipilih sebagai referensi
- Setiap template memiliki:
  - Color palette (primary, bg, text)
  - Font choice
  - Border radius default
  - Line/stroke style
  - Shadow preset
- User bisa apply ke design mereka
- **File yang di-modify**: `templates.py` atau file baru `style_templates.py`

## Priority
1. Start dengan fitur #1 (auto-navigate) - paling urgent
2. Lanjut #2 (destination/link)
3. Lanjut #3 (component editing)
4. Terakhir #4 (30 template gaya)

## Status terbaru (8 Oktober 2026)

- **Tampilan glassmorphism**: CSS editor (`css_glass.py`) dan halaman hasil diperbarui.
  Editor memakai latar aurora dengan panel, kartu, tombol, tab, dan kolom isian berbahan kaca;
  halaman hasil mendapat lapisan kaca yang bisa dinyalakan dari tab **Tema → Efek kaca**
  (atau preset **Glassmorphism** / **Kaca samudra**) beserta pengatur kekuatan blur 4–40 px.
- **Berkas baru**: `css_glass.py` (lapisan kaca) dan `.streamlit/config.toml` (warna dasar widget).
- **Berkas yang diubah**: `css.py`, `design.py`, `design_refs.py`, `design_refs_extra.py`,
  `html_builder.py`, `prompt_builder.py`, `dnd_components.py`, `app.py`.
- Desain lama tetap aman: tanpa `glass: True`, HTML hasil identik seperti sebelumnya.

## Status sebelumnya (6 Oktober 2026)

- **#1 Navigasi halaman** dan **#2 tautan internal/eksternal**: sudah tersedia.
- **#3 Edit komponen**: selesai — seluruh field `BAR_SPECS` diedit otomatis di panel Properti.
- **#4 Referensi gaya**: 30 preset tambahan sudah ditambahkan; total kini **56 gaya** (26 yang sudah ada + 30 baru).
- **Galeri template**: 30 template galeri tambahan sudah ditambahkan; total **50 template Galeri** dan **84 template keseluruhan**.
- **Komponen**: 50 komponen tambahan baru sudah ditambahkan tanpa mengganti katalog lama; kini ada **170 komponen bar + 12 elemen dasar = 182 komponen**.
- **Kerapian editor**: panel kiri dan kanan diperluas, ringkasan halaman diperjelas, serta daftar template/gaya/komponen dibuat lebih mudah dicari dan dipindai.
- **Preview** tetap memakai bingkai 780 px; area kontainer editor maksimal 1920 px.
