"""Renderer HTML untuk 50 komponen bar paket "Pro".

Spesifikasinya ada di bar_specs_pro.py, CSS-nya di css_pro.py. Fungsi di sini
didaftarkan pada PRO_BAR_RENDERERS dan otomatis dipakai bars.render_bar()
(bars.py memeriksa EXTRA_BAR_RENDERERS lalu PRO_BAR_RENDERERS).

Konvensi kelas CSS: setiap komponen punya kelas induk sesuai tipe (mis.
`.appbar`) dan kelas anak berawalan pendek yang khas (mis. `.apb-text`)
supaya tidak bertabrakan dengan komponen lain.
"""
from bars_extra import (
    _avatar as avatar_html,
    _hex as safe_hex,
    _ints as int_list,
    _sa as style_attr,
    _stars as stars_html,
)
from utils import clamp_int, esc, lines_of, mi, parts_of, safe_url

TONE_BY_STATUS = {
    # metrik & kesehatan
    "safe": "safe", "warning": "warning", "danger": "danger",
    # tren
    "up": "safe", "down": "danger", "flat": "muted",
    # pesanan
    "pending": "warning", "packed": "info", "shipped": "info", "done": "safe",
    # anggaran
    "over": "danger",
    # tagihan
    "due": "warning", "paid": "safe", "late": "danger",
    # kehadiran
    "in": "safe", "out": "muted",
    # tempat
    "open": "safe", "closed": "danger", "busy": "warning",
    # uang
    "out_money": "danger", "in_money": "safe",
}
DONUT_FALLBACK = ["#6366f1", "#f59e0b", "#22c55e", "#ef4444", "#0ea5e9", "#a855f7"]
GAUGE_TONE = {"safe": "#22c55e", "warning": "#f59e0b", "danger": "#ef4444"}


def _pill(text, tone="muted"):
    """Label kecil berwarna untuk status."""
    return f'<span class="pill chip-{esc(tone)}">{esc(text)}</span>'


def _tone(status):
    return TONE_BY_STATUS.get(str(status or "").strip().lower(), "muted")


def _pct(value):
    return clamp_int(value, 0, 100, 0)


def _fill_bar(fill_class, value, tone_class=""):
    tone = f" {tone_class}" if tone_class else ""
    return (f'<span class="{fill_class}{tone}" style="width:{_pct(value)}%"></span>')


def _rows_to_pcts(rows):
    """Ubah daftar (nama, nilai) menjadi persentase terhadap nilai terbesar."""
    top = max([v for _, v in rows] + [1])
    return [(name, max(4, round(v * 100 / top))) for name, v in rows]


def _numbers(value, limit=24):
    return [max(0, min(999, n)) for n in int_list(value, limit)]


# ------------------------------- Navigasi ----------------------------------
def r_appbar(el):
    g = el.get
    back = (f'<a class="apb-back" href="#">{mi("arrow_back")}<span>{esc(g("back"))}</span></a>'
            if g("back") else "")
    icon = str(g("icon", "")).strip() or "more_vert"
    action = (f'<a class="apb-action" href="#">{esc(g("action"))}{mi(icon)}</a>'
              if g("action") else "")
    subtitle = f'<small>{esc(g("subtitle"))}</small>' if g("subtitle") else ""
    return (f'<div class="bar appbar"{style_attr(el)}>{back}'
            f'<span class="apb-text"><strong>{esc(g("title", ""))}</strong>{subtitle}</span>'
            f'{action}</div>')


