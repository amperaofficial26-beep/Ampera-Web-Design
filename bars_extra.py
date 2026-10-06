"""Renderer HTML untuk 50 komponen bar tambahan.

Spesifikasi (label, ikon, group, default, field editor) ada di bar_specs.py;
file ini hanya mengubah sebuah elemen menjadi HTML. Renderer didaftarkan di
EXTRA_BAR_RENDERERS dan dipakai otomatis oleh bars.render_bar().

Konvensi nama kelas CSS: tiap komponen memakai kelas induk sesuai tipe
(mis. `.pilltabs`) dan kelas anak berawalan pendek yang khas (mis. `.pl-item`),
lalu di-scope di css.py supaya tidak saling bertabrakan.
"""
from bar_specs import STATUS_ICONS, STATUS_KINDS
from config import INPUT_KINDS
from styles import soft_style
from utils import clamp_int, esc, lines_of, mi, parts_of, safe_url

AVATAR_FALLBACK = "#94a3b8"
VIEW_ALIGN = {"left": "flex-start", "center": "center", "right": "flex-end"}


def _sa(el, extra=""):
    """Atribut style inline dari gaya visual elemen (ditambah CSS tambahan)."""
    css = soft_style(el, extra)
    return f' style="{css}"' if css else ""


def _hex(value, fallback=AVATAR_FALLBACK):
    """Warna aman untuk atribut style (hanya #rgb / #rrggbb)."""
    text = str(value or "").strip()
    if len(text) in (4, 7) and text.startswith("#") and all(c in "0123456789abcdefABCDEF" for c in text[1:]):
        return text
    return fallback


def _initials(name):
    words = [w for w in str(name or "").replace("@", " ").split() if w]
    if not words:
        return "?"
    return (words[0][0] + (words[1][0] if len(words) > 1 else "")).upper()


def _avatar(url, name=""):
    """Isi bulatan avatar: foto bila ada URL, kalau tidak inisial nama."""
    url = str(url or "").strip()
    if url:
        return f'<img src="{esc(safe_url(url))}" alt="{esc(name)}">'
    return f"<span>{esc(_initials(name))}</span>"


def _ints(value, limit=40):
    """Baca deretan angka dipisah koma / titik koma (untuk grafik & gelombang)."""
    out = []
    for chunk in str(value or "").replace(";", ",").split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            out.append(max(0, int(float(chunk))))
        except ValueError:
            continue
        if len(out) >= limit:
            break
    return out


def _stars(value):
    out = ""
    for i in range(1, 6):
        if value >= i - 0.25:
            out += mi("star")
        elif value >= i - 0.75:
            out += mi("star_half")
        else:
            out += f'<span class="off">{mi("star")}</span>'
    return out


def _is_on(value):
    return str(value or "").strip().lower() in ("on", "1", "true", "ya", "yes", "aktif")


# ------------------------------- Navigasi ----------------------------------
def r_menubar(el):
    g = el.get
    rows = lines_of(g("items"))
    act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
    items = "".join(
        f'<a class="mb-item{" on" if i == act else ""}" href="#">{esc(lb)}</a>' for i, lb in enumerate(rows)
    )
    action = f'<a class="btn sm" href="#">{esc(g("action"))}</a>' if g("action") else ""
    return (f'<div class="bar menubar"{_sa(el)}>'
            f'<span class="mb-brand">{mi("apps")}</span>{items}{action}</div>')


def r_pilltabs(el):
    g = el.get
    rows = lines_of(g("items"))
    act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
    items = "".join(
        f'<a class="pl-item{" on" if i == act else ""}" href="#">{esc(lb)}</a>' for i, lb in enumerate(rows)
    )
    return f'<nav class="bar pilltabs"{_sa(el)}>{items}</nav>'


def r_railnav(el):
    g = el.get
    rows = parts_of(g("items"), 3)
    act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
    items = ""
    for i, (label, icon, badge) in enumerate(rows):
        dot = f'<span class="rn-badge">{esc(badge)}</span>' if badge else ""
        items += (f'<a class="rn-item{" on" if i == act else ""}" href="#">'
                  f'<span class="rn-ico">{mi(icon or "circle")}{dot}</span>'
                  f'<span class="rn-lbl">{esc(label)}</span></a>')
    return f'<nav class="bar railnav"{_sa(el)}>{items}</nav>'


