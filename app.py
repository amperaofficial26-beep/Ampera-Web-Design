"""UI Builder: titik masuk aplikasi Streamlit (hanya tata letak halaman).

Jalankan dengan:  streamlit run app.py
Logika dipisah ke modul lain; lihat README.md untuk peta modul.
"""
import hashlib
import json
import uuid

import streamlit as st

# set_page_config harus jadi perintah Streamlit pertama.
st.set_page_config(
    page_title="UI Builder",
    page_icon=":material/widgets:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from actions import (  # noqa: E402
    add_element, add_page, apply_design_ref, clear_selection, close_template_preview,
    delete_page, load_design, preview_template, reset_design, use_template,
)
from bar_specs import GROUP_ORDER  # noqa: E402
from config import (  # noqa: E402
    DEVICES, ELEMENT_GROUP, ELEMENT_LABELS, FONTS, ICONS, PANEL_HEIGHT,
)
from css import APP_CSS  # noqa: E402
from design import valid_design  # noqa: E402
from design_refs import DESIGN_REFS, ref_preview_html, swatches_html  # noqa: E402
from dnd_components import get_dnd_component, get_preview_component, handle_dnd_event, handle_preview_event  # noqa: E402
from html_builder import build_html  # noqa: E402
from projects import (  # noqa: E402
    autosave_project, current_page, delete_project, init_state, list_projects,
    new_project, rename_project, selected_element, switch_project,
)
from prompt_builder import build_prompt  # noqa: E402
from properties import edit_properties, summary_of  # noqa: E402
from templates import TEMPLATES, template_design  # noqa: E402

init_state()
design = st.session_state.design

st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)

autosave_project()

# ---------------------------- HEADER & PROYEK ------------------------------
with st.container(key="hero"):
    hc1, hc2 = st.columns([3, 1.4], vertical_alignment="center")
    hc1.markdown("## :material/dashboard_customize: UI Builder")
    hc1.caption("Susun tampilan aplikasi, lihat hasilnya langsung, lalu ambil kode HTML atau prompt master AI.")
    hc2.markdown(
        f":material/widgets: {len(ELEMENT_LABELS)} komponen &nbsp;·&nbsp; "
        f":material/dashboard: {len(TEMPLATES)} template &nbsp;·&nbsp; :material/palette: {len(DESIGN_REFS)} gaya"
    )

project_list = list_projects()
project_ids = [p["id"] for p in project_list]
project_names = {p["id"]: p["name"] for p in project_list}
if st.session_state.get("project_id") not in project_ids:
    project_ids.insert(0, st.session_state.project_id)
    project_names[st.session_state.project_id] = st.session_state.project_name
if st.session_state.get("project_selector_topbar") not in project_ids:
    st.session_state.project_selector_topbar = st.session_state.project_id

with st.container(border=True, key="projbar"):
    p1, p2, p3, p4 = st.columns([3.1, 1.15, 1.15, 1.15])
    p1.selectbox(
        "Proyek",
        project_ids,
        format_func=lambda pid: project_names.get(pid, pid),
        key="project_selector_topbar",
        on_change=switch_project,
        label_visibility="collapsed",
    )
    p2.button("Baru", icon=":material/add:", key="new_project_btn", on_click=new_project, use_container_width=True)
    p3.button("Nama", icon=":material/edit:", key="rename_project_btn", on_click=rename_project, use_container_width=True)
    p4.button(
        "Hapus", icon=":material/delete:", key="delete_project_btn", on_click=delete_project,
        disabled=len(project_ids) <= 1, use_container_width=True,
    )
    r1, r2 = st.columns([3.1, 4.45])
    r1.text_input(
        "Nama proyek", value=st.session_state.project_name, key="project_rename",
        label_visibility="collapsed", placeholder="Nama proyek",
    )
    status = {
        "saved": ":material/cloud_done: Tersimpan otomatis",
        "saving": ":material/sync: Menyimpan...",
        "error": ":material/error: Gagal menyimpan",
    }.get(st.session_state.get("autosave_status"), ":material/cloud_done: Tersimpan otomatis")
    saved_at = st.session_state.get("last_saved_at")
    r2.caption(f"{status}" + (f" · {saved_at}" if saved_at else ""))

with st.expander(":material/lightbulb: Cara pakai singkat", expanded=False):
    g1, g2, g3, g4 = st.columns(4)
    g1.markdown(":material/add_circle: **1. Tambah komponen**\n\nSeret dari daftar Komponen ke Susunan, atau klik untuk menambah di akhir.")
    g2.markdown(":material/tune: **2. Atur properti**\n\nKlik satu baris di Susunan, lalu ubah teks, ikon, dan gaya di tab Properti.")
    g3.markdown(":material/dashboard: **3. Mulai dari template**\n\nTab Template berisi galeri siap pakai dan referensi gaya desain.")
    g4.markdown(":material/code: **4. Ambil hasilnya**\n\nPilih Kode HTML atau Prompt AI di atas preview, lalu unduh.")

