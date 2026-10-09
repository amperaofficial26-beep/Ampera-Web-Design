"""CSS 50 komponen bar tambahan (paket lama).

Setiap komponen memakai kelas induk sendiri, anak-anaknya di-scope agar tidak bentrok.
Disusun oleh ui_builder/themes/css.py.
"""

BAR_CSS_EXTRA = """
  .avatar.sm { width: 36px; height: 36px; font-size: 14px; }
  /* ---------- Navigasi ---------- */
  .menubar { display: flex; align-items: center; gap: 4px; padding: 6px; border: 1px solid rgba(128,128,128,.3); }
  .menubar .mb-brand { display: inline-flex; align-items: center; justify-content: center; width: 34px; height: 34px;
    border-radius: 10px; background: var(--primary); color: var(--on-primary); margin-right: 4px; flex: none; }
  .menubar .mb-item { padding: 8px 12px; border-radius: 9px; font-size: 14px; opacity: .8; white-space: nowrap; }
  .menubar .mb-item:hover { background: rgba(128,128,128,.14); }
  .menubar .mb-item.on { background: rgba(128,128,128,.16); opacity: 1; font-weight: 600; }
  .menubar .btn { margin-left: auto; }
  .pilltabs { display: flex; gap: 6px; flex-wrap: wrap; padding: 6px; background: rgba(128,128,128,.12); }
  .pilltabs .pl-item { padding: 7px 16px; border-radius: 999px; font-size: 14px; opacity: .75; white-space: nowrap; }
  .pilltabs .pl-item.on { background: var(--bg); color: var(--primary); opacity: 1; font-weight: 600;
    box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .railnav { display: flex; flex-direction: column; gap: 4px; padding: 8px; width: 90px; border: 1px solid rgba(128,128,128,.3); }
  .railnav .rn-item { display: flex; flex-direction: column; align-items: center; gap: 3px; padding: 9px 4px;
    border-radius: 12px; font-size: 11px; opacity: .75; }
  .railnav .rn-item.on { background: var(--primary); color: var(--on-primary); opacity: 1; }
  .railnav .rn-ico { position: relative; display: inline-flex; }
  .railnav .rn-lbl { max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .railnav .rn-badge { position: absolute; top: -6px; right: -9px; min-width: 16px; padding: 0 4px; border-radius: 999px;
    background: #ef4444; color: #fff; font-size: 10px; line-height: 16px; text-align: center; font-weight: 700; }
  .backbar { display: flex; align-items: center; gap: 10px; padding: 6px 2px; }
  .backbar .bb-back { display: inline-flex; align-items: center; gap: 4px; font-size: 14px; opacity: .8; white-space: nowrap; }
  .backbar .bb-title { flex: 1; text-align: center; }
  .backbar .bb-action { display: inline-flex; align-items: center; gap: 4px; font-size: 14px; color: var(--primary);
    white-space: nowrap; }
  .anchorlinks { position: sticky; top: 0; z-index: 4; display: flex; gap: 18px; overflow-x: auto; padding: 10px 2px;
    background: var(--bg); border-bottom: 1px solid rgba(128,128,128,.25); border-radius: 0; }
  .anchorlinks .an-item { font-size: 14px; white-space: nowrap; opacity: .75; padding-bottom: 2px; }
  .anchorlinks .an-item.on { color: var(--primary); opacity: 1; font-weight: 600; border-bottom: 2px solid var(--primary); }
  .prevnext { display: flex; gap: 12px; }
  .prevnext .pn-card { flex: 1; min-width: 0; display: flex; align-items: center; gap: 10px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); border-radius: 12px; }
  .prevnext .pn-card:hover { border-color: var(--primary); }
  .prevnext .pn-card.next { justify-content: flex-end; text-align: right; }
  .prevnext .pn-text { display: flex; flex-direction: column; min-width: 0; }
  .prevnext .pn-text strong { font-size: 14px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .prevnext .pn-text small { font-size: 12px; opacity: .65; }
  .prevnext .pn-gap { flex: 1; }
  .meganav { padding: 14px; border: 1px solid rgba(128,128,128,.3); }
  .meganav .mg-title { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .06em;
    opacity: .6; margin-bottom: 8px; }
  .meganav .mg-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 6px; }
  .meganav .mg-item { display: flex; gap: 10px; align-items: flex-start; padding: 10px; border-radius: 10px; }
  .meganav .mg-item:hover { background: rgba(128,128,128,.12); }
  .meganav .mg-ico { color: var(--primary); display: inline-flex; }
  .meganav .mg-text { display: flex; flex-direction: column; min-width: 0; }
  .meganav .mg-text strong { font-size: 14px; }
  .meganav .mg-text small { font-size: 12px; opacity: .65; }
  /* ---------- Aksi ---------- */
  .actionbar { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
  .actionbar .ab-note { flex: 1; min-width: 140px; font-size: 13px; opacity: .7; }
  .actionbar .ab-btns { display: inline-flex; gap: 8px; margin-left: auto; }
  .commandbar { display: flex; align-items: center; gap: 10px; padding: 6px 6px 6px 14px;
    border: 1px solid rgba(128,128,128,.4); border-radius: 12px; }
  .commandbar input { flex: 1; min-width: 0; padding: 7px 0; border: 0; outline: 0; background: transparent;
    color: inherit; font: inherit; }
  .commandbar .cb-kbd { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; padding: 5px 9px;
    border-radius: 7px; border: 1px solid rgba(128,128,128,.4); background: rgba(128,128,128,.12); white-space: nowrap; }
  .sortbar { display: flex; align-items: center; gap: 10px; padding: 6px; border: 1px solid rgba(128,128,128,.3); }
  .sortbar .sr-label { font-size: 13px; opacity: .7; }
  .sortbar .sr-select { margin-left: auto; display: inline-flex; align-items: center; gap: 4px; padding: 8px 10px;
    border: 1px solid rgba(128,128,128,.35); border-radius: 10px; background: transparent; color: inherit;
    font: inherit; font-size: 14px; cursor: pointer; white-space: nowrap; }
  .sortbar .sr-views { display: inline-flex; gap: 2px; padding: 3px; background: rgba(128,128,128,.14); border-radius: 10px; }
  .sortbar .sr-view { display: inline-flex; padding: 5px; border: 0; border-radius: 8px; background: transparent;
    color: inherit; opacity: .65; cursor: pointer; }
  .sortbar .sr-view.on { background: var(--bg); color: var(--primary); opacity: 1; }
  .sharebar { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
  .sharebar .sh-label { font-size: 13px; opacity: .7; }
  .sharebar .sh-items { display: inline-flex; gap: 8px; flex-wrap: wrap; }
  .sharebar .sh-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; border-radius: 999px;
    border: 1px solid rgba(128,128,128,.35); background: transparent; color: inherit; font: inherit; font-size: 13px;
    cursor: pointer; }
  .sharebar .sh-btn:hover { border-color: var(--primary); color: var(--primary); }
  .commentbar { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; padding: 10px;
    border: 1px solid rgba(128,128,128,.3); }
  .commentbar input { flex: 1; min-width: 150px; padding: 9px 14px; border-radius: 999px;
    border: 1px solid rgba(128,128,128,.35); background: transparent; color: inherit; font: inherit; }
  .commentbar .cm-hint { flex-basis: 100%; padding-left: 46px; font-size: 11px; opacity: .6; }
  .quickactions { display: flex; gap: 10px; overflow-x: auto; padding: 4px; }
  .quickactions .qa-item { flex: none; display: flex; flex-direction: column; align-items: center; gap: 6px; width: 86px;
    padding: 12px 6px; border: 1px solid rgba(128,128,128,.25); border-radius: 14px; background: transparent;
    color: inherit; font: inherit; font-size: 12px; cursor: pointer; }
  .quickactions .qa-item:hover { border-color: var(--primary); }
  .quickactions .qa-ico { color: var(--primary); display: inline-flex; }
  .quickactions .qa-ico .mi { font-size: 24px; }
  .linkbar { display: flex; flex-wrap: wrap; gap: 2px 0; justify-content: center; font-size: 13px; }
  .linkbar .lk-item { opacity: .75; }
  .linkbar .lk-item:hover { color: var(--primary); opacity: 1; }
  .linkbar .lk-item + .lk-item::before { content: "·"; margin: 0 10px; opacity: .5; }
  /* ---------- Informasi ---------- */
  .infobanner { display: flex; align-items: flex-start; gap: 12px; padding: 14px 16px; border: 1px solid; font-size: 14px; }
  .infobanner.info { background: #eff6ff; border-color: #bfdbfe; color: #1e3a8a; }
  .infobanner.success { background: #f0fdf4; border-color: #bbf7d0; color: #14532d; }
  .infobanner.warning { background: #fffbeb; border-color: #fde68a; color: #78350f; }
  .infobanner.error { background: #fef2f2; border-color: #fecaca; color: #7f1d1d; }
  .infobanner .ib-ico { display: inline-flex; }
  .infobanner .ib-text { flex: 1; min-width: 0; display: flex; flex-direction: column; }
  .infobanner a { color: inherit; font-weight: 600; text-decoration: underline; white-space: nowrap; }
  .tipbar { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; padding: 12px 16px;
    border: 1px dashed rgba(128,128,128,.5); background: rgba(128,128,128,.07); }
  .tipbar > .mi { color: #f59e0b; }
  .tipbar .tp-text { flex: 1; min-width: 160px; display: flex; flex-direction: column; font-size: 13px; }
  .tipbar .tp-label { font-size: 11px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; opacity: .6; }
  .quotebar { margin: 0; padding: 16px 18px; border-left: 4px solid var(--primary); background: rgba(128,128,128,.07); }
  .quotebar > .mi { color: var(--primary); opacity: .5; }
  .quotebar p { margin: 4px 0 8px; font-size: 16px; font-style: italic; }
  .quotebar footer { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; font-size: 13px; font-weight: 600; }
  .quotebar footer small { font-weight: 400; opacity: .65; }
  .totalbar { padding: 14px 16px; border: 1px solid rgba(128,128,128,.3); font-size: 14px; }
  .totalbar .tt-row { display: flex; justify-content: space-between; gap: 12px; padding: 4px 0; }
  .totalbar .tt-row span:first-child { opacity: .75; }
  .totalbar .tt-total { margin-top: 8px; padding-top: 10px; border-top: 1px solid rgba(128,128,128,.3); font-size: 16px; }
  .totalbar .tt-total strong { color: var(--primary); }
  .countdownbar { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; padding: 12px 16px;
    border: 1px solid rgba(128,128,128,.3); }
  .countdownbar .cd-label { flex: 1; min-width: 140px; font-size: 14px; font-weight: 600; }
  .countdownbar .cd-set { display: inline-flex; gap: 8px; }
  .countdownbar .cd-box { display: flex; flex-direction: column; align-items: center; min-width: 56px; padding: 8px 6px;
    border-radius: 10px; background: var(--primary); color: var(--on-primary); }
  .countdownbar .cd-box strong { font-size: 20px; line-height: 1.1; }
  .countdownbar .cd-box small { font-size: 11px; opacity: .85; }
  .stockbar { display: flex; align-items: flex-start; gap: 10px; padding: 12px 14px; font-size: 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .stockbar .sk-dot { flex: none; width: 10px; height: 10px; margin-top: 6px; border-radius: 50%; background: #22c55e; }
  .stockbar.low .sk-dot { background: #f59e0b; }
  .stockbar.out .sk-dot { background: #ef4444; }
  .stockbar .sk-body { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 6px; }
  .stockbar .sk-track { height: 6px; border-radius: 999px; background: rgba(128,128,128,.25); overflow: hidden; }
  .stockbar .sk-track span { display: block; height: 100%; background: #22c55e; }
  .stockbar.low .sk-track span { background: #f59e0b; }
  .stockbar.out .sk-track span { background: #ef4444; }
  .stockbar .sk-note { font-size: 12px; opacity: .65; }
  .livebar { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border: 1px solid rgba(128,128,128,.3); }
  .livebar .lv-badge { display: inline-flex; align-items: center; gap: 6px; padding: 5px 10px; border-radius: 999px;
    background: #ef4444; color: #fff; font-size: 11px; font-weight: 700; letter-spacing: .08em; }
  .livebar .lv-dot { width: 7px; height: 7px; border-radius: 50%; background: #fff; animation: lvpulse 1.4s ease-in-out infinite; }
  @keyframes lvpulse { 0%, 100% { opacity: 1 } 50% { opacity: .25 } }
  .livebar .lv-text { flex: 1; min-width: 0; display: flex; flex-direction: column; }
  .livebar .lv-text small { display: inline-flex; align-items: center; gap: 4px; font-size: 12px; opacity: .65; }
  .livebar .lv-text small .mi { font-size: 15px; }
  /* ---------- Data ---------- */
  .tablebar { overflow-x: auto; border: 1px solid rgba(128,128,128,.3); }
  .tablebar table { width: 100%; border-collapse: collapse; font-size: 14px; }
  .tablebar th { text-align: left; padding: 10px 12px; font-size: 12px; text-transform: uppercase;
    letter-spacing: .04em; opacity: .75; background: rgba(128,128,128,.12); }
  .tablebar td { padding: 10px 12px; border-top: 1px solid rgba(128,128,128,.25); }
  .comparebar { padding: 14px 16px; border: 1px solid rgba(128,128,128,.3); }
  .comparebar .cp-title { font-size: 14px; font-weight: 600; margin-bottom: 8px; }
  .comparebar .cp-row { display: flex; align-items: center; gap: 10px; padding: 4px 0; font-size: 13px; }
  .comparebar .cp-label { flex: 0 0 96px; opacity: .8; }
  .comparebar .cp-track { flex: 1; height: 10px; border-radius: 999px; background: rgba(128,128,128,.2); overflow: hidden; }
  .comparebar .cp-fill { display: block; height: 100%; border-radius: 999px; background: var(--primary); }
  .comparebar .cp-fill.alt { background: rgba(128,128,128,.55); }
  .comparebar .cp-row strong { flex: 0 0 46px; text-align: right; }
  .comparebar .cp-note { display: block; margin-top: 8px; font-size: 12px; opacity: .65; }
  .sparkbar { display: flex; align-items: flex-end; gap: 12px; padding: 14px 16px; border: 1px solid rgba(128,128,128,.3); }
  .sparkbar .sp-label { flex: 0 0 auto; font-size: 13px; font-weight: 600; }
  .sparkbar .sp-chart { flex: 1; display: flex; align-items: flex-end; gap: 5px; height: 56px; }
  .sparkbar .sp-bar { flex: 1; min-width: 6px; border-radius: 4px 4px 0 0; background: rgba(128,128,128,.35); }
  .sparkbar .sp-bar.last { background: var(--primary); }
  .sparkbar .sp-note { flex: 0 0 auto; font-size: 12px; opacity: .65; }
  .legendbar { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; padding: 10px 14px;
    border: 1px solid rgba(128,128,128,.3); font-size: 13px; }
  .legendbar .lg-title { font-weight: 600; opacity: .8; }
  .legendbar .lg-item { display: inline-flex; align-items: center; gap: 6px; opacity: .85; }
  .legendbar .lg-dot { width: 12px; height: 12px; border-radius: 4px; }
  .timelinebar { display: flex; align-items: flex-start; }
  .timelinebar .tl-step { flex: 1; position: relative; display: flex; flex-direction: column; align-items: center;
    gap: 2px; font-size: 13px; text-align: center; }
  .timelinebar .tl-step::before { content: ""; position: absolute; top: 14px; left: -50%; width: 100%; height: 2px;
    background: rgba(128,128,128,.35); }
  .timelinebar .tl-step:first-child::before { display: none; }
  .timelinebar .tl-dot { position: relative; z-index: 1; width: 30px; height: 30px; margin-bottom: 4px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; background: var(--bg); font-size: 13px; font-weight: 600;
    border: 2px solid rgba(128,128,128,.5); }
  .timelinebar .tl-dot .mi { font-size: 17px; }
  .timelinebar .tl-step.done .tl-dot { background: var(--primary); border-color: var(--primary); color: var(--on-primary); }
  .timelinebar .tl-step.done::before, .timelinebar .tl-step.now::before { background: var(--primary); }
  .timelinebar .tl-step.now .tl-dot { border-color: var(--primary); color: var(--primary); }
  .timelinebar .tl-step.now strong { color: var(--primary); }
  .timelinebar .tl-step small { font-size: 11px; opacity: .6; }
  .rangebar { padding: 14px 16px; border: 1px solid rgba(128,128,128,.3); }
  .rangebar .rg-head { display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 14px; }
  .rangebar .rg-track { position: relative; height: 6px; border-radius: 999px; background: rgba(128,128,128,.25); }
  .rangebar .rg-fill { position: absolute; top: 0; height: 100%; background: var(--primary); border-radius: 999px; }
  .rangebar .rg-knob { position: absolute; top: 50%; width: 18px; height: 18px; margin-left: -9px; border-radius: 50%;
    background: var(--bg); border: 3px solid var(--primary); transform: translateY(-50%); box-sizing: border-box; }
  .rangebar .rg-labels { display: flex; justify-content: space-between; margin-top: 10px; font-size: 12px; opacity: .65; }
  .calendarstrip { display: flex; gap: 8px; overflow-x: auto; padding: 4px; }
  .calendarstrip .cs-day { flex: none; display: flex; flex-direction: column; align-items: center; gap: 2px;
    width: 54px; padding: 8px 4px; border: 1px solid rgba(128,128,128,.3); border-radius: 12px; background: transparent;
    color: inherit; font: inherit; cursor: pointer; }
  .calendarstrip .cs-day small { font-size: 11px; opacity: .65; }
  .calendarstrip .cs-day strong { font-size: 16px; }
  .calendarstrip .cs-day.on { background: var(--primary); border-color: var(--primary); color: var(--on-primary); }
  .calendarstrip .cs-day.on small { opacity: .9; }
  /* ---------- Formulir ---------- */
  .formbar { display: block; padding: 12px 14px; border: 1px solid rgba(128,128,128,.3); }
  .formbar .fm-label { display: block; margin-bottom: 6px; font-size: 13px; font-weight: 600; }
  .formbar .fm-row { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  .formbar input { flex: 1; min-width: 150px; padding: 10px 12px; border-radius: 10px;
    border: 1px solid rgba(128,128,128,.45); background: transparent; color: inherit; font: inherit; }
  .newsletterbar { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; padding: 16px;
    border: 1px solid rgba(128,128,128,.3); background: rgba(128,128,128,.06); }
  .newsletterbar > .mi { color: var(--primary); font-size: 28px; }
  .newsletterbar .nl-text { display: flex; flex-direction: column; min-width: 160px; }
  .newsletterbar .nl-note { font-size: 12px; opacity: .65; }
  .newsletterbar .nl-form { display: flex; gap: 8px; flex: 1; min-width: 220px; }
  .newsletterbar input { flex: 1; min-width: 120px; padding: 10px 12px; border-radius: 10px;
    border: 1px solid rgba(128,128,128,.45); background: var(--bg); color: inherit; font: inherit; }
  .otpbar { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; padding: 14px 16px;
    border: 1px solid rgba(128,128,128,.3); }
  .otpbar .ot-label { flex: 1; min-width: 150px; font-size: 14px; font-weight: 600; }
  .otpbar .ot-set { display: inline-flex; gap: 8px; }
  .otpbar .ot-box { width: 40px; height: 48px; border-radius: 10px; border: 2px solid rgba(128,128,128,.4);
    background: rgba(128,128,128,.08); }
  .otpbar .ot-box.on { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(99,102,241,.2); }
  .otpbar .ot-note { flex-basis: 100%; font-size: 12px; opacity: .6; }
  .tagsinputbar { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; padding: 10px 12px;
    border: 1px solid rgba(128,128,128,.3); }
  .tagsinputbar .tg-set { flex: 1; min-width: 180px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
  .tagsinputbar .tg-chip { display: inline-flex; align-items: center; gap: 4px; padding: 5px 8px 5px 12px;
    border-radius: 999px; background: rgba(128,128,128,.16); font-size: 13px; }
  .tagsinputbar .tg-chip .mi { font-size: 16px; opacity: .6; }
  .tagsinputbar input { flex: 1; min-width: 110px; border: 0; outline: 0; background: transparent; color: inherit;
    font: inherit; padding: 6px 2px; }
  .sliderbar { padding: 14px 16px; border: 1px solid rgba(128,128,128,.3); }
  .sliderbar .sl-head { display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 14px; }
  .sliderbar .sl-track { position: relative; height: 6px; border-radius: 999px; background: rgba(128,128,128,.25); }
  .sliderbar .sl-fill { position: absolute; top: 0; height: 100%; border-radius: 999px; background: var(--primary); }
  .sliderbar .sl-knob { position: absolute; top: 50%; width: 20px; height: 20px; margin-left: -10px; border-radius: 50%;
    background: var(--primary); border: 3px solid var(--bg); transform: translateY(-50%); box-sizing: border-box;
    box-shadow: 0 1px 6px rgba(0,0,0,.25); }
  .sliderbar .sl-labels { display: flex; justify-content: space-between; margin-top: 10px; font-size: 12px; opacity: .65; }
  .switchbar { padding: 6px 14px; border: 1px solid rgba(128,128,128,.3); }
  .switchbar .sw-row { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 10px 0;
    font-size: 14px; cursor: pointer; }
  .switchbar .sw-row + .sw-row { border-top: 1px solid rgba(128,128,128,.2); }
  .switchbar .sw-track { flex: none; width: 46px; height: 26px; border-radius: 999px; background: rgba(128,128,128,.4);
    padding: 3px; box-sizing: border-box; }
  .switchbar .sw-track.on { background: var(--primary); }
  .switchbar .sw-knob { display: block; width: 20px; height: 20px; border-radius: 50%; background: #fff;
    transition: transform .16s ease; }
  .switchbar .sw-track.on .sw-knob { transform: translateX(20px); }
  .loginbar { display: flex; flex-direction: column; gap: 10px; padding: 18px; border: 1px solid rgba(128,128,128,.3);
    box-shadow: 0 8px 24px rgba(0,0,0,.08); }
  .loginbar strong { font-size: 16px; }
  .loginbar input { padding: 11px 12px; border-radius: 10px; border: 1px solid rgba(128,128,128,.45);
    background: transparent; color: inherit; font: inherit; }
  .loginbar .lg-note { font-size: 13px; text-align: center; opacity: .75; text-decoration: underline; }
  /* ---------- Media ---------- */
  .playbar { display: flex; gap: 14px; padding: 14px; border: 1px solid rgba(128,128,128,.3); }
  .playbar .pb-cover { flex: none; width: 64px; height: 64px; border-radius: 12px; display: flex; align-items: center;
    justify-content: center; background: rgba(128,128,128,.16); color: var(--primary); }
  .playbar .pb-cover .mi { font-size: 30px; }
  .playbar .pb-body { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 8px; }
  .playbar .pb-head { display: flex; gap: 10px; align-items: flex-start; }
  .playbar .pb-title { flex: 1; min-width: 0; display: flex; flex-direction: column; }
  .playbar .pb-title small { font-size: 12px; opacity: .65; }
  .playbar .pb-times { display: inline-flex; gap: 8px; font-size: 12px; opacity: .65; white-space: nowrap; }
  .playbar .pb-track { height: 6px; border-radius: 999px; background: rgba(128,128,128,.25); overflow: hidden; }
  .playbar .pb-track span { display: block; height: 100%; background: var(--primary); }
  .playbar .pb-ctrl { display: flex; align-items: center; justify-content: center; gap: 18px; opacity: .8; }
  .playbar .pb-play { display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px;
    border: 0; border-radius: 50%; background: var(--primary); color: var(--on-primary); cursor: pointer; }
  .playbar .pb-play .mi { font-size: 26px; }
  .storiesbar { display: flex; gap: 14px; overflow-x: auto; padding: 6px 2px; }
  .storiesbar .st-item { flex: none; display: flex; flex-direction: column; align-items: center; gap: 5px; width: 68px; }
  .storiesbar .st-item small { font-size: 11px; opacity: .75; max-width: 68px; overflow: hidden;
    text-overflow: ellipsis; white-space: nowrap; }
  .storiesbar .st-ring { position: relative; display: flex; align-items: center; justify-content: center; width: 62px;
    height: 62px; border-radius: 50%; padding: 3px; box-sizing: border-box;
    background: linear-gradient(135deg, #f472b6, #8b5cf6, #f59e0b); }
  .storiesbar .st-ring.plain { background: rgba(128,128,128,.35); }
  .storiesbar .st-avatar { width: 100%; height: 100%; border-radius: 50%; overflow: hidden; background: var(--primary);
    color: var(--on-primary); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 15px;
    border: 2px solid var(--bg); box-sizing: border-box; }
  .storiesbar .st-avatar img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .storiesbar .st-badge { position: absolute; right: -1px; bottom: -1px; width: 22px; height: 22px; border-radius: 50%;
    background: var(--primary); color: var(--on-primary); display: flex; align-items: center; justify-content: center;
    border: 2px solid var(--bg); box-sizing: border-box; }
  .storiesbar .st-badge .mi { font-size: 15px; }
  .thumbstripbar { display: flex; align-items: center; gap: 10px; padding: 10px; border: 1px solid rgba(128,128,128,.3); }
  .thumbstripbar .ts-count { flex: none; font-size: 12px; opacity: .65; }
  .thumbstripbar .ts-strip { flex: 1; display: flex; gap: 8px; overflow-x: auto; }
  .thumbstripbar .ts-item { flex: none; width: 104px; border-radius: 10px; overflow: hidden; padding: 2px;
    border: 2px solid transparent; }
  .thumbstripbar .ts-item.on { border-color: var(--primary); }
  .thumbstripbar .ts-item img { display: block; width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 7px; }
  .captionsbar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: rgba(17,24,39,.88);
    color: #f9fafb; }
  .captionsbar .cc-badge { flex: none; padding: 3px 7px; border-radius: 6px; font-size: 11px; font-weight: 700;
    background: #f9fafb; color: #111827; }
  .captionsbar p { margin: 0; flex: 1; min-width: 0; font-size: 14px; }
  .captionsbar .cc-lang { flex: none; font-size: 11px; opacity: .75; }
  .recordbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border: 1px solid rgba(128,128,128,.3); }
  .recordbar .rc-dot { flex: none; width: 12px; height: 12px; border-radius: 50%; background: #ef4444;
    animation: lvpulse 1.4s ease-in-out infinite; }
  .recordbar .rc-label { font-size: 13px; font-weight: 600; white-space: nowrap; }
  .recordbar .rc-wave { flex: 1; display: flex; align-items: center; gap: 3px; height: 34px; min-width: 90px;
    overflow: hidden; }
  .recordbar .rc-wave span { flex: 1; min-width: 2px; border-radius: 2px; background: var(--primary); opacity: .75; }
  .recordbar .rc-time { font-size: 13px; font-variant-numeric: tabular-nums; opacity: .8; }
  /* ---------- Sosial ---------- */
  .reactionbar { display: flex; gap: 8px; flex-wrap: wrap; }
  .reactionbar .rx-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; border-radius: 999px;
    border: 1px solid rgba(128,128,128,.35); background: transparent; color: inherit; font: inherit; font-size: 13px;
    cursor: pointer; }
  .reactionbar .rx-btn:hover { border-color: var(--primary); color: var(--primary); }
  .userstackbar { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
  .userstackbar .us-set { display: inline-flex; align-items: center; }
  .userstackbar .us-avatar { width: 38px; height: 38px; border-radius: 50%; overflow: hidden; background: var(--primary);
    color: var(--on-primary); display: flex; align-items: center; justify-content: center; font-size: 13px;
    font-weight: 700; border: 2px solid var(--bg); box-sizing: border-box; }
  .userstackbar .us-avatar + .us-avatar { margin-left: -12px; }
  .userstackbar .us-avatar img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .userstackbar .us-count { background: rgba(128,128,128,.28); color: inherit; font-size: 12px; }
  .userstackbar .us-note small { font-size: 13px; opacity: .75; }
  .reviewbar { display: flex; gap: 12px; padding: 14px; border: 1px solid rgba(128,128,128,.3); }
  .reviewbar .rw-body { flex: 1; min-width: 0; }
  .reviewbar .rw-head { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; }
  .reviewbar .rw-time { font-size: 11px; opacity: .6; }
  .reviewbar .rw-stars { display: inline-flex; color: #f59e0b; margin: 2px 0 4px; }
  .reviewbar .rw-stars .mi { font-size: 18px; font-variation-settings: 'FILL' 1; }
  .reviewbar .rw-stars .off { opacity: .3; display: inline-flex; }
  .reviewbar p { margin: 0; font-size: 14px; }
  .chatbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border: 1px solid rgba(128,128,128,.3); }
  .chatbar .ch-body { flex: 1; min-width: 0; display: flex; flex-direction: column; }
  .chatbar .ch-body span { font-size: 13px; opacity: .75; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .chatbar .ch-side { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; }
  .chatbar .ch-time { font-size: 11px; opacity: .6; white-space: nowrap; }
  .chatbar .ch-badge { min-width: 22px; padding: 2px 7px; border-radius: 999px; background: var(--primary);
    color: var(--on-primary); font-size: 12px; font-weight: 700; text-align: center; }
  .followbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border: 1px solid rgba(128,128,128,.3); }
  .followbar .fw-body { flex: 1; min-width: 0; display: flex; flex-direction: column; }
  .followbar .fw-body small { font-size: 12px; opacity: .7; }
  .followbar .fw-note { color: var(--primary); opacity: .9; }
  /* ---------- Toko ---------- */
  .cartbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border: 1px solid rgba(128,128,128,.3);
    box-shadow: 0 -4px 16px rgba(0,0,0,.06); }
  .cartbar .ct-ico { position: relative; display: inline-flex; color: var(--primary); }
  .cartbar .ct-ico .mi { font-size: 26px; }
  .cartbar .ct-badge { position: absolute; top: -7px; right: -9px; min-width: 18px; padding: 0 5px; border-radius: 999px;
    background: #ef4444; color: #fff; font-size: 11px; font-weight: 700; line-height: 18px; text-align: center; }
  .cartbar .ct-text { flex: 1; min-width: 0; display: flex; flex-direction: column; }
  .cartbar .ct-text small { font-size: 12px; opacity: .7; }
  .couponbar { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; padding: 14px 16px;
    border: 2px dashed rgba(128,128,128,.5); background: rgba(128,128,128,.06); }
  .couponbar .cu-ico { color: var(--primary); }
  .couponbar .cu-text { flex: 1; min-width: 170px; display: flex; flex-direction: column; gap: 2px; }
  .couponbar .cu-code { display: inline-flex; align-items: center; gap: 6px; font-family: ui-monospace, Menlo, monospace;
    font-size: 16px; font-weight: 700; letter-spacing: .06em; color: var(--primary); }
  .couponbar .cu-text small { font-size: 12px; opacity: .75; }
  .couponbar .cu-exp { font-size: 11px; opacity: .6; }
  .shippingbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border: 1px solid rgba(128,128,128,.3); }
  .shippingbar > .mi { color: var(--primary); }
  .shippingbar .hp-body { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 6px; font-size: 13px; }
  .shippingbar .hp-label { font-size: 13px; font-weight: 600; }
  .shippingbar .hp-track { height: 8px; border-radius: 999px; background: rgba(128,128,128,.22); overflow: hidden; }
  .shippingbar .hp-track span { display: block; height: 100%; border-radius: 999px; background: var(--primary); }
  .shippingbar .hp-labels { display: flex; justify-content: space-between; font-size: 11px; opacity: .6; }
  .productbar { display: flex; align-items: center; gap: 14px; padding: 12px 14px; border: 1px solid rgba(128,128,128,.3); }
  .productbar .pd-thumb { flex: none; width: 72px; height: 72px; border-radius: 12px; overflow: hidden;
    background: rgba(128,128,128,.16); }
  .productbar .pd-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .productbar .pd-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .productbar .pd-text small { font-size: 12px; opacity: .65; }
  .productbar .pd-price { display: flex; align-items: baseline; gap: 8px; font-weight: 700; }
  .productbar .pd-price s { font-size: 12px; font-weight: 400; opacity: .55; }
  .paymentbar { padding: 8px 14px 12px; border: 1px solid rgba(128,128,128,.3); }
  .paymentbar .py-row { display: flex; align-items: center; gap: 12px; padding: 12px 0; cursor: pointer; }
  .paymentbar .py-row + .py-row { border-top: 1px solid rgba(128,128,128,.2); }
  .paymentbar .py-ico { color: var(--primary); display: inline-flex; }
  .paymentbar .py-text { flex: 1; min-width: 0; display: flex; flex-direction: column; }
  .paymentbar .py-text strong { font-size: 14px; }
  .paymentbar .py-text small { font-size: 12px; opacity: .65; }
  .paymentbar .py-check { color: var(--primary); display: inline-flex; opacity: 0; }
  .paymentbar .py-row.on .py-check { opacity: 1; }
  .paymentbar .py-note { display: block; padding-top: 6px; font-size: 12px; opacity: .6; }
"""
