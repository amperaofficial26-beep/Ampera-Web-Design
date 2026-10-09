"""CSS 20 komponen bar inti. Disusun oleh ui_builder/themes/css.py."""

BAR_CSS_CORE = """
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