def r_backbar(el):
    g = el.get
    action = ""
    if g("action"):
        action = (f'<a class="bb-action" href="#">{mi(g("icon") or "more_horiz")}'
                  f'<span>{esc(g("action"))}</span></a>')
    return (f'<div class="bar backbar"{_sa(el)}>'
            f'<a class="bb-back" href="#">{mi("arrow_back")}<span>{esc(g("back", ""))}</span></a>'
            f'<strong class="bb-title">{esc(g("title", ""))}</strong>{action}</div>')


def r_anchorlinks(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
    items = "".join(
        f'<a class="an-item{" on" if i == act else ""}" href="{esc(safe_url(url))}">{esc(lb)}</a>'
        for i, (lb, url) in enumerate(rows)
    )
    return f'<nav class="bar anchorlinks"{_sa(el)}>{items}</nav>'


def r_prevnext(el):
    g = el.get

    def card(direction, label, note):
        if not label:
            return '<span class="pn-gap"></span>'
        text = f'<strong>{esc(label)}</strong><small>{esc(note)}</small>' if note else f'<strong>{esc(label)}</strong>'
        arrow = mi("arrow_back" if direction == "prev" else "arrow_forward")
        body = f'{arrow}<span class="pn-text">{text}</span>' if direction == "prev" else f'<span class="pn-text">{text}</span>{arrow}'
        return f'<a class="pn-card {direction}" href="#">{body}</a>'

    return (f'<nav class="bar prevnext"{_sa(el)}>'
            f'{card("prev", g("prev"), g("prev_note"))}{card("next", g("next"), g("next_note"))}</nav>')


def r_meganav(el):
    g = el.get
    rows = parts_of(g("items"), 3)
    cards = "".join(
        f'<a class="mg-item" href="#"><span class="mg-ico">{mi(ic or "chevron_right")}</span>'
        f'<span class="mg-text"><strong>{esc(title)}</strong><small>{esc(note)}</small></span></a>'
        for title, note, ic in rows
    )
    head = f'<div class="mg-title">{esc(g("title", ""))}</div>' if g("title") else ""
    return f'<nav class="bar meganav"{_sa(el)}>{head}<div class="mg-grid">{cards}</div></nav>'


# --------------------------------- Aksi ------------------------------------
def r_actionbar(el):
    g = el.get
    note = f'<span class="ab-note">{esc(g("note", ""))}</span>' if g("note") else ""
    second = f'<button type="button" class="btn ghost sm">{esc(g("secondary"))}</button>' if g("secondary") else ""
    first = f'<button type="button" class="btn sm">{esc(g("primary"))}</button>' if g("primary") else ""
    return f'<div class="bar actionbar"{_sa(el)}>{note}<span class="ab-btns">{second}{first}</span></div>'


def r_commandbar(el):
    g = el.get
    key = f'<kbd class="cb-kbd">{esc(g("hint"))}</kbd>' if g("hint") else ""
    return (f'<div class="bar commandbar"{_sa(el)}>{mi(g("icon") or "search")}'
            f'<input type="text" placeholder="{esc(g("placeholder", ""))}" aria-label="Perintah atau pencarian">'
            f'{key}</div>')


def r_sortbar(el):
    g = el.get
    options = lines_of(g("options"))
    act = clamp_int(g("active"), 1, max(1, len(options)), 1) - 1
    current = options[act] if options else ""
    view = g("view") if g("view") in ("grid", "list") else "grid"
    grid_on = " on" if view == "grid" else ""
    list_on = " on" if view == "list" else ""
    return (f'<div class="bar sortbar"{_sa(el)}><span class="sr-label">{esc(g("label", ""))}</span>'
            f'<button type="button" class="sr-select">{esc(current)}{mi("expand_more")}</button>'
            f'<span class="sr-views">'
            f'<button type="button" class="sr-view{grid_on}" aria-label="Tampilan grid">{mi("grid_view")}</button>'
            f'<button type="button" class="sr-view{list_on}" aria-label="Tampilan daftar">{mi("view_list")}</button>'
            f'</span></div>')


def r_sharebar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    items = "".join(
        f'<button type="button" class="sh-btn" title="{esc(lb)}">{mi(ic or "link")}<span>{esc(lb)}</span></button>'
        for lb, ic in rows
    )
    label = f'<span class="sh-label">{esc(g("label", ""))}</span>' if g("label") else ""
    return f'<div class="bar sharebar"{_sa(el)}>{label}<span class="sh-items">{items}</span></div>'


def r_commentbar(el):
    g = el.get
    hint = f'<small class="cm-hint">{esc(g("hint", ""))}</small>' if g("hint") else ""
    return (f'<div class="bar commentbar"{_sa(el)}>'
            f'<span class="avatar sm">{_avatar(g("avatar"), "Kamu")}</span>'
            f'<input type="text" placeholder="{esc(g("placeholder", ""))}" aria-label="Komentar">'
            f'<button type="button" class="btn sm">{esc(g("button", ""))}</button>{hint}</div>')


def r_quickactions(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    items = "".join(
        f'<button type="button" class="qa-item"><span class="qa-ico">{mi(ic or "apps")}</span>{esc(lb)}</button>'
        for lb, ic in rows
    )
    return f'<div class="bar quickactions"{_sa(el)}>{items}</div>'


def r_linkbar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    align = g("align") if g("align") in VIEW_ALIGN else "center"
    items = "".join(
        f'<a class="lk-item" href="{esc(safe_url(url))}">{esc(lb)}</a>' for lb, url in rows
    )
    return f'<nav class="bar linkbar"{_sa(el, f"justify-content:{VIEW_ALIGN[align]};")}>{items}</nav>'


# ------------------------------ Informasi ----------------------------------
def r_infobanner(el):
    g = el.get
    kind = g("kind") if g("kind") in STATUS_KINDS else "info"
    link = ""
    if g("link_text"):
        link = f'<a href="{esc(safe_url(g("link", "#")))}">{esc(g("link_text"))}</a>'
    title = f'<strong>{esc(g("title", ""))}</strong>' if g("title") else ""
    return (f'<div class="bar infobanner {kind}"{_sa(el)}><span class="ib-ico">{mi(STATUS_ICONS[kind])}</span>'
            f'<div class="ib-text">{title}<span>{esc(g("text", ""))}</span></div>{link}</div>')


def r_tipbar(el):
    g = el.get
    label = f'<span class="tp-label">{esc(g("title", ""))}</span>' if g("title") else ""
    btn = f'<button type="button" class="btn ghost sm">{esc(g("dismiss"))}</button>' if g("dismiss") else ""
    return (f'<div class="bar tipbar"{_sa(el)}>{mi("lightbulb")}'
            f'<div class="tp-text">{label}<span>{esc(g("text", ""))}</span></div>{btn}</div>')


def r_quotebar(el):
    g = el.get
    who = ""
    if g("author") or g("role"):
        who = f'<footer>— {esc(g("author", ""))}<small>{esc(g("role", ""))}</small></footer>'
    return (f'<blockquote class="bar quotebar"{_sa(el)}>{mi("format_quote")}'
            f'<p>{esc(g("text", ""))}</p>{who}</blockquote>')


def r_totalbar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    lines = "".join(
        f'<div class="tt-row"><span>{esc(lb)}</span><span>{esc(val)}</span></div>' for lb, val in rows
    )
    return (f'<div class="bar totalbar"{_sa(el)}>{lines}'
            f'<div class="tt-row tt-total"><span>{esc(g("total_label", ""))}</span>'
            f'<strong>{esc(g("total", ""))}</strong></div></div>')


def r_countdownbar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    boxes = "".join(
        f'<span class="cd-box"><strong>{esc(val)}</strong><small>{esc(unit)}</small></span>' for val, unit in rows
    )
    label = f'<span class="cd-label">{esc(g("label", ""))}</span>' if g("label") else ""
    return f'<div class="bar countdownbar"{_sa(el)}>{label}<span class="cd-set">{boxes}</span></div>'


def r_stockbar(el):
    g = el.get
    status = g("status") if g("status") in ("ready", "low", "out") else "ready"
    value = clamp_int(g("value"), 0, 100, 0)
    note = f'<small class="sk-note">{esc(g("note", ""))}</small>' if g("note") else ""
    return (f'<div class="bar stockbar {status}"{_sa(el)}><span class="sk-dot"></span>'
            f'<div class="sk-body"><strong>{esc(g("label", ""))}</strong>'
            f'<div class="sk-track"><span style="width:{value}%"></span></div>{note}</div></div>')


def r_livebar(el):
    g = el.get
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar livebar"{_sa(el)}><span class="lv-badge"><span class="lv-dot"></span>LIVE</span>'
            f'<div class="lv-text"><strong>{esc(g("title", ""))}</strong>'
            f'<small>{mi("visibility")}{esc(g("viewers", ""))}</small></div>{btn}</div>')


# --------------------------------- Data ------------------------------------
def r_tablebar(el):
    g = el.get
    cols = parts_of(g("columns"), 2)
    if not cols:
        return f'<div class="bar tablebar"{_sa(el)}></div>'
    head = "".join(
        f'<th style="width:{clamp_int(w, 5, 100, 33)}%">{esc(title)}</th>' for title, w in cols
    )
    values = [c.strip() for c in str(g("row", "")).split("|")]
    cells = "".join(f'<td>{esc(values[i] if i < len(values) else "")}</td>' for i in range(len(cols)))
    return (f'<div class="bar tablebar"{_sa(el)}><table><thead><tr>{head}</tr></thead>'
            f"<tbody><tr>{cells}</tr></tbody></table></div>")


def r_comparebar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    bars = ""
    for i, (label, value) in enumerate(rows):
        val = clamp_int(value, 0, 100, 0)
        alt = " alt" if i % 2 else ""
        bars += (f'<div class="cp-row"><span class="cp-label">{esc(label)}</span>'
                 f'<span class="cp-track"><span class="cp-fill{alt}" style="width:{val}%"></span></span>'
                 f'<strong>{val}%</strong></div>')
    title = f'<div class="cp-title">{esc(g("title", ""))}</div>' if g("title") else ""
    note = f'<small class="cp-note">{esc(g("caption", ""))}</small>' if g("caption") else ""
    return f'<div class="bar comparebar"{_sa(el)}>{title}{bars}{note}</div>'


def r_sparkbar(el):
    g = el.get
    values = _ints(g("values"))
    top = max(values) if values else 1
    bars = "".join(
        f'<span class="sp-bar{" last" if i == len(values) - 1 else ""}" '
        f'style="height:{max(6, round(v * 100 / top))}%"></span>'
        for i, v in enumerate(values)
    )
    label = f'<span class="sp-label">{esc(g("label", ""))}</span>' if g("label") else ""
    note = f'<small class="sp-note">{esc(g("caption", ""))}</small>' if g("caption") else ""
    return f'<div class="bar sparkbar"{_sa(el)}>{label}<span class="sp-chart">{bars}</span>{note}</div>'


def r_legendbar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    items = "".join(
        f'<span class="lg-item"><span class="lg-dot" style="background:{_hex(color)}"></span>{esc(lb)}</span>'
        for lb, color in rows
    )
    title = f'<span class="lg-title">{esc(g("title", ""))}</span>' if g("title") else ""
    return f'<div class="bar legendbar"{_sa(el)}>{title}{items}</div>'


def r_timelinebar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    cur = clamp_int(g("current"), 1, max(1, len(rows)), 1)
    steps = ""
    for i, (label, time) in enumerate(rows, start=1):
        state = "done" if i < cur else ("now" if i == cur else "")
        dot = mi("check") if i < cur else str(i)
        steps += (f'<div class="tl-step {state}"><span class="tl-dot">{dot}</span>'
                  f'<strong>{esc(label)}</strong><small>{esc(time)}</small></div>')
    return f'<div class="bar timelinebar"{_sa(el)}>{steps}</div>'


def r_rangebar(el):
    g = el.get
    low = clamp_int(g("low"), 0, 100, 0)
    high = clamp_int(g("high"), 0, 100, 100)
    if low > high:
        low, high = high, low
    return (f'<div class="bar rangebar"{_sa(el)}><div class="rg-head"><span>{esc(g("label", ""))}</span>'
            f'<strong>{low}% – {high}%</strong></div>'
            f'<div class="rg-track"><span class="rg-fill" style="left:{low}%;width:{high - low}%"></span>'
            f'<span class="rg-knob" style="left:{low}%"></span><span class="rg-knob" style="left:{high}%"></span></div>'
            f'<div class="rg-labels"><small>{esc(g("min_label", ""))}</small>'
            f'<small>{esc(g("max_label", ""))}</small></div></div>')


def r_calendarstrip(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
    days = "".join(
        f'<button type="button" class="cs-day{" on" if i == act else ""}">'
        f'<small>{esc(day)}</small><strong>{esc(num)}</strong></button>'
        for i, (day, num) in enumerate(rows)
    )
    return f'<div class="bar calendarstrip"{_sa(el)}>{days}</div>'


# -------------------------------- Formulir ---------------------------------
def r_formbar(el):
    g = el.get
    kind = g("kind") if g("kind") in INPUT_KINDS else "text"
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<label class="bar formbar"{_sa(el)}><span class="fm-label">{esc(g("label", ""))}</span>'
            f'<span class="fm-row"><input type="{kind}" placeholder="{esc(g("placeholder", ""))}">{btn}</span></label>')


def r_newsletterbar(el):
    g = el.get
    note = f'<small class="nl-note">{esc(g("note", ""))}</small>' if g("note") else ""
    return (f'<div class="bar newsletterbar"{_sa(el)}>{mi("mark_email_read")}'
            f'<div class="nl-text"><strong>{esc(g("title", ""))}</strong>{note}</div>'
            f'<span class="nl-form"><input type="email" placeholder="{esc(g("placeholder", ""))}" aria-label="Email">'
            f'<button type="button" class="btn sm">{esc(g("button", ""))}</button></span></div>')


def r_otpbar(el):
    g = el.get
    digits = clamp_int(g("digits"), 4, 8, 6)
    boxes = "".join(f'<span class="ot-box{" on" if i == 0 else ""}"></span>' for i in range(digits))
    note = f'<small class="ot-note">{esc(g("note", ""))}</small>' if g("note") else ""
    return (f'<div class="bar otpbar"{_sa(el)}><span class="ot-label">{esc(g("label", ""))}</span>'
            f'<span class="ot-set">{boxes}</span>{note}</div>')


def r_tagsinputbar(el):
    g = el.get
    tags = "".join(f'<span class="tg-chip">{esc(tag)}{mi("close")}</span>' for tag in lines_of(g("tags")))
    btn = f'<button type="button" class="btn ghost sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar tagsinputbar"{_sa(el)}><span class="tg-set">{tags}'
            f'<input type="text" placeholder="{esc(g("placeholder", ""))}" aria-label="Tambah tag"></span>{btn}</div>')


