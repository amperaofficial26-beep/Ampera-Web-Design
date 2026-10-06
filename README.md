# UI Builder (versi modular)

Jalankan: `streamlit run app.py` (semua modul Python berada dalam satu folder).

## Peta modul

| File | Isi | Ubah kalau mau... |
|---|---|---|
| `app.py` | Tata letak halaman Streamlit, panel editor, katalog, dan pencarian | mengubah susunan panel/tab/tombol |
| `config.py` | Label, nilai bawaan elemen, font, perangkat, dan grup | menambah elemen dasar, font, atau ukuran perangkat |
| `bar_specs.py` | Gabungan spesifikasi **170 komponen bar** | melihat katalog gabungan |
| `bar_specs_pro.py` | Spesifikasi **50 komponen Pro** | mengubah komponen paket Pro |
| `bar_specs_addons.py` | Spesifikasi **50 komponen tambahan terbaru** | menambah/mengubah field komponen tambahan |
| `bars.py` | Dispatcher renderer, deskripsi prompt, dan editor field | mengubah alur render/editor komponen |
| `bars_extra.py` | Renderer untuk **50 komponen tambahan** | mengubah render paket komponen tambahan lama |
| `bars_pro.py` | Renderer **50 komponen Pro** | mengubah render komponen Pro |
| `bars_addons.py` | Renderer **50 komponen tambahan terbaru** | mengubah tampilan HTML komponen terbaru |
| `css.py` | CSS gabungan untuk preview/hasil dan editor Streamlit | mengubah tema tampilan |
| `css_pro.py` | CSS untuk 50 komponen Pro | mengubah gaya paket Pro |
| `css_addons.py` | CSS untuk 50 komponen tambahan terbaru | mengubah gaya komponen terbaru |
| `templates.py` | **84 template** dan fungsi pembantu `H`, `P`, `B`, `BAR`, dst. | menambah template siap pakai |
| `gallery_templates.py` | **30 template galeri tambahan** (total 50 template kategori Galeri) | menambah koleksi khusus galeri |
| `design_refs.py` | Gabungan **56 referensi gaya desain** | mengubah katalog gaya yang bisa diterapkan |
| `design_refs_extra.py` | **30 referensi gaya tambahan** | menambah palet dan bentuk baru |
| `design.py` | Struktur desain, desain bawaan, dan validasi | mengubah format desain |
| `styles.py` | Gaya visual per elemen (garis, bayangan, padding, dll.) | mengubah penerapan gaya elemen |
| `projects.py` | Simpan/muat proyek, autosave, dan state sesi | mengubah penyimpanan proyek |
| `actions.py` | Callback untuk elemen, halaman, template, dan gaya | mengubah perilaku tombol |
| `html_builder.py` | Renderer desain menjadi HTML preview/ekspor | mengubah hasil HTML |
| `prompt_builder.py` | Generator Prompt Master AI | mengubah format prompt |
| `dnd_components.py` | Susunan seret-lepas, preview, dan penangan event | mengubah komponen interaktif |
| `properties.py` | Panel properti dan editor gaya | mengubah editor elemen |

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

## Template dan referensi gaya

- **84 template** total, termasuk **50 template kategori Galeri** (20 yang sudah ada + 30 tambahan).
- **56 referensi gaya** yang dapat langsung diterapkan (26 yang sudah ada + 30 tambahan).
- Setiap preset gaya mengatur palet warna, font, lebar konten, radius, garis, permukaan, dan bayangan.
- Template dan gaya bisa dicari; galeri katalog dibatasi area scroll agar panel kanan tetap ringkas.
- Panel halaman dan panel editor dibuat lebih lapang, dengan hierarki dan ringkasan yang lebih jelas.

## Menambah komponen

Spesifikasi komponen bar menyediakan label, grup, nilai bawaan, dan field yang langsung dipakai panel Properti serta Prompt Master AI. Untuk paket tambahan terbaru, tambahkan entri di `bar_specs_addons.py`, renderer di `bars_addons.py`, lalu gaya CSS di `css_addons.py`.

Komponen bar baru otomatis masuk ke pustaka, dapat dicari dan difilter berdasarkan grup, serta dapat dipakai pada template atau desain sendiri.