def r_quicknav(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
    items = "".join(
        f'<a class="qn-item{" on" if i == act else ""}" href="#">'
        f'<span class="qn-ico">{mi(icon or "circle")}</span><span>{esc(label)}</span></a>'
        for i, (label, icon) in enumerate(rows)
    )
    return f'<nav class="bar quicknav"{style_attr(el)}>{items}</nav>'


def r_subnav(el):
    g = el.get
    rows = lines_of(g("items"))
    act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
    items = "".join(
        f'<a class="sn-item{" on" if i == act else ""}" href="#">{esc(label)}</a>'
        for i, label in enumerate(rows)
    )
    return f'<nav class="bar subnav"{style_attr(el)}>{items}</nav>'


def r_stepdots(el):
    g = el.get
    total = clamp_int(g("total"), 1, 12, 5)
    cur = clamp_int(g("current"), 1, total, 1)
    dots = "".join(
        f'<span class="sd-dot{" done" if i < cur else (" on" if i == cur else "")}"></span>'
        for i in range(1, total + 1)
    )
    label = f'<span class="sd-label">{esc(g("label"))}</span>' if g("label") else ""
    return (f'<div class="bar stepdots" role="group" aria-label="Langkah {cur} dari {total}"{style_attr(el)}>'
            f'<span class="sd-dots">{dots}</span>{label}</div>')


def r_swipenav(el):
    g = el.get
    prev = f'<a class="sw-nav" href="#">{mi("chevron_left")}{esc(g("prev"))}</a>' if g("prev") else ""
    nxt = f'<a class="sw-nav" href="#">{esc(g("next"))}{mi("chevron_right")}</a>' if g("next") else ""
    return (f'<div class="bar swipenav"{style_attr(el)}>{prev}'
            f'<span class="sw-label">{esc(g("label", ""))}</span>{nxt}</div>')


# --------------------------------- Aksi ------------------------------------
def r_bulkactionbar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    actions = "".join(
        f'<button type="button" class="bk-btn{" danger" if icon in ("delete", "block", "report") else ""}">'
        f'{mi(icon or "bolt")}<span>{esc(label)}</span></button>'
        for label, icon in rows
    )
    all_note = f'<a class="bk-all" href="#">{esc(g("select_all"))}</a>' if g("select_all") else ""
    return (f'<div class="bar bulkactionbar" role="toolbar"{style_attr(el)}>'
            f'<span class="bk-count">{mi("check_circle")}{esc(g("count"))} dipilih</span>{all_note}'
            f'<span class="bk-actions">{actions}</span></div>')


def r_exportbar(el):
    g = el.get
    rows = lines_of(g("formats"))
    act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
    formats = "".join(
        f'<span class="ex-fmt{" on" if i == act else ""}">{esc(name)}</span>' for i, name in enumerate(rows)
    )
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar exportbar"{style_attr(el)}>{mi("file_download")}'
            f'<span class="ex-label">{esc(g("label", ""))}</span>'
            f'<span class="ex-formats">{formats}</span>{btn}</div>')


def r_approvalbar(el):
    g = el.get
    yes = f'<button type="button" class="btn sm">{esc(g("approve"))}</button>' if g("approve") else ""
    no = f'<button type="button" class="btn ghost sm">{esc(g("reject"))}</button>' if g("reject") else ""
    note = f'<small>{esc(g("note"))}</small>' if g("note") else ""
    return (f'<div class="bar approvalbar"{style_attr(el)}>'
            f'<div class="apv-head"><span class="apv-ico">{mi("approval")}</span>'
            f'<span class="apv-text"><strong>{esc(g("title", ""))}</strong>{note}</span></div>'
            f'<div class="apv-actions">{no}{yes}</div></div>')


def r_printbar(el):
    g = el.get
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    copies = f'{clamp_int(g("copies"), 1, 20, 1)} salinan'
    size = str(g("size", "")).strip()
    meta = " · ".join([p for p in (size, copies) if p])
    return (f'<div class="bar printbar"{style_attr(el)}><span class="pr-ico">{mi("print")}</span>'
            f'<span class="pr-text"><strong>{esc(g("label", ""))}</strong><small>{esc(meta)}</small></span>'
            f'{btn}</div>')


# ------------------------------ Informasi ----------------------------------
def r_weatherbar(el):
    g = el.get
    icon = str(g("icon", "")).strip() or "wb_sunny"
    note = f'<small>{esc(g("note"))}</small>' if g("note") else ""
    rng = " · ".join([p for p in (str(g("high", "")).strip(), str(g("low", "")).strip()) if p])
    rng_html = f'<span class="wt-range">{mi("thermostat")}{esc(rng)}</span>' if rng else ""
    return (f'<div class="bar weatherbar"{style_attr(el)}><span class="wt-ico">{mi(icon)}</span>'
            f'<span class="wt-main"><strong>{esc(g("temp", ""))}</strong>'
            f'<small>{esc(g("place", ""))} · {esc(g("note", ""))}</small></span>'
            f'{rng_html}</div>')


def r_notificationbar(el):
    g = el.get
    unread = str(g("unread", "")).strip()
    badge = f'<span class="nt-badge">{esc(unread)}</span>' if unread else ""
    time = f'<small>{esc(g("time"))}</small>' if g("time") else ""
    return (f'<div class="bar notificationbar"{style_attr(el)}>'
            f'<span class="nt-ico">{mi("notifications")}{badge}</span>'
            f'<span class="nt-text"><small>{esc(g("app", ""))}</small>'
            f'<strong>{esc(g("title", ""))}</strong>{time}</span>'
            f'<span class="nt-go">{mi("chevron_right")}</span></div>')


def r_metricbar(el):
    g = el.get
    status = str(g("status", "")).strip().lower()
    trend = str(g("trend", "")).strip().lower()
    trend_icon = {"up": "trending_up", "down": "trending_down"}.get(trend, "trending_flat")
    tag = _pill({"safe": "Aman", "warning": "Perlu perhatian", "danger": "Kritis"}.get(status, "Aman"), _tone(status))
    note = f'<small>{esc(g("note"))}</small>' if g("note") else ""
    return (f'<div class="bar metricbar"{style_attr(el)}>'
            f'<span class="mt-ico">{mi("sensors")}</span>'
            f'<span class="mt-text"><small>{esc(g("label", ""))}</small>'
            f'<span class="mt-line"><strong>{esc(g("value", ""))}</strong>'
            f'<em class="mt-delta tone-{_tone(trend)}">{mi(trend_icon)}{esc(g("delta", ""))}</em></span>'
            f'{note}</span>{tag}</div>')


