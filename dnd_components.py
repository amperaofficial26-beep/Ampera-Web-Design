"""Komponen Streamlit kustom (HTML5, tanpa paket tambahan): Susunan seret-lepas,
palet komponen, dan preview interaktif, beserta penangan event-nya."""
import hashlib
import tempfile
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from actions import add_element, delete_element, insert_element
from config import ELEMENT_LABELS
from projects import current_page

DND_HTML = r'''
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0">
<style>
  .mi { font-family:'Material Symbols Rounded'; font-size:18px; line-height:1; display:inline-block;
    width:1em; overflow:hidden; white-space:nowrap; vertical-align:middle; font-feature-settings:'liga'; }
  :root { --fg:#0f172a; --bg2:rgba(255,255,255,.62); --accent:#6366f1; --line:rgba(148,163,184,.35);
    --glass:1px solid rgba(255,255,255,.65); }
  *{box-sizing:border-box} html,body{margin:0;padding:0;background:transparent;color:var(--fg);
    font-family:Inter,system-ui,sans-serif;font-size:13px}
  .title{font-weight:700;margin:2px 0 5px}.hint{opacity:.62;font-size:11px;margin:0 0 8px}
  #list{list-style:none;margin:0;padding:6px;min-height:74px;border:1px dashed var(--line);
    border-radius:14px;max-height:280px;overflow:auto;
    background:rgba(255,255,255,.34);
    -webkit-backdrop-filter:blur(12px) saturate(150%);backdrop-filter:blur(12px) saturate(150%);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.6)}
  #list:empty::before{content:"Tarik komponen ke sini, atau pilih komponen di bawah";
    display:block;text-align:center;opacity:.55;padding:26px 8px}
  #list.ins-empty{border-color:var(--accent);background:rgba(99,102,241,.10)}
  li{display:flex;align-items:center;gap:7px;padding:8px 9px;margin:0 0 6px;border:var(--glass);
    border-radius:11px;background:var(--bg2);cursor:grab;user-select:none;position:relative;
    -webkit-backdrop-filter:blur(10px) saturate(150%);backdrop-filter:blur(10px) saturate(150%);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.7),0 4px 12px rgba(15,23,42,.06)}
  li:hover{border-color:rgba(99,102,241,.45)}
  li.sel{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
  li.dragging{opacity:.4}
  li.ins-before::before,li.ins-after::after{content:"";position:absolute;left:0;right:0;height:3px;
    background:var(--accent);border-radius:2px}
  li.ins-before::before{top:-5px} li.ins-after::after{bottom:-5px}
  .grip{opacity:.45}.lbl{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .del{border:0;background:transparent;color:inherit;cursor:pointer;opacity:.55;padding:0 3px}
  .del:hover{opacity:1;color:var(--accent)}
</style>
</head>
<body>
<div class="title">Susunan halaman</div>
<p class="hint">Klik untuk memilih · seret untuk mengubah urutan · × untuk menghapus</p>
<ul id="list"></ul>
<script>
(function(){
  var items=[],selected=null,drag=null;
  var listEl=document.getElementById("list");
  function post(type,data){window.parent.postMessage(Object.assign({isStreamlitMessage:true,type:type},data),"*");}
  function send(payload){payload.id=Date.now()+"-"+Math.random().toString(36).slice(2);
    post("streamlit:setComponentValue",{value:payload,dataType:"json"});}
  function fit(){post("streamlit:setFrameHeight",{height:Math.min(document.documentElement.scrollHeight+4,360)});}
  function clearInd(){listEl.classList.remove("ins-empty");
    listEl.querySelectorAll("li").forEach(function(li){li.classList.remove("ins-before","ins-after");});}
  function indexAt(y){var lis=listEl.querySelectorAll("li"),idx=0;
    for(var i=0;i<lis.length;i++){var r=lis[i].getBoundingClientRect();if(y>r.top+r.height/2)idx++;else break;}return idx;}
  function showInd(idx){clearInd();var lis=listEl.querySelectorAll("li");
    if(!lis.length){listEl.classList.add("ins-empty");return;}
    if(idx<lis.length)lis[idx].classList.add("ins-before");else lis[lis.length-1].classList.add("ins-after");}
  function icon(name){var s=document.createElement("span");s.className="mi";s.textContent=name;return s;}
  function fit(){post("streamlit:setFrameHeight",{height:78});}
  function render(){
    listEl.textContent="";
    items.forEach(function(it,i){
      var li=document.createElement("li");li.draggable=true;li.dataset.id=it.id;
      if(it.id===selected)li.classList.add("sel");
      var grip=document.createElement("span");grip.className="grip";grip.textContent="⠿";
      var lbl=document.createElement("span");lbl.className="lbl";lbl.appendChild(icon(it.icon));
      lbl.appendChild(document.createTextNode(" "+(i+1)+". "+it.label));
      var del=document.createElement("button");del.className="del";del.type="button";del.title="Hapus";
      del.appendChild(icon("close"));del.addEventListener("click",function(e){e.stopPropagation();send({action:"delete",target:it.id});});
      li.appendChild(grip);li.appendChild(lbl);li.appendChild(del);
      li.addEventListener("click",function(){send({action:"select",target:it.id});});
      li.addEventListener("dragstart",function(e){drag={id:it.id};li.classList.add("dragging");
        e.dataTransfer.setData("text/plain","move:"+it.id);e.dataTransfer.effectAllowed="move";});
      li.addEventListener("dragend",function(){drag=null;li.classList.remove("dragging");clearInd();});
      listEl.appendChild(li);
    });
    fit();
  }
  listEl.addEventListener("dragover",function(e){
    var external=e.dataTransfer.getData("text/plain")||"";
    if(!drag && !external.startsWith("new:"))return;
    e.preventDefault();
    e.dataTransfer.dropEffect=external.startsWith("new:")?"copy":"move";
    showInd(indexAt(e.clientY));
  });
  listEl.addEventListener("dragleave",function(e){if(!listEl.contains(e.relatedTarget))clearInd();});
  listEl.addEventListener("drop",function(e){
    e.preventDefault();
    var external=e.dataTransfer.getData("text/plain")||"";
    var idx=indexAt(e.clientY);clearInd();
    if(external.startsWith("new:")){
      send({action:"insert",type:external.slice(4),index:idx});
      drag=null;
      return;
    }
    if(!drag)return;
    var ids=items.map(function(x){return x.id;});
    var from=ids.indexOf(drag.id);if(from<0){drag=null;return;}var to=idx;if(from<to)to--;
    if(to!==from){ids.splice(from,1);ids.splice(to,0,drag.id);selected=drag.id;send({action:"reorder",order:ids,selected:drag.id});}
    drag=null;
  });
  window.addEventListener("message",function(e){
    var d=e.data;if(!d||d.type!=="streamlit:render")return;
    var a=d.args||{};items=a.items||[];selected=a.selected||null;render();
  });
  window.addEventListener("resize",fit);
  post("streamlit:componentReady",{apiVersion:1});
})();
</script>
</body>
</html>
'''

