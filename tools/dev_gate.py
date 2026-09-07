# The developer portal's password gate: one definition, applied to the three
# pages behind it.
#
#   python tools/dev_gate.py --password <the password>
#
# The password is an argument, never a line in this file: this file is
# committed, and a password in a committed file is a published password.
# Pass the current one to re-apply the gate unchanged, a new one to change it.
#
# The password itself is NOT in the pages. What is stored is a salted digest:
# sha256 of (salt + password), re-hashed with the salt 20,000 times. The page
# hashes what is typed the same way and compares. Getting the digest back to a
# password means guessing passwords.
#
# What this is: a lock on the door of the developer section, so a link shared
# with the wrong person does not open it. What it is NOT: encryption. The page
# body is still in the file, and anyone who reads the source can read it. Keep
# real secrets (API keys) out of these pages regardless - llm-api.html says
# "see the internal note" wherever a key belongs, and that is the actual
# protection.
import hashlib
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent   # the site is the folder above this one
PAGES = ["developer.html", "manual.html", "llm-api.html"]

SALT = "a7f3c1e95b2d84061cf7e8b34d2a9105"   # not a secret; it makes the digest specific to this site
ROUNDS = 20000

OPEN = "<!-- developer gate \u00b7 identical in every page behind it: edit one, edit all -->"
CLOSE = "<!-- /developer gate -->"


def digest(password):
    d = hashlib.sha256((SALT + password).encode("utf-8")).hexdigest()
    for _ in range(ROUNDS - 1):
        d = hashlib.sha256((d + SALT).encode("utf-8")).hexdigest()
    return d


# ---- SHA-256 tables, generated rather than typed: no room for a wrong constant
def _roots(n, power):
    out, p, i = [], [], 2
    while len(p) < n:
        if all(i % q for q in p):
            p.append(i)
        i += 1
    for prime in p:
        frac = prime ** (1.0 / power) % 1
        out.append(int(frac * (1 << 32)))
    return out


def _js_words(vals):
    return ",".join("0x%08x" % v for v in vals)