def r_updatebar(el):
    g = el.get
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    size = f' · {esc(g("size"))}' if g("size") else ""
    return (f'<div class="bar updatebar"{style_attr(el)}><span class="up-ico">{mi("system_update")}</span>'
            f'<span class="up-text"><strong>{esc(g("version", ""))}{size}</strong>'
            f'<small>{esc(g("note", ""))}</small></span>{btn}</div>')


# --------------------------------- Data ------------------------------------
def r_donutbar(el):
    g = el.get
    rows = parts_of(g("items"), 3)
    total = 0
    segments, legend, stops = [], [], []
    for i, (name, value, color) in enumerate(rows):
        val = _pct(value)
        total += val
        color = safe_hex(color, DONUT_FALLBACK[i % len(DONUT_FALLBACK)])
        segments.append((color, val))
        legend.append(f'<span class="dn-item"><span class="dn-dot" style="background:{color}"></span>'
                      f'{esc(name)}<strong>{val}%</strong></span>')
    if total <= 0:
        segments = [("#e5e7eb", 100)]
    scale = 100 / max(1, total)
    at = 0.0
    for color, val in segments:
        span = val * scale
        stops.append(f"{color} {at:.2f}% {at + span:.2f}%")
        at += span
    caption = f'<small class="dn-caption">{esc(g("caption"))}</small>' if g("caption") else ""
    return (f'<div class="bar donutbar"{style_attr(el)}>'
            f'<span class="dn-chart" style="background:conic-gradient({";".join(stops)})">'
            f'<span class="dn-hole">{mi("donut_large")}</span></span>'
            f'<span class="dn-list"><strong>{esc(g("label", ""))}</strong>{"".join(legend)}{caption}</span></div>')


def r_gaugebar(el):
    g = el.get
    value = _pct(g("value"))
    tone = "safe" if value < 70 else ("warning" if value < 90 else "danger")
    return (f'<div class="bar gaugebar"{style_attr(el)}>'
            f'<div class="gg-head"><span>{esc(g("label", ""))}</span>'
            f'<strong>{value}{esc(g("unit", ""))}</strong></div>'
            f'<div class="gg-track">{_fill_bar("gg-fill", value, tone)}</div>'
            f'<div class="gg-labels"><small>{esc(g("min_label", ""))}</small>'
            f'<small>{esc(g("max_label", ""))}</small></div></div>')


def r_rankingbar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    top = max([clamp_int(v, 0, 9999, 0) for _, v in rows] + [1])
    items = ""
    for i, (name, value) in enumerate(rows):
        val = clamp_int(value, 0, 9999, 0)
        width = max(6, round(val * 100 / top))
        items += (f'<div class="rk-row{" top" if i == 0 else ""}">'
                  f'<span class="rk-no">{i + 1}</span><span class="rk-name">{esc(name)}</span>'
                  f'<span class="rk-track"><span class="rk-fill" style="width:{width}%"></span></span>'
                  f'<strong class="rk-val">{val}</strong></div>')
    unit = f'<small class="rk-unit">{esc(g("unit"))}</small>' if g("unit") else ""
    return (f'<div class="bar rankingbar"{style_attr(el)}>'
            f'<div class="rk-head"><span class="rk-title">{esc(g("title", ""))}</span>{unit}</div>'
            f'{items}</div>')


def r_heatmapbar(el):
    g = el.get
    values = _numbers(g("values"))
    top = max(values + [1])
    cells = ""
    for v in values:
        alpha = 0.12 + 0.88 * (v / top)
        cells += f'<span class="hm-cell" style="background:rgba(99,102,241,{alpha:.2f})" title="{v}"></span>'
    caption = f'<small>{mi("trending_up")}{esc(g("caption"))}</small>' if g("caption") else ""
    return (f'<div class="bar heatmapbar"{style_attr(el)}><strong>{esc(g("label", ""))}</strong>'
            f'<span class="hm-grid">{cells}</span>'
            f'<span class="hm-foot">{caption}</span></div>')


def r_distributionbar(el):
    g = el.get
    rows = parts_of(g("items"), 3)
    segments, legend = [], []
    for i, (name, value, color) in enumerate(rows):
        val = _pct(value)
        color = safe_hex(color, DONUT_FALLBACK[i % len(DONUT_FALLBACK)])
        segments.append(f'<span class="ds-seg" style="width:{val}%;background:{color}"></span>')
        legend.append(f'<span class="ds-item"><span class="ds-dot" style="background:{color}"></span>'
                      f'{esc(name)} <strong>{val}%</strong></span>')
    caption = f'<small class="ds-caption">{esc(g("caption"))}</small>' if g("caption") else ""
    return (f'<div class="bar distributionbar"{style_attr(el)}><strong>{esc(g("label", ""))}</strong>'
            f'<span class="ds-track">{"".join(segments)}</span>'
            f'<span class="ds-legend">{"".join(legend)}</span>{caption}</div>')