PALETTE_HTML = r'''
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0">
<style>
  *{box-sizing:border-box}html,body{margin:0;padding:0;background:transparent;font-family:Inter,system-ui,sans-serif;color:#0f172a}
  .dock{border:1px solid rgba(255,255,255,.65);background:rgba(255,255,255,.52);border-radius:18px;padding:10px 12px;
    -webkit-backdrop-filter:blur(16px) saturate(150%);backdrop-filter:blur(16px) saturate(150%);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.7),0 12px 30px rgba(31,38,135,.12)}
  .head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:8px}
  .title{font-size:13px;font-weight:700}.hint{font-size:11px;opacity:.58}
  .scroll{display:flex;gap:7px;overflow-x:auto;padding:2px 1px 5px;scrollbar-width:thin}
  .chip{flex:0 0 auto;display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(255,255,255,.65);
    background:linear-gradient(180deg,rgba(255,255,255,.78),rgba(255,255,255,.52));border-radius:12px;padding:8px 11px;
    font-size:12px;cursor:pointer;white-space:nowrap;
    -webkit-backdrop-filter:blur(10px) saturate(150%);backdrop-filter:blur(10px) saturate(150%);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.75),0 4px 12px rgba(15,23,42,.06);transition:.14s}
  .chip:hover{transform:translateY(-1px);border-color:rgba(99,102,241,.6);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.85),0 12px 26px rgba(99,102,241,.22)}
  .chip .mi{font-family:'Material Symbols Rounded';font-size:17px;line-height:1}
  .group{flex:0 0 auto;font-size:10px;font-weight:700;opacity:.55;padding:8px 3px 0}
</style>
</head>
<body>
<div class="dock">
  <div class="head"><div class="title">Komponen</div><div class="hint">Klik komponen untuk menambah ke Susunan</div></div>
  <div id="scroll" class="scroll"></div>
</div>
<script>
(function(){
  var palette=[],root=document.getElementById("scroll");
  function post(type,data){window.parent.postMessage(Object.assign({isStreamlitMessage:true,type:type},data),"*");}
  function send(payload){payload.id=Date.now()+"-"+Math.random().toString(36).slice(2);
    post("streamlit:setComponentValue",{value:payload,dataType:"json"});}
  function fit(){post("streamlit:setFrameHeight",{height:96});}
  function icon(name){var s=document.createElement("span");s.className="mi";s.textContent=name;return s;}
  function render(){
    root.textContent="";var last="";
    palette.forEach(function(p){
      if(p.group!==last){var g=document.createElement("span");g.className="group";g.textContent=p.group;root.appendChild(g);last=p.group;}
      var c=document.createElement("button");c.type="button";c.className="chip";c.draggable=true;
      c.appendChild(icon(p.icon||"widgets"));
      c.appendChild(document.createTextNode(p.label));c.title="Klik atau seret ke Susunan";
      c.addEventListener("dragstart",function(e){
        e.dataTransfer.setData("text/plain","new:"+p.type);
        e.dataTransfer.effectAllowed="copy";
      });
      c.addEventListener("click",function(){send({action:"insert",type:p.type});});
      root.appendChild(c);
    });
    fit();
  }
  window.addEventListener("message",function(e){var d=e.data;if(!d||d.type!=="streamlit:render")return;
    palette=(d.args||{}).palette||[];render();});
  post("streamlit:componentReady",{apiVersion:1});
})();
</script>
</body>
</html>
'''

