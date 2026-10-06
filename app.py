"""AOG Web Desain (Visual Website Builder): titik masuk aplikasi Streamlit (hanya tata letak halaman).

Jalankan dengan:  streamlit run app.py
Logika dipisah ke modul lain; lihat README.md untuk peta modul.
"""
import hashlib
import json
import uuid
from collections import Counter

import streamlit as st

# set_page_config harus jadi perintah Streamlit pertama.
st.set_page_config(
    page_title="AOG Web Desain",
    page_icon=":material/widgets:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from actions import (  # noqa: E402
    add_element, add_page, apply_design_ref, clear_selection, close_template_preview,
    delete_page, load_design, preview_template, reset_design, use_template,
)
from bar_specs import GROUP_ORDER  # noqa: E402
from bar_specs_addons import COMPONENT_BAR_SPECS  # noqa: E402
from config import (  # noqa: E402
    DEVICES, ELEMENT_GROUP, ELEMENT_LABELS, FONTS, ICONS, PANEL_HEIGHT,
)
from css_aog import AOG_CSS  # noqa: E402
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

ALL_GROUPS = "Semua grup"
VIEW_LABELS = {
    "Preview": ":material/visibility: Preview",
    "Kode HTML": ":material/code: Code",
    "Prompt Master AI": ":material/auto_awesome: AI Builder",
}


def _show_group(group):
    """Callback: tampilkan satu grup di Component Library."""
    st.session_state.dock_group = group


def _open_ai_builder():
    """Callback: pindah ke tampilan AI Builder (Prompt Master AI)."""
    st.session_state.view_mode = "Prompt Master AI"


init_state()
design = st.session_state.design

st.markdown(f"<style>{AOG_CSS}</style>", unsafe_allow_html=True)

autosave_project()

# ------------------------------ DATA PROYEK --------------------------------
project_list = list_projects()
project_ids = [p["id"] for p in project_list]
project_names = {p["id"]: p["name"] for p in project_list}
if st.session_state.get("project_id") not in project_ids:
    project_ids.insert(0, st.session_state.project_id)
    project_names[st.session_state.project_id] = st.session_state.project_name
if st.session_state.get("project_selector_topbar") not in project_ids:
    st.session_state.project_selector_topbar = st.session_state.project_id

pages = design["pages"]
page = current_page()
page.setdefault("id", uuid.uuid4().hex[:8])
page_label = str(st.session_state.get(f"pname_{page['id']}", page["name"]) or "Tanpa nama")

# ----------------------------- HEADER / TOOLBAR ----------------------------
# HEADER = CONTROL: halaman, mode tampilan, status simpan, proyek.
with st.container(key="aog_header"):
    hc_brand, hc_page, hc_view, hc_status, hc_proj = st.columns([1.5, 1.5, 3, 1.6, 1.1], vertical_alignment="center")

    hc_brand.markdown(
        '<div class="aog-brand"><span class="aog-name">AOG Web Desain</span>'
        '<span class="aog-sub">Visual Website Builder</span></div>',
        unsafe_allow_html=True,
    )

    with hc_page.popover(page_label, icon=":material/description:", use_container_width=True):
        st.caption("HALAMAN")
        st.selectbox(
            "Halaman aktif",
            options=list(range(len(pages))),
            format_func=lambda i: pages[i]["name"] if i < len(pages) else "",
            key="page_idx",
            on_change=clear_selection,
        )
        page = current_page()
        page.setdefault("id", uuid.uuid4().hex[:8])
        page["name"] = st.text_input("Nama halaman", page["name"], key=f"pname_{page['id']}")
        b1, b2 = st.columns(2, gap="small")
        b1.button("Tambah halaman", icon=":material/add:", on_click=add_page, use_container_width=True,
                  help="Buat halaman baru dan langsung buka halaman tersebut.")
        b2.button(
            "Hapus", icon=":material/delete:", on_click=delete_page,
            disabled=len(pages) <= 1, use_container_width=True,
            help="Hapus halaman aktif. Minimal satu halaman harus tersisa.",
        )

    view = hc_view.radio(
        "Tampilan",
        list(VIEW_LABELS),
        format_func=lambda v: VIEW_LABELS[v],
        horizontal=True,
        label_visibility="collapsed",
        key="view_mode",
    )

    status = {
        "saved": ":material/cloud_done: Tersimpan",
        "saving": ":material/sync: Menyimpan...",
        "error": ":material/error: Gagal menyimpan",
    }.get(st.session_state.get("autosave_status"), ":material/cloud_done: Tersimpan")
    saved_at = st.session_state.get("last_saved_at")
    hc_status.caption(status + (f" · {saved_at}" if saved_at else ""))

    with hc_proj.popover("Proyek", icon=":material/folder_open:", use_container_width=True):
        st.caption("PROYEK")
        st.selectbox(
            "Proyek",
            project_ids,
            format_func=lambda pid: project_names.get(pid, pid),
            key="project_selector_topbar",
            on_change=switch_project,
        )
        st.text_input(
            "Nama proyek", value=st.session_state.project_name, key="project_rename",
            placeholder="Nama proyek",
        )
        p1, p2, p3 = st.columns(3, gap="small")
        p1.button("Baru", icon=":material/add:", key="new_project_btn", on_click=new_project, use_container_width=True)
        p2.button("Nama", icon=":material/edit:", key="rename_project_btn", on_click=rename_project, use_container_width=True)
        p3.button(
            "Hapus", icon=":material/delete:", key="delete_project_btn", on_click=delete_project,
            disabled=len(project_ids) <= 1, use_container_width=True,
        )
        st.divider()
        st.caption("CARA PAKAI SINGKAT")
        st.markdown(
            ":material/widgets: **Kiri**: pilih elemen\n\n"
            ":material/visibility: **Tengah**: lihat hasil website\n\n"
            ":material/tune: **Kanan**: edit properti elemen\n\n"
            ":material/inventory_2: **Bawah**: cari di Component Library"
        )