# Preview di tengah dibuat paling lebar supaya hasil desain terlihat lega.
col_left, col_center, col_right = st.columns([0.85, 4.05, 1.25], gap="medium")

# ---------------------------- PANEL KIRI ----------------------------------
# Panel kiri hanya untuk mengelola halaman. Daftar komponen ada di dock bawah.
with col_left:
    with st.container(height=PANEL_HEIGHT, border=True, key="panel_left"):
        st.markdown("##### :material/description: Halaman")
        pages = design["pages"]
        st.selectbox(
            "Halaman aktif",
            options=list(range(len(pages))),
            format_func=lambda i: pages[i]["name"] if i < len(pages) else "",
            key="page_idx",
            on_change=clear_selection,
            label_visibility="collapsed",
        )
        page = current_page()
        page.setdefault("id", uuid.uuid4().hex[:8])
        page["name"] = st.text_input("Nama halaman", page["name"], key=f"pname_{page['id']}")
        b1, b2 = st.columns(2)
        b1.button("Tambah", icon=":material/add:", on_click=add_page, use_container_width=True)
        b2.button(
            "Hapus", icon=":material/delete:", on_click=delete_page,
            disabled=len(pages) <= 1, use_container_width=True
        )

        st.divider()
        st.markdown("##### :material/layers: Ringkasan")
        st.caption(f"{len(page['elements'])} komponen di halaman ini")
        if st.session_state.get("selected_id"):
            _, _sel = selected_element()
            if _sel:
                st.success(
                    f"Terpilih: {ELEMENT_LABELS[_sel['type']]}",
                    icon=":material/touch_app:",
                )
        else:
            st.info(
                "Pilih komponen dari Preview atau panel Susunan di kanan.",
                icon=":material/touch_app:",
            )

        st.divider()
        st.markdown("##### :material/lightbulb: Alur baru")
        st.caption("1. Pilih komponen di dock bawah.")
        st.caption("2. Komponen masuk ke Susunan di kanan.")
        st.caption("3. Klik komponen di Preview atau Susunan.")
        st.caption("4. Edit langsung di panel Properti.")

# ---------------------------- PANEL TENGAH --------------------------------
with col_center:
    top1, top2 = st.columns([2.2, 1])
    VIEW_LABELS = {
        "Preview": ":material/visibility: Preview",
        "Kode HTML": ":material/code: Kode HTML",
        "Prompt Master AI": ":material/auto_awesome: Prompt AI",
    }
    view = top1.radio(
        "Tampilan",
        list(VIEW_LABELS),
        format_func=lambda v: VIEW_LABELS[v],
        horizontal=True,
        label_visibility="collapsed",
        key="view_mode",
    )
    device = top2.selectbox(
        "Ukuran layar",
        list(DEVICES),
        index=0,
        label_visibility="collapsed",
        disabled=view != "Preview",
    )
    center_output = st.empty()
    target = None
    if view == "Prompt Master AI":
        target = st.selectbox(
            "Target pembuatan",
            [
                "HTML/CSS/JavaScript satu file",
                "React dengan Tailwind CSS",
                "Streamlit (Python)",
                "Flutter (Dart)",
            ],
            key="prompt_target",
        )

