#!/usr/bin/env python3
"""Checks the static site before a push: every local link, image and anchor resolves, each page has one h1, a unique title
(<= 60) and description (<= 160), a self-referencing canonical, Open Graph + Twitter tags, valid JSON-LD, and that sitemap.xml
lists exactly the pages. Run:  python3 tools/check_site.py     (exit code 1 when something is wrong)"""
import json, pathlib, re, sys, xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlparse, urldefrag

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://zohara-website.onrender.com"
bad = []


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.ids = set(); s.refs = []; s.meta = {}; s.links = []; s.h = []; s.title = ""; s._t = False; s.ld = []; s._ld = False
    def handle_starttag(s, tag, a):
        a = dict(a)
        if a.get("id"): s.ids.add(a["id"])
        if tag == "a" and a.get("href"): s.refs.append(a["href"])
        if tag in ("img", "script") and a.get("src"): s.refs.append(a["src"])
        if tag == "link" and a.get("href"): s.refs.append(a["href"]); s.links.append(a)
        if tag == "meta": s.meta[a.get("name") or a.get("property") or ""] = a.get("content", "")
        if re.fullmatch(r"h[1-6]", tag): s.h.append(int(tag[1]))
        if tag == "img" and "alt" not in a: bad.append(f"img without alt: {a.get('src')}")
        if tag == "title": s._t = True
        if tag == "script" and a.get("type") == "application/ld+json": s._ld = True
    def handle_endtag(s, tag):
        if tag == "title": s._t = False
        if tag == "script": s._ld = False
    def handle_data(s, d):
        if s._t: s.title += d
        if s._ld: s.ld.append(d)


pages = sorted(p for p in ROOT.glob("*.html") if not p.name.startswith("google"))
parsed = {p.name: P() for p in pages}
for p in pages: parsed[p.name].feed(p.read_text(encoding="utf-8"))
titles, descs = {}, {}
for p in pages:
    n, d = p.name, parsed[p.name]
    for r in d.refs:
        u = urlparse(r)
        if u.scheme in ("mailto", "tel", "javascript") or r.startswith("data:"): continue
        if u.scheme == "http": bad.append(f"{n}: insecure link {r}")
        if u.scheme == "https":
            if u.netloc != "zohara-website.onrender.com": continue
            path = u.path.lstrip("/") or "index.html"
        else:
            path = u.path or n
        if path in ("", "./"): path = "index.html"
        if path.endswith("/"): path += "index.html"
        f = ROOT / path
        if not f.exists(): bad.append(f"{n}: broken link {r}"); continue
        if u.fragment and f.suffix == ".html" and f.name in parsed and u.fragment not in parsed[f.name].ids:
            bad.append(f"{n}: missing anchor {r}")
    if n == "404.html":
        if "noindex" not in d.meta.get("robots", ""): bad.append("404 must be noindex")
        continue
    t, desc = d.title.strip(), d.meta.get("description", "")
    if len(t) > 60 or not t: bad.append(f"{n}: title length {len(t)}")
    if len(desc) > 160 or not desc: bad.append(f"{n}: description length {len(desc)}")
    titles.setdefault(t, []).append(n); descs.setdefault(desc, []).append(n)
    if d.h.count(1) != 1: bad.append(f"{n}: {d.h.count(1)} h1")
    for a, b in zip(d.h, d.h[1:]):
        if b > a + 1: bad.append(f"{n}: heading jumps h{a} -> h{b}")
    want = SITE + "/" + ("" if n == "index.html" else n)
    can = [l["href"] for l in d.links if l.get("rel") == "canonical"]
    if can != [want]: bad.append(f"{n}: canonical {can} != {want}")
    if d.meta.get("og:url") != want: bad.append(f"{n}: og:url")
    for k in ("og:title", "og:description", "og:image", "twitter:card", "twitter:image", "theme-color", "viewport"):
        if not d.meta.get(k): bad.append(f"{n}: missing {k}")
    for blob in d.ld:
        try: json.loads(blob)
        except Exception as ex: bad.append(f"{n}: JSON-LD invalid: {ex}")
for k, v in {**titles, **{"D:" + a: b for a, b in descs.items()}}.items():
    if len(v) > 1: bad.append(f"duplicate title/description {k!r}: {v}")
loc = [e.text for e in ET.parse(ROOT / "sitemap.xml").getroot().iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
want_locs = sorted(SITE + "/" + ("" if p.name == "index.html" else p.name) for p in pages if p.name != "404.html")
if sorted(loc) != want_locs: bad.append(f"sitemap mismatch: {sorted(set(loc) ^ set(want_locs))}")
print("\n".join(bad) if bad else f"OK: {len(pages)} pages, {len(loc)} sitemap URLs, no problems")
sys.exit(1 if bad else 0)