def gate_block(password):
    css = """
<style id="wk-gate">
  html.wk-locked{overflow:hidden}
  html.wk-locked body > *:not(.wknav):not(.wklock):not(style):not(script){display:none !important}
  html:not(.wk-locked) .wklock{display:none}
  .wklock{position:fixed;left:0;right:0;top:46px;bottom:0;z-index:150;display:flex;
          align-items:flex-start;justify-content:center;background:#F5F7FA;
          font-family:"Aptos Display","Segoe UI Variable Display","Segoe UI","Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif}
  .wklock-in{width:min(430px,calc(100vw - 44px));margin-top:min(16vh,140px);background:#fff;
             border:1px solid #DCE3EA;border-radius:14px;padding:30px 32px 28px;
             box-shadow:0 18px 44px rgba(20,36,58,.10)}
  .wklock .ic{width:34px;height:34px;color:#E0632A;margin-bottom:16px}
  .wklock .ic svg{width:100%;height:100%;display:block}
  .wklock h2{font-size:23px;line-height:1.15;letter-spacing:-.022em;color:#1C3557;margin:0 0 8px;font-weight:700}
  .wklock p{margin:0 0 20px;font-size:14px;line-height:1.5;color:#5B6B7F;
            font-family:"Aptos","Segoe UI Variable Text","Segoe UI","Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif}
  .wklock form{display:flex;gap:8px}
  .wklock input{flex:1 1 auto;min-width:0;height:40px;padding:0 13px;font:inherit;font-size:14px;
                font-family:ui-monospace,"Cascadia Mono",Consolas,monospace;letter-spacing:.08em;
                color:#14243A;background:#F8FAFC;border:1px solid #DCE3EA;border-radius:7px}
  .wklock input:focus{outline:0;border-color:#E0632A;background:#fff;box-shadow:0 0 0 3px rgba(224,99,42,.14)}
  .wklock button{flex:0 0 auto;height:40px;padding:0 18px;font:inherit;font-weight:600;font-size:14px;
                 color:#fff;background:#1C3557;border:0;border-radius:7px;cursor:pointer}
  .wklock button:hover{background:#14243A}
  .wklock button:focus-visible{outline:2px solid #E0632A;outline-offset:2px}
  .wklock .msg{margin:14px 0 0;min-height:18px;font-size:13px;color:#B44538;font-weight:600}
  .wklock .msg:empty{margin:0}
  .wklock .back{margin:22px 0 0;font-size:12.5px;color:#8D9BAB}
  .wklock .back a{color:#E0632A;text-decoration:none}
  .wklock .back a:hover{text-decoration:underline}
  .wklock-in.no{animation:wkshake .4s}
  @keyframes wkshake{25%{transform:translateX(-6px)}50%{transform:translateX(6px)}75%{transform:translateX(-3px)}}
  @media (prefers-reduced-motion:reduce){.wklock-in.no{animation:none}}
  /* a locked page prints as nothing: the point of the lock is that the content is not shown */
  @media print{.wklock{display:none}}
</style>
"""
    html = """
<div class="wklock" role="dialog" aria-modal="true" aria-labelledby="wklock-h">
  <div class="wklock-in" id="wklock-card">
    <div class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10.5" width="16" height="10.5" rx="2.4"/><path d="M8 10.5V7.2a4 4 0 0 1 8 0v3.3"/><path d="M12 14.6v2.4"/></svg></div>
    <h2 id="wklock-h"><span class="wk-en">Developer portal</span><span class="wk-zh">\u5f00\u53d1\u8005\u95e8\u6237</span></h2>
    <p>
      <span class="wk-en">This part of the wiki is for the project team. Ask Yibei for the password.</span>
      <span class="wk-zh">\u672c\u7ad9\u8fd9\u4e00\u90e8\u5206\u9762\u5411\u9879\u76ee\u56e2\u961f\u3002\u5bc6\u7801\u8bf7\u5411 Yibei \u7d22\u53d6\u3002</span>
    </p>
    <form id="wklock-f" autocomplete="off">
      <input type="password" id="wklock-i" aria-label="Password" autocomplete="current-password" spellcheck="false">
      <button type="submit"><span class="wk-en">Unlock</span><span class="wk-zh">\u89e3\u9501</span></button>
    </form>
    <p class="msg" id="wklock-m" role="alert"></p>
    <p class="back">
      <span class="wk-en">The rest of the wiki needs no password \u2014 <a href="index.html">back to the overview</a>.</span>
      <span class="wk-zh">\u672c\u7ad9\u5176\u4f59\u9875\u9762\u65e0\u9700\u5bc6\u7801 \u2014 <a href="index.html">\u8fd4\u56de\u603b\u89c8</a>\u3002</span>
    </p>
  </div>
</div>
"""
    js = """
<script>
"use strict";
/* The password is not in this file. Only the digest below is, and it is the
   result of hashing the password with the salt 20,000 times. */
(function(){
  var SALT="__SALT__", ROUNDS=__ROUNDS__, WANT="__DIGEST__", ROOT=document.documentElement;
  var K=[__K__];
  function sha256(str){
    var H=[__H__];
    var b=[],i,c,cp;
    for(i=0;i<str.length;i++){
      c=str.charCodeAt(i);
      if(c<0x80){b.push(c);}
      else if(c<0x800){b.push(0xc0|(c>>6),0x80|(c&63));}
      else if(c<0xd800||c>=0xe000){b.push(0xe0|(c>>12),0x80|((c>>6)&63),0x80|(c&63));}
      else{i++;cp=0x10000+(((c&0x3ff)<<10)|(str.charCodeAt(i)&0x3ff));
           b.push(0xf0|(cp>>18),0x80|((cp>>12)&63),0x80|((cp>>6)&63),0x80|(cp&63));}
    }
    var bits=b.length*8;
    b.push(0x80);
    while(b.length%64!==56){b.push(0);}
    b.push(0,0,0,0,(bits>>>24)&255,(bits>>>16)&255,(bits>>>8)&255,bits&255);
    function rr(n,x){return (x>>>n)|(x<<(32-n));}
    var w=new Array(64),j,t,a,bb,cc,d,e,f,g,h,s0,s1,S0,S1,ch,mj,t1,t2;
    for(j=0;j<b.length;j+=64){
      for(t=0;t<16;t++){w[t]=(b[j+4*t]<<24)|(b[j+4*t+1]<<16)|(b[j+4*t+2]<<8)|b[j+4*t+3];}
      for(t=16;t<64;t++){
        s0=rr(7,w[t-15])^rr(18,w[t-15])^(w[t-15]>>>3);
        s1=rr(17,w[t-2])^rr(19,w[t-2])^(w[t-2]>>>10);
        w[t]=(w[t-16]+s0+w[t-7]+s1)|0;
      }
      a=H[0];bb=H[1];cc=H[2];d=H[3];e=H[4];f=H[5];g=H[6];h=H[7];
      for(t=0;t<64;t++){
        S1=rr(6,e)^rr(11,e)^rr(25,e);
        ch=(e&f)^((~e)&g);
        t1=(h+S1+ch+K[t]+w[t])|0;
        S0=rr(2,a)^rr(13,a)^rr(22,a);
        mj=(a&bb)^(a&cc)^(bb&cc);
        t2=(S0+mj)|0;
        h=g;g=f;f=e;e=(d+t1)|0;d=cc;cc=bb;bb=a;a=(t1+t2)|0;
      }
      H[0]=(H[0]+a)|0;H[1]=(H[1]+bb)|0;H[2]=(H[2]+cc)|0;H[3]=(H[3]+d)|0;
      H[4]=(H[4]+e)|0;H[5]=(H[5]+f)|0;H[6]=(H[6]+g)|0;H[7]=(H[7]+h)|0;
    }
    var out="";
    for(var k=0;k<8;k++){out+=("00000000"+(H[k]>>>0).toString(16)).slice(-8);}
    return out;
  }
  function stretch(pw){
    var d=sha256(SALT+pw);
    for(var i=1;i<ROUNDS;i++){d=sha256(d+SALT);}
    return d;
  }
  function remembered(){
    try{return window.sessionStorage.getItem("aidp.dev");}catch(e){return null;}
  }
  function open_(){
    ROOT.classList.remove("wk-locked");
    try{window.sessionStorage.setItem("aidp.dev",WANT);}catch(e){}
  }
  if(remembered()===WANT){ROOT.classList.remove("wk-locked");}
  document.addEventListener("DOMContentLoaded",function(){
    var f=document.getElementById("wklock-f"),
        i=document.getElementById("wklock-i"),
        m=document.getElementById("wklock-m"),
        card=document.getElementById("wklock-card");
    if(!f) return;
    if(ROOT.classList.contains("wk-locked")) i.focus();
    f.addEventListener("submit",function(ev){
      ev.preventDefault();
      var zh=ROOT.getAttribute("data-lang")==="zh"||/^zh/.test(ROOT.getAttribute("lang")||"");
      m.textContent=zh?"\u6b63\u5728\u6838\u5bf9\u2026":"Checking\u2026";
      window.setTimeout(function(){
        if(stretch(i.value)===WANT){
          m.textContent="";
          open_();
        }else{
          m.textContent=zh?"\u5bc6\u7801\u4e0d\u5bf9\u3002":"That is not the password.";
          i.value="";i.focus();
          card.classList.remove("no");void card.offsetWidth;card.classList.add("no");
        }
      },10);
    });
  });
})();
</script>
"""
    js = (js.replace("__SALT__", SALT)
            .replace("__ROUNDS__", str(ROUNDS))
            .replace("__DIGEST__", digest(password))
            .replace("__K__", _js_words(_roots(64, 3)))
            .replace("__H__", _js_words(_roots(8, 2))))
    return "\n" + OPEN + css + html + js + CLOSE + "\n"


