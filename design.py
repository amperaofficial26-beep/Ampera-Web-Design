"""Struktur data desain: desain bawaan dan validasi."""
import copy
import uuid

from config import ELEMENT_DEFAULTS, ELEMENT_LABELS
from styles import ensure_element_style


def theme_of(primary, bg, text, font="Sans-serif modern", width=720):
    return {"primary": primary, "bg": bg, "text": text, "font": font, "width": width}


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
        "pages": [{"id": uuid.uuid4().hex[:8], "name": "Beranda", "elements": []}],
    }


def valid_design(data):
    try:
        assert isinstance(data["title"], str)
        assert isinstance(data["theme"], dict)
        assert isinstance(data["pages"], list) and data["pages"]
        for page in data["pages"]:
            assert isinstance(page["name"], str)
            page.setdefault("id", uuid.uuid4().hex[:8])
            for el in page["elements"]:
                assert el["type"] in ELEMENT_LABELS
                el.setdefault("id", uuid.uuid4().hex[:8])
                for k, v in ELEMENT_DEFAULTS[el["type"]].items():
                    el.setdefault(k, copy.deepcopy(v))
                ensure_element_style(el)
        for k, v in default_design()["theme"].items():
            data["theme"].setdefault(k, v)
        return True
    except (KeyError, TypeError, AssertionError):
        return False
