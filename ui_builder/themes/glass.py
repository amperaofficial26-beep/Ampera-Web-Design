"""Lapisan glassmorphism.

Modul ini berisi dua bagian:

* ``APP_CSS_GLASS`` – CSS tampilan aplikasi editor Streamlit (panel, tombol,
  tab, input, kartu template) dengan permukaan kaca: tembus pandang,
  ``backdrop-filter``, garis tepi putih tipis, dan bayangan lembut.
* ``GLASS_PAGE_CSS`` – efek kaca untuk HTML preview/ekspor. Hanya dipakai saat
  tema desain memiliki ``glass: True`` (lihat ``export/html_builder.py``).

Semua warna diatur lewat token ``--g-*`` supaya mudah disetel ulang.
"""

# ---------------------------------------------------------------------------
# 1. Tampilan aplikasi editor Streamlit
# ---------------------------------------------------------------------------
APP_CSS_GLASS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ---------- Token kaca ---------- */
:root {
  --g-blur: 18px;
  --g-sat: 150%;
  --g-surface: rgba(255, 255, 255, .55);
  --g-surface-soft: rgba(255, 255, 255, .38);
  --g-surface-strong: rgba(255, 255, 255, .72);
  --g-border: rgba(255, 255, 255, .65);
  --g-edge: rgba(148, 163, 184, .30);
  --g-shadow: 0 14px 36px rgba(15, 23, 42, .10), 0 2px 6px rgba(15, 23, 42, .05);
  --g-shadow-hover: 0 20px 46px rgba(79, 70, 229, .20), 0 3px 8px rgba(15, 23, 42, .06);
  --g-highlight: inset 0 1px 0 rgba(255, 255, 255, .80);
  --g-radius: 18px;
  --g-radius-sm: 12px;
  --g-ink: #0f172a;
  --g-ink-soft: #55637c;
  --g-accent: #6366f1;
  --g-accent-2: #a855f7;
}

/* ---------- Sembunyikan elemen bawaan Streamlit ---------- */
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stAppDeployButton"], [data-testid="stMainMenu"],
.stAppDeployButton, .stDeployButton, [data-testid="stSidebarCollapsedControl"] {
  display: none !important; visibility: hidden !important; height: 0 !important; }