# ------------------------------ AREA EDITOR --------------------------------
# LEFT = CHOOSE, CENTER = SEE, RIGHT = EDIT.
col_left, col_center, col_right = st.columns([1.0, 4.0, 1.6], gap="small")

group_counts = Counter(ELEMENT_GROUP.values())

# ---------------------------- PANEL KIRI: ELEMENTS --------------------------
with col_left:
    with st.container(height=PANEL_HEIGHT, border=True, key="panel_left"):
        st.markdown("#### :material/widgets: Elements")
        el_q = str(st.text_input(
            "Cari elemen", key="el_q", placeholder="Cari elemen...", label_visibility="collapsed",
        )).strip().lower()

        if el_q:
            hits = [
                t for t in sorted(ELEMENT_LABELS, key=lambda x: ELEMENT_LABELS[x])
                if el_q in ELEMENT_LABELS[t].lower() or el_q in t.lower() or el_q in ELEMENT_GROUP[t].lower()
            ]
            st.caption(f"{len(hits)} hasil")
            if not hits:
                st.info("Tidak ada elemen yang cocok.", icon=":material/search_off:")
            for t in hits[:15]:
                st.button(
                    ELEMENT_LABELS[t], icon=f":material/{ICONS.get(t, 'widgets')}:", key=f"left_el_{t}",
                    on_click=add_element, args=(t,), use_container_width=True,
                    help=f"Tambah {ELEMENT_LABELS[t]} ({ELEMENT_GROUP[t]})",
                )
            if len(hits) > 15:
                st.caption("Hasil lainnya ada di Component Library di bawah.")
        else:
            st.caption("ELEMEN DASAR")
            basics = [t for t in ELEMENT_LABELS if ELEMENT_GROUP[t] == "Dasar"]
            for i in range(0, len(basics), 2):
                bc = st.columns(2, gap="small")
                for c, t in zip(bc, basics[i:i + 2]):
                    c.button(
                        ELEMENT_LABELS[t], icon=f":material/{ICONS.get(t, 'widgets')}:", key=f"left_el_{t}",
                        on_click=add_element, args=(t,), use_container_width=True,
                        help=f"Tambah {ELEMENT_LABELS[t]} ke halaman",
                    )
            st.caption("KATEGORI")
            for g in GROUP_ORDER:
                st.button(
                    f"{g} ({group_counts.get(g, 0)})", icon=":material/chevron_right:", key=f"left_grp_{g}",
                    on_click=_show_group, args=(g,), use_container_width=True,
                    help=f"Tampilkan grup {g} di Component Library",
                )

        st.divider()
        _, selected = selected_element()
        if selected:
            st.caption(f":material/touch_app: {ELEMENT_LABELS[selected['type']]} dipilih")
        st.caption(
            f"{len(current_page()['elements'])} komponen di halaman ini · {len(ELEMENT_LABELS)} komponen tersedia · "
            f"{len(TEMPLATES)} template · {len(DESIGN_REFS)} gaya"
        )