# ---------------------------- PANEL KANAN ---------------------------------
# Panel kanan: Susunan + Properti, Template, Tema, Berkas.
with col_right:
    with st.container(height=PANEL_HEIGHT, border=True, key="panel_right"):
        tab_editor, tab_tpl, tab_theme, tab_file = st.tabs([
            ":material/edit_note: Editor",
            ":material/dashboard: Template",
            ":material/palette: Tema",
            ":material/folder: Berkas",
        ])

        with tab_editor:
            elements = current_page()["elements"]
            st.markdown("##### :material/account_tree: Susunan")
            st.caption("Komponen yang kamu tambahkan muncul di sini. Seret untuk mengubah urutan.")

            dnd = get_dnd_component()
            dnd_signature = hashlib.md5(
                "|".join(
                    [
                        str(current_page().get("id", "")),
                        *[f"{el.get('id','')}:{el.get('type','')}" for el in elements],
                    ]
                ).encode("utf-8")
            ).hexdigest()[:10]

            dnd_event = dnd(
                items=[
                    {
                        "id": el["id"],
                        "label": ELEMENT_LABELS[el["type"]] + summary_of(el),
                        "icon": ICONS.get(el["type"], "widgets"),
                    }
                    for el in elements
                ],
                selected=st.session_state.selected_id,
                key=f"layer_list_{dnd_signature}",
                default=None,
            )
            if handle_dnd_event(dnd_event):
                st.rerun()

            st.divider()
            st.markdown("##### :material/tune: Properti")

            idx, sel = selected_element()
            if sel is None:
                st.info(
                    "Belum ada komponen yang dipilih. Klik komponen di Preview atau Susunan.",
                    icon=":material/touch_app:",
                )
            else:
                edit_properties(sel, idx)

        with tab_tpl:
            sub_gal, sub_ref = st.tabs([":material/grid_view: Galeri", ":material/palette: Referensi gaya"])
            with sub_gal:
                st.text_input("Cari template", key="tpl_q", placeholder="Ketik nama, kategori, atau kata kunci")
                cats = ["Semua"] + sorted({t["category"] for t in TEMPLATES.values()})
                st.selectbox("Kategori", cats, key="tpl_cat")
                st.radio(
                    "Cara menerapkan",
                    ["Ganti seluruh desain", "Tambahkan sebagai halaman baru"],
                    key="tpl_mode",
                )
                if st.session_state.get("tpl_preview") and st.session_state.get("tpl_choice") in TEMPLATES:
                    st.info(
                        f"Pratinjau aktif: {TEMPLATES[st.session_state.tpl_choice]['name']}",
                        icon=":material/visibility:",
                    )
                    st.button(
                        "Tutup pratinjau", icon=":material/close:",
                        on_click=close_template_preview, use_container_width=True,
                    )
                q = str(st.session_state.get("tpl_q", "")).strip().lower()
                cat = st.session_state.get("tpl_cat", "Semua")
                shown = [
                    k for k, t in TEMPLATES.items()
                    if (cat == "Semua" or t["category"] == cat)
                    and (not q or q in t["name"].lower() or q in t["category"].lower() or q in t["desc"].lower())
                ]
                st.caption(f"{len(shown)} dari {len(TEMPLATES)} template")
                if not shown:
                    st.info("Tidak ada template yang cocok. Ubah kata kunci atau kategori.", icon=":material/search_off:")
                for k in shown:
                    tpl = TEMPLATES[k]
                    n_el = sum(len(p["elements"]) for p in tpl["pages"])
                    with st.container(border=True):
                        st.markdown(f"**{tpl['name']}**")
                        st.markdown(swatches_html(tpl["theme"]), unsafe_allow_html=True)
                        st.caption(f"{tpl['category']} · {len(tpl['pages'])} halaman · {n_el} elemen")
                        st.caption(tpl["desc"])
                        b1, b2 = st.columns(2)
                        b1.button(
                            "Pratinjau", key=f"tpv_{k}", icon=":material/visibility:",
                            on_click=preview_template, args=(k,), use_container_width=True,
                        )
                        b2.button(
                            "Pakai", key=f"tus_{k}", icon=":material/check:", type="primary",
                            on_click=use_template, args=(k,), use_container_width=True,
                        )
                st.caption("Mode ganti akan menimpa desain yang sedang dikerjakan. Unduh dulu lewat tab Berkas bila perlu.")

            with sub_ref:
                st.caption("Pilih gaya visual sebagai titik awal. Warna, font, dan lebar langsung diterapkan ke tema desainmu.")
                st.checkbox(
                    "Terapkan juga ke bentuk elemen (sudut, garis, bayangan)",
                    value=True, key="ref_shape",
                    help="Matikan bila kamu hanya ingin mengganti warna, font, dan lebar tema.",
                )
                for name, ref in DESIGN_REFS.items():
                    with st.container(border=True):
                        st.markdown(f"**{name}**")
                        st.markdown(ref_preview_html(ref), unsafe_allow_html=True)
                        st.caption(ref["desc"])
                        st.button(
                            "Terapkan gaya", key=f"ref_{name}", icon=":material/palette:",
                            on_click=apply_design_ref, args=(name,), use_container_width=True,
                        )

        with tab_theme:
            design["title"] = st.text_input("Nama aplikasi", design["title"])
            theme = design["theme"]
            theme["primary"] = st.color_picker("Warna utama", theme["primary"])
            theme["bg"] = st.color_picker("Warna latar", theme["bg"])
            theme["text"] = st.color_picker("Warna teks", theme["text"])
            font_names = list(FONTS)
            theme["font"] = st.selectbox(
                "Font", font_names, font_names.index(theme["font"]) if theme["font"] in font_names else 0
            )
            theme["width"] = st.slider("Lebar konten (px)", 360, 1200, int(theme["width"]), step=20)

        with tab_file:
            st.download_button(
                "Unduh desain (.json)",
                json.dumps(design, ensure_ascii=False, indent=2),
                file_name="desain.json",
                mime="application/json",
                icon=":material/download:",
                use_container_width=True,
            )
            uploaded = st.file_uploader("Muat desain (.json)", type=["json"])
            if uploaded is not None and st.button("Terapkan file", icon=":material/upload_file:", use_container_width=True):
                try:
                    data = json.loads(uploaded.getvalue().decode("utf-8"))
                    if valid_design(data):
                        load_design(data)
                        st.rerun()
                    else:
                        st.error("Struktur file tidak sesuai format desain.")
                except (json.JSONDecodeError, UnicodeDecodeError):
                    st.error("File bukan JSON yang valid.")
            st.button("Reset desain", icon=":material/restart_alt:", on_click=reset_design, use_container_width=True)

