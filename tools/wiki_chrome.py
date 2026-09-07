# The AI Data+ wiki's shared chrome: one definition, applied to every page.
#
#   python tools/wiki_chrome.py     # re-apply the bar to every page
#
# Each page carries its own copy between the two markers, so a page still
# works opened on its own off a shared folder. This script is how the copies
# stay identical.
#
# The chrome owns four things every page would otherwise invent:
#   the colour tokens, the nav bar, the language switch, and the skip link.
# Edit them here. Re-run. Do not restyle seven copies by hand.
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent   # the site is the folder above this one

OPEN = "<!-- wiki chrome \u00b7 identical in every page of this site: edit one, edit all -->"
CLOSE = "<!-- /wiki chrome -->"

CHROME_CSS = """
<style id="wk-chrome">
  /* ---- project wiki chrome (shared across every page of this site) ---- */
  :root{
    --ink:#14243A; --navy:#1C3557; --slate:#5B6B7F; --mute:#8D9BAB;
    --paper:#F5F7FA; --card:#FFFFFF; --line:#DCE3EA;
    --orange:#E0632A; --purple:#7B2D8E; --green:#3F8F5F; --amber:#C98A1E; --halt:#B44538;
    --person:#C4674A; --blue:#4A7DBD;
    --disp:"Aptos Display","Segoe UI Variable Display","Segoe UI","Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;
    --body:"Aptos","Segoe UI Variable Text","Segoe UI","Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;
    --mono:ui-monospace,"Cascadia Mono","Segoe UI Mono",Consolas,monospace;
    --wk-nav-h:46px;
    --r-ctl:6px; --r-card:10px; --r-lg:14px;
  }
  .wknav *,.wkc *,.wklang *{box-sizing:border-box}
  .wk-zh{display:none}
  html[data-lang="zh"] .wk-zh,html[lang^="zh"] .wk-zh,body[data-lang="zh"] .wk-zh{display:inline}
  html[data-lang="zh"] .wk-en,html[lang^="zh"] .wk-en,body[data-lang="zh"] .wk-en{display:none}

  .wkskip{position:absolute;left:16px;top:-56px;z-index:400;padding:8px 14px;
          background:var(--navy);color:#fff;text-decoration:none;border-radius:var(--r-ctl);
          font-family:var(--disp);font-weight:600;font-size:13px}
  .wkskip:focus{top:8px;color:#fff;outline:2px solid var(--orange);outline-offset:2px}

  .wknav{position:sticky;top:0;z-index:200;background:rgba(255,255,255,.90);
         -webkit-backdrop-filter:saturate(1.5) blur(10px);backdrop-filter:saturate(1.5) blur(10px);
         border-bottom:1px solid rgba(20,36,58,.10);
         font-family:var(--disp)}
  .wknav-in{max-width:1200px;margin:0 auto;padding:0 40px;height:var(--wk-nav-h);display:flex;align-items:center;
            gap:14px;overflow-x:auto;scrollbar-width:none;-ms-overflow-style:none}
  .wknav-in::-webkit-scrollbar{display:none}
  .wkmark{flex:0 0 auto;display:inline-flex;align-items:baseline;gap:8px;text-decoration:none;white-space:nowrap}
  .wkmark b{font-size:14px;font-weight:700;letter-spacing:-.012em;color:var(--ink)}
  .wkmark b i{font-style:normal;color:var(--orange)}
  .wkmark span{font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#9AA6B4;font-weight:600}
  .wkrule{flex:0 0 auto;width:1px;height:17px;background:rgba(20,36,58,.14)}
  .wklinks{flex:1 1 auto;display:flex;align-items:center;gap:1px;white-space:nowrap}
  .wknav a{position:relative;padding:7px 10px;border-radius:5px;font-size:13px;font-weight:600;
           color:var(--slate);text-decoration:none;white-space:nowrap;transition:color .15s,background .15s}
  .wknav .wklinks a:hover,.wknav .wkdev:hover{background:rgba(20,36,58,.055);color:var(--ink)}
  .wknav a:focus-visible{outline:2px solid var(--orange);outline-offset:1px}
  .wknav a[aria-current="page"]{color:var(--ink)}
  .wknav a[aria-current="page"]::after{content:"";position:absolute;left:10px;right:10px;bottom:0;
           height:2px;border-radius:2px;background:var(--orange)}
  .wkdev{flex:0 0 auto;display:inline-flex;align-items:center;gap:6px}
  .wkdev::before{content:"";position:absolute;left:-8px;top:9px;bottom:9px;width:1px;background:rgba(20,36,58,.14)}

  .wklang{flex:0 0 auto;display:flex;height:28px;overflow:hidden;margin-left:4px;
          background:var(--card);border:1px solid var(--line);border-radius:var(--r-ctl)}
  .wklang button{font:inherit;font-family:var(--disp);font-weight:600;font-size:11.5px;
                 padding:0 10px;border:0;background:transparent;color:var(--slate);cursor:pointer}
  .wklang button + button{border-left:1px solid var(--line)}
  .wklang button:hover{background:#EEF2F6;color:var(--navy)}
  .wklang button[aria-selected="true"]{background:var(--navy);color:#fff}
  .wklang button[aria-selected="true"]:hover{background:var(--navy);color:#fff}
  .wklang button:focus-visible{outline:2px solid var(--orange);outline-offset:-2px}

  @media (max-width:980px){.wknav-in{padding:0 22px}}
  @media (max-width:780px){.wkmark span{display:none}}
  @media print{.wknav,.wkskip,.wklang{display:none}}
</style>
"""