def r_sliderbar(el):
    g = el.get
    value = clamp_int(g("value"), 0, 100, 0)
    unit = esc(str(g("unit", "") or ""))
    extra = f"{value}{unit}"
    return (f'<div class="bar sliderbar"{_sa(el)}><div class="sl-head"><span>{esc(g("label", ""))}</span>'
            f'<strong>{extra}</strong></div>'
            f'<div class="sl-track"><span class="sl-fill" style="width:{value}%"></span>'
            f'<span class="sl-knob" style="left:{value}%"></span></div>'
            f'<div class="sl-labels"><small>{esc(g("min_label", ""))}</small>'
            f'<small>{esc(g("max_label", ""))}</small></div></div>')


def r_switchbar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    items = "".join(
        f'<label class="sw-row"><span>{esc(label)}</span>'
        f'<span class="sw-track{" on" if _is_on(state) else ""}"><span class="sw-knob"></span></span></label>'
        for label, state in rows
    )
    return f'<div class="bar switchbar"{_sa(el)}>{items}</div>'


def r_loginbar(el):
    g = el.get
    note = f'<a class="lg-note" href="#">{esc(g("note", ""))}</a>' if g("note") else ""
    return (f'<div class="bar loginbar"{_sa(el)}><strong>{esc(g("title", ""))}</strong>'
            f'<input type="email" value="{esc(g("user", ""))}" aria-label="Email">'
            f'<input type="password" placeholder="{esc(g("placeholder", ""))}" aria-label="Kata sandi">'
            f'<button type="button" class="btn sm">{esc(g("button", ""))}</button>{note}</div>')


