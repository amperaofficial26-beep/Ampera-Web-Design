import copy
import html
import json
import uuid

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="UI Builder", page_icon="🧩", layout="wide")

# ---------------------------------------------------------------------------
# Konfigurasi dasar
# ---------------------------------------------------------------------------
ELEMENT_LABELS = {
    "heading": "Judul",
    "text": "Paragraf",
    "button": "Tombol",
    "image": "Gambar",
    "input": "Kolom isian",
    "card": "Kartu",
    "divider": "Garis pemisah",
    "spacer": "Jarak kosong",
}

ELEMENT_DEFAULTS = {
    "heading": {"text": "Judul baru", "size": 36, "align": "left"},
    "text": {"text": "Tulis isi paragraf di sini.", "align": "left"},
    "button": {"text": "Klik di sini", "link": "", "align": "left"},
    "image": {
        "url": "https://picsum.photos/800/400",
        "alt": "Gambar",
        "radius": 12,
    },
    "input": {"label": "Nama", "placeholder": "Ketik di sini"},
    "card": {"title": "Judul kartu", "text": "Isi singkat kartu."},
    "divider": {},
    "spacer": {"height": 24},
}

FONTS = {
    "Sans-serif modern": "'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    "Serif klasik": "Georgia, 'Times New Roman', serif",
    "Monospace": "'Courier New', Consolas, monospace",
}

ALIGNS = ["left", "center", "right"]


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
def default_design():
    return {
        "title": "Aplikasi Saya",
        "theme": {
            "primary": "#4f46e5",
            "bg": "#ffffff",
            "text": "#1f2937",
            "font": "Sans-serif modern",
            "width": 720,
        },
        "pages": [{"name": "Beranda", "elements": []}],
    }


def init_state():
    if "design" not in st.session_state:
        st.session_state.design = default_design()
    if "page_idx" not in st.session_state:
        st.session_state.page_idx = 0


def current_page():
    pages = st.session_state.design["pages"]
    idx = min(st.session_state.page_idx, len(pages) - 1)
    return pages[idx]


# ---------------------------------------------------------------------------
# Callback (dijalankan sebelum rerun, jadi aman mengubah state)
# ---------------------------------------------------------------------------
def add_element(el_type):
    el = {"id": uuid.uuid4().hex[:8], "type": el_type}
    el.update(copy.deepcopy(ELEMENT_DEFAULTS[el_type]))
    current_page()["elements"].append(el)


def move_element(index, delta):
    els = current_page()["elements"]
    new = index + delta
    if 0 <= new < len(els):
        els[index], els[new] = els[new], els[index]


def delete_element(index):
    els = current_page()["elements"]
    if 0 <= index < len(els):
        els.pop(index)


def duplicate_element(index):
    els = current_page()["elements"]
    clone = copy.deepcopy(els[index])
    clone["id"] = uuid.uuid4().hex[:8]
    els.insert(index + 1, clone)


def add_page():
    pages = st.session_state.design["pages"]
    pages.append({"name": f"Halaman {len(pages) + 1}", "elements": []})
    st.session_state.page_idx = len(pages) - 1


def delete_page():
    pages = st.session_state.design["pages"]
    if len(pages) > 1:
        pages.pop(st.session_state.page_idx)
        st.session_state.page_idx = max(0, st.session_state.page_idx - 1)


def reset_design():
    st.session_state.design = default_design()
    st.session_state.page_idx = 0


def load_design(data):
    st.session_state.design = data
    st.session_state.page_idx = 0


def valid_design(data):
    try:
        assert isinstance(data["title"], str)
        assert isinstance(data["theme"], dict)
        assert isinstance(data["pages"], list) and data["pages"]
        for page in data["pages"]:
            assert isinstance(page["name"], str)
            for el in page["elements"]:
                assert el["type"] in ELEMENT_LABELS
                el.setdefault("id", uuid.uuid4().hex[:8])
        base = default_design()["theme"]
        for k, v in base.items():
            data["theme"].setdefault(k, v)
        return True
    except (KeyError, TypeError, AssertionError):
        return False