# ----------------------------- PANEL TENGAH: CANVAS -------------------------
with col_center:
    devices = list(reversed(list(DEVICES)))  # Desktop, Tablet, Ponsel
    DEVICE_VIEW = {}
    for dname in devices:
        w = DEVICES[dname]
        if w is None:
            DEVICE_VIEW[dname] = ":material/desktop_windows: Desktop"
        elif w >= 600:
            DEVICE_VIEW[dname] = ":material/tablet: Tablet"
        else:
            DEVICE_VIEW[dname] = ":material/smartphone: Mobile"

    cb1, cb2 = st.columns([1, 2], vertical_alignment="center")
    cb1.caption(f"Canvas · {page_label}")
    with cb2:
        device = st.radio(
            "Ukuran layar",
            devices,
            format_func=lambda d: DEVICE_VIEW[d],
            horizontal=True,
            label_visibility="collapsed",
            key="device_mode",
            disabled=view != "Preview",
        )

    target = None
    if view == "Prompt Master AI":
        st.caption(
            "AI Builder menyusun Prompt Master dari desain Anda. Salin atau unduh, lalu tempel ke AI favorit Anda "
            "untuk menghasilkan kodenya."
        )
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
    with st.container(key="canvas_area"):
        center_output = st.empty()

# ---------------------------- PANEL KANAN: PROPERTIES -----------------------
with col_right:
    with st.container(height=PANEL_HEIGHT, border=True, key="panel_right"):
        st.markdown("#### :material/tune: Properties")
        tab_editor, tab_tpl, tab_theme, tab_file = st.tabs([
            ":material/edit_note: Properti",
            ":material/dashboard: Template",
            ":material/palette: Tema",
            ":material/folder: Berkas",
        ])

        with tab_editor:
            elements = current_page()["elements"]
            with st.expander("Susunan", expanded=True, icon=":material/account_tree:"):
                st.caption("Seret untuk mengubah urutan komponen.")
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

            idx, sel = selected_element()
            if sel is None:
                st.info(
                    "Belum ada elemen dipilih. Pilih elemen pada canvas atau Susunan untuk mengedit properti dan tampilannya.",
                    icon=":material/tune:",
                )
            else:
                edit_properties(sel, idx)

        with tab_tpl:
            sub_gal, sub_ref = st.tabs([":material/grid_view: Galeri", ":material/palette: Gaya"])
            with sub_gal:
                st.text_input("Cari template", key="tpl_q", placeholder="Nama, kategori, atau kata kunci")
                cats = ["Semua"] + sorted({t["category"] for t in TEMPLATES.values()})
                st.selectbox("Kategori", cats, key="tpl_cat")
                st.selectbox(
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
                gallery_count = sum(t["category"] == "Galeri" for t in TEMPLATES.values())
                st.caption(f"{len(shown)} dari {len(TEMPLATES)} template · {gallery_count} template galeri")
                if not shown:
                    st.info("Tidak ada template yang cocok. Ubah kata kunci atau kategori.", icon=":material/search_off:")
                else:
                    with st.container(height=340, border=False):
                        for k in shown:
                            tpl = TEMPLATES[k]
                            n_el = sum(len(p["elements"]) for p in tpl["pages"])
                            with st.expander(f"{tpl['name']} · {tpl['category']}", expanded=False):
                                st.markdown(swatches_html(tpl["theme"]), unsafe_allow_html=True)
                                st.caption(f"{len(tpl['pages'])} halaman · {n_el} elemen")
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
                st.caption("Mode ganti menimpa desain saat ini. Unduh desain terlebih dahulu bila ingin menyimpan salinan.")

            with sub_ref:
                st.caption("Pilih preset warna, font, dan bentuk. Gaya diterapkan ke tema serta elemen yang ada.")
                st.checkbox(
                    "Terapkan juga ke bentuk elemen (sudut, garis, bayangan)",
                    value=True, key="ref_shape",
                    help="Matikan bila hanya ingin mengganti warna, font, dan lebar tema.",
                )
                st.text_input("Cari gaya", key="ref_q", placeholder="Ketik nama atau karakter gaya…")
                ref_q = str(st.session_state.get("ref_q", "")).strip().lower()
                shown_refs = [
                    (name, ref) for name, ref in DESIGN_REFS.items()
                    if not ref_q or ref_q in name.lower() or ref_q in ref["desc"].lower()
                ]
                st.caption(f"{len(shown_refs)} dari {len(DESIGN_REFS)} referensi gaya")
                if not shown_refs:
                    st.info("Tidak ada gaya yang cocok dengan pencarian.", icon=":material/search_off:")
                else:
                    with st.container(height=360, border=False):
                        for name, ref in shown_refs:
                            with st.expander(name, expanded=False):
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

# ----------------------- BAWAH: COMPONENT LIBRARY ---------------------------
# BOTTOM = DISCOVER. Widget Streamlit biasa (bukan iframe) agar selalu terlihat
# dan tetap bekerja di Streamlit Cloud.
st.markdown("### :material/inventory_2: Component Library")
st.caption("Pilih komponen untuk menambahkannya ke halaman. Komponen baru langsung dipilih dan siap diedit.")

f1, f2, f3 = st.columns([1.1, 1.6, 3], vertical_alignment="bottom")
f1.selectbox("Grup", [ALL_GROUPS] + GROUP_ORDER, key="dock_group")
f2.text_input("Cari komponen", key="dock_q", placeholder="Cari komponen...")
dock_group = st.session_state.get("dock_group", ALL_GROUPS)
dock_q = str(st.session_state.get("dock_q", "")).strip().lower()
component_types = [
    t for t in sorted(ELEMENT_LABELS, key=lambda x: (GROUP_ORDER.index(ELEMENT_GROUP[x]), ELEMENT_LABELS[x]))
    if (dock_group == ALL_GROUPS or ELEMENT_GROUP[t] == dock_group)
    and (
        not dock_q
        or dock_q in ELEMENT_LABELS[t].lower()
        or dock_q in t.lower()
        or dock_q in ELEMENT_GROUP[t].lower()
    )
]
f3.caption(
    f"{len(component_types)} dari {len(ELEMENT_LABELS)} komponen tampil · "
    f"{len(COMPONENT_BAR_SPECS)} komponen tambahan baru"
    + (f" · grup {dock_group}" if dock_group != ALL_GROUPS else "")
    + (f" · kata kunci “{st.session_state.get('dock_q', '')}”" if dock_q else "")
)

with st.container(height=380, border=True, key="component_library"):
    if not component_types:
        st.info("Tidak ada komponen yang cocok. Ubah grup atau kata kunci.", icon=":material/search_off:")
    else:
        COMPONENTS_PER_ROW = 8
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

# ---------------------- RENDER OUTPUT TERBARU ------------------------------
with center_output.container():
    if view == "Preview":
        tpl_key = st.session_state.get("tpl_choice")
        tpl_active = bool(st.session_state.get("tpl_preview")) and tpl_key in TEMPLATES
        if not tpl_active and not current_page()["elements"]:
            with st.container(key="aog_empty"):
                st.markdown("# :material/add_circle:")
                st.markdown(
                    '<div class="aog-empty"><h3>Mulai membangun halaman Anda</h3>'
                    "<p>Tambahkan komponen dari Elements atau Component Library, atau gunakan AI Builder "
                    "untuk menyusun prompt layout secara otomatis.</p></div>",
                    unsafe_allow_html=True,
                )
                st.button(
                    "Gunakan AI Builder", icon=":material/auto_awesome:", type="primary",
                    key="empty_ai_btn", on_click=_open_ai_builder,
                )
        else:
            if tpl_active:
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
        with st.container(height=PANEL_HEIGHT - 150, border=True):
            st.code(output, language="html")

    else:
        output = build_prompt(st.session_state.design, target)
        st.download_button(
            "Unduh prompt_master.txt", output, file_name="prompt_master.txt",
            mime="text/plain", icon=":material/download:",
        )
        with st.container(height=PANEL_HEIGHT - 230, border=True):
            st.code(output, language="markdown")

# Autosave terakhir dijalankan setelah seluruh widget pada rerun ini menerapkan perubahan.
autosave_project()
