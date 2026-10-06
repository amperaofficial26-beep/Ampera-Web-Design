# UI Builder (versi modular)

Jalankan: `streamlit run app.py`  (semua file harus berada di satu folder)

## Peta modul

| File | Isi | Ubah kalau mau... |
|---|---|---|
| `app.py` | Tata letak halaman Streamlit saja | mengubah susunan panel/tab/tombol |
| `config.py` | Konstanta: label, nilai bawaan elemen, font, perangkat, bayangan | menambah elemen dasar, font, ukuran perangkat |
| `bar_specs.py` | Data **70 komponen bar** + grup | menambah/mengubah field bar |
| `bars.py` | Render HTML bar inti (20), deskripsi prompt, editor field bar | menambah cabang render bar inti |
| `bars_extra.py` | Render HTML **50 komponen tambahan** (`EXTRA_BAR_RENDERERS`) | menambah/mengubah render komponen tambahan |
| `css.py` | `BAR_CSS` + `BAR_CSS_EXTRA` (hasil), `APP_CSS` (editor), tautan font ikon | mengubah tampilan |
| `styles.py` | Gaya visual per elemen (border, bayangan, padding, dll.) | mengubah cara gaya diterapkan |
| `utils.py` | Fungsi bantu: esc, safe_url, mi (ikon), parse, on_color | fungsi umum |
| `design.py` | `default_design`, `valid_design`, `theme_of` | struktur/validasi desain |
| `projects.py` | Simpan/muat proyek (folder `projects/`), autosave, state sesi | penyimpanan proyek |
| `actions.py` | Semua callback (tambah/hapus/pindah elemen, halaman, template, gaya) | perilaku tombol |
| `templates.py` | 33 template (termasuk “Galeri 50 komponen bar baru”) + fungsi pembantu `H`, `P`, `B`, `BAR`, dst. | menambah template |
| `design_refs.py` | 6 referensi gaya (Minimalis, Glassmorphism, dst.) | menambah gaya |
| `html_builder.py` | `render_element`, `build_html` | HTML hasil/preview |
| `prompt_builder.py` | Generator Prompt Master AI | format prompt |
| `dnd_components.py` | Komponen seret-lepas, palet, preview, dan penangan event | JS/HTML komponen kustom |
| `properties.py` | Panel Properti dan editor gaya | field editor per elemen |

## Daftar komponen (70 bar)

| Grup | Jumlah | Contoh |
|---|---|---|
| Navigasi | 12 | navigasi bawah, tab bar, breadcrumb, menu samping, bilah menu, rail ikon, menu mega |
| Aksi | 12 | toolbar, pencarian, filter, tombol melayang, bar bagikan, aksi cepat, bar komentar |
| Informasi | 12 | pengumuman, bar status, progres, langkah, rating, banner info, hitung mundur, siaran langsung |
| Data | 12 | statistik, harga, kategori, profil, tabel, perbandingan, grafik mini, lini masa, strip tanggal |
| Formulir | 7 | bar formulir, buletin, kode OTP, input tag, penggeser, sakelar, masuk cepat |
| Media | 5 | pemutar musik, cerita, strip gambar mini, takarir, perekam suara |
| Sosial | 5 | reaksi, tumpukan pengguna, ulasan, obrolan, ikuti |
| Toko | 5 | keranjang, kupon, gratis ongkir, produk, metode pembayaran |

Ditambah 12 elemen dasar (judul, paragraf, tombol, gambar, galeri, daftar, kolom isian, kartu, garis, jarak, footer, menu navigasi) = **82 komponen**.

## Menambah komponen baru
- **Bar baru (cara 1, bar inti)**: entri di `bar_specs.py` + cabang `if t == "..."` di `bars.render_bar`.
- **Bar baru (cara 2, komponen tambahan)**: entri di `bar_specs.py` + fungsi `r_<tipe>` di `bars_extra.py`,
  lalu daftarkan di `EXTRA_BAR_RENDERERS`. CSS-nya tambahkan di `BAR_CSS_EXTRA` (`css.py`) dengan
  kelas induk sesuai tipe agar tidak bentrok. Grup baru harus didaftarkan di `GROUP_ORDER`.
- **Elemen dasar baru**: `config.py` (label, default, ikon) + cabang di `html_builder.render_element`,
  `prompt_builder.describe_element`, dan `properties.edit_properties`.

Panel Properti, Prompt Master AI, dan referensi gaya membaca `BAR_SPECS` secara otomatis, jadi komponen
baru langsung dapat diedit, dideskripsikan, dan ikut terkena “Terapkan gaya”.
