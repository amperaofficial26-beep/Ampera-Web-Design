# UI Builder (versi modular)

Jalankan: `streamlit run app.py`  (semua file harus berada di satu folder)

## Peta modul

| File | Isi | Ubah kalau mau... |
|---|---|---|
| `app.py` | Tata letak halaman Streamlit saja | mengubah susunan panel/tab/tombol |
| `config.py` | Konstanta: label, nilai bawaan elemen, font, perangkat, bayangan | menambah elemen dasar, font, ukuran perangkat |
| `bar_specs.py` | Data **120 komponen bar** + grup (70 lama + 50 paket Pro) | menambah/mengubah field bar |
| `bar_specs_pro.py` | Spesifikasi **50 komponen paket Pro** + grup baru | menambah/mengubah field komponen Pro |
| `bars.py` | Render HTML bar inti (20), deskripsi prompt, editor field bar | menambah cabang render bar inti |
| `bars_extra.py` | Render HTML **50 komponen tambahan** (`EXTRA_BAR_RENDERERS`) | menambah/mengubah render komponen tambahan |
| `bars_pro.py` | Render HTML **50 komponen Pro** (`PRO_BAR_RENDERERS`) | menambah/mengubah render komponen Pro |
| `css.py` | `BAR_CSS` + `BAR_CSS_EXTRA` (hasil), `APP_CSS` (editor), tautan font ikon | mengubah tampilan |
| `css_pro.py` | `BAR_CSS_PRO` — CSS 50 komponen Pro | mengubah tampilan komponen Pro |
| `styles.py` | Gaya visual per elemen (border, bayangan, padding, dll.) | mengubah cara gaya diterapkan |
| `utils.py` | Fungsi bantu: esc, safe_url, mi (ikon), parse, on_color | fungsi umum |
| `design.py` | `default_design`, `valid_design`, `theme_of` | struktur/validasi desain |
| `projects.py` | Simpan/muat proyek (folder `projects/`), autosave, state sesi | penyimpanan proyek |
| `actions.py` | Semua callback (tambah/hapus/pindah elemen, halaman, template, gaya) | perilaku tombol |
| `templates.py` | 54 template (33 lama + 20 template galeri + “Galeri 50 komponen Pro”) + fungsi pembantu `H`, `P`, `B`, `BAR`, dst. | menambah template |
| `design_refs.py` | 26 referensi gaya (6 lama + 20 baru: Neumorphism, Material You, Gaya iOS, dst.) | menambah gaya |
| `html_builder.py` | `render_element`, `build_html` | HTML hasil/preview |
| `prompt_builder.py` | Generator Prompt Master AI | format prompt |
| `dnd_components.py` | Komponen seret-lepas, palet, preview, dan penangan event | JS/HTML komponen kustom |
| `properties.py` | Panel Properti dan editor gaya | field editor per elemen |

## Daftar komponen (120 bar + 12 elemen dasar)

| Grup | Jumlah | Contoh |
|---|---|---|
| Navigasi | 17 | navigasi bawah, tab bar, breadcrumb, menu samping, rail ikon, menu mega, header aplikasi, navigasi cepat, sub navigasi, titik langkah, navigasi geser |
| Aksi | 16 | toolbar, pencarian, filter, tombol melayang, bar bagikan, aksi cepat, aksi massal, bar ekspor, bar persetujuan, bar cetak |
| Informasi | 16 | pengumuman, bar status, progres, langkah, rating, hitung mundur, siaran langsung, bar cuaca, bar notifikasi, metrik ambang, bar pembaruan |
| Data | 18 | statistik, harga, kategori, tabel, perbandingan, grafik mini, lini masa, donat, pengukur, peringkat, peta panas, distribusi, corong |
| Formulir | 12 | bar formulir, buletin, kode OTP, input tag, penggeser, sakelar, unggah berkas, pemilih tanggal, masukan rating, jumlah, kekuatan sandi |
| Media | 10 | pemutar musik, cerita, strip gambar mini, takarir, perekam suara, bar video, equalizer, podcast, kamera, lirik |
| Sosial | 8 | reaksi, tumpukan pengguna, ulasan, obrolan, ikuti, komunitas, tren, penghargaan |
| Toko | 9 | keranjang, kupon, gratis ongkir, produk, pembayaran, daftar keinginan, pesanan, bundling, loyalitas |
| Konten | 5 | bar artikel, penulis, bab, progres baca, bacaan terkait |
| Keuangan | 5 | saldo, transaksi, anggaran, tagihan, target tabungan |
| Peta & Lokasi | 4 | lokasi, rute, tempat terdekat, absen |

Ditambah 12 elemen dasar (judul, paragraf, tombol, gambar, galeri, daftar, kolom isian, kartu, garis, jarak, footer, menu navigasi) = **132 komponen**.

## Template & referensi gaya

- **54 template** dalam kategori Acara, Aplikasi, Bisnis, Data, **Galeri** (20 template baru), Konten, Pendidikan,
  Pribadi, Referensi komponen, Sosial, Toko dan kuliner, Utilitas.
- **26 referensi gaya** siap terapkan (palet warna, font, lebar konten, sudut, garis, bayangan).
- Preview tengah dibuat paling lebar (`st.columns([0.85, 4.05, 1.25])`) dengan tinggi bingkai 780 px.

## Menambah komponen baru
- **Bar baru (cara 1, bar inti)**: entri di `bar_specs.py` + cabang `if t == "..."` di `bars.render_bar`.
- **Bar baru (cara 2, komponen tambahan)**: entri di `bar_specs.py` + fungsi `r_<tipe>` di `bars_extra.py`,
  lalu daftarkan di `EXTRA_BAR_RENDERERS`. CSS-nya tambahkan di `BAR_CSS_EXTRA` (`css.py`) dengan
  kelas induk sesuai tipe agar tidak bentrok. Grup baru harus didaftarkan di `GROUP_ORDER`.
- **Bar baru (cara 3, paket Pro)**: entry di `bar_specs_pro.PRO_BAR_SPECS` + fungsi render di `bars_pro.py`
  yang didaftarkan di `PRO_BAR_RENDERERS`, CSS di `css_pro.BAR_CSS_PRO`. `bar_specs.py` dan `bars.py`
  menggabungkannya otomatis, jadi tidak perlu mengubah file lama.
- **Elemen dasar baru**: `config.py` (label, default, ikon) + cabang di `html_builder.render_element`,
  `prompt_builder.describe_element`, dan `properties.edit_properties`.

Panel Properti, Prompt Master AI, dan referensi gaya membaca `BAR_SPECS` secara otomatis, jadi komponen
baru langsung dapat diedit, dideskripsikan, dan ikut terkena “Terapkan gaya”.
