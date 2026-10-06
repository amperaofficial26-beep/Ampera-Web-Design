# UI Builder (versi modular)

Jalankan: `streamlit run app.py`  (semua file harus berada di satu folder)

## Peta modul

| File | Isi | Ubah kalau mau... |
|---|---|---|
| `app.py` | Tata letak halaman Streamlit saja | mengubah susunan panel/tab/tombol |
| `config.py` | Konstanta: label, nilai bawaan elemen, font, perangkat, bayangan | menambah elemen dasar, font, ukuran perangkat |
| `bar_specs.py` | Data 20 komponen bar | menambah/mengubah field bar |
| `bars.py` | Render HTML bar, deskripsi prompt bar, editor field bar | menambah cabang render bar baru |
| `css.py` | `BAR_CSS` (hasil), `APP_CSS` (editor), tautan font ikon | mengubah tampilan |
| `styles.py` | Gaya visual per elemen (border, bayangan, padding, dll.) | mengubah cara gaya diterapkan |
| `utils.py` | Fungsi bantu: esc, safe_url, parse, on_color | fungsi umum |
| `design.py` | `default_design`, `valid_design`, `theme_of` | struktur/validasi desain |
| `projects.py` | Simpan/muat proyek (folder `projects/`), autosave, state sesi | penyimpanan proyek |
| `actions.py` | Semua callback (tambah/hapus/pindah elemen, halaman, template, gaya) | perilaku tombol |
| `templates.py` | 32 template + fungsi pembantu `H`, `P`, `B`, `BAR`, dst. | menambah template |
| `design_refs.py` | 6 referensi gaya (Minimalis, Glassmorphism, dst.) | menambah gaya |
| `html_builder.py` | `render_element`, `build_html` | HTML hasil/preview |
| `prompt_builder.py` | Generator Prompt Master AI | format prompt |
| `dnd_components.py` | Komponen seret-lepas, palet, preview, dan penangan event | JS/HTML komponen kustom |
| `properties.py` | Panel Properti dan editor gaya | field editor per elemen |

## Menambah komponen baru
- **Bar baru**: entri di `bar_specs.py` + cabang `if t == "..."` di `bars.render_bar`.
- **Elemen dasar baru**: `config.py` (label, default, ikon) + cabang di `html_builder.render_element`,
  `prompt_builder.describe_element`, dan `properties.edit_properties`.
