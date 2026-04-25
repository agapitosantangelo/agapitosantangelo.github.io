# Personal academic website — Agapito E. Santangelo, PhD

Trilingual static site (English · Italian · Spanish) for the personal academic profile of Agapito E. Santangelo, PhD. Pure HTML + CSS, no build step, no JavaScript framework, no static-site generator. Auto-detects browser language at the root and redirects to the appropriate version.

## File structure

```
website/
├── index.html              # auto-redirects by browser language → en/, it/, or es/
├── README.md
├── assets/
│   ├── style.css           # single stylesheet shared by all pages
│   ├── cv.pdf              # downloadable CV
│   └── profile.jpg         # profile picture
├── en/                     # English version
│   ├── index.html              About — bio, research interests, professional experience, education
│   ├── research.html           Publications, working papers, conference papers, reports
│   ├── teaching.html           Teaching activities
│   ├── conferences.html        Talks & conferences
│   └── contact.html            Contact details
├── it/                     # Italian version (Profilo / Ricerca / Didattica / Talk e Conferenze / Contatti)
│   └── …same five pages
└── es/                     # Spanish version (Sobre mí / Investigación / Docencia / Charlas / Contacto)
    └── …same five pages
```

## Live URLs

- `https://agapitosantangelo.github.io/`        → auto-redirects to your browser's language
- `https://agapitosantangelo.github.io/en/`     → English
- `https://agapitosantangelo.github.io/it/`     → Italiano
- `https://agapitosantangelo.github.io/es/`     → Español

The language switcher at the bottom of every sidebar lets visitors switch language while staying on the same page.

---

## How to deploy this update onto your existing GitHub Pages repo

You already have the site live at `https://agapitosantangelo.github.io/` from the earlier (single-language) version. This update **restructures everything** into language folders. To deploy cleanly:

### Step 1 — Delete the orphan files from the previous version

Open <https://github.com/agapitosantangelo/agapitosantangelo.github.io>. The four files below at the root level are no longer needed (their replacements live inside `en/`, `it/`, `es/`). Delete them one by one:

1. Click on `research.html` → click the trash icon (top right) → "Commit changes"
2. Same for `teaching.html`
3. Same for `conferences.html`
4. Same for `contact.html`

Don't worry about `index.html`, `README.md`, or the files inside `assets/` — those will be overwritten by the upload in step 2.

### Step 2 — Upload the new contents

Extract this ZIP to a folder on your computer. You should see:

```
index.html      assets/      en/      it/      es/      README.md
```

In the GitHub repo, click `Add file → Upload files`, then drag the **contents** of the extracted folder (NOT the wrapping folder itself) onto the upload zone:

- `index.html` (the auto-redirect)
- `README.md`
- the `assets/` folder
- the `en/`, `it/`, `es/` folders

GitHub uploads everything, including subfolders, in one go. Wait for the bar to complete. Scroll to the bottom, write a commit message ("Trilingual restructure") and click **Commit changes**.

### Step 3 — Wait for the build

GitHub Pages rebuilds automatically. Check progress at the **Actions** tab in the repo: when the workflow `pages build and deployment` shows ✅, the new site is live.

### Step 4 — Verify

Open in a fresh browser window:

- <https://agapitosantangelo.github.io/> — should auto-redirect (English on most setups, Italian if your browser language is `it`, Spanish if `es`).
- <https://agapitosantangelo.github.io/en/> — English homepage
- <https://agapitosantangelo.github.io/it/> — Italian homepage
- <https://agapitosantangelo.github.io/es/> — Spanish homepage

In each version:
- The language switcher at the bottom of the sidebar should show the current language as active and the others as clickable links.
- Clicking the navigation should navigate inside the same language.
- The CV button and profile picture should load.

If anything looks broken: do a hard reload (Ctrl+Shift+R / Cmd+Shift+R) to bypass browser cache.

---

## How to update the site later

### Editing one language

Open the relevant `.html` file in `en/` (or `it/`, `es/`) on GitHub, click the pencil icon, edit, commit. Live in ~60 seconds.

### Adding a new publication

Open `en/research.html`, find an existing `<li class="entry">…</li>` block under "Peer-reviewed publications", copy it, paste it as the new top entry, edit the authors / title / venue / link. Then do the same in `it/research.html` and `es/research.html`. The publication metadata (titles, journal names) stays in English; only intro paragraphs and section headings are translated.

### Replacing the CV

Build the new `cv.pdf` from your LaTeX source. Upload it to `assets/cv.pdf` (replacing the old one). All language versions point to the same file at `../assets/cv.pdf`, so one update covers everything.

### Adding a new conference

Edit all three `conferences.html` files (en/it/es). The structure is identical; only the text differs.

---

## Things to verify periodically

- ORCID profile is populated (works, employment, education) — your sidebar links to it from every page.
- Google Scholar profile reflects all your peer-reviewed work — same.
- ResearchGate has the latest preprints uploaded.
- The CV in `assets/cv.pdf` is the latest version.
- The "expected April 2026" / "Apr 2026" wording remains aligned with reality (when the PhD is officially conferred, you may want to update Education to read "PhD obtained in [month] 2026").

---

## Site mechanics

- **Auto-redirect on root**: a small JS reads `navigator.language`, picks `en`/`it`/`es` if supported, otherwise falls back to English. The `<meta http-equiv="refresh">` is a no-JS fallback.
- **`<link rel="alternate" hreflang>`** tags are present on every page, telling search engines about the multilingual structure.
- **No tracking, no cookies, no third-party scripts** beyond Google Fonts (Crimson Pro + Geist).
- **Mobile responsive** below 880px viewport: sidebar becomes a horizontal banner, content flows below.

---

## Long-term: when to consider Jekyll / AcademicPages

This static structure works well for ≤30 publications and 3 languages. If you reach a point where:

- you find yourself updating the same change in three files repeatedly,
- you want a blog or a "talks" page with auto-generated index,
- you want tag-based filtering of publications,

then it's time to migrate to [AcademicPages](https://github.com/academicpages/academicpages.github.io) (the same stack used by `santirimedio.github.io`). The content is portable: keep the same URLs, fork the AcademicPages repo, paste your existing text into Markdown front-matter files, and you're done.
