"""Callback Streamlit: dijalankan sebelum rerun, jadi aman mengubah session_state."""
import copy
import uuid

import streamlit as st

from config import ELEMENT_DEFAULTS, ELEMENT_STYLE_DEFAULTS
from design import default_design
from design_refs import DESIGN_REFS, SHAPE_TYPES, SURFACE_TYPES
from projects import current_page, selected_element
from styles import ensure_element_style
from templates import TEMPLATES, template_design


# ---- Seleksi dan elemen ----------------------------------------------------
def select_element(eid):
    st.session_state.selected_id = eid


def clear_selection():
    st.session_state.selected_id = None


def normalize_page_name(name):
    text = str(name or "").strip()
    if not text:
        return f"Halaman {len(st.session_state.design['pages']) + 1}"
    return text


def find_page_index_by_name(name):
    raw = str(name or "").strip()
    if not raw:
        return None
    lowered = raw.lower()
    for idx, page in enumerate(st.session_state.design["pages"]):
        if str(page.get("name", "")).strip().lower() == lowered:
            return idx
    return None


def create_page_named(name=None):
    pages = st.session_state.design["pages"]
    desired = normalize_page_name(name)
    match = find_page_index_by_name(desired)
    if match is not None:
        st.session_state.page_idx = match
        st.session_state.selected_id = None
        return match
    pages.append({"id": uuid.uuid4().hex[:8], "name": desired, "elements": []})
    st.session_state.page_idx = len(pages) - 1
    st.session_state.selected_id = None
    return st.session_state.page_idx

def open_page_target(el):
    """Buka halaman sesuai link_target; buat otomatis jika belum ada."""
    name = str(el.get("link_target", "")).strip()
    if not name:
        return
    create_page_named(name)
    
def insert_element(el_type, index=None):
    el = {"id": uuid.uuid4().hex[:8], "type": el_type}
    el.update(copy.deepcopy(ELEMENT_DEFAULTS[el_type]))
    el["visual_style"] = copy.deepcopy(ELEMENT_STYLE_DEFAULTS)
    els = current_page()["elements"]
    if index is None or not isinstance(index, int):
        index = len(els)
    els.insert(min(max(index, 0), len(els)), el)
    st.session_state.selected_id = el["id"]


def add_element(el_type):
    """Tambah komponen dari dock bawah setelah elemen yang sedang dipilih."""
    _, selected = selected_element()
    if selected is None:
        insert_element(el_type)
        return
    elements = current_page()["elements"]
    selected_index = next((i for i, el in enumerate(elements) if el["id"] == selected["id"]), len(elements) - 1)
    insert_element(el_type, selected_index + 1)


def move_element(index, delta):
    els = current_page()["elements"]
    new = index + delta
    if 0 <= new < len(els):
        els[index], els[new] = els[new], els[index]


def delete_element(index):
    els = current_page()["elements"]
    if 0 <= index < len(els):
        removed = els.pop(index)
        if st.session_state.selected_id == removed["id"]:
            st.session_state.selected_id = None


def duplicate_element(index):
    els = current_page()["elements"]
    clone = copy.deepcopy(els[index])
    clone["id"] = uuid.uuid4().hex[:8]
    els.insert(index + 1, clone)
    st.session_state.selected_id = clone["id"]


# ---- Halaman dan desain ----------------------------------------------------
def add_page():
    pages = st.session_state.design["pages"]
    name = f"Halaman {len(pages) + 1}"
    if "page_name_new" in st.session_state and str(st.session_state.get("page_name_new", "")).strip():
        name = str(st.session_state.page_name_new).strip()
    create_page_named(name)
    st.session_state.pop("page_name_new", None)


def delete_page():
    pages = st.session_state.design["pages"]
    if len(pages) > 1:
        pages.pop(st.session_state.page_idx)
        st.session_state.page_idx = max(0, st.session_state.page_idx - 1)
        st.session_state.selected_id = None


def reset_design():
    st.session_state.design = default_design()
    st.session_state.page_idx = 0
    st.session_state.selected_id = None


def load_design(data):
    st.session_state.design = data
    st.session_state.page_idx = 0
    st.session_state.selected_id = None


# ---- Template dan gaya -----------------------------------------------------
def apply_template():
    key = st.session_state.get("tpl_choice")
    if key not in TEMPLATES:
        return
    new = template_design(key)
    mode = st.session_state.get("tpl_mode", "Ganti seluruh desain")
    if mode == "Ganti seluruh desain":
        load_design(new)
    else:
        pages = st.session_state.design["pages"]
        start = len(pages)
        pages.extend(new["pages"])
        st.session_state.page_idx = start
        st.session_state.selected_id = None
    st.session_state.tpl_preview = False


def preview_template(key):
    if key in TEMPLATES:
        st.session_state.tpl_choice = key
        st.session_state.tpl_preview = True
        st.session_state.view_mode = "Preview"


def close_template_preview():
    st.session_state.tpl_preview = False


def use_template(key):
    if key in TEMPLATES:
        st.session_state.tpl_choice = key
        apply_template()


def apply_design_ref(name):
    ref = DESIGN_REFS.get(name)
    if not ref:
        return
    design = st.session_state.design
    design["theme"].update(copy.deepcopy(ref["theme"]))
    if st.session_state.get("ref_shape", True):
        for page in design["pages"]:
            for el in page["elements"]:
                if el.get("type") not in SHAPE_TYPES:
                    continue
                style = ensure_element_style(el)
                style.update(ref["shape"])
                if el["type"] in SURFACE_TYPES:
                    style["background"] = ref["surface"]
                    style["color"] = ref["ink"]
                # Hapus state widget lama supaya panel properti memakai nilai terbaru.
                for k in [k for k in st.session_state.keys() if str(k).startswith(f"{el['id']}_")]:
                    del st.session_state[k]