def r_funnelbar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    top = max([clamp_int(v, 0, 100, 0) for _, v in rows] + [1])
    steps = ""
    for i, (name, value) in enumerate(rows):
        val = clamp_int(value, 0, 100, 0)
        width = max(8, round(val * 100 / top))
        steps += (f'<div class="fn-row"><span class="fn-name">{esc(name)}</span>'
                  f'<span class="fn-track"><span class="fn-fill" style="width:{width}%;opacity:{1 - i * 0.16:.2f}"></span>'
                  f'</span><strong class="fn-val">{val}</strong></div>')
    caption = f'<small class="fn-caption">{esc(g("caption"))}</small>' if g("caption") else ""
    return (f'<div class="bar funnelbar"{style_attr(el)}><strong>{esc(g("label", ""))}</strong>'
            f'{steps}{caption}</div>')


# ------------------------------- Formulir ----------------------------------
def r_uploadinputbar(el):
    g = el.get
    name = str(g("file", "")).strip()
    progress = _pct(g("progress"))
    file_row = (f'<span class="ui-file"><strong>{mi("description")}{esc(name)}</strong>'
                f'<small>{esc(g("note", ""))}</small></span>') if name else ""
    track = (f'<span class="ui-track">{_fill_bar("ui-fill", progress)}</span>' if name and progress else "")
    return (f'<div class="bar uploadinputbar"{style_attr(el)}>'
            f'<div class="ui-drop">{mi("cloud_upload")}'
            f'<span class="ui-text"><strong>{esc(g("label", ""))}</strong>'
            f'<small>{esc(g("note", ""))}</small></span>'
            f'<button type="button" class="btn sm">{esc(g("button", ""))}</button></div>'
            f'{file_row}{track}</div>')


def r_datepickerbar(el):
    g = el.get
    rows = lines_of(g("presets"))
    act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
    presets = "".join(
        f'<span class="dp-preset{" on" if i == act else ""}">{esc(name)}</span>' for i, name in enumerate(rows)
    )
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar datepickerbar"{style_attr(el)}>'
            f'<span class="dp-label">{mi("event")}{esc(g("label", ""))}</span>'
            f'<div class="dp-dates">'
            f'<span class="dp-field"><small>Mulai</small><strong>{esc(g("start", ""))}</strong></span>'
            f'<span class="dp-arrow">{mi("arrow_right_alt")}</span>'
            f'<span class="dp-field"><small>Selesai</small><strong>{esc(g("end", ""))}</strong></span></div>'
            f'<div class="dp-foot"><span class="dp-presets">{presets}</span>{btn}</div></div>')


def r_ratinginputbar(el):
    g = el.get
    value = clamp_int(g("value"), 0, 5, 0)
    stars = "".join(
        f'<span class="ri-star{" on" if i <= value else ""}">{mi("star")}</span>' for i in range(1, 6)
    )
    return (f'<div class="bar ratinginputbar" role="group"{style_attr(el)}>'
            f'<span class="ri-label">{esc(g("label", ""))}</span>'
            f'<span class="ri-stars">{stars}</span>'
            f'<span class="ri-labels"><small>{esc(g("low_label", ""))}</small>'
            f'<small>{esc(g("high_label", ""))}</small></span></div>')


def r_quantitybar(el):
    g = el.get
    value = clamp_int(g("value"), 0, 99, 1)
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    note = f'<small>{esc(g("note"))}</small>' if g("note") else ""
    return (f'<div class="bar quantitybar"{style_attr(el)}>'
            f'<span class="qt-text"><strong>{esc(g("label", ""))}</strong>{note}</span>'
            f'<span class="qt-ctrl"><button type="button" class="qt-btn">{mi("remove")}</button>'
            f'<span class="qt-val">{value}</span>'
            f'<button type="button" class="qt-btn">{mi("add")}</button></span>{btn}</div>')


def r_passstrengthbar(el):
    g = el.get
    level = clamp_int(g("value"), 1, 4, 1)
    tones = {1: "#ef4444", 2: "#f59e0b", 3: "#22c55e", 4: "#0ea5e9"}
    segs = "".join(
        f'<span class="ps-seg" style="background:{tones[level] if i < level else "rgba(128,128,128,.25)"}"></span>'
        for i in range(1, 5)
    )
    levels = lines_of(g("levels"))
    level_name = levels[level - 1] if len(levels) >= level else ""
    hints = "".join(
        f'<span class="ps-hint">{mi("check")}{esc(text)}</span>' for text in lines_of(g("hints"))
    )
    return (f'<div class="bar passstrengthbar"{style_attr(el)}>'
            f'<span class="ps-head"><strong>{esc(g("label", ""))}</strong>'
            f'<em style="color:{tones[level]}">{esc(level_name)}</em></span>'
            f'<span class="ps-bars">{segs}</span>'
            f'<span class="ps-hints">{hints}</span></div>')