# --------------------------------- Media -----------------------------------
def r_playbar(el):
    g = el.get
    value = clamp_int(g("value"), 0, 100, 0)
    playing = g("playing") if g("playing") in ("play", "pause") else "pause"
    play_icon = "pause" if playing == "pause" else "play_arrow"
    return (f'<div class="bar playbar"{_sa(el)}><span class="pb-cover">{mi("music_note")}</span>'
            f'<div class="pb-body">'
            f'<div class="pb-head"><span class="pb-title"><strong>{esc(g("title", ""))}</strong>'
            f'<small>{esc(g("artist", ""))}</small></span>'
            f'<span class="pb-times"><small>{esc(g("current", ""))}</small>'
            f'<small>{esc(g("duration", ""))}</small></span></div>'
            f'<div class="pb-track"><span style="width:{value}%"></span></div>'
            f'<div class="pb-ctrl">{mi("shuffle")}{mi("skip_previous")}'
            f'<button type="button" class="pb-play" aria-label="Putar atau jeda">{mi(play_icon)}</button>'
            f'{mi("skip_next")}{mi("repeat")}</div></div></div>')


def r_storiesbar(el):
    g = el.get
    rows = parts_of(g("items"), 3)
    items = ""
    for label, url, badge in rows:
        dot = f'<span class="st-badge">{mi(badge)}</span>' if badge else ""
        plain = " plain" if badge else ""
        items += (f'<a class="st-item" href="#"><span class="st-ring{plain}">'
                  f'<span class="st-avatar">{_avatar(url, label)}</span>{dot}</span>'
                  f"<small>{esc(label)}</small></a>")
    return f'<div class="bar storiesbar"{_sa(el)}>{items}</div>'


