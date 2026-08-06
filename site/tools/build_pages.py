#!/usr/bin/env python3
"""Genera i frammenti HTML delle pagine dai file dati centralizzati.

Eseguito da Quarto come pre-render (vedi _quarto.yml). Legge site/data/*.yml
ed emette site/_generated/<lang>/*.html, inclusi dalle pagine .qmd.
Un solo posto per aggiungere una pubblicazione; tre lingue servite.
"""
import os
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "_generated")

LANGS = ["it", "en", "es"]

T = {  # etichette d'interfaccia
    "it": {
        "peer": "Pubblicazioni peer-reviewed", "wp": "Working paper",
        "confpapers": "Contributi a conferenze", "under_review": "In revisione",
        "jmp": "Job Market Paper", "project_link": "Progetto collegato",
        "philosophy": "Filosofia didattica", "university": "Didattica universitaria",
        "targeted": "Corsi mirati e lezioni", "experience": "Esperienza professionale",
        "education": "Istruzione", "awards": "Riconoscimenti e affiliazioni",
        "training": "Formazione avanzata",
    },
    "en": {
        "peer": "Peer-reviewed publications", "wp": "Working papers",
        "confpapers": "Conference papers", "under_review": "Under review",
        "jmp": "Job Market Paper", "project_link": "Funded project",
        "philosophy": "Teaching philosophy", "university": "University teaching",
        "targeted": "Targeted training & lectures", "experience": "Professional experience",
        "education": "Education", "awards": "Awards & memberships",
        "training": "Advanced training",
    },
    "es": {
        "peer": "Publicaciones peer-reviewed", "wp": "Working papers",
        "confpapers": "Contribuciones a congresos", "under_review": "En revisión",
        "jmp": "Job Market Paper", "project_link": "Proyecto relacionado",
        "philosophy": "Filosofía docente", "university": "Docencia universitaria",
        "targeted": "Formaciones específicas y charlas", "experience": "Experiencia profesional",
        "education": "Formación", "awards": "Reconocimientos y afiliaciones",
        "training": "Formación avanzada",
    },
}


def L(v, lang):
    """Campo scalare o {en,it,es} -> stringa nella lingua richiesta."""
    if isinstance(v, dict):
        return v.get(lang) or v.get("en") or next(iter(v.values()))
    return v


def load(name):
    with open(os.path.join(DATA, name + ".yml")) as f:
        return yaml.safe_load(f)


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;")


def links_html(links, sep=" · "):
    if not links:
        return ""
    if isinstance(links, dict):
        links = [{"label": k.replace("_", " ").upper() if len(k) <= 4 else k, "url": u}
                 for k, u in links.items()]
    parts = [f'<a href="{l["url"]}">{esc(l.get("label") or "Link")} →</a>' for l in links]
    return " " + sep.join(parts)


_PROJECTS = None
def project_title(pid, lang):
    global _PROJECTS
    if _PROJECTS is None:
        _PROJECTS = {p["id"]: p["title"] for p in load("projects")}
    return L(_PROJECTS.get(pid, pid), lang)


def pub_entry(p, lang, t):
    tagcls = {"peer-reviewed": "peer", "working-paper": "wp"}.get(p["type"], "")
    taglbl = {"peer-reviewed": "Peer-reviewed", "working-paper": "Working paper"}[p["type"]]
    h = [f'<li class="entry"><span class="entry-tag {tagcls}">{taglbl}</span>']
    title = esc(p["title"].rstrip("."))
    if p.get("jmp"):
        title += f' <em>({t["jmp"]})</em>'
    h.append(f'{esc(p["authors"])} ({p["year"]}). <span class="entry-title">{title}.</span>')
    venue = L(p.get("venue"), lang)
    line = esc(venue) if venue else ""
    line += links_html(p.get("links"))
    if p.get("under_review"):
        line += f'<br>{t["under_review"]}: <em>{esc(p["under_review"])}</em>.'
    h.append(f'<span class="entry-venue">{line}</span>')
    if p.get("cross_ref"):
        h.append(f'<div class="cross-ref">→ {t["project_link"]}: '
                 f'<a href="projects.html#{p["cross_ref"]}">{esc(project_title(p["cross_ref"], lang))}</a></div>')
    h.append("</li>")
    return "\n".join(h)


