"""Panel Properti (kanan): editor untuk elemen yang sedang dipilih."""
import re

import streamlit as st

from actions import delete_element, duplicate_element, move_element, open_page_target
from bar_specs import BAR_SPECS
from bars import edit_bar_fields
from config import (ALIGNS, ELEMENT_LABELS, INPUT_KINDS, LINK_TYPES, SHADOW_OPTIONS, WIDTH_OPTIONS)
from projects import current_page
from styles import ensure_element_style
from utils import align_of, input_kind


def summary_of(el):
    for k in ("text", "title", "label", "brand", "alt"):
        v = str(el.get(k, "")).strip().replace("\n", " ")
        v = re.sub(r"[*_`\[\]]", "", v)
        if v:
            return " – " + (v[:16] + "…" if len(v) > 16 else v)
    return ""


def align_radio(el, key):
    return st.radio("Rata", ALIGNS, ALIGNS.index(align_of(el)), horizontal=True, key=key)


def edit_visual_properties(el, key):
    """Panel gaya umum untuk setiap elemen."""
    style = ensure_element_style(el)
    with st.expander(":material/palette: Tampilan & Bentuk", expanded=False):
        c1, c2 = st.columns(2)
        style["background"] = c1.color_picker(
            "Warna latar", style.get("background", "#ffffff") if style.get("background") != "transparent" else "#ffffff",
            key=f"{key}_bg_color",
        )
        transparent = c2.checkbox("Transparan", style.get("background") == "transparent", key=f"{key}_bg_transparent")
        if transparent:
            style["background"] = "transparent"

        c1, c2 = st.columns(2)
        style["color"] = c1.color_picker(
            "Warna teks", style.get("color", "#1f2937") if style.get("color") != "inherit" else "#1f2937",
            key=f"{key}_text_color",
        )
        style["border_color"] = c2.color_picker(
            "Warna garis", style.get("border_color", "#d1d5db"), key=f"{key}_border_color"
        )

        c1, c2 = st.columns(2)
        style["border_width"] = c1.slider(
            "Ketebalan garis", 0, 6, int(style.get("border_width", 0)), key=f"{key}_border_width"
        )
        style["radius"] = c2.slider(
            "Bentuk / radius", 0, 48, int(style.get("radius", 8)), key=f"{key}_radius_style"
        )

        c1, c2 = st.columns(2)
        shadow_label = next((label for label, value in SHADOW_OPTIONS.items() if value == style.get("shadow")), "Tanpa bayangan")
        selected_shadow = c1.selectbox(
            "Bayangan", list(SHADOW_OPTIONS), index=list(SHADOW_OPTIONS).index(shadow_label), key=f"{key}_shadow"
        )
        style["shadow"] = SHADOW_OPTIONS[selected_shadow]
        style["padding"] = c2.slider(
            "Padding", 0, 48, int(style.get("padding", 0)), key=f"{key}_padding"
        )

        width_label = next((label for label, value in WIDTH_OPTIONS.items() if value == style.get("width")), "Auto")
        style["width"] = WIDTH_OPTIONS[c1.selectbox(
            "Lebar elemen", list(WIDTH_OPTIONS), index=list(WIDTH_OPTIONS).index(width_label), key=f"{key}_width"
        )]


