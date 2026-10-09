"""Generator HTML: dari struktur desain menjadi halaman HTML (preview dan ekspor)."""
import html
import re

from ui_builder.components.render.core import render_bar
from ui_builder.components.specs import BAR_SPECS
from ui_builder.core.config import FONTS
from ui_builder.themes.css import BAR_CSS, GLASS_PAGE_CSS, ICON_LINK
from ui_builder.core.element_style import element_style_attr, ensure_element_style
from ui_builder.core.utils import align_of, clamp_int, esc, input_kind, lines_of, num, on_color, parse_links, safe_url


def render_element(el):
    t = el["type"]
    common = element_style_attr(el)
    if t == "navbar":
        links = "".join(
            f'<a href="{esc(safe_url(url))}">{esc(label)}</a>'
            for label, url in parse_links(el.get("links"))
        )
        return (
            f'<header class="topbar" style="{common}"><strong>{esc(el.get("brand", ""))}</strong>'
            f"<nav>{links}</nav></header>"
        )
    if t == "heading":
        extra = f"font-size:{num(el.get('size'), 36)}px;text-align:{align_of(el)};"
        return f'<h1 style="{element_style_attr(el, extra)}">{esc(el.get("text", ""))}</h1>'
    if t == "text":
        return f'<p style="{element_style_attr(el, f"text-align:{align_of(el)};")}">{esc(el.get("text", ""))}</p>'
    if t == "button":
        label = esc(el.get("text", ""))
        link = (el.get("link") or "").strip()
        button_style = element_style_attr(el, "display:inline-block;font:inherit;text-decoration:none;cursor:pointer;")
        inner = (
            f'<a class="btn" style="{button_style}" href="{esc(safe_url(link))}">{label}</a>'
            if link
            else f'<button class="btn" style="{button_style}" type="button">{label}</button>'
        )
        return f'<div style="text-align:{align_of(el)}">{inner}</div>'
    if t == "image":
        style = element_style_attr(el, "display:block;max-width:100%;height:auto;")
        return f'<img src="{esc(safe_url(el.get("url", "")))}" alt="{esc(el.get("alt", ""))}" style="{style}">'
    if t == "gallery":
        cols = min(max(num(el.get("columns"), 3), 1), 4)
        gallery_style = element_style_attr(el, f"display:grid;gap:10px;grid-template-columns:repeat({cols},1fr);")
        imgs = "".join(
            f'<img src="{esc(safe_url(u))}" alt="Gambar galeri {n}" style="width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:{max(0, int(ensure_element_style(el).get("radius", 8) or 0))}px">'
            for n, u in enumerate(lines_of(el.get("urls")), start=1)
        )
        return f'<div class="gallery" style="{gallery_style}">{imgs}</div>'
    if t == "list":
        tag = "ol" if el.get("style") == "number" else "ul"
        items = "".join(f"<li>{esc(i)}</li>" for i in lines_of(el.get("items")))
        return f'<{tag} style="{element_style_attr(el)}">{items}</{tag}>'
    if t == "input":
        style = ensure_element_style(el)
        input_style = (
            f'width:100%;padding:10px 12px;font:inherit;'
            f'background:{esc(style.get("background", "transparent"))};color:{esc(style.get("color", "inherit"))};'
            f'border:{max(1, int(style.get("border_width", 0) or 0))}px solid {esc(style.get("border_color", "#d1d5db"))};'
            f'border-radius:{max(0, int(style.get("radius", 8) or 0))}px;box-shadow:{esc(style.get("shadow", "none"))};'
        )
        label_style = f'color:{esc(style.get("color", "inherit"))};'
        return (
            f'<label class="field" style="width:{esc(style.get("width", "auto"))};padding:{max(0, int(style.get("padding", 0) or 0))}px;">'
            f'<span style="{label_style}">{esc(el.get("label", ""))}</span>'
            f'<input type="{input_kind(el)}" placeholder="{esc(el.get("placeholder", ""))}" style="{input_style}"></label>'
        )
    if t == "card":
        return (
            f'<div class="card" style="{common}"><h3>{esc(el.get("title", ""))}</h3>'
            f'<p>{esc(el.get("text", ""))}</p></div>'
        )
    if t == "divider":
        style = ensure_element_style(el)
        bw = max(1, int(style.get("border_width", 1) or 1))
        return f'<hr style="border:0;border-top:{bw}px solid {esc(style.get("border_color", "#d1d5db"))};margin:0 0 16px;box-shadow:{esc(style.get("shadow", "none"))};width:{esc(style.get("width", "100%"))}">'
    if t == "spacer":
        return f'<div style="height:{num(el.get("height"), 24)}px;background:{esc(ensure_element_style(el).get("background", "transparent"))};border-radius:{max(0, int(ensure_element_style(el).get("radius", 8) or 0))}px;"></div>'
    if t == "footer":
        return f'<footer class="footer" style="{common}">{esc(el.get("text", ""))}</footer>'
    if t in BAR_SPECS:
        return render_bar(el)
    return ""


