#!/usr/bin/env python3
"""Post-render SEO: canonical + hreflang su ogni pagina delle tre lingue,
e pulizia del sitemap (via la root di redirect, la 404 e gli stub alias).

I tre alberi it/en/es sono pagine parallele con lo stesso nome file:
senza hreflang reciproci Google può servire la lingua sbagliata e
trattare it/es come near-duplicate.
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "_site")
BASE = "https://agapitosantangelo.github.io"
LANGS = ["it", "en", "es"]
X_DEFAULT = "en"


def pretty(lang, page):
    """URL canonico senza index.html finale."""
    return f"{BASE}/{lang}/" if page == "index.html" else f"{BASE}/{lang}/{page}"


def head_tags(lang, page):
    tags = [f'<link rel="canonical" href="{pretty(lang, page)}">']
    for l in LANGS:
        tags.append(f'<link rel="alternate" hreflang="{l}" href="{pretty(l, page)}">')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{pretty(X_DEFAULT, page)}">')
    return "\n".join(tags) + "\n"


def is_redirect_stub(html):
    return "<title>Redirect</title>" in html


def main():
    injected = 0
    for lang in LANGS:
        for path in glob.glob(os.path.join(SITE, lang, "*.html")):
            page = os.path.basename(path)
            with open(path) as f:
                html = f.read()
            if is_redirect_stub(html) or "rel=\"canonical\"" in html:
                continue
            html = html.replace("</head>", head_tags(lang, page) + "</head>", 1)
            with open(path, "w") as f:
                f.write(html)
            injected += 1

    # sitemap: via la root di redirect, la 404 e gli stub conferences.html
    sm_path = os.path.join(SITE, "sitemap.xml")
    if os.path.exists(sm_path):
        with open(sm_path) as f:
            sm = f.read()
        drop = re.compile(
            r"\s*<url>\s*<loc>[^<]*(?:/index\.html|/404\.html|/conferences\.html)</loc>.*?</url>",
            re.S)
        sm, dropped = drop.subn("", sm)
        # le home di lingua rientrano in forma directory pulita
        entries = "".join(f"<url><loc>{BASE}/{l}/</loc></url>" for l in LANGS)
        sm = sm.replace("</urlset>", entries + "</urlset>")
        with open(sm_path, "w") as f:
            f.write(sm)
        print(f"[postprocess_seo] sitemap: {dropped} voci rimosse, home di lingua reinserite")

    print(f"[postprocess_seo] canonical+hreflang su {injected} pagine")


if __name__ == "__main__":
    main()