def r_thumbstripbar(el):
    g = el.get
    urls = lines_of(g("items"))
    act = clamp_int(g("active"), 1, max(1, len(urls)), 1)
    items = "".join(
        f'<span class="ts-item{" on" if i + 1 == act else ""}">'
        f'<img src="{esc(safe_url(url))}" alt="Gambar mini {i + 1}"></span>'
        for i, url in enumerate(urls)
    )
    counter = f'<small class="ts-count">{act}/{len(urls)}</small>' if urls else ""
    return f'<div class="bar thumbstripbar"{_sa(el)}>{counter}<span class="ts-strip">{items}</span></div>'


def r_captionsbar(el):
    g = el.get
    badge = f'<span class="cc-badge">{esc(g("button", ""))}</span>' if g("button") else ""
    lang = f'<small class="cc-lang">{esc(g("lang", ""))}</small>' if g("lang") else ""
    return f'<div class="bar captionsbar"{_sa(el)}>{badge}<p>{esc(g("text", ""))}</p>{lang}</div>'


def r_recordbar(el):
    g = el.get
    wave = _ints(g("wave"))
    bars = "".join(f'<span style="height:{max(10, min(100, v * 5))}%"></span>' for v in wave)
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar recordbar"{_sa(el)}><span class="rc-dot"></span>'
            f'<span class="rc-label">{esc(g("label", ""))}</span>'
            f'<span class="rc-wave">{bars}</span>'
            f'<strong class="rc-time">{esc(g("time", ""))}</strong>{btn}</div>')