# ---------------------------------------------------------------------------
# Generator HTML
# ---------------------------------------------------------------------------
def esc(value):
    return html.escape(str(value), quote=True)


def safe_url(url):
    url = str(url).strip()
    if url.lower().startswith(("http://", "https://", "mailto:", "#", "data:image/")):
        return url
    return "#"


def num(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def align_of(el):
    return el.get("align", "left") if el.get("align") in ALIGNS else "left"


def render_element(el):
    t = el["type"]
    if t == "heading":
        return (
            f'<h1 style="font-size:{num(el.get("size"), 36)}px;'
            f'text-align:{align_of(el)}">{esc(el.get("text", ""))}</h1>'
        )
    if t == "text":
        return f'<p style="text-align:{align_of(el)}">{esc(el.get("text", ""))}</p>'
    if t == "button":
        label = esc(el.get("text", ""))
        link = (el.get("link") or "").strip()
        inner = (
            f'<a class="btn" href="{esc(safe_url(link))}">{label}</a>'
            if link
            else f'<button class="btn" type="button">{label}</button>'
        )
        return f'<div style="text-align:{align_of(el)}">{inner}</div>'
    if t == "image":
        return (
            f'<img src="{esc(safe_url(el.get("url", "")))}" alt="{esc(el.get("alt", ""))}" '
            f'style="border-radius:{num(el.get("radius"), 0)}px">'
        )
    if t == "input":
        return (
            f'<label class="field"><span>{esc(el.get("label", ""))}</span>'
            f'<input type="text" placeholder="{esc(el.get("placeholder", ""))}"></label>'
        )
    if t == "card":
        return (
            f'<div class="card"><h3>{esc(el.get("title", ""))}</h3>'
            f'<p>{esc(el.get("text", ""))}</p></div>'
        )
    if t == "divider":
        return "<hr>"
    if t == "spacer":
        return f'<div style="height:{num(el.get("height"), 24)}px"></div>'
    return ""


def build_html(design):
    theme = design["theme"]
    font = FONTS.get(theme.get("font"), FONTS["Sans-serif modern"])
    pages = design["pages"]
    multi = len(pages) > 1

    nav = ""
    if multi:
        links = "".join(
            f'<button type="button" class="nav-btn{" active" if i == 0 else ""}" '
            f'data-target="page-{i}">{esc(p["name"])}</button>'
            for i, p in enumerate(pages)
        )
        nav = f'<nav class="nav">{links}</nav>'

    sections = []
    for i, page in enumerate(pages):
        body = "\n".join(render_element(el) for el in page["elements"])
        if not body:
            body = '<p class="empty">Halaman ini masih kosong.</p>'
        hidden = "" if i == 0 else " hidden"
        sections.append(f'<section id="page-{i}" class="page"{hidden}>\n{body}\n</section>')

    script = ""
    if multi:
        script = """
<script>
  document.querySelectorAll('.nav-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.page').forEach(function (p) { p.hidden = true; });
      document.querySelectorAll('.nav-btn').forEach(function (b) { b.classList.remove('active'); });
      document.getElementById(btn.dataset.target).hidden = false;
      btn.classList.add('active');
    });
  });
</script>"""

    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(design["title"])}</title>
