"""Renderer untuk 50 komponen baru di katalog UI Builder."""
from ui_builder.components.specs.addons import COMPONENT_BAR_SPECS
from ui_builder.core.element_style import soft_style
from ui_builder.core.utils import clamp_int, esc, lines_of, mi, parts_of, safe_url


def _style(el):
    value = soft_style(el)
    return f' style="{value}"' if value else ""


def _root(el, kind, content):
    return f'<div class="bar addonbar aa-{kind}"{_style(el)}>{content}</div>'


def _button(label, secondary=False):
    if not label:
        return ""
    kind = "aa-button secondary" if secondary else "aa-button"
    return f'<button type="button" class="{kind}">{esc(label)}</button>'


def _avatar(name, url=""):
    if url:
        return f'<span class="aa-avatar"><img src="{esc(safe_url(url))}" alt="{esc(name)}"></span>'
    initials = "".join(word[0] for word in str(name or "?").split()[:2]).upper() or "?"
    return f'<span class="aa-avatar" aria-hidden="true">{esc(initials)}</span>'


def _tone(value):
    key = str(value or "info").strip().lower()
    return key if key in {"info", "success", "warning", "error", "online", "offline", "sync", "danger"} else "info"


def _progress(value):
    return clamp_int(value, 0, 100, 0)


def _image(url, alt, class_name="aa-image"):
    return f'<span class="{class_name}"><img src="{esc(safe_url(url))}" alt="{esc(alt)}"></span>'