CHROME_JS = """
<script>
"use strict";
(function(){
  function read(){
    try{ return localStorage.getItem("aidp.lang")==="zh" ? "zh" : "en"; }
    catch(e){ return "en"; }
  }
  function paint(v){
    document.querySelectorAll(".wklang button").forEach(function(b){
      b.setAttribute("aria-selected", b.getAttribute("data-v")===v ? "true" : "false");
    });
  }
  function apply(v, silent){
    var r=document.documentElement;
    r.setAttribute("data-lang", v);
    r.setAttribute("lang", v==="zh" ? "zh-Hans" : "en");
    if(document.body) document.body.setAttribute("data-lang", v);
    try{ localStorage.setItem("aidp.lang", v); }catch(e){}
    paint(v);
    if(!silent){
      try{ document.dispatchEvent(new CustomEvent("aidp:lang", {detail:v})); }
      catch(e){}
    }
  }
  window.aidpSetLang = function(v){ apply(v==="zh"?"zh":"en", false); };
  apply(read(), true);
  document.addEventListener("click", function(e){
    var b=e.target && e.target.closest && e.target.closest(".wklang button");
    if(!b) return;
    apply(b.getAttribute("data-v"), false);
  });
  document.addEventListener("aidp:lang", function(e){
    if(e && e.detail) paint(e.detail==="zh"?"zh":"en");
  });
})();
</script>
"""

# href, English label, Chinese label
NAV_LINKS = [
    ("index.html",     "Overview",     "\u603b\u89c8"),
    ("flow.html",      "How it works", "\u6574\u4f53\u6d41\u7a0b"),
    ("lifecycle.html", "Step by step", "\u9010\u6b65\u6d41\u7a0b"),
    ("gate.html",      "RAG Gate",     "RAG \u95f8\u95e8"),
]
DEV = ("developer.html", "Developer portal", "\u5f00\u53d1\u8005\u95e8\u6237")


def nav(current):
    rows = []
    for href, en, zh in NAV_LINKS:
        cur = ' aria-current="page"' if href == current else ""
        rows.append(f'      <a href="{href}"{cur}><span class="wk-en">{en}</span>'
                    f'<span class="wk-zh">{zh}</span></a>')
    links = "\n".join(rows)
    dcur = ' aria-current="page"' if current == DEV[0] else ""
    return f"""
<a class="wkskip" href="#main"><span class="wk-en">Skip to content</span><span class="wk-zh">\u8df3\u5230\u6b63\u6587</span></a>
<nav class="wknav" aria-label="Project wiki">
  <div class="wknav-in">
    <a class="wkmark" href="index.html">
      <b>AI Data<i>+</i></b><span class="wk-en">project wiki</span><span class="wk-zh">\u9879\u76ee\u624b\u518c</span>
    </a>
    <span class="wkrule" aria-hidden="true"></span>
    <div class="wklinks">
{links}
    </div>
    <a class="wkdev" href="{DEV[0]}"{dcur}><span class="wk-en">{DEV[1]}</span><span class="wk-zh">{DEV[2]}</span></a>
    <div class="wklang" role="group" aria-label="Language">
      <button type="button" data-v="en" aria-selected="true">EN</button>
      <button type="button" data-v="zh" aria-selected="false">\u4e2d\u6587</button>
    </div>
  </div>
</nav>
"""


def block(current):
    return "\n" + OPEN + CHROME_CSS + nav(current) + CHROME_JS + CLOSE + "\n"


def apply(path, current):
    html = path.read_text(encoding="utf-8")
    fresh = block(current)
    if OPEN in html:
        start = html.index(OPEN)
        end = html.index(CLOSE, start) + len(CLOSE)
        # keep the newline handling identical whether we replace or insert
        html = html[:start].rstrip("\n") + fresh + html[end:].lstrip("\n")
    else:
        m = re.search(r"<body[^>]*>", html)
        if not m:
            raise SystemExit(f"{path.name}: no <body>")
        html = html[:m.end()] + fresh + html[m.end():]
    with open(path, "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(html)
    print(f"  {path.name}: bar applied (current = {current})")


PAGES = {
    "index.html":     "index.html",
    "flow.html":      "flow.html",
    "lifecycle.html": "lifecycle.html",
    "gate.html":      "gate.html",
    "developer.html": "developer.html",
    "manual.html":    "developer.html",
    "llm-api.html":   "developer.html",
}

if __name__ == "__main__":
    for name, current in PAGES.items():
        p = SITE / name
        if p.exists():
            apply(p, current)
        else:
            print(f"  {name}: not on disk yet, skipped")
    print("done")
