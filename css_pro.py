"""CSS untuk 50 komponen bar paket "Pro" (dipakai css.py).

Semua kelas anak memakai awalan pendek yang khas per komponen supaya tidak
bertabrakan dengan BAR_CSS / BAR_CSS_EXTRA. Beberapa kelas bantu generik
(`.pill`, `.chip-*`, `.tone-*`) hanya dipakai komponen di berkas ini.
"""

BAR_CSS_PRO = """
  /* Kelas bantu status (dipakai komponen paket Pro) */
  .pill { display: inline-flex; align-items: center; gap: 4px; padding: 3px 9px; border-radius: 999px;
    font-size: 11px; font-weight: 600; white-space: nowrap; }
  .chip-safe { background: rgba(34,197,94,.16); color: #15803d; }
  .chip-warning { background: rgba(245,158,11,.18); color: #b45309; }
  .chip-danger { background: rgba(239,68,68,.16); color: #b91c1c; }
  .chip-info { background: rgba(59,130,246,.16); color: #1d4ed8; }
  .chip-muted { background: rgba(128,128,128,.18); color: inherit; }
  .tone-safe { color: #16a34a; }
  .tone-warning { color: #d97706; }
  .tone-danger { color: #dc2626; }
  .tone-info { color: #2563eb; }
  .tone-muted { color: #6b7280; }

  /* ---- Navigasi ---- */
  .appbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .appbar .apb-back { display: inline-flex; align-items: center; gap: 4px; font-size: 13px; opacity: .8; }
  .appbar .apb-text { flex: 1; min-width: 0; display: flex; flex-direction: column; }
  .appbar .apb-text strong { font-size: 15px; }
  .appbar .apb-text small { font-size: 12px; opacity: .65; }
  .appbar .apb-action { display: inline-flex; align-items: center; gap: 6px; padding: 7px 11px; font-size: 13px;
    border-radius: 10px; background: var(--primary); color: var(--on-primary); font-weight: 600; }
  .quicknav { display: flex; gap: 6px; overflow-x: auto; padding: 6px; border: 1px solid rgba(128,128,128,.3); }
  .quicknav .qn-item { flex: 1; min-width: 74px; display: flex; flex-direction: column; align-items: center;
    gap: 4px; padding: 9px 6px; border-radius: 12px; font-size: 12px; text-align: center; }
  .quicknav .qn-item:hover { background: rgba(128,128,128,.12); }
  .quicknav .qn-item.on { background: var(--primary); color: var(--on-primary); font-weight: 600; }
  .quicknav .qn-ico { font-size: 22px; }
  .subnav { display: flex; gap: 2px; overflow-x: auto; border-bottom: 1px solid rgba(128,128,128,.3); border-radius: 0; }
  .subnav .sn-item { padding: 10px 14px; font-size: 14px; opacity: .7; white-space: nowrap;
    border-bottom: 2px solid transparent; margin-bottom: -1px; }
  .subnav .sn-item.on { opacity: 1; font-weight: 600; color: var(--primary); border-color: var(--primary); }
  .stepdots { display: flex; align-items: center; gap: 12px; padding: 12px 14px; }
  .stepdots .sd-dots { display: inline-flex; align-items: center; gap: 6px; }
  .stepdots .sd-dot { width: 8px; height: 8px; border-radius: 999px; background: rgba(128,128,128,.4); }
  .stepdots .sd-dot.done { background: var(--primary); opacity: .45; }
  .stepdots .sd-dot.on { width: 24px; background: var(--primary); }
  .stepdots .sd-label { font-size: 12px; opacity: .7; }
  .swipenav { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 10px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .swipenav .sw-nav { display: inline-flex; align-items: center; gap: 2px; font-size: 13px; padding: 6px 10px;
    border-radius: 10px; }
  .swipenav .sw-nav:hover { background: rgba(128,128,128,.12); }
  .swipenav .sw-label { font-size: 13px; font-weight: 600; }

  /* ---- Aksi ---- */
  .bulkactionbar { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; padding: 10px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .bulkactionbar .bk-count { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 600; }
  .bulkactionbar .bk-count .mi { color: var(--primary); }
  .bulkactionbar .bk-all { font-size: 12px; opacity: .7; text-decoration: underline; }
  .bulkactionbar .bk-actions { margin-left: auto; display: flex; gap: 6px; flex-wrap: wrap; }
  .bulkactionbar .bk-btn { display: inline-flex; align-items: center; gap: 5px; padding: 7px 10px; font-size: 12px;
    border: 1px solid rgba(128,128,128,.3); border-radius: 9px; background: transparent; color: inherit;
    font-family: inherit; cursor: pointer; }
  .bulkactionbar .bk-btn .mi { font-size: 16px; }
  .bulkactionbar .bk-btn.danger { color: #dc2626; border-color: rgba(220,38,38,.4); }
  .exportbar { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; padding: 10px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .exportbar > .mi { color: var(--primary); }
  .exportbar .ex-label { font-size: 14px; font-weight: 600; }
  .exportbar .ex-formats { display: flex; gap: 4px; }
  .exportbar .ex-fmt { padding: 5px 11px; font-size: 12px; border-radius: 999px;
    border: 1px solid rgba(128,128,128,.35); }
  .exportbar .ex-fmt.on { background: var(--primary); border-color: var(--primary); color: var(--on-primary);
    font-weight: 600; }
  .approvalbar { display: flex; flex-direction: column; gap: 10px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .approvalbar .apv-head { display: flex; align-items: center; gap: 10px; }
  .approvalbar .apv-ico { color: var(--primary); font-size: 22px; }
  .approvalbar .apv-text { flex: 1; display: flex; flex-direction: column; }
  .approvalbar .apv-text strong { font-size: 14px; }
  .approvalbar .apv-text small { font-size: 12px; opacity: .65; }
  .approvalbar .apv-actions { display: flex; gap: 8px; justify-content: flex-end; }
  .printbar { display: flex; align-items: center; gap: 10px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .printbar .pr-ico { color: var(--primary); font-size: 22px; }
  .printbar .pr-text { flex: 1; display: flex; flex-direction: column; }
  .printbar .pr-text strong { font-size: 14px; }
  .printbar .pr-text small { font-size: 12px; opacity: .65; }

  /* ---- Informasi ---- */
  .weatherbar { display: flex; align-items: center; gap: 14px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3);
    background: linear-gradient(120deg, rgba(56,189,248,.18), rgba(250,204,21,.14)); }
  .weatherbar .wt-ico { font-size: 32px; color: var(--primary); }
  .weatherbar .wt-main { flex: 1; display: flex; flex-direction: column; }
  .weatherbar .wt-main strong { font-size: 20px; }
  .weatherbar .wt-main small { font-size: 12px; opacity: .75; }
  .weatherbar .wt-range { display: inline-flex; align-items: center; gap: 4px; font-size: 12px; opacity: .8; }
  .notificationbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .notificationbar .nt-ico { position: relative; display: inline-flex; color: var(--primary); font-size: 22px; }
  .notificationbar .nt-badge { position: absolute; top: -6px; right: -8px; min-width: 16px; height: 16px;
    padding: 0 4px; border-radius: 999px; background: #ef4444; color: #fff; font-size: 10px; font-weight: 700;
    display: inline-flex; align-items: center; justify-content: center; }
  .notificationbar .nt-text { flex: 1; min-width: 0; display: flex; flex-direction: column; }
  .notificationbar .nt-text small { font-size: 11px; text-transform: uppercase; letter-spacing: .04em; opacity: .6; }
  .notificationbar .nt-text strong { font-size: 14px; }
  .notificationbar .nt-text small + strong + small { font-size: 12px; opacity: .6; }
  .notificationbar .nt-go { opacity: .45; }
  .metricbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .metricbar .mt-ico { width: 38px; height: 38px; border-radius: 11px; display: inline-flex; align-items: center;
    justify-content: center; background: rgba(99,102,241,.14); color: var(--primary); }
  .metricbar .mt-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .metricbar .mt-text small { font-size: 12px; opacity: .65; }
  .metricbar .mt-line { display: flex; align-items: baseline; gap: 8px; }
  .metricbar .mt-line strong { font-size: 17px; }
  .metricbar .mt-delta { display: inline-flex; align-items: center; gap: 2px; font-size: 12px; font-style: normal;
    font-weight: 600; }
  .metricbar .mt-delta .mi { font-size: 16px; }
  .updatebar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .updatebar .up-ico { color: var(--primary); font-size: 24px; }
  .updatebar .up-text { flex: 1; display: flex; flex-direction: column; }
  .updatebar .up-text strong { font-size: 14px; }
  .updatebar .up-text small { font-size: 12px; opacity: .65; }

  /* ---- Data ---- */
  .donutbar { display: flex; align-items: center; gap: 14px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .donutbar .dn-chart { flex: none; width: 76px; height: 76px; border-radius: 50%; display: inline-flex;
    align-items: center; justify-content: center; }
  .donutbar .dn-hole { width: 46px; height: 46px; border-radius: 50%; background: var(--bg); display: inline-flex;
    align-items: center; justify-content: center; color: var(--primary); font-size: 18px; }
  .donutbar .dn-list { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3px; }
  .donutbar .dn-list > strong { font-size: 13px; }
  .donutbar .dn-item { display: flex; align-items: center; gap: 6px; font-size: 12px; }
  .donutbar .dn-item strong { margin-left: auto; }
  .donutbar .dn-dot { width: 10px; height: 10px; border-radius: 3px; flex: none; }
  .donutbar .dn-caption { font-size: 11px; opacity: .6; }
  .gaugebar { display: flex; flex-direction: column; gap: 7px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .gaugebar .gg-head { display: flex; align-items: baseline; justify-content: space-between; font-size: 13px; }
  .gaugebar .gg-head strong { font-size: 16px; }
  .gaugebar .gg-track { height: 12px; border-radius: 999px; background: rgba(128,128,128,.2); overflow: hidden; }
  .gaugebar .gg-fill { display: block; height: 100%; border-radius: 999px; background: var(--primary); }
  .gaugebar .gg-fill.safe { background: #22c55e; }
  .gaugebar .gg-fill.warning { background: #f59e0b; }
  .gaugebar .gg-fill.danger { background: #ef4444; }
  .gaugebar .gg-labels { display: flex; justify-content: space-between; font-size: 11px; opacity: .6; }
  .rankingbar { display: flex; flex-direction: column; gap: 7px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .rankingbar .rk-head { display: flex; align-items: baseline; justify-content: space-between; }
  .rankingbar .rk-title { font-size: 13px; font-weight: 600; }
  .rankingbar .rk-unit { font-size: 11px; opacity: .6; }
  .rankingbar .rk-row { display: flex; align-items: center; gap: 9px; font-size: 13px; }
  .rankingbar .rk-no { flex: none; width: 22px; height: 22px; border-radius: 999px; font-size: 11px;
    font-weight: 700; display: inline-flex; align-items: center; justify-content: center;
    background: rgba(128,128,128,.16); }
  .rankingbar .rk-row.top .rk-no { background: var(--primary); color: var(--on-primary); }
  .rankingbar .rk-name { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .rankingbar .rk-track { flex: none; width: 84px; height: 6px; border-radius: 999px;
    background: rgba(128,128,128,.2); overflow: hidden; }
  .rankingbar .rk-fill { display: block; height: 100%; border-radius: 999px; background: var(--primary); }
  .rankingbar .rk-val { font-size: 12px; }
  .heatmapbar { display: flex; flex-direction: column; gap: 8px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .heatmapbar > strong { font-size: 13px; }
  .heatmapbar .hm-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 4px; }
  .heatmapbar .hm-cell { height: 22px; border-radius: 4px; }
  .heatmapbar .hm-foot { display: flex; align-items: center; font-size: 11px; opacity: .6; }
  .heatmapbar .hm-foot small { display: inline-flex; align-items: center; gap: 5px; }
  .heatmapbar .hm-foot .mi { font-size: 14px; }
  .distributionbar { display: flex; flex-direction: column; gap: 8px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .distributionbar > strong { font-size: 13px; }
  .distributionbar .ds-track { display: flex; height: 14px; border-radius: 999px; overflow: hidden;
    background: rgba(128,128,128,.18); }
  .distributionbar .ds-seg { height: 100%; }
  .distributionbar .ds-legend { display: flex; flex-wrap: wrap; gap: 6px 12px; font-size: 12px; }
  .distributionbar .ds-item { display: inline-flex; align-items: center; gap: 5px; }
  .distributionbar .ds-dot { width: 9px; height: 9px; border-radius: 3px; }
  .distributionbar .ds-caption { font-size: 11px; opacity: .6; }
  .funnelbar { display: flex; flex-direction: column; gap: 6px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .funnelbar > strong { font-size: 13px; }
  .funnelbar .fn-row { display: flex; align-items: center; gap: 9px; font-size: 12px; }
  .funnelbar .fn-name { flex: none; width: 92px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .funnelbar .fn-track { flex: 1; height: 14px; border-radius: 6px; background: rgba(128,128,128,.18);
    overflow: hidden; }
  .funnelbar .fn-fill { display: block; height: 100%; border-radius: 6px; background: var(--primary); }
  .funnelbar .fn-val { flex: none; width: 34px; text-align: right; font-size: 12px; }
  .funnelbar .fn-caption { font-size: 11px; opacity: .6; }

  /* ---- Formulir ---- */
  .uploadinputbar { display: flex; flex-direction: column; gap: 8px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .uploadinputbar .ui-drop { display: flex; align-items: center; gap: 12px; padding: 12px;
    border: 1px dashed rgba(128,128,128,.55); border-radius: 12px; }
  .uploadinputbar .ui-drop > .mi { font-size: 26px; color: var(--primary); }
  .uploadinputbar .ui-text { flex: 1; min-width: 0; display: flex; flex-direction: column; }
  .uploadinputbar .ui-text strong { font-size: 13px; }
  .uploadinputbar .ui-text small { font-size: 12px; opacity: .65; }
  .uploadinputbar .ui-file { display: flex; justify-content: space-between; align-items: center; gap: 8px;
    font-size: 12px; }
  .uploadinputbar .ui-file strong { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; }
  .uploadinputbar .ui-track { display: block; height: 6px; border-radius: 999px;
    background: rgba(128,128,128,.2); overflow: hidden; }
  .uploadinputbar .ui-fill { display: block; height: 100%; border-radius: 999px; background: var(--primary); }
  .datepickerbar { display: flex; flex-direction: column; gap: 9px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .datepickerbar .dp-label { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 600; }
  .datepickerbar .dp-label .mi { color: var(--primary); }
  .datepickerbar .dp-dates { display: flex; align-items: center; gap: 10px; }
  .datepickerbar .dp-field { flex: 1; display: flex; flex-direction: column; gap: 2px; padding: 9px 12px;
    border: 1px solid rgba(128,128,128,.3); border-radius: 11px; }
  .datepickerbar .dp-field small { font-size: 11px; opacity: .6; }
  .datepickerbar .dp-field strong { font-size: 13px; }
  .datepickerbar .dp-arrow { opacity: .5; }
  .datepickerbar .dp-foot { display: flex; align-items: center; justify-content: space-between; gap: 8px;
    flex-wrap: wrap; }
  .datepickerbar .dp-presets { display: flex; gap: 5px; }
  .datepickerbar .dp-preset { padding: 5px 11px; font-size: 12px; border-radius: 999px;
    border: 1px solid rgba(128,128,128,.35); }
  .datepickerbar .dp-preset.on { background: var(--primary); border-color: var(--primary);
    color: var(--on-primary); font-weight: 600; }
  .ratinginputbar { display: flex; flex-direction: column; gap: 6px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .ratinginputbar .ri-label { font-size: 13px; font-weight: 600; }
  .ratinginputbar .ri-stars { display: flex; gap: 2px; }
  .ratinginputbar .ri-star { font-size: 26px; color: rgba(128,128,128,.45); }
  .ratinginputbar .ri-star.on { color: #f59e0b; }
  .ratinginputbar .ri-labels { display: flex; justify-content: space-between; font-size: 12px; opacity: .7; }
  .quantitybar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .quantitybar .qt-text { flex: 1; display: flex; flex-direction: column; }
  .quantitybar .qt-text strong { font-size: 14px; }
  .quantitybar .qt-text small { font-size: 12px; opacity: .65; }
  .quantitybar .qt-ctrl { display: inline-flex; align-items: center; border: 1px solid rgba(128,128,128,.35);
    border-radius: 10px; overflow: hidden; }
  .quantitybar .qt-btn { width: 34px; height: 34px; border: 0; background: rgba(128,128,128,.14); color: inherit;
    cursor: pointer; display: inline-flex; align-items: center; justify-content: center; }
  .quantitybar .qt-btn .mi { font-size: 18px; }
  .quantitybar .qt-val { min-width: 44px; text-align: center; font-size: 15px; font-weight: 700; }
  .passstrengthbar { display: flex; flex-direction: column; gap: 8px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .passstrengthbar .ps-head { display: flex; align-items: baseline; justify-content: space-between; font-size: 13px; }
  .passstrengthbar .ps-head em { font-style: normal; font-weight: 700; font-size: 12px; }
  .passstrengthbar .ps-bars { display: flex; gap: 4px; }
  .passstrengthbar .ps-seg { flex: 1; height: 6px; border-radius: 999px; }
  .passstrengthbar .ps-hints { display: flex; flex-direction: column; gap: 3px; }
  .passstrengthbar .ps-hint { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; opacity: .75; }
  .passstrengthbar .ps-hint .mi { font-size: 15px; color: #16a34a; }

  /* ---- Media ---- */
  .videobar { display: flex; align-items: center; gap: 12px; padding: 10px 12px;
    border: 1px solid rgba(128,128,128,.3); }
  .videobar .vd-thumb { position: relative; flex: none; width: 132px; aspect-ratio: 16 / 9; border-radius: 10px;
    overflow: hidden; background: rgba(128,128,128,.18); display: block; }
  .videobar .vd-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .videobar .vd-empty { width: 100%; height: 100%; display: inline-flex; align-items: center;
    justify-content: center; opacity: .5; }
  .videobar .vd-play { position: absolute; inset: 0; margin: auto; width: 34px; height: 34px; border-radius: 50%;
    background: rgba(255,255,255,.86); color: #111827; display: inline-flex; align-items: center;
    justify-content: center; }
  .videobar .vd-dur { position: absolute; right: 6px; bottom: 6px; padding: 2px 6px; border-radius: 6px;
    background: rgba(17,24,39,.78); color: #fff; font-size: 11px; }
  .videobar .vd-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .videobar .vd-text strong { font-size: 14px; }
  .videobar .vd-text small { font-size: 12px; opacity: .65; }
  .equalizerbar { display: flex; flex-direction: column; gap: 10px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .equalizerbar .eq-head { display: flex; align-items: center; gap: 8px; }
  .equalizerbar .eq-head .mi { color: var(--primary); }
  .equalizerbar .eq-head strong { flex: 1; font-size: 13px; }
  .equalizerbar .eq-bands { display: flex; align-items: flex-end; gap: 8px; height: 74px; }
  .equalizerbar .eq-band { flex: 1; height: 100%; display: flex; flex-direction: column; align-items: center;
    justify-content: flex-end; gap: 5px; }
  .equalizerbar .eq-bar { width: 9px; border-radius: 5px; background: var(--primary); }
  .equalizerbar .eq-band small { font-size: 10px; opacity: .7; white-space: nowrap; }
  .podcastbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .podcastbar .pc-ico { flex: none; width: 44px; height: 44px; border-radius: 50%; display: inline-flex;
    align-items: center; justify-content: center; background: var(--primary); color: var(--on-primary); }
  .podcastbar .pc-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .podcastbar .pc-text small { font-size: 11px; text-transform: uppercase; letter-spacing: .04em; opacity: .6; }
  .podcastbar .pc-text strong { font-size: 14px; }
  .podcastbar .pc-text small + strong + small { display: inline-flex; align-items: center; gap: 4px;
    font-size: 12px; text-transform: none; letter-spacing: 0; opacity: .65; }
  .camerabar { display: flex; flex-direction: column; gap: 12px; padding: 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .camerabar .cm-modes { display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; }
  .camerabar .cm-mode { padding: 5px 12px; font-size: 12px; border-radius: 999px; opacity: .7; }
  .camerabar .cm-mode.on { background: var(--primary); color: var(--on-primary); opacity: 1; font-weight: 600; }
  .camerabar .cm-main { display: flex; align-items: center; justify-content: space-between; }
  .camerabar .cm-side { width: 42px; height: 42px; border-radius: 12px; display: inline-flex;
    align-items: center; justify-content: center; background: rgba(128,128,128,.16); }
  .camerabar .cm-shutter { width: 56px; height: 56px; border-radius: 50%; border: 3px solid var(--text);
    display: inline-flex; align-items: center; justify-content: center; position: relative; }
  .camerabar .cm-shutter::after { content: ""; width: 40px; height: 40px; border-radius: 50%;
    background: rgba(128,128,128,.35); }
  .camerabar .cm-note { text-align: center; font-size: 11px; opacity: .6; }
  .lyricsbar { display: flex; flex-direction: column; gap: 5px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .lyricsbar .ly-head { color: var(--primary); font-size: 20px; }
  .lyricsbar .ly-line { font-size: 14px; opacity: .55; }
  .lyricsbar .ly-line.on { opacity: 1; font-weight: 700; color: var(--primary); }
  .lyricsbar .ly-note { display: inline-flex; align-items: center; gap: 5px; font-size: 11px; opacity: .6; }
  .lyricsbar .ly-note .mi { font-size: 14px; }

  /* ---- Sosial ---- */
  .groupsbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .groupsbar .gr-av { flex: none; width: 46px; height: 46px; border-radius: 50%; overflow: hidden;
    background: var(--primary); color: var(--on-primary); display: inline-flex; align-items: center;
    justify-content: center; font-weight: 700; }
  .groupsbar .gr-av img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .groupsbar .gr-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .groupsbar .gr-text strong { font-size: 14px; }
  .groupsbar .gr-text small { font-size: 12px; opacity: .65; display: inline-flex; align-items: center; gap: 4px; }
  .groupsbar .gr-text small .mi { font-size: 14px; }
  .trendbar { display: flex; flex-direction: column; gap: 2px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .trendbar .tr-head { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 600;
    margin-bottom: 4px; }
  .trendbar .tr-head .mi { color: var(--primary); }
  .trendbar .tr-row { display: flex; align-items: center; justify-content: space-between; gap: 10px;
    padding: 6px 8px; border-radius: 9px; font-size: 13px; }
  .trendbar .tr-row:hover { background: rgba(128,128,128,.12); }
  .trendbar .tr-tag { font-weight: 600; color: var(--primary); }
  .trendbar .tr-row small { font-size: 12px; opacity: .65; }
  .awardbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3);
    background: linear-gradient(120deg, rgba(253,230,138,.35), rgba(251,191,36,.12)); }
  .awardbar .aw-ico { flex: none; width: 46px; height: 46px; border-radius: 50%; display: inline-flex;
    align-items: center; justify-content: center; background: linear-gradient(140deg, #fde68a, #f59e0b);
    color: #7c2d12; font-size: 24px; }
  .awardbar .aw-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .awardbar .aw-text strong { display: inline-flex; align-items: center; gap: 8px; font-size: 14px; }
  .awardbar .aw-points { font-style: normal; font-size: 12px; font-weight: 700; color: #b45309; }
  .awardbar .aw-text small { font-size: 12px; opacity: .7; }

  /* ---- Toko ---- */
  .wishlistbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .wishlistbar .wl-thumb { flex: none; width: 64px; height: 64px; border-radius: 12px; overflow: hidden;
    background: rgba(128,128,128,.16); display: inline-flex; align-items: center; justify-content: center; }
  .wishlistbar .wl-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .wishlistbar .wl-empty { opacity: .45; }
  .wishlistbar .wl-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .wishlistbar .wl-text strong { font-size: 14px; }
  .wishlistbar .wl-price { font-size: 14px; font-weight: 700; }
  .wishlistbar .wl-text small { font-size: 12px; opacity: .6; }
  .orderbar { display: flex; flex-direction: column; gap: 8px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .orderbar .or-head { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
  .orderbar .or-code { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 700; }
  .orderbar .or-code .mi { color: var(--primary); }
  .orderbar .or-meta { display: flex; align-items: baseline; justify-content: space-between; font-size: 12px; }
  .orderbar .or-meta small { opacity: .65; }
  .orderbar .or-total { font-size: 14px; }
  .orderbar .or-foot { display: flex; justify-content: flex-end; }
  .bundlingbar { display: flex; flex-direction: column; gap: 8px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .bundlingbar .bd-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
  .bundlingbar .bd-head strong { font-size: 14px; }
  .bundlingbar .bd-save { display: inline-flex; align-items: center; gap: 4px; padding: 3px 9px; border-radius: 999px;
    background: rgba(34,197,94,.16); color: #15803d; font-size: 11px; font-weight: 700; }
  .bundlingbar .bd-save .mi { font-size: 14px; }
  .bundlingbar .bd-items { display: flex; flex-direction: column; gap: 4px; font-size: 12px; }
  .bundlingbar .bd-item { display: flex; justify-content: space-between; gap: 10px; }
  .bundlingbar .bd-item small { opacity: .7; }
  .bundlingbar .bd-foot { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
  .bundlingbar .bd-price { font-size: 15px; }
  .loyaltybar { display: flex; flex-direction: column; gap: 8px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .loyaltybar .lt-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
  .loyaltybar .lt-head strong { display: inline-flex; align-items: center; gap: 6px; font-size: 14px; }
  .loyaltybar .lt-head .mi { color: #f59e0b; }
  .loyaltybar .lt-points { font-style: normal; font-size: 13px; font-weight: 700; color: var(--primary); }
  .loyaltybar .lt-track { display: block; height: 10px; border-radius: 999px; background: rgba(128,128,128,.2);
    overflow: hidden; }
  .loyaltybar .lt-fill { display: block; height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, var(--primary), #f59e0b); }
  .loyaltybar .lt-note { font-size: 12px; opacity: .65; }
  .loyaltybar .lt-foot { display: flex; justify-content: flex-end; }

  /* ---- Keuangan ---- */
  .balancebar { display: flex; align-items: center; gap: 12px; padding: 14px 16px;
    border: 1px solid rgba(128,128,128,.3);
    background: linear-gradient(120deg, rgba(99,102,241,.16), rgba(99,102,241,.04)); }
  .balancebar .bl-ico { flex: none; width: 46px; height: 46px; border-radius: 14px; display: inline-flex;
    align-items: center; justify-content: center; background: var(--primary); color: var(--on-primary);
    font-size: 24px; }
  .balancebar .bl-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .balancebar .bl-text small { font-size: 12px; opacity: .7; }
  .balancebar .bl-amount { font-size: 20px; }
  .transactionbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .transactionbar .tx-ico { flex: none; width: 40px; height: 40px; border-radius: 50%; display: inline-flex;
    align-items: center; justify-content: center; }
  .transactionbar .tx-ico.in { background: rgba(34,197,94,.16); color: #16a34a; }
  .transactionbar .tx-ico.out { background: rgba(239,68,68,.16); color: #dc2626; }
  .transactionbar .tx-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .transactionbar .tx-text strong { font-size: 14px; }
  .transactionbar .tx-text small { font-size: 12px; opacity: .65; }
  .transactionbar .tx-side { display: flex; align-items: center; gap: 8px; }
  .transactionbar .tx-amount { font-style: normal; font-size: 14px; font-weight: 700; white-space: nowrap; }
  .transactionbar .tx-amount.in { color: #16a34a; }
  .transactionbar .tx-amount.out { color: #dc2626; }
  .budgetbar { display: flex; flex-direction: column; gap: 8px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .budgetbar .bg-head { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; }
  .budgetbar .bg-head strong { font-size: 13px; }
  .budgetbar .bg-head em { font-style: normal; font-size: 12px; font-weight: 700; }
  .budgetbar .bg-track { display: block; height: 10px; border-radius: 999px; background: rgba(128,128,128,.2);
    overflow: hidden; }
  .budgetbar .bg-fill { display: block; height: 100%; border-radius: 999px; background: var(--primary); }
  .budgetbar .bg-fill.safe { background: #22c55e; }
  .budgetbar .bg-fill.warning { background: #f59e0b; }
  .budgetbar .bg-fill.danger { background: #ef4444; }
  .budgetbar > small { font-size: 12px; opacity: .65; }
  .invoicebar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .invoicebar .iv-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .invoicebar .iv-title { display: inline-flex; align-items: center; gap: 6px; }
  .invoicebar .iv-title .mi { color: var(--primary); font-size: 18px; }
  .invoicebar .iv-title strong { font-size: 14px; }
  .invoicebar .iv-text small { font-size: 12px; opacity: .65; }
  .invoicebar .iv-side { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
  .invoicebar .iv-amount { font-style: normal; font-size: 15px; font-weight: 700; }
  .savingsbar { display: flex; flex-direction: column; gap: 8px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .savingsbar .sv-head { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; }
  .savingsbar .sv-head strong { font-size: 13px; }
  .savingsbar .sv-head em { font-style: normal; font-size: 12px; font-weight: 700; color: var(--primary); }
  .savingsbar .sv-track { display: block; height: 10px; border-radius: 999px; background: rgba(128,128,128,.2);
    overflow: hidden; }
  .savingsbar .sv-fill { display: block; height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, var(--primary), #22c55e); }
  .savingsbar .sv-meta { display: flex; justify-content: space-between; font-size: 12px; opacity: .7; }
  .savingsbar > small { font-size: 12px; opacity: .65; }
  .savingsbar .sv-foot { display: flex; justify-content: flex-end; }

  /* ---- Peta & Lokasi ---- */
  .locationbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .locationbar .lc-ico { flex: none; width: 42px; height: 42px; border-radius: 12px; display: inline-flex;
    align-items: center; justify-content: center; background: rgba(99,102,241,.14); color: var(--primary); }
  .locationbar .lc-thumb { flex: none; width: 46px; height: 46px; border-radius: 10px; overflow: hidden;
    background: rgba(128,128,128,.16); }
  .locationbar .lc-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .locationbar .lc-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .locationbar .lc-text small { font-size: 11px; opacity: .6; }
  .locationbar .lc-text strong { font-size: 14px; }
  .locationbar .lc-text small + strong + small { display: inline-flex; align-items: center; gap: 4px;
    font-size: 12px; opacity: .65; }
  .locationbar .lc-text small + strong + small .mi { font-size: 14px; }
  .routebar { display: flex; flex-direction: column; gap: 4px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .routebar .rt-points { display: flex; flex-direction: column; }
  .routebar .rt-row { display: flex; align-items: center; gap: 10px; font-size: 13px; padding: 3px 0; }
  .routebar .rt-dot { flex: none; width: 11px; height: 11px; border-radius: 999px; background: rgba(128,128,128,.6); }
  .routebar .rt-dot.from { background: #22c55e; }
  .routebar .rt-dot.to { background: var(--primary); border-radius: 3px; }
  .routebar .rt-rail { width: 2px; height: 14px; margin-left: 4.5px; background: rgba(128,128,128,.4);
    border-radius: 2px; }
  .routebar .rt-foot { display: flex; align-items: center; justify-content: space-between; gap: 10px;
    margin-top: 6px; }
  .routebar .rt-foot small { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; opacity: .7; }
  .routebar .rt-foot .mi { color: var(--primary); font-size: 18px; }
  .nearbybar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .nearbybar .nr-thumb { flex: none; width: 60px; height: 60px; border-radius: 12px; overflow: hidden;
    background: rgba(128,128,128,.16); display: inline-flex; align-items: center; justify-content: center; }
  .nearbybar .nr-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .nearbybar .nr-empty { opacity: .45; }
  .nearbybar .nr-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .nearbybar .nr-text strong { font-size: 14px; }
  .nearbybar .nr-text > small { font-size: 12px; opacity: .65; }
  .nearbybar .nr-meta { display: flex; align-items: center; gap: 10px; }
  .nearbybar .nr-rate { display: inline-flex; align-items: center; gap: 3px; font-style: normal; font-size: 12px;
    font-weight: 700; }
  .nearbybar .nr-rate .mi { color: #f59e0b; font-size: 15px; }
  .nearbybar .nr-meta small { font-size: 12px; opacity: .6; }
  .nearbybar .nr-side { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; }
  .checkinbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .checkinbar .ck-ico { flex: none; width: 44px; height: 44px; border-radius: 50%; display: inline-flex;
    align-items: center; justify-content: center; background: rgba(34,197,94,.16); color: #16a34a; }
  .checkinbar .ck-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .checkinbar .ck-text small { font-size: 12px; opacity: .65; }
  .checkinbar .ck-time { font-size: 18px; }
  .checkinbar .ck-side { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; }

  /* ---- Konten ---- */
  .articlebar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .articlebar .ar-cat { flex: none; padding: 4px 10px; border-radius: 999px; font-size: 11px; font-weight: 700;
    background: rgba(99,102,241,.14); color: var(--primary); }
  .articlebar .ar-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .articlebar .ar-text strong { font-size: 14px; }
  .articlebar .ar-text small { display: inline-flex; align-items: center; gap: 5px; font-size: 12px; opacity: .65; }
  .articlebar .ar-text small .mi { font-size: 14px; }
  .authorbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .authorbar .au-av { flex: none; width: 46px; height: 46px; border-radius: 50%; overflow: hidden;
    background: var(--primary); color: var(--on-primary); display: inline-flex; align-items: center;
    justify-content: center; font-weight: 700; }
  .authorbar .au-av img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .authorbar .au-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .authorbar .au-text strong { font-size: 14px; }
  .authorbar .au-text small { font-size: 12px; opacity: .65; }
  .authorbar .au-posts { font-size: 11px; opacity: .55; }
  .chaptersbar { display: flex; flex-direction: column; gap: 6px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .chaptersbar .ch-head { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; }
  .chaptersbar .ch-head .mi { color: var(--primary); }
  .chaptersbar .ch-track { display: block; height: 6px; border-radius: 999px; background: rgba(128,128,128,.2);
    overflow: hidden; }
  .chaptersbar .ch-fill { display: block; height: 100%; border-radius: 999px; background: var(--primary); }
  .chaptersbar .ch-item { display: flex; align-items: center; gap: 8px; padding: 6px 8px; border-radius: 9px;
    font-size: 13px; }
  .chaptersbar .ch-item.done { opacity: .7; }
  .chaptersbar .ch-item.on { background: rgba(99,102,241,.14); font-weight: 600; color: var(--primary); }
  .chaptersbar .ch-no { flex: none; width: 20px; text-align: center; font-size: 12px; }
  .chaptersbar .ch-item.done .ch-no .mi { font-size: 16px; color: #16a34a; }
  .readingprogressbar { display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .readingprogressbar .rp-ico { flex: none; color: var(--primary); font-size: 24px; }
  .readingprogressbar .rp-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 5px; }
  .readingprogressbar .rp-text strong { font-size: 14px; }
  .readingprogressbar .rp-track { display: block; height: 6px; border-radius: 999px;
    background: rgba(128,128,128,.2); overflow: hidden; }
  .readingprogressbar .rp-fill { display: block; height: 100%; border-radius: 999px; background: var(--primary); }
  .readingprogressbar .rp-text small { font-size: 12px; opacity: .65; }
  .relatedbar { display: flex; flex-direction: column; gap: 2px; padding: 12px 14px;
    border: 1px solid rgba(128,128,128,.3); }
  .relatedbar .rl-head { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 600;
    margin-bottom: 4px; }
  .relatedbar .rl-head .mi { color: var(--primary); }
  .relatedbar .rl-item { display: flex; align-items: center; justify-content: space-between; gap: 10px;
    padding: 8px 6px; font-size: 13px; border-top: 1px dashed rgba(128,128,128,.3); }
  .relatedbar .rl-item:first-of-type { border-top: 0; }
  .relatedbar .rl-item small { display: inline-flex; align-items: center; gap: 4px; font-size: 12px; opacity: .65; }
  .relatedbar .rl-item small .mi { font-size: 14px; }
  .relatedbar .rl-foot { display: flex; justify-content: flex-end; padding-top: 4px; }
"""