def gen_research(lang, t):
    pubs = load("publications")
    cps = load("conference-papers")
    h = [f"<h2>{t['peer']}</h2>", '<ul class="entries">']
    h += [pub_entry(p, lang, t) for p in pubs if p["type"] == "peer-reviewed"]
    h.append("</ul>")
    h.append(f"<h2>{t['wp']}</h2>")
    h.append('<ul class="entries">')
    wps = [p for p in pubs if p["type"] == "working-paper"]
    wps.sort(key=lambda p: not p.get("jmp"))  # JMP in testa
    h += [pub_entry(p, lang, t) for p in wps]
    h.append("</ul>")
    h.append(f"<h2>{t['confpapers']}</h2>")
    h.append('<ul class="entries">')
    for c in cps:
        h.append(f'<li class="entry"><span class="entry-tag conf">Conference</span>'
                 f'{esc(c["authors"])} ({c["year"]}). <span class="entry-title">{esc(c["title"].rstrip("."))}.</span>'
                 f'<span class="entry-venue">{esc(L(c.get("venue"), lang))}.{links_html(c.get("links"))}</span></li>')
    h.append("</ul>")
    return "\n".join(h)


def gen_projects(lang, t):
    h = []
    for p in load("projects"):
        meta = p.get("meta") or {}
        h.append(f'<div class="project" id="{p["id"]}">')
        h.append(f'<div class="project-header"><h2 class="project-title">{esc(L(p["title"], lang))}</h2>'
                 f'<span class="project-status {p["status"]}">{esc(L(p["status_label"], lang))}</span></div>')
        h.append(f'<p class="project-summary">{esc(L(p["summary"], lang))}</p>')
        rows = "".join(
            f"<dt>{esc(k.title())}</dt><dd>{esc(L(v, lang))}</dd>"
            for k, v in meta.items() if v)
        if rows:
            h.append(f'<dl class="project-meta">{rows}</dl>')
        h.append("</div>")
    return "\n".join(h)


def gen_talks(lang, t):
    talks = load("talks")
    years = sorted({tk["year"] for tk in talks}, reverse=True)
    h = []
    for y in years:
        h.append(f"<h2>{y}</h2>")
        h.append('<ul class="entries">')
        for tk in [x for x in talks if x["year"] == y]:
            h.append(f'<li class="entry"><span class="entry-tag">{esc(L(tk["role"], lang))}</span>'
                     f'<span class="entry-title">{esc(L(tk["title"], lang))}</span>'
                     f'<span class="entry-venue">{esc(L(tk["venue"], lang))}'
                     + (links_html([{"label": "Link", "url": tk["link"]}]) if tk.get("link") else "")
                     + "</span>")
            for ph in tk.get("photos") or []:
                h.append(f'<figure class="entry-photo"><img src="assets/photos/{os.path.basename(ph["src"])}" '
                         f'alt="{esc(L(ph.get("alt"), lang))}" loading="lazy">'
                         f'<figcaption>{esc(L(ph.get("caption"), lang))}</figcaption></figure>')
            h.append("</li>")
        h.append("</ul>")
    return "\n".join(h)


def gen_teaching(lang, t):
    d = load("teaching")
    h = [f"<h2>{t['university']}</h2>", '<div class="timeline">']
    for c in d["university"]:
        cur = " current" if c.get("current") else ""
        h.append(f'<div class="exp-item"><div class="exp-date{cur}">{esc(L(c["period"], lang))}</div><div>'
                 f'<span class="exp-role">{esc(L(c["role"], lang))}</span>'
                 f'<div class="exp-org">{esc(L(c["org"], lang))}</div>'
                 f'<p class="exp-desc">{esc(L(c["description"], lang))}</p>'
                 f'<div class="exp-keywords">{esc(L(c.get("keywords"), lang) or "")}</div></div></div>')
    h.append("</div>")
    h.append(f"<h2>{t['targeted']}</h2>")
    h.append('<div class="timeline">')
    for c in d.get("targeted") or []:
        h.append(f'<div class="exp-item"><div class="exp-date">{esc(L(c.get("period"), lang) or "")}</div><div>'
                 f'<span class="exp-role">{esc(L(c["role"], lang))}</span>'
                 f'<div class="exp-org">{esc(L(c.get("org"), lang) or "")}</div>'
                 f'<p class="exp-desc">{esc(L(c.get("description"), lang) or "")}</p></div></div>')
    h.append("</div>")
    if d.get("philosophy"):
        h.append(f"<h2>{t['philosophy']}</h2>")
        h.append(f'<p class="lead">{esc(L(d["philosophy"], lang))}</p>')
    return "\n".join(h)


