"""Semua CSS dan tautan font: ikon, gaya bar, dan gaya tampilan editor."""

ICON_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:'
    'opsz,wght,FILL,GRAD@24,400,0..1,0">'
)

# CSS untuk komponen bar di dalam HTML hasil (preview dan ekspor).
BAR_CSS = """
  .mi { font-family: 'Material Symbols Rounded'; font-weight: 400; font-style: normal; font-size: 20px;
    line-height: 1; display: inline-block; width: 1em; overflow: hidden; white-space: nowrap;
    vertical-align: middle; font-feature-settings: 'liga'; -webkit-font-smoothing: antialiased; flex: none; }
  .bar { border-radius: 12px; }
  .bar a { color: inherit; text-decoration: none; }
  .bar .btn { color: var(--on-primary); }
  .bar .btn.sm { padding: 8px 14px; font-size: 14px; }
  .bar .btn.ghost { background: transparent; color: var(--text); border: 1px solid rgba(128,128,128,.5); }
  .bottomnav { display: flex; justify-content: space-around; position: sticky; bottom: 0; z-index: 5;
    background: var(--bg); border: 1px solid rgba(128,128,128,.3); padding: 8px 4px; box-shadow: 0 -4px 16px rgba(0,0,0,.08); }
  .bn-item { display: flex; flex-direction: column; align-items: center; gap: 2px; font-size: 12px;
    padding: 4px 12px; border-radius: 12px; opacity: .65; }
  .bn-item.on { color: var(--primary); opacity: 1; font-weight: 600; }
  .tabbar { display: flex; gap: 4px; overflow-x: auto; border-bottom: 2px solid rgba(128,128,128,.25); border-radius: 0; }
  .tabbar .tab { padding: 10px 16px; margin-bottom: -2px; border-bottom: 2px solid transparent; opacity: .7; white-space: nowrap; }
  .tabbar .tab.on { border-color: var(--primary); color: var(--primary); opacity: 1; font-weight: 600; }
  .crumbs { display: flex; align-items: center; flex-wrap: wrap; gap: 2px; font-size: 14px; }
  .crumbs a { opacity: .7; }
  .crumbs .cur { font-weight: 600; }
  .crumbs .mi { font-size: 18px; opacity: .45; }
  .sidemenu { display: flex; flex-direction: column; gap: 2px; padding: 8px; border: 1px solid rgba(128,128,128,.3); }
  .sm-title { font-size: 13px; opacity: .6; padding: 6px 12px; }
  .sm-item { display: flex; align-items: center; gap: 10px; padding: 9px 12px; border-radius: 10px; }
  .sm-item:hover { background: rgba(128,128,128,.12); }
  .sm-item.on { background: var(--primary); color: var(--on-primary); }
  .pager { display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; }
  .pager a { min-width: 36px; height: 36px; display: inline-flex; align-items: center; justify-content: center;
    border: 1px solid rgba(128,128,128,.35); border-radius: 10px; padding: 0 8px; }
  .pager a.on { background: var(--primary); border-color: var(--primary); color: var(--on-primary); font-weight: 600; }
  .pager .dots { display: inline-flex; align-items: center; opacity: .6; }
  .toolbar { display: flex; gap: 6px; flex-wrap: wrap; padding: 6px; border: 1px solid rgba(128,128,128,.3); }
  .tb-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 12px; border-radius: 10px; border: 0;
    background: transparent; color: inherit; font: inherit; font-size: 14px; cursor: pointer; }
  .tb-btn:hover { background: rgba(128,128,128,.15); }
  .searchbar { display: flex; align-items: center; gap: 8px; padding: 6px 6px 6px 14px; border: 1px solid rgba(128,128,128,.4); border-radius: 999px; }
  .searchbar input { flex: 1; min-width: 0; border: 0; outline: 0; background: transparent; color: inherit; font: inherit; padding: 6px 0; }
  .searchbar .btn { padding: 8px 18px; border-radius: 999px; }
  .chips { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 2px; }
  .fchip { white-space: nowrap; padding: 7px 14px; border: 1px solid rgba(128,128,128,.4); border-radius: 999px; font-size: 14px; }
  .fchip.on { background: var(--primary); border-color: var(--primary); color: var(--on-primary); font-weight: 600; }
  .fabwrap { position: sticky; bottom: 16px; z-index: 5; pointer-events: none; }
  .fab { pointer-events: auto; display: inline-flex; align-items: center; gap: 8px; background: var(--primary);
    color: var(--on-primary) !important; padding: 14px 20px; border-radius: 999px; box-shadow: 0 8px 20px rgba(0,0,0,.25); font-weight: 600; }
  .social { display: flex; gap: 8px; flex-wrap: wrap; }
  .social a { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; border: 1px solid rgba(128,128,128,.35); border-radius: 999px; font-size: 14px; }
  .announce { background: var(--primary); color: var(--on-primary); text-align: center; padding: 10px 16px; font-size: 14px; border-radius: 0; }
  .announce a { color: var(--on-primary); text-decoration: underline; font-weight: 600; margin-left: 8px; }
  .status { display: flex; gap: 10px; align-items: flex-start; padding: 12px 14px; border: 1px solid; border-left-width: 4px; font-size: 14px; }
  .status.info { background: #eff6ff; border-color: #3b82f6; color: #1e3a8a; }
  .status.success { background: #f0fdf4; border-color: #22c55e; color: #14532d; }
  .status.warning { background: #fffbeb; border-color: #f59e0b; color: #78350f; }
  .status.error { background: #fef2f2; border-color: #ef4444; color: #7f1d1d; }
  .pg-head { display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 6px; }
  .pg-track { height: 10px; border-radius: 999px; background: rgba(128,128,128,.25); overflow: hidden; }
  .pg-fill { height: 100%; background: var(--primary); border-radius: 999px; }
  .stepper { display: flex; align-items: flex-start; }
  .st-step { flex: 1; text-align: center; position: relative; font-size: 13px; }
  .st-step::before { content: ""; position: absolute; top: 15px; left: -50%; width: 100%; height: 2px; background: rgba(128,128,128,.35); }
  .st-step:first-child::before { display: none; }
  .st-dot { position: relative; z-index: 1; width: 32px; height: 32px; margin: 0 auto 6px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; background: var(--bg); border: 2px solid rgba(128,128,128,.5); font-weight: 600; font-size: 14px; }
  .st-dot .mi { font-size: 18px; }
  .st-step.done .st-dot, .st-step.now .st-dot { border-color: var(--primary); }
  .st-step.done .st-dot { background: var(--primary); color: var(--on-primary); }
  .st-step.done::before, .st-step.now::before { background: var(--primary); }
  .st-step.now { color: var(--primary); font-weight: 600; }
  .rating { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
  .rating .stars { display: inline-flex; color: #f59e0b; }
  .rating .mi { font-size: 22px; font-variation-settings: 'FILL' 1; }
  .rating .off { opacity: .3; display: inline-flex; }
  .rating small { opacity: .65; }
  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 12px; }
  .stat { text-align: center; padding: 14px 8px; border: 1px solid rgba(128,128,128,.3); border-radius: 12px; }
  .stat strong { display: block; font-size: 24px; color: var(--primary); }
  .stat span { font-size: 13px; opacity: .7; }
  .pricebar { position: sticky; bottom: 0; z-index: 5; display: flex; align-items: center; justify-content: space-between;
    gap: 12px; padding: 12px 16px; background: var(--bg); border: 1px solid rgba(128,128,128,.3); box-shadow: 0 -4px 16px rgba(0,0,0,.08); }
  .pricebar strong { font-size: 20px; }
  .pricebar small { display: block; opacity: .65; }
  .cats { display: flex; gap: 14px; overflow-x: auto; padding: 4px; }
  .cat { display: flex; flex-direction: column; align-items: center; gap: 6px; font-size: 12px; min-width: 64px; }
  .cat-ico { width: 52px; height: 52px; border-radius: 16px; display: flex; align-items: center; justify-content: center;
    background: rgba(128,128,128,.14); color: var(--primary); }
  .cat-ico .mi { font-size: 26px; }
  .profilebar { display: flex; align-items: center; gap: 12px; padding: 12px; border: 1px solid rgba(128,128,128,.3); }
  .avatar { width: 48px; height: 48px; border-radius: 50%; background: var(--primary); color: var(--on-primary); display: flex;
    align-items: center; justify-content: center; font-weight: 700; overflow: hidden; flex: none; }
  .avatar img { width: 100%; height: 100%; object-fit: cover; }
  .pf-text { flex: 1; min-width: 0; }
  .pf-text small { display: block; opacity: .65; }
  .cookie { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; padding: 14px 16px;
    border: 1px solid rgba(128,128,128,.3); box-shadow: 0 8px 24px rgba(0,0,0,.12); }
  .cookie p { flex: 1; min-width: 180px; margin: 0; font-size: 14px; }
"""