def render_catalog_bar(el):
    """Render komponen berdasarkan presentasi terstruktur yang ditentukan spesifikasinya."""
    kind = COMPONENT_BAR_SPECS[el["type"]]["renderer"]
    g = el.get

    if kind == "workspace":
        badge = f'<span class="aa-badge">{esc(g("badge"))}</span>' if g("badge") else ""
        return _root(el, kind,
            f'<span class="aa-logo">{mi("workspaces")}</span>'
            f'<span class="aa-copy"><strong>{esc(g("brand", ""))}</strong><small>{esc(g("subtitle", ""))}</small></span>'
            f'{badge}{_button(g("action", ""))}')

    if kind == "steps":
        items = lines_of(g("items"))
        current = clamp_int(g("current"), 1, max(1, len(items)), 1)
        steps = "".join(
            f'<div class="aa-step{" done" if i < current else (" active" if i == current else "")}">'
            f'<span class="aa-step-dot">{mi("check") if i < current else i}</span><span>{esc(label)}</span></div>'
            for i, label in enumerate(items, 1)
        )
        return _root(el, kind, f'<strong class="aa-title">{esc(g("title", ""))}</strong><div class="aa-steps">{steps}</div>')

    if kind == "tabs":
        rows = parts_of(g("items"), 2)
        active = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
        tabs = "".join(
            f'<a class="aa-tab{" active" if i == active else ""}" href="#">{mi(icon or "circle")}<span>{esc(label)}</span></a>'
            for i, (label, icon) in enumerate(rows)
        )
        return _root(el, kind, f'<nav class="aa-tabs">{tabs}</nav>')

    if kind == "links":
        rows = parts_of(g("items"), 3)
        links = "".join(
            f'<a class="aa-link-row" href="#"><span class="aa-icon">{mi(icon or "chevron_right")}</span>'
            f'<span class="aa-copy"><strong>{esc(label)}</strong><small>{esc(note)}</small></span>{mi("chevron_right")}</a>'
            for label, note, icon in rows
        )
        return _root(el, kind, f'<strong class="aa-title">{esc(g("title", ""))}</strong><div class="aa-link-list">{links}</div>')

    if kind == "profile_nav":
        rows = parts_of(g("items"), 2)
        active = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
        nav = "".join(
            f'<a class="aa-nav-row{" active" if i == active else ""}" href="#">{mi(icon or "circle")}<span>{esc(label)}</span></a>'
            for i, (label, icon) in enumerate(rows)
        )
        head = (_avatar(g("name"), g("avatar")) +
                f'<span class="aa-copy"><strong>{esc(g("name", ""))}</strong><small>{esc(g("role", ""))}</small></span>'
                f'{mi("more_horiz")}')
        return _root(el, kind, f'<div class="aa-profile-head">{head}</div><nav class="aa-profile-nav">{nav}</nav>')

    if kind == "command":
        return _root(el, kind,
            f'<span class="aa-command-icon">{mi(g("icon") or "search")}</span>'
            f'<input type="search" placeholder="{esc(g("placeholder", ""))}" aria-label="Pencarian perintah">'
            f'<kbd>{esc(g("shortcut", ""))}</kbd>')

    if kind == "undo":
        return _root(el, kind,
            f'<span class="aa-state-icon">{mi("history")}</span><span class="aa-copy"><strong>{esc(g("title", ""))}</strong>'
            f'<small>{esc(g("note", ""))}</small></span><span class="aa-actions">'
            f'{_button(g("undo", ""), True)}{_button(g("redo", ""))}</span>')

    if kind == "share_link":
        url = str(g("url", "") or "")
        return _root(el, kind,
            f'<span class="aa-copy"><strong>{esc(g("title", ""))}</strong><small>{esc(g("note", ""))}</small></span>'
            f'<span class="aa-share-url">{mi("link")}<span>{esc(url)}</span></span>{_button(g("button", ""))}')

    if kind == "selection":
        rows = parts_of(g("items"), 2)
        actions = "".join(
            f'<button type="button" class="aa-icon-action" title="{esc(label)}">{mi(icon or "bolt")}<span>{esc(label)}</span></button>'
            for label, icon in rows
        )
        return _root(el, kind,
            f'<strong class="aa-selection-count">{mi("check_circle")} {clamp_int(g("count"), 0, 999, 0)} dipilih</strong>'
            f'<span class="aa-actions">{actions}</span>')

    if kind == "create_action":
        return _root(el, kind,
            f'<span class="aa-copy"><strong>{esc(g("title", ""))}</strong><small>{esc(g("note", ""))}</small></span>'
            f'<span class="aa-actions">{_button(g("secondary", ""), True)}{_button(g("primary", ""))}</span>')

    if kind == "alert_list":
        rows = parts_of(g("items"), 3)
        icons = {"info": "info", "success": "check_circle", "warning": "warning", "error": "error", "danger": "error"}
        entries = "".join(
            f'<div class="aa-alert {_tone(tone)}"><span>{mi(icons.get(_tone(tone), "info"))}</span>'
            f'<span class="aa-copy"><strong>{esc(title)}</strong><small>{esc(note)}</small></span></div>'
            for tone, title, note in rows
        )
        return _root(el, kind, f'<strong class="aa-title">{esc(g("title", ""))}</strong><div class="aa-alert-list">{entries}</div>')

    if kind == "event":
        return _root(el, kind,
            f'<span class="aa-event-date">{mi("event")}<small>{esc(g("date", ""))}</small></span>'
            f'<span class="aa-copy"><strong>{esc(g("title", ""))}</strong>'
            f'<small>{mi("location_on")}{esc(g("place", ""))}</small><em>{esc(g("note", ""))}</em></span>'
            f'{_button(g("button", ""))}')

    if kind == "connection":
        status = _tone(g("status"))
        icon = {"online": "cloud_done", "offline": "cloud_off", "sync": "sync", "warning": "warning"}.get(status, "cloud_done")
        return _root(el, kind,
            f'<span class="aa-status-dot {status}">{mi(icon)}</span><span class="aa-copy"><strong>{esc(g("title", ""))}</strong>'
            f'<small>{esc(g("note", ""))}</small></span>{_button(g("action", ""), True)}')

    if kind == "reminder":
        return _root(el, kind,
            f'<span class="aa-reminder-icon">{mi("alarm")}</span><span class="aa-copy"><strong>{esc(g("title", ""))}</strong>'
            f'<small>{mi("schedule")}{esc(g("deadline", ""))}</small><small>{mi("person")}{esc(g("owner", ""))}</small>'
            f'<em>{esc(g("note", ""))}</em></span>{_button(g("button", ""), True)}')

    if kind == "release":
        return _root(el, kind,
            f'<span class="aa-release-mark">{mi("new_releases")}</span><span class="aa-copy">'
            f'<span class="aa-badge">{esc(g("version", ""))} · {esc(g("date", ""))}</span>'
            f'<strong>{esc(g("title", ""))}</strong><small>{esc(g("note", ""))}</small></span>{_button(g("button", ""))}')

    if kind == "metric":
        return _root(el, kind,
            f'<span class="aa-metric-icon">{mi(g("icon") or "query_stats")}</span>'
            f'<span class="aa-copy"><small>{esc(g("label", ""))}</small><strong class="aa-metric-value">{esc(g("value", ""))}</strong>'
            f'<span class="aa-metric-foot"><b>{esc(g("delta", ""))}</b><small>{esc(g("note", ""))}</small></span></span>')

    if kind == "progress_list":
        rows = parts_of(g("items"), 2)
        progress_rows = "".join(
            f'<div class="aa-progress-row"><span><strong>{esc(label)}</strong><small>{_progress(value)}%</small></span>'
            f'<span class="aa-track"><i style="width:{_progress(value)}%"></i></span></div>'
            for label, value in rows
        )
        return _root(el, kind, f'<strong class="aa-title">{esc(g("title", ""))}</strong><div class="aa-progress-list">{progress_rows}</div>')

    if kind == "activity":
        rows = parts_of(g("items"), 3)
        entries = "".join(
            f'<div class="aa-activity-row"><time>{esc(time)}</time><span class="aa-activity-dot"></span>'
            f'<span class="aa-copy"><strong>{esc(title)}</strong><small>{esc(note)}</small></span></div>'
            for time, title, note in rows
        )
        return _root(el, kind, f'<strong class="aa-title">{esc(g("title", ""))}</strong><div class="aa-activity-list">{entries}</div>')

    if kind == "comparison":
        rows = parts_of(g("items"), 3)
        entries = "".join(
            f'<div class="aa-comparison-row"><strong>{esc(name)}</strong><span>{esc(value)}</span>'
            f'<em>{esc(change)}</em></div>' for name, value, change in rows
        )
        return _root(el, kind,
            f'<strong class="aa-title">{esc(g("title", ""))}</strong>'
            f'<div class="aa-comparison-head"><span>Kanal</span><span>{esc(g("left_label", "Nilai"))}</span><span>{esc(g("right_label", "Tren"))}</span></div>'
            f'<div class="aa-comparison-list">{entries}</div>')

    if kind == "goal":
        value = _progress(g("progress"))
        return _root(el, kind,
            f'<span class="aa-goal-head"><span class="aa-copy"><strong>{esc(g("title", ""))}</strong>'
            f'<small>{esc(g("note", ""))}</small></span><span class="aa-goal-value">{value}%</span></span>'
            f'<span class="aa-goal-track"><i style="width:{value}%"></i></span>'
            f'<span class="aa-goal-meta"><b>{esc(g("value", ""))}</b><small>dari {esc(g("target", ""))}</small>{_button(g("button", ""), True)}</span>')

    if kind == "address":
        return _root(el, kind,
            f'<span class="aa-form-head"><span class="aa-icon">{mi("location_on")}</span>'
            f'<span class="aa-copy"><strong>{esc(g("label", ""))}</strong><small>{esc(g("note", ""))}</small></span>'
            f'{_button(g("button", ""), True)}</span><address>{esc(g("address", ""))}</address>')

    if kind == "checklist":
        rows = parts_of(g("items"), 2)
        checks = "".join(
            f'<li class="{"done" if str(status).lower() in ("done", "on", "ya", "true") else "todo"}">'
            f'{mi("check_circle" if str(status).lower() in ("done", "on", "ya", "true") else "radio_button_unchecked")}<span>{esc(label)}</span></li>'
            for status, label in rows
        )
        return _root(el, kind, f'<strong class="aa-title">{esc(g("title", ""))}</strong><ul class="aa-checklist">{checks}</ul>')

    if kind == "upload":
        rows = parts_of(g("items"), 3)
        files = "".join(
            f'<div class="aa-file-row"><span class="aa-file-icon">{mi("description")}</span>'
            f'<span class="aa-copy"><strong>{esc(name)}</strong><small>{esc(size)} · {_progress(pct)}%</small>'
            f'<span class="aa-track"><i style="width:{_progress(pct)}%"></i></span></span>{mi("more_horiz")}</div>'
            for name, size, pct in rows
        )
        return _root(el, kind,
            f'<span class="aa-upload-head"><strong>{esc(g("title", ""))}</strong>{_button(g("button", ""), True)}</span>'
            f'<div class="aa-file-list">{files}</div>')

    if kind == "contact_form":
        return _root(el, kind,
            f'<strong class="aa-title">{esc(g("title", ""))}</strong>'
            f'<label class="aa-field"><span>{esc(g("label", ""))}</span><span class="aa-field-row">'
            f'<input type="email" placeholder="{esc(g("placeholder", ""))}" aria-label="{esc(g("label", "Email"))}">'
            f'{_button(g("button", ""))}</span></label><small class="aa-form-note">{esc(g("note", ""))}</small>')

    if kind == "consent":
        rows = parts_of(g("items"), 2)
        options = "".join(
            f'<div class="aa-consent-row"><span><strong>{esc(label)}</strong>'
            f'{"<small>Selalu aktif</small>" if str(state).lower() == "on" and label.lower() == "wajib" else ""}</span>'
            f'<span class="aa-switch{" on" if str(state).lower() in ("on", "ya", "true", "1") else ""}"></span></div>'
            for label, state in rows
        )
        return _root(el, kind,
            f'<strong class="aa-title">{esc(g("title", ""))}</strong><div class="aa-consent-list">{options}</div>'
            f'<span class="aa-form-note">{esc(g("note", ""))}</span>{_button(g("button", ""))}')

    if kind == "media_card":
        return _root(el, kind,
            f'{_image(g("image", ""), g("title", ""), "aa-cover")}<span class="aa-copy">'
            f'<strong>{esc(g("title", ""))}</strong><small>{esc(g("meta", ""))}</small></span>{_button(g("button", ""), True)}')

    if kind == "audio":
        value = _progress(g("progress"))
        return _root(el, kind,
            f'<span class="aa-play">{mi("play_arrow")}</span><span class="aa-copy">'
            f'<strong>{esc(g("title", ""))}</strong><small>{esc(g("artist", ""))}</small>'
            f'<span class="aa-audio-track"><i style="width:{value}%"></i></span>'
            f'<span class="aa-audio-meta"><small>{esc(g("current", ""))}</small><small>{esc(g("duration", ""))}</small></span>'
            f'</span>{mi("more_horiz")}')

    if kind == "playlist":
        rows = parts_of(g("items"), 3)
        active = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
        songs = "".join(
            f'<div class="aa-song{" active" if i == active else ""}"><span class="aa-song-no">'
            f'{mi("graphic_eq") if i == active else i + 1}</span><span class="aa-copy"><strong>{esc(title)}</strong>'
            f'<small>{esc(state) if state not in ("now", "next") else ("Sedang diputar" if state == "now" else "Berikutnya")}</small>'
            f'</span><time>{esc(duration)}</time></div>' for i, (title, duration, state) in enumerate(rows)
        )
        return _root(el, kind, f'<strong class="aa-title">{esc(g("title", ""))}</strong><div class="aa-song-list">{songs}</div>')

    if kind == "photo_credit":
        return _root(el, kind,
            f'{_image(g("image", ""), g("alt", ""), "aa-photo")}<span class="aa-copy">'
            f'<strong>{esc(g("caption", ""))}</strong><small>{esc(g("credit", ""))}</small></span>')

    if kind == "recording":
        values = []
        for raw in str(g("wave", "")).replace(";", ",").split(",")[:40]:
            try:
                values.append(max(3, min(30, int(float(raw.strip())))))
            except ValueError:
                continue
        bars = "".join(f'<i style="height:{value}px"></i>' for value in values)
        return _root(el, kind,
            f'<span class="aa-record-dot"></span><span class="aa-copy"><strong>{esc(g("label", ""))}</strong>'
            f'<small>{esc(g("status", ""))}</small></span><time>{esc(g("time", ""))}</time>'
            f'<span class="aa-wave">{bars}</span>{_button(g("button", ""))}')

    if kind == "poll":
        rows = parts_of(g("items"), 2)
        amounts = []
        for _, val in rows:
            try:
                amounts.append(max(0, int(float(val))))
            except ValueError:
                amounts.append(0)
        top = max(amounts + [1])
        choices = "".join(
            f'<div class="aa-poll-row"><span class="aa-poll-label"><strong>{esc(label)}</strong><b>{votes}</b></span>'
            f'<span class="aa-track"><i style="width:{min(100, round(votes * 100 / top))}%"></i></span></div>'
            for (label, _), votes in zip(rows, amounts)
        )
        return _root(el, kind,
            f'<strong class="aa-title">{esc(g("title", ""))}</strong><div class="aa-poll-list">{choices}</div>'
            f'<small class="aa-form-note">{esc(g("note", ""))}</small>')

    if kind == "community":
        return _root(el, kind,
            f'{_avatar(g("name"), g("avatar"))}<span class="aa-copy"><strong>{esc(g("name", ""))}</strong>'
            f'<small>{esc(g("members", ""))}</small><em>{esc(g("note", ""))}</em></span>{_button(g("button", ""))}')

    if kind == "social_proof":
        return _root(el, kind,
            f'<span class="aa-quote-mark">{mi("format_quote")}</span><blockquote>{esc(g("quote", ""))}</blockquote>'
            f'<span class="aa-profile-inline">{_avatar(g("name"), g("avatar"))}'
            f'<span class="aa-copy"><strong>{esc(g("name", ""))}</strong><small>{esc(g("role", ""))}</small></span></span>')

    if kind == "creator":
        return _root(el, kind,
            f'{_avatar(g("name"), g("avatar"))}<span class="aa-copy"><strong>{esc(g("name", ""))}</strong>'
            f'<small>{esc(g("handle", ""))} · {esc(g("followers", ""))}</small></span>{_button(g("button", ""), True)}')

    if kind == "reactions":
        rows = parts_of(g("items"), 3)
        reactions = "".join(
            f'<button type="button" class="aa-reaction">{mi(icon or "favorite")}<span>{esc(label)}</span><b>{esc(count)}</b></button>'
            for label, icon, count in rows
        )
        return _root(el, kind, f'<strong class="aa-title">{esc(g("title", ""))}</strong><div class="aa-reaction-list">{reactions}</div>')

    if kind == "cart_item":
        return _root(el, kind,
            f'{_image(g("image", ""), g("name", ""), "aa-thumb")}<span class="aa-copy">'
            f'<strong>{esc(g("name", ""))}</strong><small>{esc(g("variant", ""))}</small>'
            f'<small>Jumlah: {clamp_int(g("quantity"), 1, 99, 1)}</small></span><strong class="aa-price">{esc(g("price", ""))}</strong>')

    if kind == "delivery":
        step = clamp_int(g("step"), 1, 3, 1)
        labels = ["Dikemas", "Dikirim", "Tiba"]
        timeline = "".join(
            f'<span class="aa-delivery-step{" done" if i < step else (" active" if i == step else "")}">'
            f'<i>{mi("check") if i < step else i}</i><small>{label}</small></span>'
            for i, label in enumerate(labels, 1)
        )
        return _root(el, kind,
            f'<span class="aa-delivery-head">{mi("local_shipping")}<span class="aa-copy"><strong>{esc(g("status", ""))}</strong>'
            f'<small>{esc(g("date", ""))}</small></span></span><div class="aa-delivery-line">{timeline}</div>'
            f'<small class="aa-form-note">{esc(g("note", ""))}</small>')

    if kind == "variant":
        rows = lines_of(g("items"))
        active = clamp_int(g("active"), 1, max(1, len(rows)), 1) - 1
        options = "".join(
            f'<button type="button" class="aa-variant{" active" if i == active else ""}">{esc(label)}</button>'
            for i, label in enumerate(rows)
        )
        return _root(el, kind,
            f'<strong class="aa-title">{esc(g("title", ""))}</strong><div class="aa-variant-list">{options}</div>'
            f'<small class="aa-form-note">{esc(g("note", ""))}</small>')

    if kind == "discount":
        value = _progress(g("progress"))
        return _root(el, kind,
            f'<span class="aa-discount-icon">{mi("local_offer")}</span><span class="aa-copy">'
            f'<strong>{esc(g("title", ""))}</strong><span class="aa-code">{esc(g("code", ""))}</span>'
            f'<small>{esc(g("note", ""))}</small><span class="aa-track"><i style="width:{value}%"></i></span>'
            f'</span>{_button(g("button", ""), True)}')

    if kind == "return":
        return _root(el, kind,
            f'<span class="aa-return-mark">{mi("assignment_return")}</span><span class="aa-copy">'
            f'<span class="aa-return-top"><strong>{esc(g("title", ""))}</strong><span class="aa-badge">{esc(g("status", ""))}</span></span>'
            f'<small>{esc(g("code", ""))} · {esc(g("date", ""))}</small><small>{esc(g("note", ""))}</small></span>'
            f'<strong class="aa-price">{esc(g("amount", ""))}</strong>')

    if kind == "wallet":
        return _root(el, kind,
            f'<span class="aa-wallet-top"><span class="aa-copy"><small>{esc(g("label", ""))}</small>'
            f'<strong class="aa-wallet-value">{esc(g("balance", ""))}</strong></span>{_button(g("button", ""), True)}</span>'
            f'<span class="aa-wallet-stats"><span><small>Pemasukan</small><strong>{esc(g("income", ""))}</strong></span>'
            f'<span><small>Pengeluaran</small><strong>{esc(g("expense", ""))}</strong></span></span>')

    if kind == "expense":
        rows = parts_of(g("items"), 3)
        entries = "".join(
            f'<div class="aa-expense-row"><span class="aa-expense-head"><strong>{esc(name)}</strong>'
            f'<b>{esc(amount)}</b></span><span class="aa-track"><i style="width:{_progress(percent)}%"></i></span></div>'
            for name, amount, percent in rows
        )
        return _root(el, kind,
            f'<span class="aa-wallet-top"><strong class="aa-title">{esc(g("title", ""))}</strong>'
            f'<strong class="aa-expense-total">{esc(g("total", ""))}</strong></span><div class="aa-expense-list">{entries}</div>')

    if kind == "cashflow":
        rows = parts_of(g("items"), 3)
        entries = "".join(
            f'<div class="aa-cash-row"><strong>{esc(period)}</strong><span><small>Masuk</small><b>{esc(inc)}</b></span>'
            f'<span><small>Keluar</small><b>{esc(out)}</b></span></div>'
            for period, inc, out in rows
        )
        return _root(el, kind,
            f'<strong class="aa-title">{esc(g("title", ""))}</strong><div class="aa-cash-head"><span>Periode</span><span>Pemasukan</span><span>Pengeluaran</span></div>'
            f'<div class="aa-cash-list">{entries}</div><small class="aa-form-note">{esc(g("note", ""))}</small>')

    if kind == "bill":
        return _root(el, kind,
            f'<span class="aa-bill-icon">{mi("receipt_long")}</span><span class="aa-copy"><strong>{esc(g("title", ""))}</strong>'
            f'<small>{esc(g("cycle", ""))}</small><span class="aa-bill-status">{esc(g("status", ""))}</span></span>'
            f'<span class="aa-bill-side"><strong>{esc(g("amount", ""))}</strong>{_button(g("button", ""), True)}</span>')

    if kind == "savings":
        value = _progress(g("progress"))
        return _root(el, kind,
            f'<span class="aa-goal-head"><span class="aa-copy"><strong>{esc(g("title", ""))}</strong>'
            f'<small>{esc(g("next", ""))}</small></span><span class="aa-goal-value">{value}%</span></span>'
            f'<span class="aa-goal-track"><i style="width:{value}%"></i></span>'
            f'<span class="aa-goal-meta"><b>{esc(g("value", ""))}</b><small>dari {esc(g("target", ""))}</small>{_button(g("button", ""), True)}</span>')

    if kind == "toc":
        items = lines_of(g("items"))
        active = clamp_int(g("active"), 1, max(1, len(items)), 1) - 1
        links = "".join(
            f'<a href="#" class="aa-toc-row{" active" if i == active else ""}><span>{i + 1:02d}</span>{esc(item)}</a>'
            for i, item in enumerate(items)
        )
        return _root(el, kind, f'<strong class="aa-title">{mi("format_list_bulleted")}{esc(g("title", ""))}</strong><nav class="aa-toc-list">{links}</nav>')

    if kind == "story":
        return _root(el, kind,
            f'{_image(g("image", ""), g("title", ""), "aa-story-cover")}<span class="aa-copy">'
            f'<span class="aa-badge">{esc(g("category", ""))}</span><strong>{esc(g("title", ""))}</strong>'
            f'<small>{esc(g("summary", ""))}</small><em>{mi("schedule")}{esc(g("read_time", ""))}</em></span>')

    if kind == "byline":
        return _root(el, kind,
            f'{_avatar(g("name"), g("avatar"))}<span class="aa-copy"><strong>{esc(g("name", ""))}</strong>'
            f'<small>{esc(g("role", ""))}</small><small>{esc(g("published", ""))} · {esc(g("posts", ""))}</small></span>')

    if kind == "reading":
        progress = _progress(g("progress"))
        current = clamp_int(g("current"), 1, 999, 1)
        total = max(current, clamp_int(g("total"), 1, 999, current))
        return _root(el, kind,
            f'<span class="aa-reading-icon">{mi("menu_book")}</span><span class="aa-copy"><strong>{esc(g("title", ""))}</strong>'
            f'<small>Halaman {current} dari {total} · {esc(g("note", ""))}</small>'
            f'<span class="aa-track"><i style="width:{progress}%"></i></span></span>'
            f'<span class="aa-reading-side"><b>{progress}%</b>{_button(g("button", ""), True)}</span>')

    if kind == "attributed_quote":
        return _root(el, kind,
            f'<span class="aa-quote-mark">{mi("format_quote")}</span><blockquote>{esc(g("quote", ""))}</blockquote>'
            f'<footer><strong>{esc(g("author", ""))}</strong><small>{esc(g("source", ""))}</small></footer>')

    # Fail-safe agar komponen yang belum dipetakan tetap terlihat dan dapat diedit.
    label = COMPONENT_BAR_SPECS[el["type"]]["label"]
    return _root(el, "fallback", f'<strong>{esc(label)}</strong>')
