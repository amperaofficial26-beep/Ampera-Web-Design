"""Penyimpanan proyek (file JSON), autosave, dan state sesi."""
import copy
import hashlib
import json
import uuid
from datetime import datetime

import streamlit as st

from ui_builder.core.config import PROJECTS_DIR
from ui_builder.core.design import default_design, valid_design


def project_file(project_id):
    return PROJECTS_DIR / f"{project_id}.json"


def project_timestamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def project_digest(design):
    payload = json.dumps(design, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def list_projects():
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    projects = []
    for path in PROJECTS_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("design"), dict):
                projects.append({
                    "id": str(data.get("id") or path.stem),
                    "name": str(data.get("name") or data["design"].get("title") or "Proyek tanpa nama"),
                    "updated_at": str(data.get("updated_at") or ""),
                })
        except (OSError, json.JSONDecodeError, TypeError):
            continue
    projects.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
    return projects


def save_project(project_id, name, design):
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": project_id,
        "name": name.strip() or "Proyek tanpa nama",
        "updated_at": project_timestamp(),
        "design": copy.deepcopy(design),
    }
    project_file(project_id).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return payload


def read_project(project_id):
    try:
        data = json.loads(project_file(project_id).read_text(encoding="utf-8"))
        design = data.get("design")
        if not isinstance(data, dict) or not valid_design(design):
            return None
        return data
    except (OSError, json.JSONDecodeError, TypeError):
        return None


def set_active_project(project_id, data):
    st.session_state.project_id = project_id
    st.session_state.project_name = str(data.get("name") or data["design"].get("title") or "Proyek tanpa nama")
    st.session_state.design = data["design"]
    st.session_state.page_idx = 0
    st.session_state.selected_id = None
    st.session_state.last_saved_hash = project_digest(st.session_state.design)
    st.session_state.last_saved_at = str(data.get("updated_at") or "")
    st.session_state.autosave_status = "saved"


def create_project(name=None, design=None):
    project_id = uuid.uuid4().hex
    design = copy.deepcopy(design or default_design())
    project_name = (name or design.get("title") or "Proyek Baru").strip() or "Proyek Baru"
    payload = save_project(project_id, project_name, design)
    set_active_project(project_id, payload)


def switch_project():
    project_id = st.session_state.get("project_selector_topbar")
    if not project_id or project_id == st.session_state.get("project_id"):
        return
    data = read_project(project_id)
    if data is not None:
        set_active_project(project_id, data)


def new_project():
    create_project("Proyek Baru")


def rename_project():
    project_id = st.session_state.get("project_id")
    name = str(st.session_state.get("project_rename", "")).strip()
    if not project_id or not name:
        return
    st.session_state.project_name = name
    payload = save_project(project_id, name, st.session_state.design)
    st.session_state.last_saved_hash = project_digest(st.session_state.design)
    st.session_state.last_saved_at = payload["updated_at"]
    st.session_state.autosave_status = "saved"


def delete_project():
    project_id = st.session_state.get("project_id")
    projects = list_projects()
    if not project_id or len(projects) <= 1:
        return
    try:
        project_file(project_id).unlink(missing_ok=True)
    except OSError:
        return
    remaining = [p for p in list_projects() if p["id"] != project_id]
    if remaining:
        data = read_project(remaining[0]["id"])
        if data is not None:
            set_active_project(remaining[0]["id"], data)


def autosave_project():
    project_id = st.session_state.get("project_id")
    if not project_id or "design" not in st.session_state:
        return
    digest = project_digest(st.session_state.design)
    if digest == st.session_state.get("last_saved_hash"):
        return
    st.session_state.autosave_status = "saving"
    try:
        payload = save_project(project_id, st.session_state.get("project_name", "Proyek Baru"), st.session_state.design)
        st.session_state.last_saved_hash = digest
        st.session_state.last_saved_at = payload["updated_at"]
        st.session_state.autosave_status = "saved"
    except OSError:
        st.session_state.autosave_status = "error"


def init_state():
    if "design" not in st.session_state:
        projects = list_projects()
        if projects:
            data = read_project(projects[0]["id"])
            if data is not None:
                set_active_project(projects[0]["id"], data)
            else:
                create_project()
        else:
            create_project()
    if "page_idx" not in st.session_state:
        st.session_state.page_idx = 0
    if "selected_id" not in st.session_state:
        st.session_state.selected_id = None
    if "project_id" not in st.session_state:
        create_project()
    if "project_name" not in st.session_state:
        st.session_state.project_name = st.session_state.design.get("title", "Proyek Baru")
    if "last_saved_hash" not in st.session_state:
        st.session_state.last_saved_hash = project_digest(st.session_state.design)
    if "last_saved_at" not in st.session_state:
        st.session_state.last_saved_at = ""
    if "autosave_status" not in st.session_state:
        st.session_state.autosave_status = "saved"


def current_page():
    pages = st.session_state.design["pages"]
    idx = min(st.session_state.page_idx, len(pages) - 1)
    return pages[idx]


def selected_element():
    sid = st.session_state.get("selected_id")
    for i, el in enumerate(current_page()["elements"]):
        if el["id"] == sid:
            return i, el
    return None, None