# --------------------------------- Media -----------------------------------
def r_videobar(el):
    g = el.get
    thumb = str(g("thumb", "")).strip()
    inner = (f'<img src="{esc(safe_url(thumb))}" alt="{esc(g("title", ""))}">' if thumb
             else f'<span class="vd-empty">{mi("movie")}</span>')
    duration = f'<span class="vd-dur">{esc(g("duration"))}</span>' if g("duration") else ""
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    meta = " · ".join([p for p in (str(g("channel", "")).strip(), str(g("views", "")).strip()) if p])
    return (f'<div class="bar videobar"{style_attr(el)}>'
            f'<span class="vd-thumb">{inner}<span class="vd-play">{mi("play_arrow")}</span>{duration}</span>'
            f'<span class="vd-text"><strong>{esc(g("title", ""))}</strong>'
            f'<small>{esc(meta)}</small></span>{btn}</div>')


def r_equalizerbar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    bands = "".join(
        f'<span class="eq-band"><span class="eq-bar" style="height:{max(6, clamp_int(v, 0, 10, 0) * 10)}%"></span>'
        f'<small>{esc(label)}</small></span>'
        for label, v in rows
    )
    btn = f'<button type="button" class="btn ghost sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar equalizerbar"{style_attr(el)}>'
            f'<span class="eq-head">{mi("graphic_eq")}<strong>{esc(g("label", ""))}</strong>{btn}</span>'
            f'<span class="eq-bands">{bands}</span></div>')


def r_podcastbar(el):
    g = el.get
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    duration = f'<small>{mi("schedule")}{esc(g("duration"))}</small>' if g("duration") else ""
    return (f'<div class="bar podcastbar"{style_attr(el)}>'
            f'<span class="pc-ico">{mi("podcasts")}</span>'
            f'<span class="pc-text"><small>{esc(g("show", ""))}</small>'
            f'<strong>{esc(g("episode", ""))}</strong>{duration}</span>{btn}</div>')


def r_camerabar(el):
    g = el.get
    rows = lines_of(g("modes"))
    act = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
    modes = "".join(
        f'<span class="cm-mode{" on" if i == act else ""}">{esc(name)}</span>' for i, name in enumerate(rows)
    )
    flash = str(g("flash", "")).strip() or "flash_on"
    return (f'<div class="bar camerabar"{style_attr(el)}>'
            f'<span class="cm-modes">{modes}</span>'
            f'<span class="cm-main"><span class="cm-side">{mi("photo_library")}</span>'
            f'<span class="cm-shutter"></span>'
            f'<span class="cm-side">{mi(flash)}</span></span>'
            f'<span class="cm-note">{esc(g("note", ""))}</span></div>')


def r_lyricsbar(el):
    g = el.get
    rows = lines_of(g("lines"))
    act = clamp_int(g("active"), 1, max(1, len(rows)), 1)
    lines = "".join(
        f'<span class="ly-line{" on" if i == act else ""}">{esc(text)}</span>'
        for i, text in enumerate(rows, start=1)
    )
    note = f'<small class="ly-note">{mi("sync")}{esc(g("note"))}</small>' if g("note") else ""
    return (f'<div class="bar lyricsbar"{style_attr(el)}>'
            f'<span class="ly-head">{mi("lyrics")}</span>{lines}{note}</div>')


# --------------------------------- Sosial ----------------------------------
def r_groupsbar(el):
    g = el.get
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    note = f'<small>{esc(g("note"))}</small>' if g("note") else ""
    return (f'<div class="bar groupsbar"{style_attr(el)}>'
            f'<span class="gr-av">{avatar_html(g("avatar"), g("name"))}</span>'
            f'<span class="gr-text"><strong>{esc(g("name", ""))}</strong>'
            f'<small>{mi("group")}{esc(g("members", ""))}</small>{note}</span>{btn}</div>')


def r_trendbar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    items = "".join(
        f'<a class="tr-row" href="#"><span class="tr-tag">{esc(tag)}</span>'
        f'<small>{esc(count)} post</small></a>'
        for tag, count in rows
    )
    return (f'<div class="bar trendbar"{style_attr(el)}>'
            f'<span class="tr-head">{mi("trending_up")}{esc(g("title", ""))}</span>{items}</div>')


def r_awardbar(el):
    g = el.get
    icon = str(g("icon", "")).strip() or "workspace_premium"
    points = f'<em class="aw-points">{esc(g("points"))}</em>' if g("points") else ""
    btn = f'<button type="button" class="btn ghost sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar awardbar"{style_attr(el)}>'
            f'<span class="aw-ico">{mi(icon)}</span>'
            f'<span class="aw-text"><strong>{esc(g("badge", ""))}{points}</strong>'
            f'<small>{esc(g("note", ""))}</small></span>{btn}</div>')


