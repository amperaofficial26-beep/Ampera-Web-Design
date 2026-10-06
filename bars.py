"""Render, deskripsi, dan editor untuk 70 komponen bar.

Spesifikasi datanya ada di bar_specs.py.
- 20 bar inti punya cabang `if t == "..."` di render_bar() di bawah ini.
- 50 bar tambahan (formulir, media, sosial, toko, dll.) renderer-nya ada di
  bars_extra.py dan otomatis dipakai lewat EXTRA_BAR_RENDERERS.
"""
import streamlit as st

from bar_specs import BAR_SPECS, ICON_HINT, STATUS_ICONS, STATUS_KINDS
from bars_extra import EXTRA_BAR_RENDERERS
from bars_pro import PRO_BAR_RENDERERS
from config import ALIGNS
from styles import soft_style
from utils import clamp_int, esc, lines_of, mi, parts_of, safe_url


def page_numbers(total, current):
    keep = sorted({1, total, current - 1, current, current + 1})
    result, prev = [], 0
    for n in keep:
        if n < 1 or n > total:
            continue
        if prev and n - prev > 1:
            result.append(None)
        result.append(n)
        prev = n
    return result


def render_bar(el):
    t = el["type"]
    css = soft_style(el)
    sa = f' style="{css}"' if css else ""
    g = el.get

    if t == "bottomnav":
        rows = parts_of(g("items"), 2)
        act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
        inner = "".join(
            f'<a class="bn-item{" on" if i == act else ""}" href="#">'
            f'{mi(ic)}<span>{esc(lb)}</span></a>' for i, (lb, ic) in enumerate(rows))
        return f'<nav class="bar bottomnav" aria-label="Navigasi bawah"{sa}>{inner}</nav>'
    if t == "tabbar":
        rows = lines_of(g("items"))
        act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
        inner = "".join(f'<a class="tab{" on" if i == act else ""}" href="#" role="tab">{esc(lb)}</a>' for i, lb in enumerate(rows))
        return f'<div class="bar tabbar" role="tablist"{sa}>{inner}</div>'
    if t == "breadcrumb":
        rows = lines_of(g("items"))
        bits = []
        for i, lb in enumerate(rows):
            if i == len(rows) - 1:
                bits.append(f'<span class="cur" aria-current="page">{esc(lb)}</span>')
            else:
                bits.append(f'<a href="#">{esc(lb)}</a>{mi("chevron_right")}')
        return f'<nav class="bar crumbs" aria-label="Breadcrumb"{sa}>{"".join(bits)}</nav>'
    if t == "sidemenu":
        rows = parts_of(g("items"), 2)
        act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
        inner = "".join(
            f'<a class="sm-item{" on" if i == act else ""}" href="#">{mi(ic)}<span>{esc(lb)}</span></a>'
            for i, (lb, ic) in enumerate(rows))
        title = f'<div class="sm-title">{esc(g("title", ""))}</div>' if g("title") else ""
        return f'<nav class="bar sidemenu"{sa}>{title}{inner}</nav>'
    if t == "pagination":
        total = clamp_int(g("pages"), 1, 99, 10)
        cur = clamp_int(g("current"), 1, total, 1)
        bits = [f'<a href="#" aria-label="Sebelumnya">{mi("chevron_left")}</a>']
        for n in page_numbers(total, cur):
            bits.append('<span class="dots">…</span>' if n is None else
                        f'<a href="#" class="{"on" if n == cur else ""}">{n}</a>')
        bits.append(f'<a href="#" aria-label="Berikutnya">{mi("chevron_right")}</a>')
        return f'<nav class="bar pager" aria-label="Paginasi"{sa}>{"".join(bits)}</nav>'
    if t == "toolbar":
        rows = parts_of(g("items"), 2)
        inner = "".join(f'<button type="button" class="tb-btn">{mi(ic)}<span>{esc(lb)}</span></button>' for lb, ic in rows)
        return f'<div class="bar toolbar" role="toolbar"{sa}>{inner}</div>'
    if t == "searchbar":
        return (f'<div class="bar searchbar"{sa}>{mi("search")}'
                f'<input type="search" placeholder="{esc(g("placeholder", ""))}" aria-label="Pencarian">'
                f'<button type="button" class="btn">{esc(g("button", ""))}</button></div>')
    if t == "filterbar":
        rows = lines_of(g("items"))
        act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
        inner = "".join(f'<a class="fchip{" on" if i == act else ""}" href="#">{esc(lb)}</a>' for i, lb in enumerate(rows))
        return f'<div class="bar chips"{sa}>{inner}</div>'
    if t == "fab":
        align = g("align") if g("align") in ALIGNS else "right"
        label = f'<span>{esc(g("text", ""))}</span>' if g("text") else ""
        return (f'<div class="fabwrap" style="text-align:{align}"><a class="fab" href="#" '
                f'aria-label="{esc(g("text") or "Aksi")}"{sa}>{mi(g("icon"))}{label}</a></div>')
    if t == "socialbar":
        rows = parts_of(g("items"), 3)
        inner = "".join(f'<a href="{esc(safe_url(u))}">{mi(ic or "link")}<span>{esc(lb)}</span></a>' for lb, u, ic in rows)
        return f'<div class="bar social"{sa}>{inner}</div>'
    if t == "announcement":
        link = ""
        if g("link_text"):
            link = f'<a href="{esc(safe_url(g("link", "#")))}">{esc(g("link_text"))}</a>'
        return f'<div class="bar announce"{sa}>{esc(g("text", ""))}{link}</div>'
    if t == "statusbar":
        kind = g("kind") if g("kind") in STATUS_KINDS else "info"
        title = f'<strong>{esc(g("title", ""))}</strong> ' if g("title") else ""
        return (f'<div class="bar status {kind}" role="status"{sa}>{mi(STATUS_ICONS[kind])}'
                f'<div>{title}{esc(g("text", ""))}</div></div>')
    if t == "progressbar":
        v = clamp_int(g("value"), 0, 100, 0)
        return (f'<div class="bar progress"{sa}><div class="pg-head"><span>{esc(g("label", ""))}</span><span>{v}%</span></div>'
                f'<div class="pg-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{v}">'
                f'<div class="pg-fill" style="width:{v}%"></div></div></div>')
    if t == "stepper":
        rows = lines_of(g("steps"))
        cur = clamp_int(g("current"), 1, max(1, len(rows)), 1)
        inner = []
        for i, lb in enumerate(rows, start=1):
            state = "done" if i < cur else ("now" if i == cur else "")
            dot = mi("check") if i < cur else str(i)
            inner.append(f'<div class="st-step {state}"><div class="st-dot">{dot}</div>{esc(lb)}</div>')
        return f'<div class="bar stepper"{sa}>{"".join(inner)}</div>'
    if t == "ratingbar":
        try:
            val = max(0.0, min(5.0, float(g("value", 0) or 0)))
        except (TypeError, ValueError):
            val = 0.0
        stars = ""
        for i in range(1, 6):
            if val >= i - 0.25:
                stars += mi("star")
            elif val >= i - 0.75:
                stars += mi("star_half")
            else:
                stars += f'<span class="off">{mi("star")}</span>'
        lab = f'<strong>{val:g}</strong>'
        return (f'<div class="bar rating"{sa}><span class="stars" role="img" aria-label="{val:g} dari 5">{stars}</span>'
                f'{lab}<span>{esc(g("label", ""))}</span><small>{esc(g("count", ""))}</small></div>')
    if t == "statsbar":
        rows = parts_of(g("items"), 2)
        inner = "".join(f'<div class="stat"><strong>{esc(n)}</strong><span>{esc(lb)}</span></div>' for n, lb in rows)
        return f'<div class="bar stats"{sa}>{inner}</div>'
    if t == "pricebar":
        btn = f'<a class="btn" href="{esc(safe_url(g("link", "#")))}">{esc(g("button", ""))}</a>' if g("button") else ""
        return (f'<div class="bar pricebar"{sa}><div><strong>{esc(g("price", ""))}</strong>'
                f'<small>{esc(g("caption", ""))}</small></div>{btn}</div>')
    if t == "categorybar":
        rows = parts_of(g("items"), 2)
        inner = "".join(f'<a class="cat" href="#"><span class="cat-ico">{mi(ic)}</span>{esc(lb)}</a>' for lb, ic in rows)
        return f'<div class="bar cats"{sa}>{inner}</div>'
    if t == "profilebar":
        name = str(g("name", "") or "")
        if g("avatar"):
            av = f'<img src="{esc(safe_url(g("avatar")))}" alt="">'
        else:
            av = esc((name.strip()[:1] or "?").upper())
        btn = f'<a class="btn sm" href="#">{esc(g("action"))}</a>' if g("action") else ""
        return (f'<div class="bar profilebar"{sa}><div class="avatar">{av}</div>'
                f'<div class="pf-text"><strong>{esc(name)}</strong><small>{esc(g("role", ""))}</small></div>{btn}</div>')
    if t == "cookiebar":
        no = f'<button type="button" class="btn ghost sm">{esc(g("decline"))}</button>' if g("decline") else ""
        return (f'<div class="bar cookie" role="dialog" aria-label="Persetujuan cookie"{sa}><p>{esc(g("text", ""))}</p>'
                f'{no}<button type="button" class="btn sm">{esc(g("accept", ""))}</button></div>')
    # 50 komponen tambahan (lihat bars_extra.py).
    render_extra = EXTRA_BAR_RENDERERS.get(t)
    if render_extra:
        return render_extra(el)
    # 50 komponen paket "Pro" (lihat bars_pro.py).
    render_pro = PRO_BAR_RENDERERS.get(t)
    if render_pro:
        return render_pro(el)
    return ""