# -------------------------------- Sosial -----------------------------------
def r_reactionbar(el):
    g = el.get
    rows = parts_of(g("items"), 3)
    items = "".join(
        f'<button type="button" class="rx-btn" title="{esc(label)}">'
        f'{mi(icon or "favorite")}<span>{esc(count or "0")}</span></button>'
        for label, icon, count in rows
    )
    return f'<div class="bar reactionbar"{_sa(el)}>{items}</div>'


def r_userstackbar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    avatars = "".join(f'<span class="us-avatar">{_avatar(url, name)}</span>' for name, url in rows)
    count = f'<span class="us-avatar us-count">{esc(g("count"))}</span>' if g("count") else ""
    note = f'<small>{esc(g("note", ""))}</small>' if g("note") else ""
    return (f'<div class="bar userstackbar"{_sa(el)}><span class="us-set">{avatars}{count}</span>'
            f'<span class="us-note">{note}</span></div>')


def r_reviewbar(el):
    g = el.get
    try:
        value = max(0.0, min(5.0, float(g("rating", 0) or 0)))
    except (TypeError, ValueError):
        value = 0.0
    name = str(g("name", "") or "")
    when = f'<small class="rw-time">{esc(g("time", ""))}</small>' if g("time") else ""
    return (f'<div class="bar reviewbar"{_sa(el)}>'
            f'<span class="avatar sm">{_avatar(g("avatar"), name)}</span>'
            f'<div class="rw-body"><span class="rw-head"><strong>{esc(name)}</strong>{when}</span>'
            f'<span class="rw-stars" role="img" aria-label="{value:g} dari 5">{_stars(value)}</span>'
            f'<p>{esc(g("text", ""))}</p></div></div>')


