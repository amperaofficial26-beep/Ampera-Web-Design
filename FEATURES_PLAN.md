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

## Status terbaru (Oktober 2026)

- **#3 Edit komponen**: selesai — panel Properti mengedit semua field `BAR_SPECS` (120 bar) otomatis.
- **#4 Template gaya**: selesai — `design_refs.py` kini berisi **26 referensi gaya** (6 lama + 20 baru).
- **Paket Pro**: 50 komponen bar baru di `bar_specs_pro.py` / `bars_pro.py` / `css_pro.py`
  (grup baru: Konten, Keuangan, Peta & Lokasi) — total 120 komponen bar.
- **Template**: 20 template galeri baru + “Galeri 50 komponen Pro” — total 54 template.
- **Preview tengah diperluas**: kolom tengah `[0.85, 4.05, 1.25]`, bingkai preview 780 px,
  lebar maksimum kontainer editor 1920 px.
