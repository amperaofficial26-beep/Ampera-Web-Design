"""Generator Prompt Master AI: ubah desain menjadi spesifikasi teks untuk AI."""
from bars import describe_bar
from bar_specs import BAR_SPECS
from config import ELEMENT_LABELS, FONTS, INPUT_KINDS
from utils import input_kind, lines_of, parse_links


def describe_element(el, number):
    t = el["type"]
    label = ELEMENT_LABELS[t]
    if t == "navbar":
        menu = ", ".join(f"{a} -> {b}" for a, b in parse_links(el.get("links")))
        detail = f'merek "{el.get("brand", "")}", menu: {menu or "-"}'
    elif t == "heading":
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
    elif t == "gallery":
        detail = (
            f'{el.get("columns")} kolom, sudut membulat {el.get("radius")}px, gambar: '
            + ", ".join(lines_of(el.get("urls")))
        )
    elif t == "list":
        gaya = "bernomor" if el.get("style") == "number" else "berpoin"
        detail = f"daftar {gaya} dengan item: " + "; ".join(lines_of(el.get("items")))
    elif t == "input":
        detail = (
            f'label "{el.get("label", "")}", placeholder "{el.get("placeholder", "")}", '
            f'jenis isian: {INPUT_KINDS[input_kind(el)].lower()}'
        )
    elif t == "card":
        detail = f'judul "{el.get("title", "")}", isi "{el.get("text", "")}"'
    elif t == "divider":
        detail = "garis horizontal tipis"
    elif t == "footer":
        detail = f'teks "{el.get("text", "")}", rata tengah'
    elif t in BAR_SPECS:
        detail = describe_bar(el)
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
    ]
    if theme.get("glass"):
        lines.append(
            "- Terapkan efek glassmorphism: permukaan semi transparan dengan backdrop-filter "
            f'blur {theme.get("glass_blur", 18)}px, garis tepi putih tipis, sudut membulat, dan bayangan lembut, '
            "di atas latar gradien berwarna."
        )
    lines += [
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
    lines += ["", "## Aturan tambahan"]
    if len(design["pages"]) > 1:
        lines.append("- Sediakan navigasi antar halaman di bagian atas tanpa memuat ulang browser.")
    lines += [
        "- Tampilan harus responsif sampai ukuran layar ponsel.",
        "- Nama ikon pada spesifikasi mengacu ke Material Symbols (Google); pakai ikon yang sama.",
        "- Gunakan HTML semantik dan pastikan fokus keyboard terlihat jelas.",
        "- Jangan menambahkan elemen, teks, atau fitur di luar spesifikasi ini.",
        "- Berikan hasil akhir berupa kode lengkap yang bisa langsung dijalankan.",
    ]
    return "\n".join(lines)