def mark_selected(rendered):
    """Beri penanda pada tag pertama supaya elemen terpilih tersorot di preview."""
    return re.sub(r"^<(\w+)", r'<\1 data-sel="1"', rendered, count=1)


def build_html(design, highlight_id=None, active=0, builder_mode=False):
    theme = design["theme"]
    font = FONTS.get(theme.get("font"), FONTS["Sans-serif modern"])
    pages = design["pages"]
    multi = len(pages) > 1
    active = min(max(active, 0), len(pages) - 1)

    # Lapisan glassmorphism untuk halaman hasil (aktif bila tema memakai efek kaca).
    glass = bool(theme.get("glass"))
    glass_blur = clamp_int(theme.get("glass_blur"), 0, 60, 18)
    glass_css = GLASS_PAGE_CSS if glass else ""
    glass_layer = '<div class="glass-bg" aria-hidden="true"><i></i><i></i><i></i></div>' if glass else ""
    body_class = ' class="glass"' if glass else ""

    nav = ""
    if multi:
        links = "".join(
            f'<button type="button" class="nav-btn{" active" if i == active else ""}" '
            f'data-target="page-{i}">{esc(p["name"])}</button>'
            for i, p in enumerate(pages)
        )
        nav = f'<nav class="nav">{links}</nav>'

    sections = []
    for i, page in enumerate(pages):
        parts = []
        for el in page["elements"]:
            rendered = render_element(el)
            if builder_mode:
                selected_attr = ' data-sel="1"' if highlight_id and el.get("id") == highlight_id else ""
                rendered = (
                    f'<div class="builder-element" data-element-id="{esc(el.get("id", ""))}"{selected_attr}>'
                    f'{rendered}</div>'
                )
            elif highlight_id and el.get("id") == highlight_id:
                rendered = mark_selected(rendered)
            parts.append(rendered)
        body = "\n".join(parts) or '<p class="empty">Halaman ini masih kosong.</p>'
        hidden = "" if i == active else " hidden"
        sections.append(f'<section id="page-{i}" class="page"{hidden}>\n{body}\n</section>')

    highlight_css = (
        "  [data-sel] { outline: 2px dashed #f59e0b; outline-offset: 4px; }\n"
        if highlight_id
        else ""
    )
    builder_css = ""
    builder_script = ""
    if builder_mode:
        builder_css = """
  .builder-element { position: relative; border: 1px solid transparent; border-radius: 6px; transition: outline .12s, background .12s, border-color .12s; cursor: pointer; }
  .builder-element:hover { border-color: rgba(99,102,241,.42); outline: 2px solid rgba(99,102,241,.12); outline-offset: 2px; }
  .builder-element[data-sel] { border-color: #6366f1; outline: 2px solid rgba(99,102,241,.18); outline-offset: 3px; }
  .builder-element > * { margin-top: 0 !important; margin-bottom: 0 !important; }
"""
        builder_script = """
<script>
  document.addEventListener("click", function (event) {
    var el = event.target.closest ? event.target.closest("[data-element-id]") : null;
    if (!el) return;
    event.preventDefault();
    event.stopPropagation();
    window.parent.postMessage({type:"ui-builder-select", id:el.getAttribute("data-element-id")}, "*");
  }, true);
</script>"""

    script = ""
    if multi:
        script = """
<script>
  document.querySelectorAll('.nav-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.page').forEach(function (p) { p.hidden = true; });
      document.querySelectorAll('.nav-btn').forEach(function (b) { b.classList.remove('active'); });
      document.getElementById(btn.dataset.target).hidden = false;
      btn.classList.add('active');
    });
  });
</script>"""

    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(design["title"])}</title>
{ICON_LINK}
<style>
  :root {{
    --primary: {esc(theme["primary"])};
    --on-primary: {on_color(theme["primary"])};
    --bg: {esc(theme["bg"])};
    --text: {esc(theme["text"])};
    --glass-blur: {glass_blur}px;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: {font};
    line-height: 1.6;
  }}
  .app {{
    max-width: {num(theme["width"], 720)}px;
    margin: 0 auto;
    padding: 24px 20px 48px;
  }}
  .app-title {{ margin: 0 0 16px; font-size: 14px; opacity: .6; }}
  .nav {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px; }}
  .nav-btn {{
    border: 1px solid var(--primary);
    background: transparent;
    color: var(--primary);
    padding: 6px 14px;
    border-radius: 999px;
    cursor: pointer;
    font: inherit;
  }}
  .nav-btn.active {{ background: var(--primary); color: var(--on-primary); }}
  .page > * {{ margin-top: 0; margin-bottom: 16px; }}
  h1, h3 {{ line-height: 1.2; }}
  img {{ max-width: 100%; height: auto; display: block; }}
  hr {{ border: 0; border-top: 1px solid rgba(128,128,128,.35); }}
  ul, ol {{ padding-left: 1.4em; }}
  .btn {{
    display: inline-block;
    background: var(--primary);
    color: var(--on-primary);
    border: 0;
    padding: 10px 20px;
    border-radius: 8px;
    font: inherit;
    text-decoration: none;
    cursor: pointer;
  }}
  .btn:focus-visible, .nav-btn:focus-visible, input:focus-visible, .topbar a:focus-visible {{
    outline: 3px solid var(--primary);
    outline-offset: 2px;
  }}
  .topbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(128,128,128,.35);
  }}
  .topbar nav {{ display: flex; gap: 16px; flex-wrap: wrap; }}
  .topbar a {{ color: var(--text); text-decoration: none; }}
  .topbar a:hover {{ color: var(--primary); }}
  .gallery {{ display: grid; gap: 10px; }}
  .gallery img {{ width: 100%; aspect-ratio: 4 / 3; object-fit: cover; }}
  .field {{ display: block; }}
  .field span {{ display: block; margin-bottom: 4px; font-size: 14px; }}
  .field input {{
    width: 100%;
    padding: 10px 12px;
    border: 1px solid rgba(128,128,128,.5);
    border-radius: 8px;
    font: inherit;
    background: transparent;
    color: inherit;
  }}
  .card {{
    border: 1px solid rgba(128,128,128,.35);
    border-radius: 12px;
    padding: 16px 18px;
  }}
  .card h3 {{ margin: 0 0 6px; }}
  .card p {{ margin: 0; }}
  .footer {{
    text-align: center;
    font-size: 14px;
    opacity: .65;
    padding-top: 16px;
    border-top: 1px solid rgba(128,128,128,.35);
  }}
  .empty {{ opacity: .5; font-style: italic; }}
{BAR_CSS}{highlight_css}{builder_css}{glass_css}</style>
</head>
<body{body_class}>
{glass_layer}
<main class="app">
<p class="app-title">{esc(design["title"])}</p>
{nav}
{chr(10).join(sections)}
</main>{script}{builder_script}
</body>
</html>
"""


def device_frame(inner_html, width):
    """Bungkus preview dalam bingkai perangkat dengan lebar tertentu."""
    w = f"{width}px" if width else "100%"
    return (
        '<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
        "html,body{margin:0;height:100%;"
        "background:linear-gradient(160deg,#eef2ff,#f8f9ff 45%,#fdf2f8)}"
        "body{display:flex;justify-content:center;padding:12px;box-sizing:border-box}"
        f"iframe{{width:{w};max-width:100%;height:100%;border:1px solid rgba(255,255,255,.7);background:#fff;"
        "border-radius:16px;box-shadow:0 18px 40px rgba(31,38,135,.18),inset 0 1px 0 rgba(255,255,255,.6)}}"
        f'</style></head><body><iframe srcdoc="{html.escape(inner_html, quote=True)}">'
        "</iframe></body></html>"
    )
