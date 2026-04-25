# Personal academic website — Agapito E. Santangelo

A static, single-stack personal site (HTML + CSS, no build step, no JavaScript framework). Five pages — About, Research, Teaching, Talks &amp; Conferences, Contact — sharing one stylesheet and one sidebar layout.

## File structure

```
website/
├── index.html          About (home)
├── research.html       Publications, working papers, conference papers, reports
├── teaching.html       Teaching activities
├── conferences.html    Talks & conferences
├── contact.html        Contact details and online presence
└── assets/
    ├── style.css       All styles
    ├── cv.pdf          Downloadable CV (the LaTeX-built one)
    └── (profile.jpg)   Place your portrait here, then update the HTML — see below
```

---

## Things to customize before going live

Open the five `.html` files and search-replace these placeholders:

| Placeholder                                | Replace with                                                    |
|--------------------------------------------|------------------------------------------------------------------|
| `agapito.santangelo@example.com`           | Your real email (5 occurrences total: one per page)              |
| `https://orcid.org/` (no ID)               | Your ORCID URL, e.g. `https://orcid.org/0000-0000-0000-0000`     |
| `https://www.researchgate.net/profile/Agapito-Santangelo` | Your real ResearchGate URL                          |
| Google Scholar URL (already correct)       | Verify it matches your profile                                   |
| `Via F. De Sanctis, 86100 Campobasso`      | Your actual office address (only on `contact.html`)              |

### Profile photo
The sidebar currently shows a placeholder text box with your initials (`AES`). To use a real photo:

1. Save a square portrait as `assets/profile.jpg` (recommended: 600×600 px, JPG or WebP).
2. In each `.html` file, replace:
   ```html
   <div class="profile-img placeholder" aria-label="Profile picture placeholder">AES</div>
   ```
   with:
   ```html
   <img class="profile-img" src="assets/profile.jpg" alt="Agapito E. Santangelo">
   ```

### Italian version (optional)
The language switcher at the bottom of the sidebar links to a non-existent `IT` page. Either:
- Remove the IT link until you build it, or
- Duplicate the five HTML files in an `it/` subfolder and translate the content. Update the relative links accordingly.

---

## How to view it locally

Just open `index.html` in your browser. No build step, no server needed:

```bash
cd website
xdg-open index.html      # Linux
open index.html          # macOS
start index.html         # Windows
```

For a slightly better local experience (so the relative paths behave like in production):

```bash
cd website
python3 -m http.server 8000
# then open http://localhost:8000
```

---

## How to put it online with GitHub Pages — step by step

GitHub Pages is free, supports custom domains, and is the standard hosting for academic personal sites (the reference site you sent uses exactly this stack).

### Option A — recommended: at `agapitosantangelo.github.io`

This gives you a clean URL with no subdirectory.

1. **Create a GitHub account** if you don't already have one: <https://github.com/signup>. Pick a username close to your name — say `agapitosantangelo` or `aesantangelo`. The username will appear in your URL.

2. **Create a new repository** at <https://github.com/new>. Two important fields:
   - **Repository name**: must be exactly `<your-username>.github.io` (e.g. `agapitosantangelo.github.io`). The trailing `.github.io` is what tells GitHub to serve the repo as a website.
   - **Visibility**: Public.
   - Leave "Add a README file" unchecked.

3. **Upload the website files**. Two ways:

   **(a) Web upload — easiest, no command line:**
   - Open the new repository.
   - Click `Add file → Upload files`.
   - Drag and drop the **contents** of the `website/` folder (the five `.html` files and the `assets/` folder). Do NOT drag the `website/` folder itself — drop its contents.
   - Scroll down, write a commit message ("Initial site"), click `Commit changes`.

   **(b) Git CLI — if you'll be updating it often:**
   ```bash
   cd website
   git init
   git add .
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-username>.github.io.git
   git push -u origin main
   ```

4. **Enable GitHub Pages**. In the repository, go to `Settings → Pages`. Under "Build and deployment":
   - Source: `Deploy from a branch`
   - Branch: `main`, folder: `/ (root)`
   - Click `Save`.

5. **Wait 1–2 minutes** for the first build. The `Pages` settings page will show a green banner with the live URL: `https://<your-username>.github.io/`.

That's it. From now on, every time you push or upload a change, the site rebuilds automatically.

### Option B — at `<username>.github.io/site` (project page)

If you want to keep the `<username>.github.io` URL free for something else later, name the repository anything you like (e.g. `web` or `site`). The site will live at `https://<username>.github.io/<repo-name>/`. Same upload steps; same `Settings → Pages → main → /` activation.

**Important:** if you go this route, all relative links inside the HTML will still work fine — they're already relative (`href="research.html"`, not `href="/research.html"`).

---

## Custom domain (optional)

If you buy `santangelo.eu` or similar:

1. In the repo: `Settings → Pages → Custom domain` → enter your domain → `Save`.
2. At your domain registrar, add a CNAME record pointing your domain to `<your-username>.github.io`.
3. Tick "Enforce HTTPS" once GitHub provisions the certificate (usually within a few minutes).

---

## How to update the site later

Whatever workflow you use:

- **Edit a page**: open the relevant `.html` in any editor, change the text, save, and either re-upload via the web or `git commit && git push`.
- **Replace the CV**: rebuild `cv.pdf` from your LaTeX source, drop it into `assets/`, replacing the old file.
- **Add a new publication**: open `research.html`, copy an existing `<li class="entry">…</li>` block, paste, edit. The styling is automatic.

A change is live ~30–90 seconds after pushing.

---

## What this is NOT (and why that's fine for now)

This site does not use Jekyll, AcademicPages, or any static-site generator. The reference site (`santirimedio.github.io`) uses AcademicPages, which adds:

- A sidebar / header / footer template that lives in one file (so you don't update navigation in five places).
- Markdown for content instead of HTML.
- A blog / talks / publications collection format with auto-generated index pages.

If at some point you want any of these, the natural upgrade path is to fork [AcademicPages](https://github.com/academicpages/academicpages.github.io) into your `<username>.github.io` repo and migrate the content. Until you have many more publications or want a blog, the static HTML approach here is faster to maintain and won't break.
