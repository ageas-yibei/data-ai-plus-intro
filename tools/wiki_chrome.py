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

  /* a group of pages under one name. The button rides in the strip; the panel
     hangs off .wknav rather than the strip, because the strip scrolls sideways
     and clips what overflows it - so the panel's left is set from the button,
     in JS. A browser with no JavaScript gets the plain links (.wkmenu-fb). */
  .wkmenu{flex:0 0 auto;display:inline-flex;align-items:center;position:static}
  .wkmenu-fb{display:none}
  .wknav .wkmenu-btn{position:relative;display:inline-flex;align-items:center;gap:6px;
           font:inherit;font-family:var(--disp);font-size:13px;font-weight:600;
           padding:7px 10px;border:0;border-radius:5px;background:transparent;color:var(--slate);
           white-space:nowrap;cursor:pointer;transition:color .15s,background .15s}
  .wknav .wkmenu-btn:hover,.wknav .wkmenu-btn[aria-expanded="true"]{background:rgba(20,36,58,.055);color:var(--ink)}
  .wknav .wkmenu-btn:focus-visible{outline:2px solid var(--orange);outline-offset:1px}
  .wknav .wkmenu-btn.wk-cur{color:var(--ink)}
  .wknav .wkmenu-btn.wk-cur::after{content:"";position:absolute;left:10px;right:10px;bottom:0;
           height:2px;border-radius:2px;background:var(--orange)}
  .wkcar{width:6px;height:6px;margin-top:-2px;opacity:.7;
         border-right:1.6px solid currentColor;border-bottom:1.6px solid currentColor;
         transform:rotate(45deg);transition:transform .18s}
  .wkmenu-btn[aria-expanded="true"] .wkcar{margin-top:1px;transform:rotate(-135deg)}

  .wkmenu-p{position:absolute;top:calc(100% + 5px);left:0;z-index:210;min-width:190px;padding:6px;
            background:var(--card);border:1px solid var(--line);border-radius:10px;
            box-shadow:0 14px 34px rgba(20,36,58,.14),0 2px 5px rgba(20,36,58,.06);
            opacity:0;transform:translateY(-4px);transition:opacity .14s,transform .14s}
  .wkmenu-p.wk-open{opacity:1;transform:none}
  .wkmenu-p[hidden]{display:none}
  .wknav .wkmenu-p a{display:block;padding:8px 11px;border-radius:6px;font-size:13px;
           font-weight:600;color:var(--ink);white-space:nowrap}
  .wknav .wkmenu-p a:hover{background:#EEF2F6;color:var(--ink)}
  .wknav .wkmenu-p a[aria-current="page"]{background:rgba(224,99,42,.09)}
  .wknav .wkmenu-p a[aria-current="page"]::after{display:none}
  @media (prefers-reduced-motion:reduce){.wkmenu-p,.wkcar{transition:none}}

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
(function(){
  var btn = document.getElementById("wkmenu-b"),
      panel = document.getElementById("wkmenu-p"),
      strip = document.querySelector(".wknav-in"),
      nav = document.querySelector(".wknav");
  if(!btn || !panel || !nav) return;

  function items(){ return Array.prototype.slice.call(panel.querySelectorAll("a")); }

  // The panel hangs off the bar, not off the strip the button sits in, so its
  // left is the button's - measured on open, because the strip can be scrolled.
  function place(){
    if(panel.hidden) return;
    var b = btn.getBoundingClientRect(), n = nav.getBoundingClientRect(),
        max = n.width - panel.offsetWidth - 8,
        x = b.left - n.left;
    if(x > max) x = max;
    if(x < 8) x = 8;
    panel.style.left = Math.round(x) + "px";
  }
  // on a narrow screen the strip scrolls sideways, and the button can be off
  // its own edge: a panel under a button nobody can see reads as a stray card.
  function reveal(){
    if(!strip) return;
    var b = btn.getBoundingClientRect(), s = strip.getBoundingClientRect();
    if(b.right > s.right) strip.scrollLeft += b.right - s.right + 10;
    else if(b.left < s.left) strip.scrollLeft -= s.left - b.left + 10;
  }
  function open_(toFirst){
    if(panel.hidden){
      panel.hidden = false;
      btn.setAttribute("aria-expanded", "true");
      reveal();
      place();
      void panel.offsetWidth;
      panel.classList.add("wk-open");
    }
    if(toFirst){ var it = items(); if(it[0]) it[0].focus(); }
  }
  function close_(toBtn){
    if(panel.hidden) return;
    panel.classList.remove("wk-open");
    panel.hidden = true;
    btn.setAttribute("aria-expanded", "false");
    if(toBtn) btn.focus();
  }

  btn.addEventListener("click", function(){ panel.hidden ? open_(false) : close_(false); });
  // in the CAPTURE phase: pages stop their own clicks from reaching the document
  // (a tooltip chip, a card), and an open panel must close under those too
  document.addEventListener("click", function(e){
    var t = e.target;
    if(!t || !t.closest) return;
    if(t.closest("#wkmenu-p") || t.closest("#wkmenu-b")) return;
    close_(false);
  }, true);
  // focus that leaves the pair closes it: Tab from the button, Shift+Tab off the
  // first link. Handled here rather than on the Tab key, which fires BEFORE the
  // browser has moved focus and would tear the panel down under it.
  nav.addEventListener("focusout", function(e){
    var to = e.relatedTarget;
    if(!to) return;                       // focus left the window: leave it be
    if(to === btn || panel.contains(to)) return;
    close_(false);
  });
  document.addEventListener("keydown", function(e){
    var k = e.key;
    if(k === "Escape" || k === "Esc"){
      // while the panel is open Escape is the menu's; closed, it is the page's
      if(!panel.hidden){
        e.preventDefault();
        if(e.stopImmediatePropagation) e.stopImmediatePropagation();
        close_(true);
      }
      return;
    }
    var onBtn = document.activeElement === btn,
        inPanel = !panel.hidden && panel.contains(document.activeElement);
    if(onBtn && (k === "ArrowDown" || k === "Down")){ e.preventDefault(); open_(true); return; }
    if(!inPanel) return;
    var it = items(), at = it.indexOf(document.activeElement), to = -1;
    if(k === "ArrowDown" || k === "Down") to = (at + 1) % it.length;
    else if(k === "ArrowUp" || k === "Up") to = (at - 1 + it.length) % it.length;
    else if(k === "Home") to = 0;
    else if(k === "End") to = it.length - 1;
    if(to > -1){ e.preventDefault(); it[to].focus(); }
  });
  window.addEventListener("resize", place);
  if(strip) strip.addEventListener("scroll", place);
  document.addEventListener("aidp:lang", place);   // every label in the bar changes width
})();
</script>
"""

KIT_OPEN = "<!-- wiki page kit · identical in every page that carries it: edit one, edit all -->"
KIT_CLOSE = "<!-- /wiki page kit -->"
NEXT_OPEN = "<!-- wiki next -->"
NEXT_CLOSE = "<!-- /wiki next -->"

# The Overview (index.html) sets the look of this wiki. The kit is that look,
# written down once, so the pages behind it read as the same site and not as
# three sites sharing a nav bar. index.html carries none of it: it IS the
# reference, and it declares the same palette for itself.
KIT_CSS = """
<style id="wk-kit">
  /* ---- AI Data+ page kit: the Overview's look, shared by the pages behind it ---- */
  :root{
    /* palette · the Overview's, to the byte */
    --navy:#13294B; --copy:#3A4A63; --mute:#8A97AA; --line:#D3DEEA; --sky:#EAF2F8;
    /* line-2 is the border a card takes when it lifts; sky-2 a row under the pointer */
    --line-2:#C3D0DD; --mute-2:#C8D3E0; --sky-2:#F6F9FC;
    /* every -ink is the readable version of its colour: 4.5:1 on white AND on its own
       wash, so a label may sit on either without a second decision */
    --orange:#E8752A; --orange-2:#F1A26C; --orange-3:#FCE9DC; --orange-ink:#A34A14;
    --purple:#6B2C91; --purple-2:#EFE6F5; --purple-ink:#6B2C91;
    --green:#2E9E6B;  --green-2:#E3F4EB;  --green-ink:#1F7A45;
    --blue-ink:#355F91;
    --amber:#C9922B;  --amber-2:#FBF0DA; --amber-ink:#8A6410;
    --halt:#C8443A;   --halt-2:#F8E3E1;  --halt-ink:#A8382F;
    --paper:#FFFFFF;  --card:#FFFFFF;
    /* surfaces · one card, one lift, everywhere */
    --sh-1:0 1px 2px rgba(19,41,75,.05);
    --sh-2:0 12px 30px rgba(19,41,75,.08);
    --sh-3:0 18px 44px rgba(19,41,75,.14);
    --r-ctl:6px; --r-card:14px; --r-lg:18px;
    /* type scale · one ladder, every page */
    --t-h1:clamp(32px,4.2vw,54px);
    --t-h2:clamp(21px,2.1vw,27px);
    --t-h3:19px;
    --t-body:15.5px;
    --t-lede:17px;
    --wkw:860px;              /* the reading column; a chart page overrides it */
    --pad-x:40px;
  }
  :focus-visible{outline:2px solid var(--orange);outline-offset:2px}

  /* the ground: two soft washes and a dot grid, exactly as the Overview draws them */
  .wkbg{position:fixed;inset:0;z-index:-1;pointer-events:none;overflow:hidden}
  .wkbg i{position:absolute;width:64vmax;height:64vmax;border-radius:50%;
          filter:blur(100px);opacity:.34;animation:wkdrift 22s ease-in-out infinite}
  .wkbg i:nth-child(1){left:-24vmax;top:-18vmax;background:var(--orange-3)}
  .wkbg i:nth-child(2){right:-28vmax;bottom:-26vmax;background:var(--sky);animation-delay:-11s}
  .wkbg:after{content:"";position:absolute;inset:0;opacity:.05;
          background-image:radial-gradient(#13294B .9px,transparent 1px);background-size:30px 30px}
  @keyframes wkdrift{0%,100%{margin-left:0;margin-top:0}50%{margin-left:3vw;margin-top:2vh}}
  @media (prefers-reduced-motion:reduce){.wkbg i{animation:none}}
  @media print{.wkbg{display:none}}

  /* the page head: eyebrow, title, lede, and whatever controls the page owns */
  .wkhead{display:flex;align-items:flex-end;justify-content:space-between;gap:16px 32px;
          flex-wrap:wrap;padding:34px 0 20px;margin:0 0 24px;border-bottom:1px solid var(--line)}
  .wkhead-t{flex:1 1 420px;min-width:0}
  .wkhead-a{flex:0 0 auto;display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding-bottom:4px}
  .wkey{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.14em;
        color:var(--purple);margin:0 0 11px}
  .wkhead h1{font-family:var(--disp);font-weight:800;color:var(--navy);font-size:var(--t-h1);
             line-height:1.02;letter-spacing:-.032em;margin:0;text-wrap:balance}
  .wklede{font-size:var(--t-lede);line-height:1.55;color:var(--copy);margin:14px 0 0;
          max-width:58ch;text-wrap:pretty}
  /* a page whose own toolbar sits right below the title draws no rule under it */
  .wkhead.wk-bare{border-bottom:0;padding-bottom:10px;margin-bottom:12px}

  /* section heads, one size on every page */
  .wkh2{font-family:var(--disp);font-weight:800;font-size:var(--t-h2);letter-spacing:-.022em;
        color:var(--navy);margin:44px 0 6px;text-wrap:balance}
  .wkh3{font-family:var(--disp);font-weight:700;font-size:var(--t-h3);letter-spacing:-.02em;
        color:var(--navy);margin:0}
  .wksub{font-size:15px;line-height:1.5;color:var(--copy);margin:0 0 16px;max-width:58ch;
         text-wrap:pretty}

  /* one card, one lift. A page adds its own edge or band on top of these. */
  .wkcard{background:var(--card);border:1px solid var(--line);border-radius:var(--r-card);
          box-shadow:var(--sh-1)}
  .wkcard-lift{transition:transform .18s cubic-bezier(.2,.7,.2,1),box-shadow .18s,border-color .18s}
  .wkcard-lift:hover{transform:translateY(-2px);border-color:var(--line-2);box-shadow:var(--sh-2)}
  @media (prefers-reduced-motion:reduce){.wkcard-lift{transition:none}
    .wkcard-lift:hover{transform:none}}

  /* keep reading: the Overview's contents cards, minus the page you are on */
  .wknext{margin:60px 0 0;padding:28px 0 0;border-top:1px solid var(--line)}
  .wknext-h{font-family:var(--disp);font-weight:800;font-size:var(--t-h2);letter-spacing:-.022em;
            color:var(--navy);margin:0 0 6px}
  .wknext-s{font-size:15px;line-height:1.5;color:var(--copy);margin:0 0 20px;max-width:52ch}
  .wknext-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;
            max-width:var(--wkw);margin:0}
  .wknext-c{position:relative;display:block;padding:18px 20px 20px;background:var(--card);
            border:1px solid var(--line);border-radius:var(--r-card);box-shadow:var(--sh-1);
            text-decoration:none;color:inherit;
            transition:transform .18s cubic-bezier(.2,.7,.2,1),box-shadow .18s,border-color .18s}
  .wknext-c:hover{transform:translateY(-2px);border-color:var(--line-2);box-shadow:var(--sh-2)}
  .wknext-c b{display:block;font-family:var(--disp);font-weight:700;font-size:18px;line-height:1.2;
              letter-spacing:-.02em;color:var(--navy);margin:0 0 6px;padding-right:20px}
  .wknext-d{display:block;font-size:13.5px;line-height:1.5;color:var(--copy);text-wrap:pretty}
  .wknext-go{position:absolute;right:18px;top:16px;font-size:15px;color:var(--mute-2);
             transition:color .18s,transform .18s}
  .wknext-c:hover .wknext-go{color:var(--orange);transform:translateX(2px)}
  @media (prefers-reduced-motion:reduce){.wknext-c,.wknext-go{transition:none}}
  @media print{.wknext{display:none}}

  /* the last line on every page, said the same way */
  .wkfoot{margin:36px 0 0;padding:14px 0 0;border-top:1px solid var(--line);
          font-family:var(--mono);font-size:11px;letter-spacing:.03em;color:var(--mute);
          display:flex;gap:18px;flex-wrap:wrap}
  .wkfoot a{color:var(--orange-ink);text-decoration:none}
  .wkfoot a:hover{text-decoration:underline}

  html[lang^="zh"] .wkhead h1{font-size:clamp(28px,3.6vw,46px);line-height:1.2;letter-spacing:.01em}
  html[lang^="zh"] .wkey{letter-spacing:.08em}
  html[lang^="zh"] .wklede,html[lang^="zh"] .wknext-s,html[lang^="zh"] .wknext-d{line-height:1.75}
  html[lang^="zh"] .wknext-h{letter-spacing:0;line-height:1.35}

  @media (max-width:980px){
    .wkhead{padding-top:26px}
    .wknext-g{grid-template-columns:1fr}
  }
</style>
<div class="wkbg" aria-hidden="true"><i></i><i></i></div>
"""

# href, English name, Chinese name, English line, Chinese line
NEXT_CARDS = [
    ("index.html", "Overview", "总览",
     "One submission, from the pack that arrives to the data the underwriter reads.",
     "一份申请：从收到的材料包，"
     "到核保人读到的数据。"),
    ("flow.html", "How it works", "整体流程",
     "The whole programme in four pictures, then the process stage by stage.",
     "先用四张图看懂整个项目，"
     "再按阶段展开流程。"),
    ("lifecycle.html", "Step by step", "逐步流程",
     "Seven steps: who runs each one, who signs it off, and every outcome it can have.",
     "七个步骤：每步由谁执行、由谁签核，"
     "可能出现哪些结果。"),
    ("rules.html", "The rules", "分拣规则",
     "What the machine looks at when it decides what each file is — folder, name, type, content.",
     "机器判定每份文件时到底看什么——"
     "位置、文件名、格式、内容。"),
    ("gate.html", "RAG Gate", "RAG 闸门",
     "Red, amber, green — every rule that decides how much attention a treaty needs.",
     "红、黄、绿——决定一份合约"
     "需要多少人工的每一条规则。"),
]

# href, English label, Chinese label
NAV_LINKS = [
    ("index.html",     "Overview",     "\u603b\u89c8"),
    ("flow.html",      "How it works", "\u6574\u4f53\u6d41\u7a0b"),
    ("lifecycle.html", "Step by step", "\u9010\u6b65\u6d41\u7a0b"),
]

# The two pages that are about one thing - what the Submission Agent decides,
# and how much attention its result needs - sit under its name rather than
# beside the pages about the programme. English, Chinese, then the contents.
MENU = ("Submission Agent", "\u6587\u4ef6\u5206\u62e3\u667a\u80fd\u4f53", [
    ("rules.html", "The rules", "\u5206\u62e3\u89c4\u5219"),
    ("gate.html",  "RAG Gate",  "RAG \u95f8\u95e8"),
])
DEV = ("developer.html", "Developer portal", "\u5f00\u53d1\u8005\u95e8\u6237")


def pair(en, zh):
    return f'<span class="wk-en">{en}</span><span class="wk-zh">{zh}</span>'


def nav(current):
    rows = []
    for href, en, zh in NAV_LINKS:
        cur = ' aria-current="page"' if href == current else ""
        rows.append(f'      <a href="{href}"{cur}>{pair(en, zh)}</a>')

    # the grouped pages: a button in the strip, a panel that hangs off the bar
    # below it, and the same links in plain sight where there is no JavaScript
    men, mzh, contents = MENU
    inside = any(href == current for href, _, _ in contents)
    mcur = " wk-cur" if inside else ""
    # the link that carries aria-current is inside a closed panel, so the button
    # says it too - "true" and not "page", because the button is not the page
    mnow = ' aria-current="true"' if inside else ""
    rooms, fallback = [], []
    for href, en, zh in contents:
        cur = ' aria-current="page"' if href == current else ""
        rooms.append(f'          <a href="{href}"{cur}>{pair(en, zh)}</a>')
        fallback.append(f'<a href="{href}"{cur}>{pair(en, zh)}</a>')
    menu = "\n".join(rooms)
    rows.append(
        f'      <span class="wkmenu"><button class="wkmenu-btn{mcur}"{mnow} type="button"'
        f' id="wkmenu-b" aria-expanded="false" aria-controls="wkmenu-p">{pair(men, mzh)}'
        f'<span class="wkcar" aria-hidden="true"></span></button>\n'
        f'        <div class="wkmenu-p" id="wkmenu-p" hidden>\n{menu}\n'
        f'        </div></span>')
    rows.append(f'      <span class="wkmenu-fb">{"".join(fallback)}</span>')
    rows.append('      <noscript><style>.wkmenu{display:none}'
                '.wkmenu-fb{display:contents}</style></noscript>')
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


# This site is shared by link, not offered to a search engine. robots.txt deliberately
# ALLOWS crawling, because a crawler has to fetch the page to read this tag — so the tag
# is the thing that actually keeps a page out of the index, and a page without it is the
# one page that gets indexed. The manual is a copy regenerated elsewhere and lost its
# tag exactly that way, so the script owns it now rather than trusting a hand-edit.
ROBOTS = '<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">'


def robots(html, name):
    if 'name="robots"' in html:
        return html
    m = re.search(r'<meta name="viewport"[^>]*>', html)
    if not m:
        raise SystemExit(f"{name}: no viewport meta to sit under")
    print(f"  {name}: noindex tag restored")
    return html[:m.end()] + "\n" + ROBOTS + html[m.end():]


def apply(path, current):
    html = robots(path.read_text(encoding="utf-8"), path.name)
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


def nxt(current):
    """The wiki pages this one is not, as cards."""
    cards = []
    for href, en, zh, den, dzh in NEXT_CARDS:
        if href == current:
            continue
        cards.append(
            f'    <a class="wknext-c" href="{href}">\n'
            f'      <b><span class="wk-en">{en}</span><span class="wk-zh">{zh}</span></b>\n'
            f'      <span class="wknext-d"><span class="wk-en">{den}</span>'
            f'<span class="wk-zh">{dzh}</span></span>\n'
            f'      <span class="wknext-go" aria-hidden="true">→</span>\n'
            f'    </a>')
    body = "\n".join(cards)
    return f"""{NEXT_OPEN}
<nav class="wknext" aria-labelledby="wknext-h">
  <h2 class="wknext-h" id="wknext-h"><span class="wk-en">Keep reading</span><span class="wk-zh">继续阅读</span></h2>
  <p class="wknext-s"><span class="wk-en">The rest of the wiki, one page at a time.</span><span class="wk-zh">手册的其余部分，一页一页看。</span></p>
  <div class="wknext-g">
{body}
  </div>
</nav>
{NEXT_CLOSE}"""


def apply_kit(path, current):
    """The shared look, and the cards that point at the rest of the wiki.

    The kit goes directly below the chrome, so its tokens win over whatever the
    page declared in its own <head>. `Keep reading` goes directly above the
    page's own <footer>.
    """
    html = path.read_text(encoding="utf-8")

    fresh = "\n" + KIT_OPEN + KIT_CSS + KIT_CLOSE + "\n"
    if KIT_OPEN in html:
        start = html.index(KIT_OPEN)
        end = html.index(KIT_CLOSE, start) + len(KIT_CLOSE)
        html = html[:start].rstrip("\n") + fresh + html[end:].lstrip("\n")
    else:
        anchor = html.index(CLOSE) + len(CLOSE)
        html = html[:anchor] + fresh.rstrip("\n") + html[anchor:]

    block = nxt(current)
    if NEXT_OPEN in html:
        start = html.index(NEXT_OPEN)
        end = html.index(NEXT_CLOSE, start) + len(NEXT_CLOSE)
        html = html[:start] + block + html[end:]
    else:
        m = re.search(r"\n([ \t]*)<footer", html)
        if not m:
            raise SystemExit(f"{path.name}: no <footer> for `Keep reading` to sit above")
        pad = m.group(1)
        indented = "\n".join(pad + ln if ln else ln for ln in block.split("\n"))
        html = html[:m.start()] + "\n" + indented + html[m.start():]

    with open(path, "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(html)
    print(f"  {path.name}: page kit applied")


PAGES = {
    "index.html":     "index.html",
    "flow.html":      "flow.html",
    "lifecycle.html": "lifecycle.html",
    "rules.html":     "rules.html",
    "gate.html":      "gate.html",
    "developer.html": "developer.html",
    "manual.html":    "developer.html",
    "llm-api.html":   "developer.html",
}

# The Overview is the reference, so it carries no kit; the developer portal is
# its own room and is left alone.
KIT_PAGES = ["flow.html", "lifecycle.html", "rules.html", "gate.html"]

if __name__ == "__main__":
    for name, current in PAGES.items():
        p = SITE / name
        if p.exists():
            apply(p, current)
        else:
            print(f"  {name}: not on disk yet, skipped")
    for name in KIT_PAGES:
        p = SITE / name
        if p.exists():
            apply_kit(p, name)
    print("done")