def edit_properties(el, index):
    key = el["id"]
    t = el["type"]
    st.markdown(f"**{ELEMENT_LABELS[t]}** (elemen ke-{index + 1})")

    if t == "navbar":
        el["brand"] = st.text_input("Nama merek", el["brand"], key=f"{key}_brand")
        el["links"] = st.text_area(
            "Menu (satu per baris, format: label|tautan)", el["links"], key=f"{key}_links", height=110
        )
    elif t == "heading":
        el["text"] = st.text_input("Teks", el["text"], key=f"{key}_text")
        el["size"] = st.slider("Ukuran (px)", 16, 72, int(el["size"]), key=f"{key}_size")
        el["align"] = align_radio(el, f"{key}_align")
    elif t == "text":
        el["text"] = st.text_area("Teks", el["text"], key=f"{key}_text")
        el["align"] = align_radio(el, f"{key}_align")
    elif t == "button":
        el["text"] = st.text_input("Label", el["text"], key=f"{key}_text")
        link_type_keys = list(LINK_TYPES)
        current_link_type = el.get("link_type", "url") if el.get("link_type", "url") in link_type_keys else "url"
        el["link_type"] = st.selectbox(
            "Jenis target",
            link_type_keys,
            index=link_type_keys.index(current_link_type),
            format_func=lambda v: LINK_TYPES[v],
            key=f"{key}_link_type",
        )
        if el["link_type"] == "page":
            el["link_target"] = st.text_input(
                "Nama halaman target",
                str(el.get("link_target", "")).strip(),
                key=f"{key}_link_target",
                placeholder="Contoh: Akun",
                help="Saat ditutup, tombol akan membuka halaman ini. Jika belum ada, halaman akan dibuat otomatis.",
            )
            if st.button("Buat & buka halaman ini", key=f"{key}_go_page", use_container_width=True):
                target_name = str(el.get("link_target", "")).strip()
                if target_name:
                    open_page_target(el)
                    st.rerun()
            st.caption("Contoh: ketik 'akun' lalu tombol akan membuka halaman Akun.")
        else:
            el["link"] = st.text_input("URL", el.get("link", ""), key=f"{key}_link")
            el["link_target"] = ""
        el["align"] = align_radio(el, f"{key}_align")
    elif t == "image":
        el["url"] = st.text_input("URL gambar", el["url"], key=f"{key}_url")
        el["alt"] = st.text_input("Teks alternatif", el["alt"], key=f"{key}_alt")
        el["radius"] = st.slider("Sudut membulat (px)", 0, 48, int(el["radius"]), key=f"{key}_radius")
    elif t == "gallery":
        el["urls"] = st.text_area("URL gambar (satu per baris)", el["urls"], key=f"{key}_urls", height=120)
        el["columns"] = st.slider("Jumlah kolom", 1, 4, int(el["columns"]), key=f"{key}_cols")
        el["radius"] = st.slider("Sudut membulat (px)", 0, 32, int(el["radius"]), key=f"{key}_radius")
    elif t == "list":
        el["items"] = st.text_area("Item (satu per baris)", el["items"], key=f"{key}_items", height=120)
        el["style"] = st.radio(
            "Gaya", ["bullet", "number"], 0 if el["style"] != "number" else 1,
            format_func=lambda s: "Poin" if s == "bullet" else "Bernomor",
            horizontal=True, key=f"{key}_style",
        )
    elif t == "input":
        el["label"] = st.text_input("Label", el["label"], key=f"{key}_label")
        el["placeholder"] = st.text_input("Placeholder", el["placeholder"], key=f"{key}_ph")
        kinds = list(INPUT_KINDS)
        el["kind"] = st.selectbox(
            "Jenis isian", kinds, kinds.index(input_kind(el)),
            format_func=lambda k: INPUT_KINDS[k], key=f"{key}_kind",
        )
    elif t == "card":
        el["title"] = st.text_input("Judul", el["title"], key=f"{key}_title")
        el["text"] = st.text_area("Isi", el["text"], key=f"{key}_text")
    elif t == "spacer":
        el["height"] = st.slider("Tinggi (px)", 4, 200, int(el["height"]), key=f"{key}_h")
    elif t == "footer":
        el["text"] = st.text_input("Teks footer", el["text"], key=f"{key}_text")
    elif t in BAR_SPECS:
        edit_bar_fields(el, key)
    else:
        st.caption("Elemen ini tidak punya pengaturan.")

    edit_visual_properties(el, key)
    st.divider()
    total = len(current_page()["elements"])
    m1, m2 = st.columns(2)
    m1.button("Naikkan", icon=":material/arrow_upward:", key=f"{key}_mvup", on_click=move_element, args=(index, -1),
              disabled=index == 0, use_container_width=True)
    m2.button("Turunkan", icon=":material/arrow_downward:", key=f"{key}_mvdn", on_click=move_element, args=(index, 1),
              disabled=index >= total - 1, use_container_width=True)
    c1, c2 = st.columns(2)
    c1.button("Gandakan", icon=":material/content_copy:", key=f"{key}_dup", on_click=duplicate_element, args=(index,), use_container_width=True)
    c2.button("Hapus", icon=":material/delete:", key=f"{key}_del", on_click=delete_element, args=(index,), use_container_width=True)
