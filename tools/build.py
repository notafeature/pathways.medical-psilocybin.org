#!/usr/bin/env python3
"""Stamp the shared header, footer, and counter beacon into every page in public/.

Each page carries three marker pairs (header, footer, counter); whatever sits between
them is replaced from public/_chrome.html and from the BEACON below. A page may also
carry a subnav pair, filled from the _subnav.html in its own folder. Every root-absolute
link must resolve to a file under public/ (a trailing slash means index.html, no
extension means .html). Run after editing a page or the chrome:

    python3 tools/build.py          # rewrite
    python3 tools/build.py --check  # exit 1 if any page is out of date

The beacon is the same one every rules page carries (tools/sync-count.py in the
rules repository); the counter's ALLOWED_ORIGINS names this host.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
ENDPOINT = "https://count.medical-psilocybin.org"

BEACON = """<script id="countjs">
(function(){
  var E="__ENDPOINT__";
  if(!E) return;
  var nav=navigator;
  if(nav.globalPrivacyControl===true||nav.doNotTrack==="1"||window.doNotTrack==="1") return;
  if(location.protocol==="file:"||location.hostname==="localhost"||location.hostname==="127.0.0.1") return;
  function send(k,p){
    var body=JSON.stringify({k:k,p:p,r:document.referrer||""});
    try{ if(nav.sendBeacon&&nav.sendBeacon(E+"/e",new Blob([body],{type:"text/plain;charset=UTF-8"}))) return; }catch(e){}
    try{ if(window.fetch){ fetch(E+"/e",{method:"POST",body:body,mode:"cors",keepalive:true,headers:{"Content-Type":"text/plain;charset=UTF-8"}}).catch(function(){}); return; } }catch(e){}
    new Image().src=E+"/px?p="+encodeURIComponent(p)+"&r="+encodeURIComponent(document.referrer||"");
  }
  send("pv",location.pathname);
  document.addEventListener("click",function(e){
    var a=e.target&&e.target.closest&&e.target.closest('a[href$=".pdf"]');
    if(a) send("dl",a.getAttribute("href"));
  },true);
})();
</script>""".replace("__ENDPOINT__", ENDPOINT)


def block(src, name):
    m = re.search(rf"<!-- {name} -->\n(.*?)\n<!-- /{name} -->", src, re.S)
    return m.group(1)


def main():
    check = "--check" in sys.argv
    chrome = open(os.path.join(PUB, "_chrome.html")).read()
    shared = {"header": block(chrome, "header"), "footer": block(chrome, "footer"), "counter": BEACON}
    stale = []
    bad_links = []
    for path in sorted(glob.glob(os.path.join(PUB, "**", "*.html"), recursive=True)):
        if os.path.basename(path).startswith("_"):
            continue
        src = open(path).read()
        new = src
        parts = dict(shared)
        # a folder's _subnav.html is stamped into pages that carry the subnav markers
        subnav = os.path.join(os.path.dirname(path), "_subnav.html")
        if "<!-- subnav -->" in src:
            if not os.path.exists(subnav):
                print(f"NO SUBNAV  {os.path.relpath(path, PUB)}: markers without {os.path.relpath(subnav, PUB)}")
                return 1
            parts["subnav"] = block(open(subnav).read(), "subnav")
        for name, body in parts.items():
            # an empty pair (marker, newline, closing marker) is the fresh state
            pat = re.compile(rf"<!-- {name} -->\n(?:.*?\n)?<!-- /{name} -->", re.S)
            if not pat.search(new):
                print(f"NO MARKER  {os.path.basename(path)}: {name}")
                return 1
            new = pat.sub(lambda m: f"<!-- {name} -->\n{body}\n<!-- /{name} -->", new, count=1)
        for href in re.findall(r'href="(/[^"#?]*)', new):
            target = os.path.join(PUB, href.lstrip("/"))
            if href.endswith("/"):
                target = os.path.join(target, "index.html")
            elif not os.path.splitext(href)[1]:
                target += ".html"
            if not os.path.exists(target):
                bad_links.append(f"{os.path.relpath(path, PUB)} -> {href}")
        if chr(8212) in new:
            print(f"EM DASH    {os.path.basename(path)}")
            return 1
        if new != src:
            stale.append(os.path.basename(path))
            if not check:
                open(path, "w").write(new)
    if bad_links:
        print("links to nothing:\n  " + "\n  ".join(bad_links))
        return 1
    if check and stale:
        print("out of date: " + ", ".join(stale))
        return 1
    count = len([p for p in glob.glob(os.path.join(PUB, "**", "*.html"), recursive=True) if not os.path.basename(p).startswith("_")])
    print(f"{'checked' if check else 'stamped'} {count} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