/* ---------- Latar aurora (agar kaca terlihat tembus pandang) ---------- */
.stApp, [data-testid="stAppViewContainer"] {
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  color: var(--g-ink);
  background-color: #eef1fb;
  background-image:
    radial-gradient(760px 460px at 4% -8%, rgba(99, 102, 241, .40), transparent 62%),
    radial-gradient(680px 400px at 96% 0%, rgba(236, 72, 153, .30), transparent 60%),
    radial-gradient(820px 560px at 78% 100%, rgba(56, 189, 248, .32), transparent 62%),
    radial-gradient(620px 460px at 18% 92%, rgba(168, 85, 247, .26), transparent 64%),
    linear-gradient(155deg, #f8f9ff 0%, #eef2ff 46%, #fdf2f8 100%);
  background-repeat: no-repeat;
  background-attachment: fixed;
}
@media (prefers-reduced-motion: no-preference) {
  .stApp, [data-testid="stAppViewContainer"] {
    animation: g-aurora 48s ease-in-out infinite alternate; }
}
@keyframes g-aurora {
  from { background-position: 0% 0%, 100% 0%, 80% 100%, 20% 90%, 0 0; }
  to   { background-position: 5% 3%, 94% 5%, 74% 95%, 26% 86%, 0 0; }
}
.stApp button, .stApp input, .stApp textarea, .stApp [data-baseweb="select"] {
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; }
.block-container { padding-top: 1.2rem !important; padding-bottom: 2.4rem !important; max-width: 1920px; }
h5 { margin-bottom: .2rem; font-weight: 700; }
.stApp h4, .stApp h5, .stApp h6 { letter-spacing: -.01em; color: var(--g-ink); }
[data-testid="stCaptionContainer"], .stApp small { color: var(--g-ink-soft); }
[data-testid="stMarkdownContainer"] a { color: var(--g-accent); text-underline-offset: 2px; }

/* ---------- Kartu kaca dasar (dipakai ulang oleh semua panel) ---------- */
.st-key-hero, .st-key-projbar, .st-key-panel_left, .st-key-panel_right, .st-key-component_library,
.stApp [data-testid="stExpander"], .stApp [data-testid="stAlertContainer"],
.stApp [data-testid="stNotification"], .stApp [data-testid="stFileUploaderDropzone"] {
  border: 1px solid var(--g-border) !important;
  background: var(--g-surface) !important;
  -webkit-backdrop-filter: blur(var(--g-blur)) saturate(var(--g-sat));
  backdrop-filter: blur(var(--g-blur)) saturate(var(--g-sat));
  box-shadow: var(--g-shadow), var(--g-highlight);
}

/* ---------- Hero / header ---------- */
.st-key-hero {
  border-radius: 22px !important;
  padding: 20px 26px !important;
  color: #fff !important;
  border-color: rgba(255, 255, 255, .40) !important;
  background:
    linear-gradient(115deg, rgba(67, 56, 202, .88) 0%, rgba(124, 58, 237, .84) 48%, rgba(190, 24, 93, .80) 118%) !important;
  box-shadow: 0 20px 48px rgba(79, 70, 229, .30), inset 0 1px 0 rgba(255, 255, 255, .38),
              inset 0 -18px 40px rgba(255, 255, 255, .10);
}
.st-key-hero, .st-key-hero * { color: #fff !important; }
.st-key-hero h2 { margin: 0 !important; padding: 0 !important; font-weight: 700; letter-spacing: -.02em;
  text-shadow: 0 1px 12px rgba(15, 23, 42, .28); }
.st-key-hero [data-testid="stCaptionContainer"] { opacity: .9; }
.st-key-hero [data-testid="stColumn"]:last-child { text-align: right; }
.st-key-hero [data-testid="stMarkdownContainer"] p { margin: 0; font-weight: 500; }

/* ---------- Bar proyek ---------- */
.st-key-projbar { border-radius: var(--g-radius) !important; padding: 12px 16px !important; }
.st-key-projbar [data-testid="stMarkdownContainer"] p { margin: 0; }

/* ---------- Panel kiri & kanan ---------- */
.st-key-panel_left, .st-key-panel_right {
  border-radius: 20px !important;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, .70), rgba(255, 255, 255, .42)) !important;
}
.st-key-panel_left h4, .st-key-panel_right h4 { margin: 0 0 .15rem; letter-spacing: -.02em; }
.st-key-panel_left [data-testid="stMetric"] {
  padding: .6rem .65rem; border: 1px solid var(--g-border); border-radius: 14px;
  background: var(--g-surface-strong);
  -webkit-backdrop-filter: blur(12px) saturate(140%); backdrop-filter: blur(12px) saturate(140%);
  box-shadow: var(--g-highlight), 0 6px 18px rgba(15, 23, 42, .06); }
.st-key-panel_left [data-testid="stMetricLabel"] { font-size: .72rem; color: var(--g-ink-soft); }
.st-key-panel_left [data-testid="stMetricValue"] { font-size: 1.3rem; color: var(--g-accent); font-weight: 700; }
.st-key-panel_left [data-testid="stVerticalBlockBorderWrapper"],
.st-key-panel_right [data-testid="stVerticalBlockBorderWrapper"] {
  border-radius: 14px;
  border-color: var(--g-border) !important;
  background: var(--g-surface-soft);
  -webkit-backdrop-filter: blur(12px) saturate(140%); backdrop-filter: blur(12px) saturate(140%);
  box-shadow: var(--g-highlight); }
.st-key-panel_left [data-testid="stVerticalBlockBorderWrapper"] { background: rgba(238, 242, 255, .55); }
.st-key-panel_right [data-baseweb="tab-list"] { gap: .2rem; border-bottom: 0; }
.st-key-panel_right [data-baseweb="tab"] { padding: .5rem .6rem; font-size: .78rem; }
.st-key-panel_right [data-testid="stExpander"] { margin-bottom: .4rem; border-radius: 14px; }
.st-key-panel_right [data-testid="stExpander"] { background: rgba(255, 255, 255, .58) !important; }

/* ---------- Pustaka komponen (dock bawah) ---------- */
.st-key-component_library { border-radius: var(--g-radius) !important; background: rgba(255, 255, 255, .46) !important; }
.st-key-component_library .stButton > button {
  min-height: 2.6rem; font-size: .78rem; line-height: 1.15; padding: .45rem .5rem; }