# CSS untuk tampilan aplikasi editor Streamlit itu sendiri.
APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stAppDeployButton"], [data-testid="stMainMenu"],
.stAppDeployButton, .stDeployButton, [data-testid="stSidebarCollapsedControl"] {
  display: none !important; visibility: hidden !important; height: 0 !important; }
.stApp { font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  background: radial-gradient(900px 420px at 8% -8%, rgba(99,102,241,.16), transparent 62%),
              radial-gradient(800px 380px at 100% 0%, rgba(236,72,153,.12), transparent 60%); }
.stApp button, .stApp input, .stApp textarea, .stApp [data-baseweb="select"] { font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; }
.block-container { padding-top: 1.1rem !important; padding-bottom: 1rem !important; max-width: 1680px; }
h5 { margin-bottom: .2rem; font-weight: 700; }
.st-key-hero { background: linear-gradient(115deg, #3730a3 0%, #6d28d9 50%, #be185d 115%); border-radius: 20px;
  padding: 18px 26px !important; box-shadow: 0 14px 34px rgba(79,70,229,.32); }
.st-key-hero, .st-key-hero * { color: #fff !important; }
.st-key-hero h2 { margin: 0 !important; padding: 0 !important; font-weight: 700; letter-spacing: -.01em; }
.st-key-hero [data-testid="stCaptionContainer"] { opacity: .88; }
.st-key-hero [data-testid="stColumn"]:last-child { text-align: right; }
.st-key-projbar { border-radius: 16px !important; border: 1px solid rgba(128,128,128,.22) !important; background: rgba(128,128,128,.045); }
.st-key-panel_left, .st-key-panel_right { border-radius: 18px !important; border: 1px solid rgba(128,128,128,.22) !important;
  background: rgba(128,128,128,.045); box-shadow: 0 8px 24px rgba(0,0,0,.06); }
.stButton > button, .stDownloadButton > button { border-radius: 10px; font-weight: 600;
  transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease; }
.stButton > button:hover, .stDownloadButton > button:hover { transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(99,102,241,.22); border-color: #6366f1; }
[data-testid="stBaseButton-primary"] { background: linear-gradient(120deg, #6366f1, #8b5cf6) !important; border: 0 !important; color: #fff !important; }
.stTabs [data-baseweb="tab"] { font-weight: 600; }
.stTabs [data-baseweb="tab-highlight"] { background-color: #6366f1 !important; height: 3px; border-radius: 3px; }
.stTabs [aria-selected="true"] { color: #6366f1 !important; }
[data-testid="stExpander"] { border-radius: 14px; border: 1px solid rgba(128,128,128,.25); }
.tpl-sws { display: flex; gap: 4px; margin: 2px 0 4px; }
.tpl-sw { width: 16px; height: 16px; border-radius: 50%; border: 1px solid rgba(128,128,128,.45); }
.ref-prev { display: flex; align-items: center; gap: 10px; padding: 12px; border-radius: 12px;
  border: 1px solid rgba(128,128,128,.25); margin-bottom: 6px; }
.ref-card { flex: 1; padding: 8px 10px; display: flex; flex-direction: column; font-size: 13px; }
.ref-card span { font-size: 12px; opacity: .8; }
.ref-btn { padding: 8px 12px; font-size: 13px; font-weight: 600; }
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-thumb { background: rgba(128,128,128,.35); border-radius: 8px; }
"""