def gen_news(lang, t, limit=None):
    news = load("news")
    if limit:
        news = news[:limit]
    h = ['<div class="updates">']
    for n in news:
        body = esc(L(n["body"], lang))
        link = n.get("link")
        if link:
            body += f' <a href="{L(link, lang)}">→</a>'
        h.append(f'<div class="update"><span class="quando">{esc(L(n["date_label"], lang))}</span>'
                 f'<span class="cosa">{body}</span></div>')
    h.append("</div>")
    return "\n".join(h)


def gen_about(lang, t):
    d = load("experience")
    h = [f"<h2>{t['experience']}</h2>", '<div class="timeline">']
    for e in d["experience"]:
        cur = " current" if e.get("current") else ""
        org = esc(L(e["org"], lang))
        if e.get("org_url"):
            org = f'<a href="{e["org_url"]}">{org}</a>'
        h.append(f'<div class="exp-item" id="{e["id"]}"><div class="exp-date{cur}">{esc(L(e["period"], lang))}</div><div>'
                 f'<span class="exp-role">{esc(L(e["role"], lang))}</span>'
                 f'<div class="exp-org">{org}</div>'
                 f'<p class="exp-desc">{esc(L(e["description"], lang))}</p>'
                 f'<div class="exp-keywords">{esc(L(e.get("keywords"), lang) or "")}</div></div></div>')
    h.append("</div>")
    h.append(f"<h2>{t['education']}</h2>")
    h.append('<div class="timeline">')
    for e in d["education"]:
        h.append(f'<div class="exp-item"><div class="exp-date">{esc(L(e["period"], lang))}</div><div>'
                 f'<span class="exp-role">{esc(L(e["title"], lang))}</span>'
                 f'<div class="exp-org">{esc(L(e["institution"], lang))}</div>'
                 f'<p class="exp-desc">{esc(L(e.get("notes"), lang) or "")}</p></div></div>')
    h.append("</div>")
    h.append(f"<h2>{t['awards']}</h2>")
    h.append('<ul class="entries">')
    for a in d["awards"]:
        h.append(f'<li class="entry"><span class="entry-tag">{esc(L(a["tag"], lang))}</span>'
                 f'<span class="entry-venue">{esc(L(a["text"], lang))}</span></li>')
    h.append("</ul>")
    h.append(f"<h2>{t['training']}</h2>")
    h.append('<ul class="entries">')
    for tr in d["training"]:
        h.append(f'<li class="entry"><span class="entry-title">{esc(L(tr["title"], lang))}</span>'
                 f'<span class="entry-venue">{esc(L(tr.get("venue"), lang) or "")}</span></li>')
    h.append("</ul>")
    return "\n".join(h)


def gen_dissemination(lang, t):
    h = []
    for sec in load("dissemination"):
        h.append(f'<h2>{esc(L(sec["heading"], lang))}</h2>')
        h.append('<ul class="entries">')
        for it in sec["items"]:
            tag = esc(L(it.get("tag"), lang) or "")
            h.append(f'<li class="entry"><span class="entry-tag report">{tag}</span>'
                     f'<span class="entry-title">{esc(L(it.get("title"), lang) or "")}</span>'
                     f'<span class="entry-venue">{esc(L(it.get("venue"), lang) or "")}{links_html(it.get("links"))}</span></li>')
        h.append("</ul>")
    return "\n".join(h)


def main():
    for lang in LANGS:
        t = T[lang]
        out = os.path.join(OUT, lang)
        os.makedirs(out, exist_ok=True)
        pages = {
            "research": gen_research, "projects": gen_projects,
            "talks": gen_talks, "teaching": gen_teaching,
            "about": gen_about, "dissemination": gen_dissemination,
        }
        for name, fn in pages.items():
            with open(os.path.join(out, name + ".html"), "w") as f:
                f.write(fn(lang, t))
        with open(os.path.join(out, "news.html"), "w") as f:
            f.write(gen_news(lang, t))
        with open(os.path.join(out, "updates.html"), "w") as f:
            f.write(gen_news(lang, t, limit=3))
        print(f"[build_pages] {lang}: {len(pages) + 2} frammenti generati")


if __name__ == "__main__":
    main()