/* ---------- Tombol ---------- */
.stButton > button, .stDownloadButton > button {
  border-radius: var(--g-radius-sm) !important;
  border: 1px solid var(--g-border) !important;
  color: var(--g-ink) !important;
  font-weight: 600;
  background: linear-gradient(180deg, rgba(255, 255, 255, .78), rgba(255, 255, 255, .52)) !important;
  -webkit-backdrop-filter: blur(12px) saturate(150%); backdrop-filter: blur(12px) saturate(150%);
  box-shadow: var(--g-highlight), 0 4px 12px rgba(15, 23, 42, .07);
  transition: transform .14s ease, box-shadow .18s ease, border-color .18s ease, background .18s ease; }
.stButton > button:hover, .stDownloadButton > button:hover {
  transform: translateY(-1px);
  border-color: rgba(255, 255, 255, .95) !important;
  background: linear-gradient(180deg, rgba(255, 255, 255, .92), rgba(255, 255, 255, .68)) !important;
  box-shadow: var(--g-shadow-hover), var(--g-highlight); }
.stButton > button:active, .stDownloadButton > button:active { transform: translateY(0); }
.stButton > button:focus-visible, .stDownloadButton > button:focus-visible,
.stApp input:focus-visible, .stApp textarea:focus-visible, .stApp [data-baseweb="select"]:focus-within {
  outline: 2px solid rgba(99, 102, 241, .55) !important; outline-offset: 2px; }

/* Tombol utama tetap memakai gradien aksen, dengan kilau kaca di tepi atas. */
.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"],
.stDownloadButton > button[kind="primary"] {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 55%, #a855f7 100%) !important;
  border-color: rgba(255, 255, 255, .45) !important;
  color: #fff !important;
  box-shadow: 0 12px 28px rgba(99, 102, 241, .35), inset 0 1px 0 rgba(255, 255, 255, .45) !important; }
.stButton > button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover,
.stDownloadButton > button[kind="primary"]:hover {
  box-shadow: 0 18px 36px rgba(99, 102, 241, .42), inset 0 1px 0 rgba(255, 255, 255, .55) !important; }
.stButton > button:disabled, .stDownloadButton > button:disabled { opacity: .55; box-shadow: none !important; }

/* ---------- Kolom isian, pilih, dan area unggah ---------- */
.stApp input, .stApp textarea,
.stApp [data-baseweb="input"], .stApp [data-baseweb="textarea"], .stApp [data-baseweb="select"] > div,
.stApp [data-baseweb="base-input"] {
  color: var(--g-ink) !important;
  background: rgba(255, 255, 255, .62) !important;
  border: 1px solid var(--g-edge) !important;
  border-radius: var(--g-radius-sm) !important;
  -webkit-backdrop-filter: blur(12px) saturate(140%); backdrop-filter: blur(12px) saturate(140%);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .70); }
.stApp [data-baseweb="select"] > div:hover, .stApp input:hover, .stApp textarea:hover { border-color: rgba(99, 102, 241, .45) !important; }
.stApp [data-baseweb="base-input"] { background: transparent !important; border: 0 !important; box-shadow: none !important; }
.stApp input::placeholder, .stApp textarea::placeholder { color: rgba(85, 99, 124, .75); }
.stApp label, .stApp [data-testid="stWidgetLabel"] p { color: var(--g-ink-soft); font-weight: 500; }
.stApp [data-testid="stFileUploaderDropzone"] { border-radius: var(--g-radius) !important; }

/* Menu pilihan melayang (dropdown) juga dibuat kaca. */
[data-baseweb="popover"] [role="listbox"], [data-baseweb="menu"], [data-baseweb="popover"] ul {
  border-radius: 14px !important;
  border: 1px solid var(--g-border) !important;
  background: rgba(255, 255, 255, .78) !important;
  -webkit-backdrop-filter: blur(20px) saturate(160%); backdrop-filter: blur(20px) saturate(160%);
  box-shadow: 0 20px 44px rgba(15, 23, 42, .16), var(--g-highlight); }
[data-baseweb="menu"] li:hover, [role="option"]:hover { background: rgba(99, 102, 241, .12) !important; }