# ---------------------------------- Toko -----------------------------------
def r_wishlistbar(el):
    g = el.get
    thumb = str(g("image", "")).strip()
    inner = (f'<img src="{esc(safe_url(thumb))}" alt="{esc(g("name", ""))}">' if thumb
             else f'<span class="wl-empty">{mi("image")}</span>')
    note = f'<small>{esc(g("note"))}</small>' if g("note") else ""
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar wishlistbar"{style_attr(el)}>'
            f'<span class="wl-thumb">{inner}</span>'
            f'<span class="wl-text"><strong>{esc(g("name", ""))}</strong>'
            f'<span class="wl-price">{esc(g("price", ""))}</span>{note}</span>{btn}</div>')


def r_orderbar(el):
    g = el.get
    labels = {"pending": "Menunggu bayar", "packed": "Dikemas", "shipped": "Dikirim", "done": "Selesai"}
    status = str(g("status", "")).strip().lower()
    tag = _pill(labels.get(status, "Menunggu bayar"), _tone(status))
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar orderbar"{style_attr(el)}>'
            f'<span class="or-head"><span class="or-code">{mi("receipt_long")}{esc(g("code", ""))}</span>{tag}</span>'
            f'<span class="or-meta"><small>{esc(g("date", ""))}</small>'
            f'<strong class="or-total">{esc(g("total", ""))}</strong></span>'
            f'<span class="or-foot">{btn}</span></div>')


def r_bundlingbar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    items = "".join(
        f'<span class="bd-item"><span>{esc(name)}</span><small>{esc(price)}</small></span>' for name, price in rows
    )
    save = f'<span class="bd-save">{mi("savings")}{esc(g("save"))}</span>' if g("save") else ""
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar bundlingbar"{style_attr(el)}>'
            f'<span class="bd-head"><strong>{esc(g("title", ""))}</strong>{save}</span>'
            f'<span class="bd-items">{items}</span>'
            f'<span class="bd-foot"><strong class="bd-price">{esc(g("price", ""))}</strong>{btn}</span></div>')


def r_loyaltybar(el):
    g = el.get
    value = _pct(g("value"))
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    note = f'<small class="lt-note">{esc(g("next"))}</small>' if g("next") else ""
    return (f'<div class="bar loyaltybar"{style_attr(el)}>'
            f'<span class="lt-head"><strong>{mi("military_tech")}{esc(g("level", ""))}</strong>'
            f'<em class="lt-points">{esc(g("points", ""))}</em></span>'
            f'<span class="lt-track">{_fill_bar("lt-fill", value)}</span>{note}'
            f'<span class="lt-foot">{btn}</span></div>')


# -------------------------------- Keuangan ---------------------------------
def r_balancebar(el):
    g = el.get
    icon = str(g("icon", "")).strip() or "account_balance_wallet"
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    note = f'<small>{esc(g("note"))}</small>' if g("note") else ""
    return (f'<div class="bar balancebar"{style_attr(el)}>'
            f'<span class="bl-ico">{mi(icon)}</span>'
            f'<span class="bl-text"><small>{esc(g("label", ""))}</small>'
            f'<strong class="bl-amount">{esc(g("amount", ""))}</strong>{note}</span>{btn}</div>')


def r_transactionbar(el):
    g = el.get
    kind = str(g("kind", "")).strip().lower()
    kind = kind if kind in ("in", "out") else "out"
    icon = str(g("icon", "")).strip() or ("south_west" if kind == "in" else "north_east")
    btn = f'<button type="button" class="btn ghost sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar transactionbar"{style_attr(el)}>'
            f'<span class="tx-ico {esc(kind)}">{mi(icon)}</span>'
            f'<span class="tx-text"><strong>{esc(g("title", ""))}</strong>'
            f'<small>{esc(g("category", ""))} · {esc(g("time", ""))}</small></span>'
            f'<span class="tx-side"><em class="tx-amount {esc(kind)}">{esc(g("amount", ""))}</em>{btn}</span></div>')


def r_budgetbar(el):
    g = el.get
    value = _pct(g("value"))
    status = str(g("status", "")).strip().lower()
    tone = {"safe": "safe", "warning": "warning", "over": "danger"}.get(status, "safe")
    note = f'<small>{esc(g("note"))}</small>' if g("note") else ""
    return (f'<div class="bar budgetbar"{style_attr(el)}>'
            f'<span class="bg-head"><strong>{esc(g("label", ""))}</strong>'
            f'<em class="tone-{tone}">{esc(g("spent", ""))} / {esc(g("total", ""))}</em></span>'
            f'<span class="bg-track">{_fill_bar("bg-fill", value, tone)}</span>{note}</div>')