def apply(path, password):
    html = path.read_text(encoding="utf-8")

    # 1. the page starts locked, so a browser with no JS shows nothing either
    m = re.search(r"<html\b[^>]*>", html)
    tag = m.group(0)
    if "wk-locked" not in tag:
        if 'class="' in tag:
            new = tag.replace('class="', 'class="wk-locked ', 1)
        else:
            new = tag[:-1] + ' class="wk-locked">'
        html = html[:m.start()] + new + html[m.end():]

    # 2. the gate itself, after the wiki chrome
    fresh = gate_block(password)
    if OPEN in html:
        s = html.index(OPEN)
        e = html.index(CLOSE, s) + len(CLOSE)
        html = html[:s].rstrip("\n") + fresh + html[e:].lstrip("\n")
    else:
        anchor = "<!-- /wiki chrome -->"
        at = html.index(anchor) + len(anchor)
        html = html[:at] + fresh + html[at:]

    with open(path, "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(html)
    print(f"  {path.name}: gated")


if __name__ == "__main__":
    if "--password" not in sys.argv:
        raise SystemExit("usage: python tools/dev_gate.py --password <the password>")
    pw = sys.argv[sys.argv.index("--password") + 1]
    print(f"  digest: {digest(pw)}")
    for name in PAGES:
        apply(SITE / name, pw)
    print("done")
