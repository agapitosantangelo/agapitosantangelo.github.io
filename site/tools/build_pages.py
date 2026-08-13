#!/usr/bin/env python3
"""Genera i frammenti HTML delle pagine dai file dati centralizzati.

Eseguito da Quarto come pre-render (vedi _quarto.yml). Legge site/data/*.yml
ed emette site/_generated/<lang>/*.html, inclusi dalle pagine .qmd.
Un solo posto per aggiungere una pubblicazione; tre lingue servite.
"""
import json
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
        "updates_title": "Aggiornamenti recenti", "all_updates": "Tutti gli aggiornamenti →",
        "filter_all": "Tutti", "filters": {"policy-evaluation": "Policy evaluation",
        "digital-methods": "Metodi digitali", "health": "Sanità", "territorial": "Territorio",
        "innovation": "Innovazione", "institutions": "Istituzioni"},
        "filter_label": "Filtra per tema:", "filter_aria": "Filtri per tema",
        "filter_count": "{n} di {m} lavori",
        "meta_labels": {"funder": "Finanziatore", "period": "Periodo", "pi": "Responsabile",
                        "role": "Ruolo", "methods": "Metodi"},
        "footer_title": "Contatti",
        "doi_label": "DOI",
    },
    "en": {
        "peer": "Peer-reviewed publications", "wp": "Working papers",
        "confpapers": "Conference papers", "under_review": "Under review",
        "jmp": "Job Market Paper", "project_link": "Funded project",
        "philosophy": "Teaching philosophy", "university": "University teaching",
        "targeted": "Targeted training & lectures", "experience": "Professional experience",
        "education": "Education", "awards": "Awards & memberships",
        "training": "Advanced training",
        "updates_title": "Recent updates", "all_updates": "All updates →",
        "filter_label": "Filter by topic:", "filter_aria": "Topic filters",
        "filter_count": "{n} of {m} works",
        "meta_labels": {"funder": "Funder", "period": "Period", "pi": "Principal investigator",
                        "role": "Role", "methods": "Methods"},
        "footer_title": "Contact",
        "doi_label": "DOI",
        "filter_all": "All", "filters": {"policy-evaluation": "Policy evaluation",
        "digital-methods": "Digital methods", "health": "Health", "territorial": "Territorial",
        "innovation": "Innovation", "institutions": "Institutions"},
    },
    "es": {
        "peer": "Publicaciones peer-reviewed", "wp": "Working papers",
        "confpapers": "Contribuciones a congresos", "under_review": "En revisión",
        "jmp": "Job Market Paper", "project_link": "Proyecto relacionado",
        "philosophy": "Filosofía docente", "university": "Docencia universitaria",
        "targeted": "Formaciones específicas y charlas", "experience": "Experiencia profesional",
        "education": "Formación", "awards": "Reconocimientos y afiliaciones",
        "training": "Formación avanzada",
        "updates_title": "Actualizaciones recientes", "all_updates": "Todas las actualizaciones →",
        "filter_label": "Filtra por tema:", "filter_aria": "Filtros por tema",
        "filter_count": "{n} de {m} trabajos",
        "meta_labels": {"funder": "Financiador", "period": "Periodo", "pi": "Investigador principal",
                        "role": "Rol", "methods": "Métodos"},
        "footer_title": "Contacto",
        "doi_label": "DOI",
        "filter_all": "Todos", "filters": {"policy-evaluation": "Policy evaluation",
        "digital-methods": "Métodos digitales", "health": "Sanidad", "territorial": "Territorio",
        "innovation": "Innovación", "institutions": "Instituciones"},
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
    topics = " ".join(p.get("topics") or [])
    # id stabile: ancorabile da CV, email e JSON-LD
    h = [f'<li class="entry" id="pub-{p["id"]}" data-topics="{topics}">'
         f'<span class="entry-tag {tagcls}">{taglbl}</span>']
    title = esc(p["title"].rstrip("."))
    if p.get("jmp"):
        title += f' <em>(<a href="jmp.html">{t["jmp"]}</a>)</em>'
    h.append(f'{esc(p["authors"])} ({p["year"]}). <span class="entry-title">{title}.</span>')
    venue = L(p.get("venue"), lang)
    line = esc(venue) if venue else ""
    line += links_html(p.get("links"))
    if p.get("doi"):
        line += f' · <a href="https://doi.org/{p["doi"]}">{t["doi_label"]} →</a>'
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
    h = [f'<div class="filter-bar" role="group" aria-label="{t["filter_aria"]}" '
         f'data-count-tpl="{t["filter_count"]}">']
    h.append(f'<span class="filter-label">{t["filter_label"]}</span>')
    h.append(f'<button class="filter-btn active" aria-pressed="true" data-filter="">{t["filter_all"]}</button>')
    for key, lbl in t["filters"].items():
        h.append(f'<button class="filter-btn" aria-pressed="false" data-filter="{key}">{lbl}</button>')
    h.append('<span class="filter-count" aria-live="polite"></span>')
    h.append('</div>')
    h += [f"<h2>{t['peer']}</h2>", '<ul class="entries">']
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
        ctopics = " ".join(c.get("topics") or [])
        h.append(f'<li class="entry" data-topics="{ctopics}"><span class="entry-tag conf">Conference</span>'
                 f'{esc(c["authors"])} ({c["year"]}). <span class="entry-title">{esc(c["title"].rstrip("."))}.</span>'
                 f'<span class="entry-venue">{esc(L(c.get("venue"), lang))}.{links_html(c.get("links"))}</span></li>')
    h.append("</ul>")
    # JSON-LD: le pubblicazioni come ScholarlyArticle, ancorate agli id
    arts = [{"@type": "ScholarlyArticle",
             "headline": p["title"].rstrip("."),
             "author": p["authors"],
             "datePublished": str(p["year"]),
             "url": f"https://agapitosantangelo.github.io/{lang}/research.html#pub-{p['id']}"}
            for p in pubs]
    h.append('<script type="application/ld+json">'
             + json.dumps({"@context": "https://schema.org", "@graph": arts}, ensure_ascii=False)
             + '</script>')
    return "\n".join(h)


def gen_projects(lang, t):
    h = []
    for p in load("projects"):
        meta = p.get("meta") or {}
        h.append(f'<div class="project" id="{p["id"]}">')
        title = esc(L(p["title"], lang))
        if p.get("url"):
            title = f'<a href="{p["url"]}">{title} →</a>'
        h.append(f'<div class="project-header"><h2 class="project-title">{title}</h2>'
                 f'<span class="project-status {p["status"]}">{esc(L(p["status_label"], lang))}</span></div>')
        h.append(f'<p class="project-summary">{esc(L(p["summary"], lang))}</p>')
        rows = "".join(
            f"<dt>{esc(t['meta_labels'].get(k, k.title()))}</dt><dd>{esc(L(v, lang))}</dd>"
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
                h.append(f'<figure class="entry-photo"><img src="../assets/photos/{os.path.basename(ph["src"])}" '
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
    h = ['<div class="updates">']
    if limit:
        # box della homepage alla Sant'Anna: titolo centrato dentro il box
        news = news[:limit]
        h.append(f'<p class="updates-title">{t["updates_title"]}</p>')
    for n in news:
        body = esc(L(n["body"], lang))
        link = n.get("link")
        if link:
            body += f' <a href="{L(link, lang)}">→</a>'
        h.append(f'<div class="update"><span class="quando">{esc(L(n["date_label"], lang))}</span>'
                 f'<span class="cosa">{body}</span></div>')
    if limit:
        h.append(f'<span class="tutti"><a href="news.html">{t["all_updates"]}</a></span>')
    h.append("</div>")
    return "\n".join(h)


def gen_about(lang, t):
    d = load("experience")
    h = [f"<h2>{t['experience']}</h2>", '<div class="timeline">']
    for e in d["experience"]:
        cur = " current" if e.get("current") else ""
        org = esc(L(e["org"], lang))
        if e.get("org_url"):
            org = f'<a href="{L(e["org_url"], lang)}">{org}</a>'
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


# icone 16x16 (tratte da Bootstrap Icons, licenza MIT) per la lista link dell'hero
ICONS = {
    "email": '<path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4Zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2Zm13 2.383-4.708 2.825L15 11.105V5.383Zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a.997.997 0 0 0 .966-.741ZM1 11.105l4.708-2.897L1 5.383v5.722Z"/>',
    "scholar": '<path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3a.5.5 0 0 0 .372 0L14 7.14V13a1 1 0 0 0-1 1v2h3v-2a1 1 0 0 0-1-1V6.739l.686-.275a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/><path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .294.605l4.5 1.8a.5.5 0 0 0 .372 0l4.5-1.8a.5.5 0 0 0 .294-.605l-.5-1.7a.5.5 0 0 0-.656-.327L8 10.466 4.176 9.032Z"/>',
    "orcid": '<circle cx="8" cy="8" r="6.6" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="8" y="10.6" text-anchor="middle" font-family="Geist, sans-serif" font-size="7" font-weight="600">iD</text>',
    "researchgate": '<circle cx="8" cy="8" r="6.6" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="8" y="10.6" text-anchor="middle" font-family="Geist, sans-serif" font-size="6.4" font-weight="600">RG</text>',
    "github": '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/>',
    "linkedin": '<path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>',
    "cv": '<path d="M5.5 7a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1h-5zM5 9.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5z"/><path d="M9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.5L9.5 0zm0 1v2A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5z"/>',
}


def gen_hero(lang, t):
    """Homepage alla psantanna.com (template 'trestles'): colonna sinistra con
    ritratto tondo, nome, aree e lista link con icone; colonna destra con
    nome grande, affiliazione, frase di apertura e paragrafi bio."""
    d = load("hero")
    aree = "".join(f'<span>{esc(L(a, lang))}</span>' for a in d["areas"])
    links = "".join(
        f'<li><a href="{l["url"]}">'
        f'<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">{ICONS[l["icon"]]}</svg>'
        f'{esc(L(l["label"], lang))}</a></li>'
        for l in d["links"])
    bio = "".join(f'<p>{esc(L(par, lang))}</p>' for par in d["bio"])
    # div e non <aside>: Quarto sposta gli <aside> nella colonna a margine
    h = ['<div class="hero-es">',
         '<div class="hero-es-side">',
         f'<img class="ritratto" src="{d["photo"]}" alt="{esc(L(d["photo_alt"], lang))}" width="720" height="720">',
         f'<p class="side-nome">{esc(d["name"])}</p>',
         f'<p class="side-aree">{aree}</p>',
         f'<ul class="side-links">{links}</ul>',
         '</div>',
         '<div class="hero-es-main">',
         # div con ruolo heading: un <h1> vero verrebbe promosso da Quarto
         # a titolo di pagina e spostato in cima al documento
         f'<div class="h1-nome" role="heading" aria-level="1">{esc(d["name"])}</div>',
         f'<p class="affiliazione">{esc(L(d["affiliazione"], lang))}</p>',
         f'<p class="lead-bio">{esc(L(d["lead"], lang))}</p>',
         '<hr>',
         bio,
         '</div>',
         '</div>']
    # JSON-LD Person: così i motori "capiscono" chi è e collegano i profili
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Agapito Emanuele Santangelo",
        "alternateName": "Agapito E. Santangelo",
        "jobTitle": L(d["affiliazione"], lang).split(" — ")[0],
        "affiliation": {"@type": "Organization", "name": "Università del Molise"},
        "url": f"https://agapitosantangelo.github.io/{lang}/",
        "image": "https://agapitosantangelo.github.io/assets/profile.jpg",
        "email": "mailto:emanuele.santangelo@unimol.it",
        "sameAs": [l["url"] for l in d["links"] if str(l["url"]).startswith("https://")],
    }
    h.append('<script type="application/ld+json">'
             + json.dumps(person, ensure_ascii=False) + '</script>')
    return "\n".join(h)


def gen_footer(lang, t):
    """Pre-footer 'Get in touch': email, profili e copyright, generato
    dagli stessi dati della hero (data/hero.yml)."""
    d = load("hero")
    links = "".join(
        f'<li><a href="{l["url"]}">'
        f'<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">{ICONS[l["icon"]]}</svg>'
        f'{esc(L(l["label"], lang))}</a></li>'
        for l in d["links"])
    return ('<footer class="site-footer"><div class="footer-inner">'
            f'<p class="footer-title">{t["footer_title"]}</p>'
            f'<p class="footer-blurb"><a href="mailto:emanuele.santangelo@unimol.it">'
            'emanuele.santangelo@unimol.it</a> · Università del Molise, Dipartimento di Economia</p>'
            f'<ul class="footer-links">{links}</ul>'
            '<p class="footer-copy">© 2026 Agapito Emanuele Santangelo</p>'
            '</div></footer>')


def main():
    for lang in LANGS:
        t = T[lang]
        out = os.path.join(OUT, lang)
        os.makedirs(out, exist_ok=True)
        pages = {
            "research": gen_research, "projects": gen_projects,
            "talks": gen_talks, "teaching": gen_teaching,
            "about": gen_about, "dissemination": gen_dissemination,
            "hero": gen_hero, "footer": gen_footer,
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