def r_chatbar(el):
    g = el.get
    name = str(g("name", "") or "")
    when = f'<small class="ch-time">{esc(g("time", ""))}</small>' if g("time") else ""
    unread = f'<span class="ch-badge">{esc(g("unread"))}</span>' if g("unread") else ""
    return (f'<div class="bar chatbar"{_sa(el)}>'
            f'<span class="avatar sm">{_avatar(g("avatar"), name)}</span>'
            f'<div class="ch-body"><strong>{esc(name)}</strong><span>{esc(g("message", ""))}</span></div>'
            f'<span class="ch-side">{when}{unread}</span></div>')


def r_followbar(el):
    g = el.get
    name = str(g("name", "") or "")
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    note = f'<small class="fw-note">{esc(g("note", ""))}</small>' if g("note") else ""
    return (f'<div class="bar followbar"{_sa(el)}>'
            f'<span class="avatar sm">{_avatar(g("avatar"), name)}</span>'
            f'<div class="fw-body"><strong>{esc(name)}</strong>'
            f'<small>{esc(g("handle", ""))}</small>{note}</div>{btn}</div>')


# --------------------------------- Toko ------------------------------------
def r_cartbar(el):
    g = el.get
    count = clamp_int(g("count"), 0, 99, 0)
    badge = f'<span class="ct-badge">{count}</span>' if count else ""
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar cartbar"{_sa(el)}><span class="ct-ico">{mi("shopping_cart")}{badge}</span>'
            f'<div class="ct-text"><strong>{esc(g("label", ""))}</strong>'
            f'<small>{esc(g("total", ""))}</small></div>{btn}</div>')


def r_couponbar(el):
    g = el.get
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    expires = f'<small class="cu-exp">{esc(g("expires", ""))}</small>' if g("expires") else ""
    return (f'<div class="bar couponbar"{_sa(el)}><span class="cu-ico">{mi("confirmation_number")}</span>'
            f'<div class="cu-text"><span class="cu-code">{esc(g("code", ""))}{mi("content_copy")}</span>'
            f'<small>{esc(g("note", ""))}</small>{expires}</div>{btn}</div>')


