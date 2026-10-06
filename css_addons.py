"""Gaya komponen baru; semua selector dibatasi pada .addonbar."""

BAR_CSS_ADDONS = r"""
  .addonbar { display: flex; align-items: center; gap: 12px; min-width: 0; padding: 14px 16px;
    border: 1px solid rgba(128,128,128,.28); background: var(--bg); color: var(--text); }
  .addonbar .aa-copy { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3px; }
  .addonbar .aa-copy strong { line-height: 1.35; }
  .addonbar .aa-copy small, .addonbar .aa-form-note { font-size: 12px; line-height: 1.45; opacity: .68; }
  .addonbar .aa-copy em { font-size: 12px; font-style: normal; color: var(--primary); }
  .addonbar .aa-title { display: flex; align-items: center; gap: 7px; margin-bottom: 9px; font-size: 15px; }
  .addonbar .aa-icon, .addonbar .aa-state-icon, .addonbar .aa-reminder-icon, .addonbar .aa-release-mark,
  .addonbar .aa-metric-icon, .addonbar .aa-metric-icon, .addonbar .aa-bill-icon, .addonbar .aa-reading-icon,
  .addonbar .aa-command-icon, .addonbar .aa-discount-icon, .addonbar .aa-return-mark {
    display: inline-flex; align-items: center; justify-content: center; flex: none; color: var(--primary); }
  .addonbar .aa-button { display: inline-flex; align-items: center; justify-content: center; flex: none; padding: 8px 13px;
    border: 1px solid var(--primary); border-radius: 9px; background: var(--primary); color: var(--on-primary);
    font: inherit; font-size: 13px; font-weight: 600; white-space: nowrap; cursor: pointer; }
  .addonbar .aa-button.secondary { background: transparent; color: var(--primary); }
  .addonbar .aa-actions { display: inline-flex; align-items: center; gap: 7px; margin-left: auto; }
  .addonbar .aa-badge { display: inline-flex; align-items: center; padding: 4px 8px; border-radius: 999px;
    background: rgba(99,102,241,.12); color: var(--primary); font-size: 11px; font-weight: 700; white-space: nowrap; }
  .addonbar .aa-logo { display: inline-flex; align-items: center; justify-content: center; flex: none; width: 40px; height: 40px;
    border-radius: 12px; background: var(--primary); color: var(--on-primary); }
  .addonbar .aa-logo .mi { font-size: 22px; }
  /* Navigasi */
  .aa-workspace { gap: 11px; }
  .aa-workspace > .aa-badge { margin-left: auto; }
  .aa-steps { display: flex; gap: 4px; width: 100%; padding-top: 8px; }
  .aa-steps > .aa-step { position: relative; display: flex; flex: 1; flex-direction: column; align-items: center; gap: 6px;
    color: inherit; text-align: center; font-size: 12px; }
  .aa-steps > .aa-step::before { content: ""; position: absolute; top: 15px; left: -50%; width: 100%; height: 2px;
    background: rgba(128,128,128,.25); }
  .aa-steps > .aa-step:first-child::before { display: none; }
  .aa-step-dot { position: relative; z-index: 1; display: inline-flex; align-items: center; justify-content: center; width: 30px; height: 30px;
    border: 1px solid rgba(128,128,128,.4); border-radius: 50%; background: var(--bg); font-size: 12px; }
  .aa-step.done .aa-step-dot, .aa-step.active .aa-step-dot { border-color: var(--primary); color: var(--primary); }
  .aa-step.done .aa-step-dot { background: var(--primary); color: var(--on-primary); }
  .aa-step.active { color: var(--primary); font-weight: 700; }
  .aa-step.done::before, .aa-step.active::before { background: var(--primary); }
  .aa-tabs { display: flex; align-items: center; gap: 4px; overflow-x: auto; width: 100%; }
  .aa-tab { display: inline-flex; align-items: center; gap: 7px; flex: 1; justify-content: center; padding: 9px 11px;
    border-radius: 10px; color: inherit; opacity: .72; text-decoration: none; font-size: 13px; white-space: nowrap; }
  .aa-tab.active { color: var(--primary); background: rgba(99,102,241,.10); opacity: 1; font-weight: 700; }
  .aa-link-list, .aa-profile-nav { display: flex; flex-direction: column; gap: 3px; width: 100%; }
  .aa-links, .aa-profile_nav { display: block; }
  .aa-link-row { display: flex; align-items: center; gap: 10px; padding: 9px 8px; color: inherit; text-decoration: none;
    border-radius: 10px; border-bottom: 1px solid rgba(128,128,128,.12); }
  .aa-link-row:last-child { border-bottom: 0; }
  .aa-link-row > .mi { margin-left: auto; opacity: .45; }
  .aa-link-row:hover, .aa-nav-row:hover { background: rgba(128,128,128,.08); }
  .aa-link-row .aa-icon { width: 34px; height: 34px; border-radius: 10px; background: rgba(99,102,241,.10); }
  .aa-link-row .aa-icon .mi { color: var(--primary); }
  .aa-profile-head { display: flex; align-items: center; gap: 10px; width: 100%; padding-bottom: 12px; margin-bottom: 8px;
    border-bottom: 1px solid rgba(128,128,128,.2); }
  .aa-avatar { display: inline-flex; align-items: center; justify-content: center; flex: none; width: 42px; height: 42px;
    overflow: hidden; border-radius: 50%; background: rgba(99,102,241,.15); color: var(--primary); font-size: 14px; font-weight: 700; }
  .aa-avatar img { display: block; width: 100%; height: 100%; object-fit: cover; }
  .aa-profile-head > .mi { opacity: .55; }
  .aa-nav-row { display: flex; align-items: center; gap: 10px; padding: 9px 10px; border-radius: 9px; color: inherit;
    text-decoration: none; font-size: 13px; }
  .aa-nav-row.active { background: rgba(99,102,241,.12); color: var(--primary); font-weight: 700; }
  /* Aksi */
  .aa-command { gap: 10px; border-radius: 13px; }
  .aa-command-icon { flex: none; }
  .aa-command input { flex: 1; min-width: 80px; border: 0; outline: 0; padding: 7px 0; background: transparent; color: inherit; font: inherit; }
  .aa-command kbd { flex: none; padding: 5px 8px; border: 1px solid rgba(128,128,128,.3); border-radius: 7px;
    background: rgba(128,128,128,.07); font-size: 11px; white-space: nowrap; }
  .aa-undo .aa-state-icon { width: 38px; height: 38px; border-radius: 12px; background: rgba(99,102,241,.10); }
  .aa-share_link { flex-wrap: wrap; }
  .aa-share-url { display: inline-flex; align-items: center; gap: 7px; min-width: 100px; max-width: 42%; padding: 8px 10px;
    overflow: hidden; border: 1px solid rgba(128,128,128,.26); border-radius: 9px; font-size: 12px; }
  .aa-share-url span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .aa-selection { flex-wrap: wrap; }
  .aa-selection-count { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; color: var(--primary); white-space: nowrap; }
  .aa-selection .aa-actions { flex-wrap: wrap; }
  .aa-icon-action { display: inline-flex; align-items: center; gap: 5px; padding: 7px 9px; border: 1px solid rgba(128,128,128,.25);
    border-radius: 8px; background: transparent; color: inherit; font: inherit; font-size: 12px; cursor: pointer; }
  .aa-icon-action:hover { color: var(--primary); border-color: var(--primary); }
  .aa-create_action { flex-wrap: wrap; }
  /* Informasi */
  .aa-alert_list { display: block; }
  .aa-alert-list { display: flex; flex-direction: column; gap: 7px; }
  .aa-alert { display: flex; align-items: flex-start; gap: 9px; padding: 9px 10px; border-radius: 9px; font-size: 13px; }
  .aa-alert.info { color: #1e40af; background: #eff6ff; }
  .aa-alert.success, .aa-alert.online { color: #166534; background: #f0fdf4; }
  .aa-alert.warning, .aa-alert.sync { color: #854d0e; background: #fffbeb; }
  .aa-alert.error, .aa-alert.danger, .aa-alert.offline { color: #991b1b; background: #fef2f2; }
  .aa-alert .aa-copy { gap: 1px; }
  .aa-event { align-items: center; }
  .aa-event-date { display: flex; flex: none; flex-direction: column; gap: 5px; max-width: 155px; color: var(--primary); font-weight: 700; }
  .aa-event-date small { color: inherit; font-size: 11px; line-height: 1.4; }
  .aa-event .aa-copy > small { display: inline-flex; align-items: center; gap: 3px; }
  .aa-event .aa-copy > em { color: #b45309; }
  .aa-status-dot { display: inline-flex; align-items: center; justify-content: center; flex: none; width: 40px; height: 40px;
    border-radius: 50%; background: #eff6ff; color: #2563eb; }
  .aa-status-dot.online, .aa-status-dot.success { background: #f0fdf4; color: #15803d; }
  .aa-status-dot.offline, .aa-status-dot.error { background: #fef2f2; color: #dc2626; }
  .aa-status-dot.sync, .aa-status-dot.warning { background: #fffbeb; color: #b45309; }
  .aa-reminder-icon, .aa-release-mark { align-self: flex-start; width: 38px; height: 38px; border-radius: 11px; background: rgba(99,102,241,.10); }
  .aa-reminder .aa-copy > small { display: inline-flex; align-items: center; gap: 5px; }
  .aa-release { align-items: flex-start; }
  .aa-release-mark { background: var(--primary); color: var(--on-primary); }
  .aa-release .aa-copy .aa-badge { align-self: flex-start; margin-bottom: 3px; }
  /* Data */
  .aa-metric { align-items: flex-start; }
  .aa-metric-icon { width: 42px; height: 42px; border-radius: 12px; background: rgba(99,102,241,.10); font-size: 22px; }
  .aa-metric-value { font-size: 27px; line-height: 1.12; letter-spacing: -.03em; }
  .aa-metric-foot { display: flex; gap: 5px; flex-wrap: wrap; align-items: baseline; }
  .aa-metric-foot b { color: #15803d; font-size: 12px; }
  .aa-metric-foot small { font-size: 11px; }
  .aa-progress_list, .aa-activity, .aa-comparison, .aa-expense, .aa-cashflow, .aa-toc { display: block; }
  .aa-progress-list, .aa-activity-list, .aa-comparison-list, .aa-expense-list, .aa-cash-list, .aa-toc-list { display: flex; flex-direction: column; gap: 8px; }
  .aa-progress-row > span:first-child, .aa-expense-head { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; }
  .aa-progress-row strong, .aa-expense-head strong { font-size: 13px; }
  .aa-progress-row small, .aa-expense-head b { font-size: 12px; opacity: .7; }
  .aa-track, .aa-audio-track, .aa-goal-track { display: block; width: 100%; height: 7px; overflow: hidden; border-radius: 999px; background: rgba(128,128,128,.2); }
  .aa-track i, .aa-audio-track i, .aa-goal-track i { display: block; height: 100%; border-radius: inherit; background: var(--primary); }
  .aa-progress-row .aa-track, .aa-file-row .aa-track, .aa-poll-row .aa-track, .aa-expense-row .aa-track { margin-top: 5px; }
  .aa-activity-row { display: grid; grid-template-columns: 66px 10px 1fr; gap: 9px; align-items: start; }
  .aa-activity-row time { padding-top: 2px; font-size: 11px; opacity: .58; }
  .aa-activity-dot { width: 9px; height: 9px; margin-top: 6px; border: 2px solid var(--primary); border-radius: 50%; }
  .aa-activity-row .aa-copy { padding-bottom: 8px; border-bottom: 1px solid rgba(128,128,128,.14); }
  .aa-activity-row:last-child .aa-copy { border-bottom: 0; }
  .aa-comparison-head, .aa-comparison-row { display: grid; grid-template-columns: minmax(80px,1fr) minmax(70px,.8fr) minmax(60px,.55fr); gap: 8px; align-items: center; }
  .aa-comparison-head { padding: 6px 0; border-bottom: 1px solid rgba(128,128,128,.18); font-size: 10px; text-transform: uppercase; opacity: .6; }
  .aa-comparison-row { padding: 8px 0; border-bottom: 1px solid rgba(128,128,128,.12); font-size: 13px; }
  .aa-comparison-row:last-child { border: 0; }
  .aa-comparison-row em { color: #15803d; font-size: 11px; font-style: normal; }
  .aa-goal { display: block; }
  .aa-goal-head, .aa-goal-meta, .aa-wallet-top, .aa-wallet-stats { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
  .aa-goal-value { color: var(--primary); font-size: 20px; font-weight: 700; }
  .aa-goal-track { height: 9px; margin: 11px 0 8px; }
  .aa-goal-meta b { font-size: 14px; }
  .aa-goal-meta small { margin-right: auto; font-size: 11px; opacity: .6; }
  .aa-goal-meta .aa-button { font-size: 11px; padding: 6px 9px; }
  .aa-wallet { display: block; }
  .aa-wallet-value { display: block; margin-top: 2px; font-size: 25px; letter-spacing: -.03em; }
  .aa-wallet-stats { justify-content: flex-start; margin-top: 14px; padding-top: 10px; border-top: 1px solid rgba(128,128,128,.2); }
  .aa-wallet-stats > span { flex: 1; display: flex; flex-direction: column; gap: 3px; }
  .aa-wallet-stats small { font-size: 11px; opacity: .62; }
  .aa-wallet-stats strong { font-size: 12px; }
  .aa-expense-total { color: var(--primary); font-size: 14px; }
  .aa-cash-head, .aa-cash-row { display: grid; grid-template-columns: .6fr 1fr 1fr; gap: 8px; align-items: center; }
  .aa-cash-head { padding: 7px 0; border-bottom: 1px solid rgba(128,128,128,.2); font-size: 10px; opacity: .6; }
  .aa-cash-row { padding: 8px 0; border-bottom: 1px solid rgba(128,128,128,.12); font-size: 12px; }
  .aa-cash-row > span { display: flex; flex-direction: column; gap: 2px; }
  .aa-cash-row small { font-size: 10px; opacity: .55; }
  .aa-cash-list { margin-bottom: 8px; }
  /* Formulir */
  .aa-address, .aa-checklist, .aa-upload, .aa-consent, .aa-poll { display: block; }
  .aa-address .aa-form-head, .aa-upload-head { display: flex; align-items: center; gap: 10px; }
  .aa-address address { display: block; margin: 10px 0 0 44px; font-size: 14px; font-style: normal; }
  .aa-checklist { margin: 0; padding: 0; list-style: none; }
  .aa-checklist li { display: flex; align-items: center; gap: 9px; padding: 8px 0; border-bottom: 1px solid rgba(128,128,128,.12); font-size: 13px; }
  .aa-checklist li:last-child { border: 0; }
  .aa-checklist li.done .mi { color: #16a34a; }
  .aa-checklist li.todo .mi { opacity: .45; }
  .aa-upload-head { justify-content: space-between; margin-bottom: 7px; }
  .aa-upload-head strong { font-size: 14px; }
  .aa-file-list { display: flex; flex-direction: column; gap: 4px; }
  .aa-file-row { display: flex; align-items: center; gap: 9px; padding: 8px 0; border-top: 1px solid rgba(128,128,128,.14); }
  .aa-file-icon { display: inline-flex; align-items: center; justify-content: center; width: 34px; height: 36px; border-radius: 8px;
    background: rgba(99,102,241,.1); color: var(--primary); }
  .aa-file-row > .mi:last-child { opacity: .5; }
  .aa-file-row .aa-copy { gap: 1px; }
  .aa-file-row .aa-copy strong { font-size: 12px; }
  .aa-file-row .aa-track { height: 4px; }
  .aa-contact_form .aa-field { display: block; margin-top: 10px; font-size: 12px; }
  .aa-field > span:first-child { display: block; margin-bottom: 4px; }
  .aa-field-row { display: flex; gap: 7px; }
  .aa-field-row input { flex: 1; min-width: 90px; padding: 9px 10px; border: 1px solid rgba(128,128,128,.35); border-radius: 8px;
    background: transparent; color: inherit; font: inherit; }
  .aa-form-note { display: block; margin-top: 8px; }
  .aa-consent-list { margin: 0 0 9px; border-top: 1px solid rgba(128,128,128,.15); }
  .aa-consent-row { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 9px 2px;
    border-bottom: 1px solid rgba(128,128,128,.15); }
  .aa-consent-row > span:first-child { display: flex; flex-direction: column; }
  .aa-consent-row strong { font-size: 13px; }
  .aa-consent-row small { font-size: 10px; opacity: .6; }
  .aa-switch { width: 34px; height: 20px; padding: 2px; border-radius: 999px; background: rgba(128,128,128,.3); }
  .aa-switch::after { content: ""; display: block; width: 16px; height: 16px; border-radius: 50%; background: #fff; transition: transform .15s; }
  .aa-switch.on { background: var(--primary); }
  .aa-switch.on::after { transform: translateX(14px); }
  .aa-consent > .aa-button { margin-top: 10px; }
  /* Media, sosial, dan toko */
  .aa-cover, .aa-photo, .aa-thumb, .aa-story-cover { display: block; flex: none; overflow: hidden; background: rgba(128,128,128,.12); }
  .aa-cover img, .aa-photo img, .aa-thumb img, .aa-story-cover img { display: block; width: 100%; height: 100%; object-fit: cover; }
  .aa-cover { width: 86px; height: 70px; border-radius: 10px; }
  .aa-photo { width: 120px; height: 82px; border-radius: 10px; }
  .aa-thumb { width: 68px; height: 68px; border-radius: 10px; }
  .aa-story-cover { width: 110px; height: 94px; border-radius: 10px; }
  .aa-audio { gap: 11px; }
  .aa-play { display: inline-flex; align-items: center; justify-content: center; flex: none; width: 40px; height: 40px;
    border-radius: 50%; background: var(--primary); color: var(--on-primary); }
  .aa-audio-track { height: 5px; margin-top: 5px; }
  .aa-audio-meta { display: flex; justify-content: space-between; }
  .aa-audio-meta small { font-size: 10px; }
  .aa-playlist, .aa-reactions, .aa-variant, .aa-toc { display: block; }
  .aa-song-list { display: flex; flex-direction: column; }
  .aa-song { display: flex; align-items: center; gap: 10px; padding: 8px 3px; border-bottom: 1px solid rgba(128,128,128,.14); }
  .aa-song:last-child { border-bottom: 0; }
  .aa-song-no { display: inline-flex; justify-content: center; width: 24px; color: var(--primary); }
  .aa-song .aa-copy strong { font-size: 13px; }
  .aa-song time { font-size: 11px; opacity: .6; }
  .aa-song.active { color: var(--primary); }
  .aa-photo_credit { align-items: center; }
  .aa-recording { flex-wrap: wrap; }
  .aa-record-dot { width: 10px; height: 10px; border-radius: 50%; background: #ef4444; box-shadow: 0 0 0 5px rgba(239,68,68,.13); }
  .aa-recording time { font-size: 12px; font-variant-numeric: tabular-nums; }
  .aa-wave { display: inline-flex; align-items: center; gap: 3px; height: 34px; padding: 0 6px; }
  .aa-wave i { display: block; width: 3px; border-radius: 5px; background: var(--primary); opacity: .75; }
  .aa-poll .aa-title { margin-bottom: 12px; }
  .aa-poll-list { display: flex; flex-direction: column; gap: 10px; }
  .aa-poll-row { display: flex; flex-direction: column; gap: 1px; }
  .aa-poll-label { display: flex; justify-content: space-between; gap: 10px; font-size: 12px; }
  .aa-poll-label b { color: var(--primary); }
  .aa-social_proof, .aa-attributed_quote { display: block; padding: 16px 18px; border-left: 4px solid var(--primary); }
  .aa-quote-mark { display: inline-flex; color: var(--primary); opacity: .65; }
  .aa-social_proof blockquote, .aa-attributed_quote blockquote { margin: 3px 0 12px; font-size: 16px; font-weight: 500; line-height: 1.5; }
  .aa-profile-inline { display: flex; align-items: center; gap: 9px; }
  .aa-profile-inline .aa-avatar { width: 36px; height: 36px; }
  .aa-profile-inline .aa-copy strong, .aa-attributed_quote footer strong { font-size: 13px; }
  .aa-profile-inline .aa-copy small, .aa-attributed_quote footer small { font-size: 11px; }
  .aa-reaction-list { display: flex; gap: 8px; flex-wrap: wrap; }
  .aa-reaction { display: inline-flex; align-items: center; gap: 6px; padding: 8px 10px; border: 1px solid rgba(128,128,128,.25);
    border-radius: 999px; background: transparent; color: inherit; font: inherit; font-size: 12px; }
  .aa-reaction .mi { color: var(--primary); }
  .aa-reaction b { opacity: .65; }
  .aa-cart_item { align-items: center; }
  .aa-price { flex: none; color: var(--primary); font-size: 14px; white-space: nowrap; }
  .aa-delivery { display: block; }
  .aa-delivery-head { display: flex; align-items: center; gap: 10px; color: var(--primary); }
  .aa-delivery-head > .mi { font-size: 24px; }
  .aa-delivery-line { display: flex; gap: 4px; margin: 14px 4px 4px; }
  .aa-delivery-step { position: relative; display: flex; flex: 1; flex-direction: column; align-items: center; gap: 5px; font-size: 10px; opacity: .55; }
  .aa-delivery-step::before { content: ""; position: absolute; top: 10px; right: 50%; width: 100%; height: 2px; background: rgba(128,128,128,.3); }
  .aa-delivery-step:first-child::before { display: none; }
  .aa-delivery-step i { position: relative; z-index: 1; display: inline-flex; align-items: center; justify-content: center; width: 22px;
    height: 22px; border-radius: 50%; border: 1px solid rgba(128,128,128,.4); background: var(--bg); font-style: normal; }
  .aa-delivery-step.done, .aa-delivery-step.active { color: var(--primary); opacity: 1; }
  .aa-delivery-step.done i { background: var(--primary); color: var(--on-primary); border-color: var(--primary); }
  .aa-delivery-step.done::before, .aa-delivery-step.active::before { background: var(--primary); }
  .aa-variant-list { display: flex; flex-wrap: wrap; gap: 7px; margin: 4px 0 8px; }
  .aa-variant { padding: 7px 12px; border: 1px solid rgba(128,128,128,.3); border-radius: 999px; background: transparent; color: inherit;
    font: inherit; font-size: 12px; }
  .aa-variant.active { color: var(--primary); border-color: var(--primary); background: rgba(99,102,241,.08); font-weight: 700; }
  .aa-discount { align-items: center; }
  .aa-discount-icon { width: 40px; height: 40px; border-radius: 12px; background: rgba(99,102,241,.1); font-size: 21px; }
  .aa-code { align-self: flex-start; padding: 3px 7px; border: 1px dashed var(--primary); border-radius: 6px; color: var(--primary);
    font: 700 11px ui-monospace, monospace; letter-spacing: .06em; }
  .aa-return { align-items: center; }
  .aa-return-mark { width: 38px; height: 38px; }
  .aa-return-top { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
  .aa-return-top .aa-badge { font-size: 10px; }
  .aa-bill { align-items: center; }
  .aa-bill-icon { width: 38px; height: 38px; border-radius: 11px; background: rgba(99,102,241,.10); }
  .aa-bill-status { align-self: flex-start; padding: 2px 7px; border-radius: 999px; background: #f0fdf4; color: #166534; font-size: 10px; }
  .aa-bill-side { display: flex; flex-direction: column; align-items: flex-end; gap: 7px; white-space: nowrap; }
  .aa-bill-side strong { font-size: 14px; }
  .aa-toc-list { gap: 2px; }
  .aa-toc-row { display: flex; align-items: center; gap: 10px; padding: 8px 9px; border-radius: 8px; color: inherit;
    font-size: 13px; text-decoration: none; }
  .aa-toc-row > span { color: var(--primary); font: 11px ui-monospace, monospace; }
  .aa-toc-row.active { background: rgba(99,102,241,.10); color: var(--primary); font-weight: 700; }
  .aa-story { align-items: stretch; }
  .aa-story .aa-copy { align-self: center; }
  .aa-story .aa-badge { align-self: flex-start; margin-bottom: 2px; }
  .aa-story .aa-copy > em { display: inline-flex; align-items: center; gap: 4px; }
  .aa-byline { align-items: center; }
  .aa-reading { gap: 12px; }
  .aa-reading-icon { width: 42px; height: 42px; border-radius: 12px; background: rgba(99,102,241,.1); font-size: 22px; }
  .aa-reading-side { display: flex; flex-direction: column; align-items: flex-end; gap: 5px; }
  .aa-reading-side b { color: var(--primary); font-size: 12px; }
  .aa-reading-side .aa-button { font-size: 11px; padding: 6px 9px; }
  .aa-attributed_quote footer { display: flex; align-items: baseline; flex-wrap: wrap; gap: 7px; }
  .aa-attributed_quote footer small { opacity: .65; }
  @media (max-width: 640px) {
    .addonbar { flex-wrap: wrap; padding: 12px; }
    .aa-button { font-size: 12px; padding: 7px 10px; }
    .aa-share-url { max-width: 100%; flex: 1 1 100%; order: 3; }
    .aa-event-date { max-width: 100%; }
    .aa-comparison-head, .aa-comparison-row { grid-template-columns: minmax(60px,1fr) minmax(50px,.8fr) minmax(44px,.55fr); }
    .aa-cover { width: 74px; height: 64px; }
    .aa-photo { width: 90px; }
    .aa-story-cover { width: 86px; height: 90px; }
  }
"""