/* ---------- Tab bergaya pil kaca ---------- */
.stTabs [data-baseweb="tab-list"] {
  gap: .25rem; padding: .25rem; border-bottom: 0;
  border-radius: 14px;
  background: var(--g-surface-soft);
  -webkit-backdrop-filter: blur(14px) saturate(150%); backdrop-filter: blur(14px) saturate(150%);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .65); }
.stTabs [data-baseweb="tab"] {
  border-radius: 10px; font-weight: 600; color: var(--g-ink-soft);
  transition: background .16s ease, color .16s ease; }
.stTabs [data-baseweb="tab"]:hover { background: rgba(255, 255, 255, .55); color: var(--g-ink); }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [aria-selected="true"], .stTabs [data-baseweb="tab"][aria-selected="true"] {
  color: var(--g-accent) !important;
  background: linear-gradient(180deg, rgba(255, 255, 255, .92), rgba(255, 255, 255, .66));
  box-shadow: var(--g-highlight), 0 6px 16px rgba(99, 102, 241, .16); }

/* ---------- Expander, notifikasi, dan blok kode ---------- */
.stApp [data-testid="stExpander"] { border-radius: 14px; overflow: hidden; }
.stApp [data-testid="stExpander"] summary { font-weight: 600; border-radius: 14px; transition: background .16s ease; }
.stApp [data-testid="stExpander"] summary:hover { background: rgba(255, 255, 255, .55); }
.stApp [data-testid="stExpander"] [data-testid="stExpanderDetails"] { border-top: 1px solid rgba(255, 255, 255, .55); }
[data-testid="stAlertContainer"] { border-radius: var(--g-radius) !important; }
[data-testid="stAlertContainer"] p { color: var(--g-ink); }
[data-testid="stCodeBlock"], [data-testid="stCode"], .stApp pre {
  border-radius: 14px !important;
  border: 1px solid rgba(255, 255, 255, .18) !important;
  background: rgba(17, 24, 39, .78) !important;
  -webkit-backdrop-filter: blur(16px) saturate(140%); backdrop-filter: blur(16px) saturate(140%);
  box-shadow: 0 16px 38px rgba(15, 23, 42, .22), inset 0 1px 0 rgba(255, 255, 255, .14); }
[data-testid="stCodeBlock"] code, [data-testid="stCode"] code, .stApp pre code { color: #e5e9f5 !important; }
.stApp [data-testid="stDivider"] hr, .stApp hr { border-color: rgba(148, 163, 184, .35); }
.stApp [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] { border-radius: 14px; }

/* ---------- Pratinjau template & gaya ---------- */
.tpl-sws { display: flex; gap: 4px; margin: 2px 0 4px; }
.tpl-sw { width: 16px; height: 16px; border-radius: 50%; border: 1px solid rgba(128, 128, 128, .45);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .6); }
.ref-prev {
  display: flex; align-items: center; gap: 10px; padding: 12px; border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, .55); margin-bottom: 6px;
  background-image: radial-gradient(240px 140px at 12% -20%, rgba(99, 102, 241, .38), transparent 65%),
                    radial-gradient(220px 150px at 96% 120%, rgba(236, 72, 153, .30), transparent 62%);
  box-shadow: var(--g-highlight), 0 8px 22px rgba(15, 23, 42, .08); }
.ref-card { flex: 1; padding: 8px 10px; display: flex; flex-direction: column; font-size: 13px; }
.ref-card span { font-size: 12px; opacity: .8; }
.ref-btn { padding: 8px 12px; font-size: 13px; font-weight: 600; }

/* ---------- Scrollbar tipis tembus pandang ---------- */
* { scrollbar-width: thin; scrollbar-color: rgba(99, 102, 241, .35) transparent; }
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99, 102, 241, .32); border-radius: 8px; border: 2px solid transparent;
  background-clip: padding-box; }
::-webkit-scrollbar-thumb:hover { background: rgba(99, 102, 241, .52); background-clip: padding-box; }