PREVIEW_HTML = r'''
<!DOCTYPE html>
<html lang="id">
<head><meta charset="utf-8"><style>
html,body{margin:0;width:100%;height:100%;background:linear-gradient(160deg,#eef2ff,#f8f9ff 45%,#fdf2f8)}
body{display:flex;justify-content:center;padding:12px;box-sizing:border-box;overflow:hidden}
iframe{width:100%;height:100%;border:1px solid rgba(255,255,255,.7);background:#fff;border-radius:16px;
  box-shadow:0 18px 40px rgba(31,38,135,.18),inset 0 1px 0 rgba(255,255,255,.6)}
</style></head>
<body><iframe id="preview"></iframe>
<script>
(function(){
  var frame=document.getElementById("preview");
  function post(type,data){window.parent.postMessage(Object.assign({isStreamlitMessage:true,type:type},data),"*");}
  function send(payload){payload.id=Date.now()+"-"+Math.random().toString(36).slice(2);
    post("streamlit:setComponentValue",{value:payload,dataType:"json"});}
  function fit(){post("streamlit:setFrameHeight",{height:780});}
  window.addEventListener("message",function(e){
    var d=e.data;if(!d)return;
    if(d.type==="streamlit:render"){
      var a=d.args||{};frame.style.width=a.deviceWidth?a.deviceWidth+"px":"100%";frame.style.maxWidth="100%";
      frame.srcdoc=a.html||"";fit();
    }
    if(d.type==="ui-builder-select"&&d.id){send({action:"select",target:d.id});}
  });
  post("streamlit:componentReady",{apiVersion:1});
})();
</script>
</body>
</html>
'''


def _declare(prefix, html_source):
    digest = hashlib.md5(html_source.encode("utf-8")).hexdigest()[:8]
    folder = Path(tempfile.gettempdir()) / f"{prefix}_{digest}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(html_source, encoding="utf-8")
    return components.declare_component(f"{prefix}_{digest}", path=str(folder))


@st.cache_resource
def get_dnd_component():
    return _declare("ui_builder_dnd", DND_HTML)


@st.cache_resource
def get_palette_component():
    return _declare("ui_builder_palette", PALETTE_HTML)


@st.cache_resource
def get_preview_component():
    return _declare("ui_builder_preview", PREVIEW_HTML)


def handle_dnd_event(event):
    """Terapkan event dari panel Susunan."""
    if not isinstance(event, dict):
        return False
    event_id = event.get("id")
    if not event_id or event_id == st.session_state.get("last_dnd_event"):
        return False
    st.session_state.last_dnd_event = event_id

    els = current_page()["elements"]
    by_id = {e["id"]: e for e in els}
    action = event.get("action")

    if action == "select":
        target = event.get("target")
        if target in by_id:
            st.session_state.selected_id = target
        return True
    if action == "reorder":
        order = event.get("order")
        if isinstance(order, list) and sorted(order) == sorted(by_id):
            els[:] = [by_id[i] for i in order]
            if event.get("selected") in by_id:
                st.session_state.selected_id = event["selected"]
        return True
    if action == "delete":
        target = event.get("target")
        for i, el in enumerate(els):
            if el["id"] == target:
                delete_element(i)
                break
        return True
    if action == "insert":
        if event.get("type") in ELEMENT_LABELS:
            insert_element(event["type"], event.get("index"))
        return True
    return False


def handle_palette_event(event):
    if not isinstance(event, dict):
        return False
    event_id = event.get("id")
    if not event_id or event_id == st.session_state.get("last_palette_event"):
        return False
    st.session_state.last_palette_event = event_id
    if event.get("action") == "insert" and event.get("type") in ELEMENT_LABELS:
        add_element(event["type"])
        return True
    return False


def handle_preview_event(event):
    if not isinstance(event, dict):
        return False
    event_id = event.get("id")
    if not event_id or event_id == st.session_state.get("last_preview_event"):
        return False
    st.session_state.last_preview_event = event_id
    if event.get("action") == "select":
        target = event.get("target")
        if any(el.get("id") == target for el in current_page()["elements"]):
            st.session_state.selected_id = target
            return True
    return False