def r_invoicebar(el):
    g = el.get
    labels = {"due": "Belum dibayar", "paid": "Lunas", "late": "Terlambat"}
    status = str(g("status", "")).strip().lower()
    tag = _pill(labels.get(status, "Belum dibayar"), _tone(status))
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar invoicebar"{style_attr(el)}>'
            f'<span class="iv-text"><span class="iv-title">{mi("request_quote")}'
            f'<strong>{esc(g("title", ""))}</strong></span>'
            f'<small>{esc(g("due", ""))}</small></span>'
            f'<span class="iv-side"><em class="iv-amount">{esc(g("amount", ""))}</em>{tag}{btn}</span></div>')


def r_savingsbar(el):
    g = el.get
    value = _pct(g("value"))
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    note = f'<small>{esc(g("note"))}</small>' if g("note") else ""
    return (f'<div class="bar savingsbar"{style_attr(el)}>'
            f'<span class="sv-head"><strong>{esc(g("title", ""))}</strong>'
            f'<em>{value}%</em></span>'
            f'<span class="sv-track">{_fill_bar("sv-fill", value)}</span>'
            f'<span class="sv-meta"><small>{esc(g("collected", ""))}</small>'
            f'<small>dari {esc(g("target", ""))}</small></span>{note}'
            f'<span class="sv-foot">{btn}</span></div>')


# ----------------------------- Peta & Lokasi -------------------------------
def r_locationbar(el):
    g = el.get
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    thumb = str(g("thumb", "")).strip()
    thumb_html = (f'<span class="lc-thumb"><img src="{esc(safe_url(thumb))}" alt=""></span>'
                  if thumb else f'<span class="lc-ico">{mi("location_on")}</span>')
    accuracy = f'<small>{mi("my_location")}{esc(g("accuracy"))}</small>' if g("accuracy") else ""
    return (f'<div class="bar locationbar"{style_attr(el)}>{thumb_html}'
            f'<span class="lc-text"><small>{esc(g("label", ""))}</small>'
            f'<strong>{esc(g("place", ""))}</strong>{accuracy}</span>{btn}</div>')


def r_routebar(el):
    g = el.get
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    meta = " · ".join([p for p in (str(g("duration", "")).strip(), str(g("distance", "")).strip()) if p])
    return (f'<div class="bar routebar"{style_attr(el)}>'
            f'<span class="rt-points">'
            f'<span class="rt-row"><span class="rt-dot from"></span>{esc(g("start", ""))}</span>'
            f'<span class="rt-rail"></span>'
            f'<span class="rt-row"><span class="rt-dot to"></span>{esc(g("end", ""))}</span></span>'
            f'<span class="rt-foot"><small>{mi("directions_car")}{esc(meta)}</small>{btn}</span></div>')


def r_nearbybar(el):
    g = el.get
    thumb = str(g("thumb", "")).strip()
    inner = (f'<img src="{esc(safe_url(thumb))}" alt="{esc(g("name", ""))}">' if thumb
             else f'<span class="nr-empty">{mi("storefront")}</span>')
    rating = clamp_int(float(g("rating", 0) or 0) * 10, 0, 50, 0) / 10
    open_labels = {"open": "Buka", "closed": "Tutup", "busy": "Ramai"}
    open_key = str(g("open", "")).strip().lower()
    open_tag = _pill(open_labels.get(open_key, "Buka"), _tone(open_key))
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar nearbybar"{style_attr(el)}>'
            f'<span class="nr-thumb">{inner}</span>'
            f'<span class="nr-text"><strong>{esc(g("name", ""))}</strong>'
            f'<small>{esc(g("category", ""))} · {esc(g("distance", ""))}</small>'
            f'<span class="nr-meta"><em class="nr-rate">{mi("star")}{rating:g}</em>'
            f'<small>{esc(g("open_note", ""))}</small></span></span>'
            f'<span class="nr-side">{open_tag}{btn}</span></div>')


def r_checkinbar(el):
    g = el.get
    labels = {"in": "Sudah masuk", "out": "Sudah pulang", "late": "Terlambat"}
    status = str(g("status", "")).strip().lower()
    tag = _pill(labels.get(status, "Sudah masuk"), _tone(status))
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar checkinbar"{style_attr(el)}>'
            f'<span class="ck-ico">{mi("how_to_reg")}</span>'
            f'<span class="ck-text"><small>{esc(g("label", ""))}</small>'
            f'<strong class="ck-time">{esc(g("time", ""))}</strong>'
            f'<small>{esc(g("place", ""))}</small></span>'
            f'<span class="ck-side">{tag}{btn}</span></div>')


# -------------------------------- Konten -----------------------------------
def r_articlebar(el):
    g = el.get
    cat = f'<span class="ar-cat">{esc(g("category"))}</span>' if g("category") else ""
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar articlebar"{style_attr(el)}>{cat}'
            f'<span class="ar-text"><strong>{esc(g("title", ""))}</strong>'
            f'<small>{mi("schedule")}{esc(g("meta", ""))}</small></span>{btn}</div>')