# ---------------------------- DOCK KOMPONEN --------------------------------
# Dibuat dengan widget Streamlit biasa (bukan iframe) agar selalu terlihat
# dan tetap bekerja di Streamlit Cloud.
st.markdown("### :material/widgets: Komponen")
st.caption("Klik komponen untuk menambahkan. Komponen baru akan langsung dipilih dan dapat diedit di panel kanan.")

f1, f2, f3 = st.columns([1.1, 1.6, 3])
f1.selectbox("Grup", ["Semua grup"] + GROUP_ORDER, key="dock_group")
f2.text_input("Cari komponen", key="dock_q", placeholder="Ketik nama komponen…")
dock_group = st.session_state.get("dock_group", "Semua grup")
dock_q = str(st.session_state.get("dock_q", "")).strip().lower()
component_types = [
    t for t in sorted(ELEMENT_LABELS, key=lambda x: (GROUP_ORDER.index(ELEMENT_GROUP[x]), ELEMENT_LABELS[x]))
    if (dock_group == "Semua grup" or ELEMENT_GROUP[t] == dock_group)
    and (not dock_q or dock_q in ELEMENT_LABELS[t].lower())
]
f3.caption(
    f"{len(component_types)} dari {len(ELEMENT_LABELS)} komponen tampil"
    + (f" · grup {dock_group}" if dock_group != "Semua grup" else "")
    + (f" · kata kunci “{st.session_state.get('dock_q', '')}”" if dock_q else "")
)

if not component_types:
    st.info("Tidak ada komponen yang cocok. Ubah grup atau kata kunci.", icon=":material/search_off:")

COMPONENTS_PER_ROW = 5
for row_start in range(0, len(component_types), COMPONENTS_PER_ROW):
    row_types = component_types[row_start:row_start + COMPONENTS_PER_ROW]
    cols = st.columns(COMPONENTS_PER_ROW, gap="small")
    for col, t in zip(cols, row_types):
        label = ELEMENT_LABELS[t]
        icon_name = ICONS.get(t, "widgets")
        col.button(
            label,
            icon=f":material/{icon_name}:",
            key=f"bottom_component_{t}",
            use_container_width=True,
            on_click=add_element,
            args=(t,),
            help=f"Tambah {label} ke halaman ({ELEMENT_GROUP[t]})",
        )

st.divider()

# ---------------------- RENDER OUTPUT TERBARU ------------------------------
with center_output.container():
    if view == "Preview":
        tpl_key = st.session_state.get("tpl_choice")
        if st.session_state.get("tpl_preview") and tpl_key in TEMPLATES:
            st.caption(f"Pratinjau template: {TEMPLATES[tpl_key]['name']} (belum diterapkan ke desainmu)")
            inner = build_html(template_design(tpl_key))
        else:
            _, sel_el = selected_element()
            inner = build_html(
                st.session_state.design,
                highlight_id=sel_el["id"] if sel_el else None,
                active=st.session_state.page_idx,
                builder_mode=True,
            )

        preview_component = get_preview_component()
        preview_event = preview_component(
            html=inner,
            deviceWidth=DEVICES[device],
            key="builder_live_preview",
            default=None,
        )
        if handle_preview_event(preview_event):
            st.rerun()

    elif view == "Kode HTML":
        output = build_html(st.session_state.design)
        st.download_button(
            "Unduh index.html", output, file_name="index.html",
            mime="text/html", icon=":material/download:"
        )
        with st.container(height=PANEL_HEIGHT - 110, border=True):
            st.code(output, language="html")

    else:
        output = build_prompt(st.session_state.design, target)
        st.download_button(
            "Unduh prompt_master.txt", output, file_name="prompt_master.txt",
            mime="text/plain", icon=":material/download:",
        )
        with st.container(height=PANEL_HEIGHT - 160, border=True):
            st.code(output, language="markdown")

# Autosave terakhir dijalankan setelah seluruh widget pada rerun ini menerapkan perubahan.
autosave_project()