<style>
  :root {{
    --primary: {esc(theme["primary"])};
    --bg: {esc(theme["bg"])};
    --text: {esc(theme["text"])};
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: {font};
    line-height: 1.6;
  }}
  .app {{
    max-width: {num(theme["width"], 720)}px;
    margin: 0 auto;
    padding: 24px 20px 48px;
  }}
  .app-title {{ margin: 0 0 16px; font-size: 14px; opacity: .6; }}
  .nav {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px; }}
  .nav-btn {{
    border: 1px solid var(--primary);
    background: transparent;
    color: var(--primary);
    padding: 6px 14px;
    border-radius: 999px;
    cursor: pointer;
    font: inherit;
  }}
  .nav-btn.active {{ background: var(--primary); color: #fff; }}
  .page > * {{ margin-top: 0; margin-bottom: 16px; }}
  h1, h3 {{ line-height: 1.2; }}
  img {{ max-width: 100%; height: auto; display: block; }}
  hr {{ border: 0; border-top: 1px solid rgba(128,128,128,.35); }}
  .btn {{
    display: inline-block;
    background: var(--primary);
    color: #fff;
    border: 0;
    padding: 10px 20px;
    border-radius: 8px;
    font: inherit;
    text-decoration: none;
    cursor: pointer;
  }}
  .btn:focus-visible, .nav-btn:focus-visible, input:focus-visible {{
    outline: 3px solid var(--primary);
    outline-offset: 2px;
  }}
  .field {{ display: block; }}
  .field span {{ display: block; margin-bottom: 4px; font-size: 14px; }}
  .field input {{
    width: 100%;
    padding: 10px 12px;
    border: 1px solid rgba(128,128,128,.5);
    border-radius: 8px;
    font: inherit;
    background: transparent;
    color: inherit;
  }}
  .card {{
    border: 1px solid rgba(128,128,128,.35);
    border-radius: 12px;
    padding: 16px 18px;
  }}
  .card h3 {{ margin: 0 0 6px; }}
  .card p {{ margin: 0; }}
  .empty {{ opacity: .5; font-style: italic; }}
</style>
</head>
<body>
<main class="app">
<p class="app-title">{esc(design["title"])}</p>
{nav}
{chr(10).join(sections)}
</main>{script}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Generator Prompt Master AI
# ---------------------------------------------------------------------------
def describe_element(el, number):
    t = el["type"]
    label = ELEMENT_LABELS[t]
    if t == "heading":
        detail = f'teks "{el.get("text", "")}", ukuran {el.get("size")}px, rata {el.get("align")}'
    elif t == "text":
        detail = f'teks "{el.get("text", "")}", rata {el.get("align")}'
    elif t == "button":
        link = el.get("link") or "tanpa tautan"
        detail = f'label "{el.get("text", "")}", tautan: {link}, rata {el.get("align")}'
    elif t == "image":
        detail = (
            f'sumber {el.get("url")}, teks alternatif "{el.get("alt", "")}", '
            f'sudut membulat {el.get("radius")}px'
        )
    elif t == "input":
        detail = f'label "{el.get("label", "")}", placeholder "{el.get("placeholder", "")}"'
    elif t == "card":
        detail = f'judul "{el.get("title", "")}", isi "{el.get("text", "")}"'
    elif t == "divider":
        detail = "garis horizontal tipis"
    else:
        detail = f'tinggi {el.get("height")}px'
    return f"   {number}. {label}: {detail}"


def build_prompt(design, target="HTML/CSS/JavaScript satu file"):
    theme = design["theme"]
    lines = [
        f'Bangun aplikasi web bernama "{design["title"]}" menggunakan {target}.',
        "Ikuti spesifikasi desain di bawah ini secara persis, termasuk urutan elemen, teks, dan nilai propertinya.",
        "",
        "## Tema visual",
        f'- Warna utama (tombol, aksen): {theme["primary"]}',
        f'- Warna latar: {theme["bg"]}',
        f'- Warna teks: {theme["text"]}',
        f'- Font: {theme["font"]} ({FONTS.get(theme["font"], "")})',
        f'- Lebar maksimum konten: {theme["width"]}px, diletakkan di tengah',
        "",
        f"## Struktur halaman ({len(design['pages'])} halaman)",
    ]
    for i, page in enumerate(design["pages"], start=1):
        lines.append(f'{i}. Halaman "{page["name"]}"')
        if page["elements"]:
            lines.append("   Elemen dari atas ke bawah:")
            for n, el in enumerate(page["elements"], start=1):
                lines.append(describe_element(el, n))
        else:
            lines.append("   (halaman kosong)")
    lines += [
        "",
        "## Aturan tambahan",
    ]
    if len(design["pages"]) > 1:
        lines.append("- Sediakan navigasi antar halaman di bagian atas tanpa memuat ulang browser.")
    lines += [
        "- Tampilan harus responsif sampai ukuran layar ponsel.",
        "- Gunakan HTML semantik dan pastikan fokus keyboard terlihat jelas.",
        "- Jangan menambahkan elemen, teks, atau fitur di luar spesifikasi ini.",
        "- Berikan hasil akhir berupa kode lengkap yang bisa langsung dijalankan.",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Editor properti per elemen
# ---------------------------------------------------------------------------
def edit_element(el, index, total):
    key = el["id"]
    title = f"{index + 1}. {ELEMENT_LABELS[el['type']]}"
    with st.expander(title, expanded=False):
        t = el["type"]
        if t == "heading":
            el["text"] = st.text_input("Teks", el["text"], key=f"{key}_text")
            el["size"] = st.slider("Ukuran (px)", 16, 72, int(el["size"]), key=f"{key}_size")
            el["align"] = st.radio("Rata", ALIGNS, ALIGNS.index(align_of(el)), horizontal=True, key=f"{key}_align")
        elif t == "text":
            el["text"] = st.text_area("Teks", el["text"], key=f"{key}_text")
            el["align"] = st.radio("Rata", ALIGNS, ALIGNS.index(align_of(el)), horizontal=True, key=f"{key}_align")
        elif t == "button":
            el["text"] = st.text_input("Label", el["text"], key=f"{key}_text")
            el["link"] = st.text_input("Tautan (opsional)", el["link"], key=f"{key}_link")
            el["align"] = st.radio("Rata", ALIGNS, ALIGNS.index(align_of(el)), horizontal=True, key=f"{key}_align")
        elif t == "image":
            el["url"] = st.text_input("URL gambar", el["url"], key=f"{key}_url")
            el["alt"] = st.text_input("Teks alternatif", el["alt"], key=f"{key}_alt")
            el["radius"] = st.slider("Sudut membulat (px)", 0, 48, int(el["radius"]), key=f"{key}_radius")
        elif t == "input":
            el["label"] = st.text_input("Label", el["label"], key=f"{key}_label")
            el["placeholder"] = st.text_input("Placeholder", el["placeholder"], key=f"{key}_ph")
        elif t == "card":
            el["title"] = st.text_input("Judul", el["title"], key=f"{key}_title")
            el["text"] = st.text_area("Isi", el["text"], key=f"{key}_text")
        elif t == "spacer":
            el["height"] = st.slider("Tinggi (px)", 4, 200, int(el["height"]), key=f"{key}_h")
        else:
            st.caption("Elemen ini tidak punya pengaturan.")

        c1, c2, c3, c4 = st.columns(4)
        c1.button("⬆️", key=f"{key}_up", on_click=move_element, args=(index, -1),
                  disabled=index == 0, help="Naikkan", use_container_width=True)
        c2.button("⬇️", key=f"{key}_down", on_click=move_element, args=(index, 1),
                  disabled=index == total - 1, help="Turunkan", use_container_width=True)
        c3.button("📄", key=f"{key}_dup", on_click=duplicate_element, args=(index,),
                  help="Gandakan", use_container_width=True)
        c4.button("🗑️", key=f"{key}_del", on_click=delete_element, args=(index,),
                  help="Hapus", use_container_width=True)


# ---------------------------------------------------------------------------
# Tampilan
# ---------------------------------------------------------------------------
init_state()
design = st.session_state.design

with st.sidebar:
    st.header("🧩 UI Builder")

    design["title"] = st.text_input("Nama aplikasi", design["title"])

    st.subheader("Halaman")
    pages = design["pages"]
    st.selectbox(
        "Halaman aktif",
        options=list(range(len(pages))),
        format_func=lambda i: pages[i]["name"] if i < len(pages) else "",
        key="page_idx",
    )
    page = current_page()
    page["name"] = st.text_input("Nama halaman", page["name"], key=f"pname_{st.session_state.page_idx}")
    pc1, pc2 = st.columns(2)
    pc1.button("➕ Halaman", on_click=add_page, use_container_width=True)
    pc2.button("🗑️ Halaman", on_click=delete_page, disabled=len(pages) <= 1, use_container_width=True)

    st.subheader("Tema")
    theme = design["theme"]
    theme["primary"] = st.color_picker("Warna utama", theme["primary"])
    theme["bg"] = st.color_picker("Warna latar", theme["bg"])
    theme["text"] = st.color_picker("Warna teks", theme["text"])
    font_names = list(FONTS)
    theme["font"] = st.selectbox(
        "Font", font_names, font_names.index(theme["font"]) if theme["font"] in font_names else 0
    )
    theme["width"] = st.slider("Lebar konten (px)", 360, 1200, int(theme["width"]), step=20)

    st.subheader("Simpan / muat desain")
    st.download_button(
        "💾 Unduh desain (.json)",
        json.dumps(design, ensure_ascii=False, indent=2),
        file_name="desain.json",
        mime="application/json",
        use_container_width=True,
    )
    uploaded = st.file_uploader("Muat desain (.json)", type=["json"])
    if uploaded is not None and st.button("📂 Terapkan file", use_container_width=True):
        try:
            data = json.loads(uploaded.getvalue().decode("utf-8"))
            if valid_design(data):
                load_design(data)
                st.rerun()
            else:
                st.error("Struktur file tidak sesuai format desain.")
        except (json.JSONDecodeError, UnicodeDecodeError):
            st.error("File bukan JSON yang valid.")
    st.button("♻️ Reset desain", on_click=reset_design, use_container_width=True)

st.title("🧩 UI Builder")
st.caption("Susun desain, lihat preview langsung, lalu ekspor sebagai kode HTML atau prompt master AI.")

page = current_page()
col_edit, col_prev = st.columns([1, 1.3], gap="large")

with col_edit:
    st.subheader(f"Editor: {page['name']}")
    st.markdown("**Tambah elemen**")
    type_keys = list(ELEMENT_LABELS)
    grid = st.columns(4)
    for n, t in enumerate(type_keys):
        grid[n % 4].button(
            ELEMENT_LABELS[t],
            key=f"add_{t}",
            on_click=add_element,
            args=(t,),
            use_container_width=True,
        )

    st.markdown("**Susunan elemen**")
    if not page["elements"]:
        st.info("Belum ada elemen. Klik salah satu tombol di atas untuk memulai.")
    for i, el in enumerate(list(page["elements"])):
        edit_element(el, i, len(page["elements"]))

with col_prev:
    st.subheader("Preview langsung")
    preview_html = build_html(design)
    if hasattr(st, "iframe"):
        st.iframe(preview_html, height=680)
    else:  # Streamlit versi lama
        components.html(preview_html, height=680, scrolling=True)

st.divider()
st.subheader("Ekspor hasil desain")
mode = st.radio("Pilih jenis output", ["Kode HTML", "Prompt Master AI"], horizontal=True)

if mode == "Kode HTML":
    output = build_html(design)
    st.code(output, language="html", line_numbers=False)
    st.download_button("⬇️ Unduh index.html", output, file_name="index.html", mime="text/html")
else:
    target = st.selectbox(
        "Target pembuatan",
        [
            "HTML/CSS/JavaScript satu file",
            "React dengan Tailwind CSS",
            "Streamlit (Python)",
            "Flutter (Dart)",
        ],
    )
    output = build_prompt(design, target)
    st.code(output, language="markdown")
    st.download_button("⬇️ Unduh prompt_master.txt", output, file_name="prompt_master.txt", mime="text/plain")

st.caption("Tips: ikon salin ada di pojok kanan atas kotak kode.")