def describe_bar(el):
    """Deskripsi teks sebuah bar, dipakai oleh generator Prompt Master AI."""
    spec = BAR_SPECS[el["type"]]
    bits = []
    for field in spec["fields"]:
        k, label = field[0], field[1]
        val = str(el.get(k, "")).replace("\n", " / ")
        bits.append(f'{label}: "{val}"')
    note = "; item ber-format label|ikon memakai nama ikon Material Symbols" if spec.get("hint") else ""
    return "; ".join(bits) + note


def edit_bar_fields(el, key):
    """Widget Streamlit untuk mengedit properti sebuah bar di panel Properti."""
    spec = BAR_SPECS[el["type"]]
    for field in spec["fields"]:
        k, label, kind = field[0], field[1], field[2]
        extra = field[3] if len(field) > 3 else None
        wk = f"{key}_{k}"
        if kind == "text":
            el[k] = st.text_input(label, str(el.get(k, "")), key=wk)
        elif kind == "area":
            el[k] = st.text_area(label, str(el.get(k, "")), key=wk, height=120)
        elif kind == "int":
            lo, hi = extra
            el[k] = st.slider(label, lo, hi, clamp_int(el.get(k), lo, hi, lo), key=wk)
        elif kind == "float":
            lo, hi, step = extra
            try:
                cur = max(lo, min(hi, float(el.get(k, lo))))
            except (TypeError, ValueError):
                cur = lo
            el[k] = st.slider(label, float(lo), float(hi), float(cur), step=float(step), key=wk)
        elif kind == "sel":
            keys = list(extra)
            cur = el.get(k) if el.get(k) in keys else keys[0]
            el[k] = st.selectbox(label, keys, keys.index(cur), format_func=lambda v, e=extra: e[v], key=wk)
    if spec.get("hint"):
        st.caption(ICON_HINT)