def r_authorbar(el):
    g = el.get
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    posts = f'<small class="au-posts">{esc(g("posts"))}</small>' if g("posts") else ""
    return (f'<div class="bar authorbar"{style_attr(el)}>'
            f'<span class="au-av">{avatar_html(g("avatar"), g("name"))}</span>'
            f'<span class="au-text"><strong>{esc(g("name", ""))}</strong>'
            f'<small>{esc(g("role", ""))}</small>{posts}</span>{btn}</div>')


def r_chaptersbar(el):
    g = el.get
    rows = lines_of(g("items"))
    cur = clamp_int(g("current"), 1, max(1, len(rows)), 1)
    items = ""
    for i, name in enumerate(rows, start=1):
        state = "done" if i < cur else ("on" if i == cur else "")
        lead = mi("check_circle") if i < cur else str(i)
        items += f'<span class="ch-item {state}"><span class="ch-no">{lead}</span>{esc(name)}</span>'
    progress = _pct(g("progress"))
    return (f'<div class="bar chaptersbar"{style_attr(el)}>'
            f'<span class="ch-head">{mi("menu_book")}<strong>{esc(g("title", ""))}</strong></span>'
            f'<span class="ch-track">{_fill_bar("ch-fill", progress)}</span>'
            f'{items}</div>')


def r_readingprogressbar(el):
    g = el.get
    value = _pct(g("value"))
    btn = f'<button type="button" class="btn sm">{esc(g("button"))}</button>' if g("button") else ""
    note = f'<small>{esc(g("note"))}</small>' if g("note") else ""
    return (f'<div class="bar readingprogressbar"{style_attr(el)}>'
            f'<span class="rp-ico">{mi("auto_stories")}</span>'
            f'<span class="rp-text"><strong>{esc(g("label", ""))}</strong>'
            f'<span class="rp-track">{_fill_bar("rp-fill", value)}</span>{note}</span>{btn}</div>')


def r_relatedbar(el):
    g = el.get
    rows = parts_of(g("items"), 2)
    items = "".join(
        f'<a class="rl-item" href="#"><span class="rl-title">{esc(title)}</span>'
        f'<small>{mi("schedule")}{esc(minutes)}</small></a>'
        for title, minutes in rows
    )
    btn = f'<button type="button" class="btn ghost sm">{esc(g("button"))}</button>' if g("button") else ""
    return (f'<div class="bar relatedbar"{style_attr(el)}>'
            f'<span class="rl-head">{mi("library_books")}{esc(g("title", ""))}</span>'
            f'{items}<span class="rl-foot">{btn}</span></div>')


# Peta tipe -> fungsi render (dipakai bars.render_bar).
PRO_BAR_RENDERERS = {
    # Navigasi
    "appbar": r_appbar,
    "quicknav": r_quicknav,
    "subnav": r_subnav,
    "stepdots": r_stepdots,
    "swipenav": r_swipenav,
    # Aksi
    "bulkactionbar": r_bulkactionbar,
    "exportbar": r_exportbar,
    "approvalbar": r_approvalbar,
    "printbar": r_printbar,
    # Informasi
    "weatherbar": r_weatherbar,
    "notificationbar": r_notificationbar,
    "metricbar": r_metricbar,
    "updatebar": r_updatebar,
    # Data
    "donutbar": r_donutbar,
    "gaugebar": r_gaugebar,
    "rankingbar": r_rankingbar,
    "heatmapbar": r_heatmapbar,
    "distributionbar": r_distributionbar,
    "funnelbar": r_funnelbar,
    # Formulir
    "uploadinputbar": r_uploadinputbar,
    "datepickerbar": r_datepickerbar,
    "ratinginputbar": r_ratinginputbar,
    "quantitybar": r_quantitybar,
    "passstrengthbar": r_passstrengthbar,
    # Media
    "videobar": r_videobar,
    "equalizerbar": r_equalizerbar,
    "podcastbar": r_podcastbar,
    "camerabar": r_camerabar,
    "lyricsbar": r_lyricsbar,
    # Sosial
    "groupsbar": r_groupsbar,
    "trendbar": r_trendbar,
    "awardbar": r_awardbar,
    # Toko
    "wishlistbar": r_wishlistbar,
    "orderbar": r_orderbar,
    "bundlingbar": r_bundlingbar,
    "loyaltybar": r_loyaltybar,
    # Keuangan
    "balancebar": r_balancebar,
    "transactionbar": r_transactionbar,
    "budgetbar": r_budgetbar,
    "invoicebar": r_invoicebar,
    "savingsbar": r_savingsbar,
    # Peta & Lokasi
    "locationbar": r_locationbar,
    "routebar": r_routebar,
    "nearbybar": r_nearbybar,
    "checkinbar": r_checkinbar,
    # Konten
    "articlebar": r_articlebar,
    "authorbar": r_authorbar,
    "chaptersbar": r_chaptersbar,
    "readingprogressbar": r_readingprogressbar,
    "relatedbar": r_relatedbar,
}