def r_shippingbar(el):
    g = el.get
    value = clamp_int(g("value"), 0, 100, 0)
    return (f'<div class="bar shippingbar"{_sa(el)}>{mi("local_shipping")}'
            f'<div class="hp-body"><span class="hp-label">{esc(g("label", ""))}</span>'
            f'<div class="hp-track"><span style="width:{value}%"></span></div>'
            f'<span class="hp-labels"><small>{esc(g("min_label", ""))}</small>'
            f'<small>{esc(g("max_label", ""))}</small></span></div></div>')


def r_productbar(el):
    g = el.get
    old = f'<s>{esc(g("old_price"))}</s>' if g("old_price") else ""
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    note = f'<small>{esc(g("note", ""))}</small>' if g("note") else ""
    return (f'<div class="bar productbar"{_sa(el)}>'
            f'<span class="pd-thumb"><img src="{esc(safe_url(g("image")))}" alt="{esc(g("name", ""))}"></span>'
            f'<div class="pd-text"><strong>{esc(g("name", ""))}</strong>{note}'
            f'<span class="pd-price">{esc(g("price", ""))}{old}</span></div>{btn}</div>')


def r_paymentbar(el):
    g = el.get
    rows = parts_of(g("items"), 3)
    act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
    items = ""
    for i, (name, note, icon) in enumerate(rows):
        on = i == act
        items += (f'<label class="py-row{" on" if on else ""}">'
                  f'<span class="py-ico">{mi(icon or "credit_card")}</span>'
                  f'<span class="py-text"><strong>{esc(name)}</strong><small>{esc(note)}</small></span>'
                  f'<span class="py-check">{mi("check_circle") if on else ""}</span></label>')
    caption = f'<small class="py-note">{esc(g("note", ""))}</small>' if g("note") else ""
    return f'<div class="bar paymentbar"{_sa(el)}>{items}{caption}</div>'


# Peta tipe -> fungsi render (dipakai bars.render_bar).
EXTRA_BAR_RENDERERS = {
    # Navigasi
    "menubar": r_menubar,
    "pilltabs": r_pilltabs,
    "railnav": r_railnav,
    "backbar": r_backbar,
    "anchorlinks": r_anchorlinks,
    "prevnext": r_prevnext,
    "meganav": r_meganav,
    # Aksi
    "actionbar": r_actionbar,
    "commandbar": r_commandbar,
    "sortbar": r_sortbar,
    "sharebar": r_sharebar,
    "commentbar": r_commentbar,
    "quickactions": r_quickactions,
    "linkbar": r_linkbar,
    # Informasi
    "infobanner": r_infobanner,
    "tipbar": r_tipbar,
    "quotebar": r_quotebar,
    "totalbar": r_totalbar,
    "countdownbar": r_countdownbar,
    "stockbar": r_stockbar,
    "livebar": r_livebar,
    # Data
    "tablebar": r_tablebar,
    "comparebar": r_comparebar,
    "sparkbar": r_sparkbar,
    "legendbar": r_legendbar,
    "timelinebar": r_timelinebar,
    "rangebar": r_rangebar,
    "calendarstrip": r_calendarstrip,
    # Formulir
    "formbar": r_formbar,
    "newsletterbar": r_newsletterbar,
    "otpbar": r_otpbar,
    "tagsinputbar": r_tagsinputbar,
    "sliderbar": r_sliderbar,
    "switchbar": r_switchbar,
    "loginbar": r_loginbar,
    # Media
    "playbar": r_playbar,
    "storiesbar": r_storiesbar,
    "thumbstripbar": r_thumbstripbar,
    "captionsbar": r_captionsbar,
    "recordbar": r_recordbar,
    # Sosial
    "reactionbar": r_reactionbar,
    "userstackbar": r_userstackbar,
    "reviewbar": r_reviewbar,
    "chatbar": r_chatbar,
    "followbar": r_followbar,
    # Toko
    "cartbar": r_cartbar,
    "couponbar": r_couponbar,
    "shippingbar": r_shippingbar,
    "productbar": r_productbar,
    "paymentbar": r_paymentbar,
}
