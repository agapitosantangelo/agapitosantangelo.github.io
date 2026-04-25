# Personal academic website — Agapito E. Santangelo, PhD

Trilingual static site (English · Italian · Spanish) — 7 pages per language, no build step, no JavaScript framework, no static-site generator. Auto-detects browser language at the root and redirects to the matching version.

## File structure

```
website/
├── index.html              # auto-redirects by browser language
├── README.md
├── assets/
│   ├── style.css
│   ├── cv.pdf
│   └── profile.jpg
├── en/
│   ├── index.html              About (bio, latest news, experience, education)
│   ├── research.html           Peer-reviewed publications, working papers, conference papers
│   ├── projects.html           Active research projects
│   ├── teaching.html           Teaching activities
│   ├── conferences.html        Talks & conferences
│   ├── dissemination.html      Policy reports, op-eds, public engagement
│   └── contact.html            Contact details
├── it/                     (Profilo · Ricerca · Progetti · Didattica · Talk e Conferenze · Divulgazione · Contatti)
└── es/                     (Sobre mí · Investigación · Proyectos · Docencia · Charlas y Congresos · Divulgación · Contacto)
```

## Live URLs

- `https://agapitosantangelo.github.io/`  → auto-redirects to browser language
- `https://agapitosantangelo.github.io/en/`
- `https://agapitosantangelo.github.io/it/`
- `https://agapitosantangelo.github.io/es/`

## Site features

- **Latest news block** on the home page (easy to edit).
- **Affiliations & collaborations bar** at the bottom of every page.
- **Auto-redirect** on root via JS, with no-JS fallback.
- **`<link rel="alternate" hreflang>`** for SEO multilingual support.
- **Mobile responsive** below 880px.
- **No tracking, no cookies** beyond Google Fonts.

## How to update

- **Latest news**: edit `<div class="latest">` block on `*/index.html` (each language).
- **New publication**: copy an existing `<li class="entry">` in `*/research.html` and edit.
- **New project**: copy a `<div class="project">…</div>` block in `*/projects.html`. Status variants: `ongoing` (green), `review` (amber), `published` (blue).
- **Replace CV**: upload new `cv.pdf` to `assets/cv.pdf` (replaces all language refs at once).
