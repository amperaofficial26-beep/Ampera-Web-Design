"""Tema AOG Web Desain: CSS untuk tampilan editor Streamlit (dark profesional + aksen hangat).

Hanya mengatur tampilan editor. CSS komponen hasil (BAR_CSS) tetap di css.py.
"""

AOG_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
:root {
  --aog-bg: #0F1115; --aog-surface: #181B21; --aog-panel: #1C2027; --aog-surface2: #22262E;
  --aog-border: rgba(255,255,255,.08); --aog-text: #F4F5F7; --aog-text2: #A8ADB7; --aog-muted: #737985;
  --aog-accent: #D6A85F; --aog-accent-soft: rgba(214,168,95,.14);
}
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stAppDeployButton"], [data-testid="stMainMenu"],
.stAppDeployButton, .stDeployButton, [data-testid="stSidebarCollapsedControl"] {
  display: none !important; visibility: hidden !important; height: 0 !important; }
.stApp { background: var(--aog-bg); color: var(--aog-text); font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; }
.stApp button, .stApp input, .stApp textarea, .stApp [data-baseweb="select"] { font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; }
.block-container { padding: .75rem 1rem 1rem !important; max-width: 100% !important; }
h4 { font-size: 13px !important; letter-spacing: .08em; text-transform: uppercase; color: var(--aog-text2); margin: 0 0 4px !important; padding: 0 !important; font-weight: 600; }
h3 { font-size: 13px !important; letter-spacing: .08em; text-transform: uppercase; color: var(--aog-text2); font-weight: 600; padding: 0 !important; }
h5 { font-size: 14px !important; font-weight: 600; margin-bottom: 4px; }
[data-testid="stCaptionContainer"] { color: var(--aog-muted); font-size: 12px; }
:focus-visible { outline: 2px solid var(--aog-accent) !important; outline-offset: 2px; }

/* Header / toolbar */
.st-key-aog_header { background: var(--aog-surface); border: 1px solid var(--aog-border); border-radius: 12px; padding: 8px 16px !important; }
.aog-brand { display: flex; flex-direction: column; line-height: 1.15; }
.aog-name { font-size: 16px; font-weight: 700; color: var(--aog-text); letter-spacing: -.01em; }
.aog-sub { font-size: 11px; color: var(--aog-accent); letter-spacing: .04em; }
.aog-status { font-size: 12px; color: var(--aog-text2); text-align: right; }

/* Panel */
.st-key-panel_left, .st-key-panel_right { background: var(--aog-panel); border: 1px solid var(--aog-border) !important; border-radius: 12px !important; }
.st-key-canvas_area { background: #14161B; border: 1px solid var(--aog-border); border-radius: 12px; padding: 16px !important; min-height: 420px; }
.st-key-canvas_area iframe { border-radius: 12px; }
.st-key-component_library { background: var(--aog-surface); border: 1px solid var(--aog-border) !important; border-radius: 12px !important; }

/* Tombol */
.stButton > button, .stDownloadButton > button { background: var(--aog-surface2); color: var(--aog-text); border: 1px solid var(--aog-border);
  border-radius: 8px; font-weight: 500; font-size: 13px; transition: border-color .15s ease, background .15s ease, color .15s ease; }
.stButton > button:hover, .stDownloadButton > button:hover { border-color: var(--aog-accent); color: var(--aog-accent); background: var(--aog-accent-soft); }
[data-testid="stBaseButton-primary"] { background: var(--aog-accent) !important; color: #1A1407 !important; border: 0 !important; font-weight: 600; }
[data-testid="stBaseButton-primary"]:hover { filter: brightness(1.06); color: #1A1407 !important; }

/* Input */
[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="textarea"] { border-radius: 8px !important; }

/* Segmented control (radio horizontal) */
.stRadio [role="radiogroup"] { gap: 4px; background: var(--aog-surface2); padding: 3px; border-radius: 10px; border: 1px solid var(--aog-border); display: inline-flex; }
.stRadio label[data-baseweb="radio"] { padding: 5px 12px; border-radius: 8px; margin: 0; cursor: pointer; transition: background .15s ease; }
.stRadio label[data-baseweb="radio"] > div:first-child { display: none; }
.stRadio label[data-baseweb="radio"]:has(input:checked) { background: var(--aog-accent-soft); box-shadow: inset 0 0 0 1px var(--aog-accent); }
.stRadio label[data-baseweb="radio"]:has(input:checked) p { color: var(--aog-accent); font-weight: 600; }
.stRadio label[data-baseweb="radio"] p { font-size: 13px; }

/* Tab */
.stTabs [data-baseweb="tab-list"] { gap: 2px; }
.stTabs [data-baseweb="tab"] { padding: 6px 10px; font-size: 12.5px; font-weight: 500; }
.stTabs [data-baseweb="tab-highlight"] { background-color: var(--aog-accent) !important; height: 2px; }
.stTabs [aria-selected="true"] { color: var(--aog-accent) !important; }
[data-testid="stExpander"] { border-radius: 10px; border: 1px solid var(--aog-border); background: var(--aog-surface); }

/* Kartu komponen di Component Library */
.st-key-component_library .stButton > button { flex-direction: column; height: 72px; gap: 4px; padding: 8px 4px; font-size: 12px; line-height: 1.2; border-radius: 10px; }
.st-key-component_library .stButton > button [data-testid="stIconMaterial"], .st-key-component_library .stButton > button span[class*="Icon"] { font-size: 22px; }
.st-key-component_library .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,.35); }

/* Empty state */
.st-key-aog_empty { padding-top: 40px; text-align: center; }
.st-key-aog_empty h1 { color: var(--aog-accent); font-size: 44px !important; text-align: center; padding: 0 !important; }
.st-key-aog_empty [data-testid="stButton"], .st-key-aog_empty [data-testid="stElementContainer"]:has(button) { display: flex; justify-content: center; }
.st-key-aog_header [data-testid="stCaptionContainer"] { text-align: right; }
.aog-empty { text-align: center; padding: 0 16px 12px; color: var(--aog-text2); }
.aog-empty h3 { text-transform: none; letter-spacing: 0; font-size: 18px !important; color: var(--aog-text); margin: 8px 0 4px !important; }
.aog-empty p { font-size: 13px; max-width: 420px; margin: 0 auto; }
.aog-hint { text-align: center; padding: 20px 8px; color: var(--aog-muted); font-size: 12.5px; border: 1px dashed var(--aog-border); border-radius: 10px; }

/* Template & gaya (dipakai fungsi swatches_html dan ref_preview_html) */
.tpl-sws { display: flex; gap: 4px; margin: 2px 0 4px; }
.tpl-sw { width: 16px; height: 16px; border-radius: 50%; border: 1px solid rgba(255,255,255,.25); }
.ref-prev { display: flex; align-items: center; gap: 10px; padding: 12px; border-radius: 10px; border: 1px solid var(--aog-border); margin-bottom: 6px; }
.ref-card { flex: 1; padding: 8px 10px; display: flex; flex-direction: column; font-size: 13px; }
.ref-card span { font-size: 12px; opacity: .8; }
.ref-btn { padding: 8px 12px; font-size: 13px; font-weight: 600; }

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,.16); border-radius: 8px; }
@media (max-width: 900px) { .block-container { padding: .5rem !important; } .st-key-canvas_area { padding: 8px !important; } }
"""