/* ---------- Cadangan bila browser tanpa backdrop-filter ---------- */
@supports not ((backdrop-filter: blur(2px)) or (-webkit-backdrop-filter: blur(2px))) {
  .st-key-hero, .st-key-projbar, .st-key-panel_left, .st-key-panel_right, .st-key-component_library,
  .stApp [data-testid="stExpander"], .stApp [data-testid="stAlertContainer"],
  .stApp [data-testid="stFileUploaderDropzone"], .stButton > button, .stDownloadButton > button {
    background: rgba(255, 255, 255, .90) !important; }
  .st-key-hero { background: linear-gradient(115deg, #4338ca, #7c3aed 48%, #be185d 118%) !important; }
  .stTabs [data-baseweb="tab-list"], .stApp [data-testid="stMetric"] { background: rgba(255, 255, 255, .90) !important; }
  [data-baseweb="popover"] [role="listbox"], [data-baseweb="menu"] { background: rgba(255, 255, 255, .97) !important; }
}
"""


# ---------------------------------------------------------------------------
# 2. Efek kaca untuk halaman hasil (preview & ekspor)
# ---------------------------------------------------------------------------
# Aktif saat ``theme["glass"]`` bernilai True. Nilai blur diambil dari variabel
# CSS ``--glass-blur`` yang diisi build_html dari ``theme["glass_blur"]``.
GLASS_PAGE_CSS = """
  /* ---------- Latar aurora: sumber warna untuk efek kaca ---------- */
  body.glass {
    background-attachment: fixed;
    background-image:
      radial-gradient(58vw 46vh at 8% -6%, rgba(124, 58, 237, .45), transparent 64%),
      radial-gradient(52vw 42vh at 98% 4%, rgba(236, 72, 153, .38), transparent 62%),
      radial-gradient(60vw 50vh at 82% 104%, rgba(56, 189, 248, .40), transparent 64%),
      radial-gradient(46vw 40vh at 12% 96%, rgba(168, 85, 247, .32), transparent 66%);
    background-repeat: no-repeat;
  }
  .glass-bg { position: fixed; inset: 0; z-index: 0; overflow: hidden; pointer-events: none; }
  .glass-bg i {
    position: absolute; display: block; border-radius: 50%; filter: blur(58px); opacity: .5;
    background: radial-gradient(circle at 30% 30%, var(--primary), transparent 70%);
  }
  /* Warna cahaya diturunkan dari warna utama agar cocok untuk palet terang maupun gelap. */
  .glass-bg i:nth-child(2) { width: 34vmax; height: 34vmax; top: 8vh; right: -12vmax; opacity: .42;
    background: #ec4899;
    background: radial-gradient(circle at 30% 30%, color-mix(in srgb, var(--primary) 45%, #ec4899), transparent 70%); }
  .glass-bg i:nth-child(3) { width: 38vmax; height: 38vmax; bottom: -16vmax; left: 22vw; opacity: .4;
    background: #38bdf8;
    background: radial-gradient(circle at 30% 30%, color-mix(in srgb, var(--primary) 45%, #38bdf8), transparent 70%); }
  @media (prefers-reduced-motion: no-preference) {
    .glass-bg i { animation: glass-float 26s ease-in-out infinite alternate; }
    .glass-bg i:nth-child(2) { animation-duration: 32s; animation-direction: alternate-reverse; }
    .glass-bg i:nth-child(3) { animation-duration: 38s; }
  }
  @keyframes glass-float {
    from { transform: translate3d(0, 0, 0) scale(1); }
    to   { transform: translate3d(4vmax, 3vmax, 0) scale(1.08); }
  }
  .app { position: relative; z-index: 1; }

  /* ---------- Permukaan kaca ---------- */
  body.glass .card, body.glass .topbar, body.glass .footer, body.glass .nav,
  body.glass .nav-btn, body.glass .btn, body.glass .field input, body.glass .bar {
    -webkit-backdrop-filter: blur(var(--glass-blur, 18px)) saturate(165%);
    backdrop-filter: blur(var(--glass-blur, 18px)) saturate(165%);
  }
  /* Kilau tipis di tepi atas supaya permukaan terasa seperti kaca asli. */
  body.glass .card, body.glass .topbar, body.glass .footer, body.glass .nav-btn, body.glass .bottomnav {
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, .65), 0 10px 30px rgba(31, 38, 135, .14);
  }
  /* Lapisan tipis memakai warna teks: otomatis terang pada tema gelap dan
     gelap pada tema terang, tanpa mengubah warna pilihan pengguna. */
  body.glass .nav {
    padding: 6px; border-radius: 999px; gap: 6px;
    background: rgba(140, 150, 180, .22);
    background: color-mix(in srgb, var(--text) 10%, transparent);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, .45), 0 8px 24px rgba(31, 38, 135, .12);
  }
  body.glass .nav-btn {
    border-color: rgba(200, 200, 215, .55);
    border-color: color-mix(in srgb, var(--text) 20%, transparent);
    background: rgba(150, 155, 180, .18);
    background: color-mix(in srgb, var(--text) 7%, transparent);
  }
  body.glass .nav-btn:hover { background: color-mix(in srgb, var(--text) 16%, transparent); }
  body.glass .nav-btn.active {
    background: linear-gradient(135deg, var(--primary), color-mix(in srgb, var(--primary) 55%, #a855f7));
    color: var(--on-primary); border-color: transparent;
    box-shadow: 0 10px 24px color-mix(in srgb, var(--primary) 40%, transparent), inset 0 1px 0 rgba(255, 255, 255, .45);
  }
  body.glass .topbar, body.glass .footer {
    border: 1px solid rgba(200, 200, 215, .55);
    border-color: color-mix(in srgb, var(--text) 20%, transparent);
    border-radius: 16px; padding: 12px 16px;
    background: rgba(150, 155, 180, .18);
    background: color-mix(in srgb, var(--text) 8%, transparent);
  }
  body.glass .footer { padding-bottom: 12px; }
  body.glass .card { position: relative; border-color: rgba(200, 200, 215, .55); }
  body.glass .card { border-color: color-mix(in srgb, var(--text) 22%, transparent); }
  body.glass .card::before {
    content: ""; position: absolute; inset: 0 0 auto; height: 46%; border-radius: inherit;
    background: linear-gradient(180deg, rgba(255, 255, 255, .26), rgba(255, 255, 255, 0));
    pointer-events: none;
  }
  body.glass .btn {
    background: linear-gradient(135deg, var(--primary), color-mix(in srgb, var(--primary) 60%, #a855f7));
    border: 1px solid rgba(255, 255, 255, .45);
    box-shadow: 0 14px 30px color-mix(in srgb, var(--primary) 32%, transparent), inset 0 1px 0 rgba(255, 255, 255, .45);
    transition: transform .16s ease, box-shadow .18s ease;
  }
  body.glass .btn:hover { transform: translateY(-1px); }
  body.glass .field input {
    border-color: rgba(200, 200, 215, .6);
    border-color: color-mix(in srgb, var(--text) 22%, transparent);
    background: rgba(150, 155, 180, .14);
    background: color-mix(in srgb, var(--bg) 45%, transparent);
    backdrop-filter: blur(var(--glass-blur, 18px)) saturate(165%);
    -webkit-backdrop-filter: blur(var(--glass-blur, 18px)) saturate(165%);
  }
  body.glass .field input::placeholder { color: color-mix(in srgb, var(--text) 55%, transparent); }
  body.glass .app-title {
    display: inline-block; padding: 5px 12px; border-radius: 999px; opacity: .85;
    background: rgba(150, 155, 180, .18);
    background: color-mix(in srgb, var(--text) 8%, transparent);
    border: 1px solid rgba(200, 200, 215, .5);
    -webkit-backdrop-filter: blur(10px) saturate(150%); backdrop-filter: blur(10px) saturate(150%);
  }
  body.glass img { border-radius: 14px; }
  body.glass hr { border-top-color: rgba(255, 255, 255, .55); }
  /* Komponen bar (kartu kecil, pill, dsb.) ikut mendapat kilau kaca. */
  body.glass .bar { border-radius: 16px; }
  body.glass .bar .btn,
  body.glass .bar .btn.ghost { border: 1px solid rgba(255, 255, 255, .45); }
  body.glass .bottomnav {
    background: rgba(150, 155, 180, .35);
    background: color-mix(in srgb, var(--bg) 62%, transparent);
    border-color: color-mix(in srgb, var(--text) 18%, transparent);
  }
  /* Hormati preferensi pengguna yang sensitif terhadap gerakan. */
  @media (prefers-reduced-motion: reduce) {
    .glass-bg i { animation: none !important; }
    body.glass .btn:hover { transform: none; }
  }
"""
