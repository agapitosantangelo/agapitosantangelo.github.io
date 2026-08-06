# Audit di accessibilità e design — modifiche applicate

**Branch:** `audit-accessibilita-design`
**Base:** `ad6b055` (main)
**File modificati:** 22 — le 21 pagine di contenuto (`en/`, `it/`, `es/` × 7) e `assets/style.css`
**Data:** 6 agosto 2026

Nessun contenuto testuale è stato riscritto. Le modifiche riguardano struttura semantica,
accessibilità, tipografia, responsività e metadati. L'aspetto del sito è invariato salvo
tre punti dichiarati più sotto (§ *Cambiamenti visibili*).

---

## Indice

1. [Conformità WCAG 2.2 AA](#1-conformità-wcag-22-aa)
2. [Struttura semantica](#2-struttura-semantica)
3. [Tipografia e responsività](#3-tipografia-e-responsività)
4. [Metadati e SEO](#4-metadati-e-seo)
5. [Pulizia del CSS](#5-pulizia-del-css)
6. [Cambiamenti visibili](#6-cambiamenti-visibili)
7. [Misure prima/dopo](#7-misure-primadopo)
8. [Cosa resta aperto](#8-cosa-resta-aperto)
9. [Come verificare](#9-come-verificare)

---

## 1. Conformità WCAG 2.2 AA

### 1.1 Contrasto del testo secondario — *1.4.3 Contrast (Minimum)*

`--ink-mute` valeva `#7a7674`: **4,30:1** su crema e **4,50:1** su bianco. Il colore è usato
su testo di 13–15px, che WCAG considera testo *normale* (non "large"), quindi la soglia è
4,5:1. Falliva in circa 18 punti: date, `entry-venue`, `exp-keywords`, `skills-grid dt`,
footer, barra lingua, `project-meta`, didascalie.

```diff
- --ink-mute: #7a7674;
+ --ink-mute: #6b6764;
```

Stessa tinta (h = 20°), luminosità ridotta: **5,36:1** su crema, **5,60:1** su bianco.

### 1.2 Dimensione dei bersagli nella barra lingua — *2.5.8 Target Size (Minimum)*

I link `EN` / `IT` / `ES` misuravano 15×27, 22×26 e 21×26 px. La soglia è 24×24.

```diff
  .top-bar a,
+ .top-bar .active {
+   display: inline-flex;
+   align-items: center;
+   justify-content: center;
+   min-width: 2.5rem;
+   min-height: 1.75rem;
+   padding: 0.25rem 0.5rem;
```

Ora tutti e tre misurano **45×32 px**.

### 1.3 Dimensione del carattere rispettosa delle preferenze — *1.4.4 Resize Text*

`html, body { font-size: 18px }` azzerava l'impostazione "dimensione testo" del browser.

```diff
+ html {
+   font-size: 112.5%;
+ }
  html, body {
-   font-size: 18px;
```

> ⚠️ **Attenzione per modifiche future.** La percentuale deve stare **solo su `html`**.
> Su `html, body` si compone: `html` diventa 18px e `body` 112,5% *di 18* = 20,25px,
> ingrandendo tutto il sito del 12,5%. `body` riceve `font-size: 1rem` esplicito.

### 1.4 Focus visibile — *2.4.7 / 2.4.11*

Non era mai definito: si ereditava l'anello di default del browser. Presente, ma sottile e
quasi invisibile sul bottone CV nero.

```css
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.cv-button:focus-visible { outline-color: var(--accent-h); outline-offset: 3px; }
main:focus, main:focus-visible { outline: none; }
```

### 1.5 Scorciatoia al contenuto — *2.4.1 Bypass Blocks*

Su ogni pagina 16 elementi tabbabili precedevano `<main>`: foto, nome, dipartimento, email,
CV, quattro link social, sette voci di menu — da riattraversare a ogni navigazione.

```diff
  <body>
+ <a class="skip-link" href="#contenuto">Salta al contenuto</a>
...
- <main class="main">
+ <main class="main" id="contenuto" tabindex="-1">
```

`tabindex="-1"` è necessario perché il focus si sposti davvero su `<main>` all'attivazione.
Testato: il focus atterra su `<main>`, il Tab successivo è già dentro il contenuto.
Etichette localizzate: *Salta al contenuto* / *Skip to content* / *Saltar al contenido*.

### 1.6 Informazione veicolata dal solo colore — *1.4.1 Use of Color*

Il pallino verde davanti alle date significava "posizione attuale", senza equivalente
testuale. Inoltre il contenuto generato `"● "` veniva letto dagli screen reader.

```diff
  .exp-date.current::before {
-   content: "● ";
-   color: #6a8859;
+   content: "";
+   display: inline-block;
+   width: 0.45em; height: 0.45em;
+   border-radius: 50%;
+   background: #4f6841;
  }
```

E nell'HTML:

```diff
- <div class="exp-date current">Set 2024 — In corso</div>
+ <div class="exp-date current"><span class="sr-only">Posizione attuale — </span>Set 2024 — In corso</div>
```

Il verde è passato da **3,81:1** a **5,93:1**. Aggiunta l'utility `.sr-only`.

### 1.7 Stato corrente esposto alle tecnologie assistive

La lingua attiva era `<a class="active">IT</a>`: un'ancora senza `href`, quindi non
focalizzabile e non annunciata come link, e lo stato "corrente" non era esposto.

```diff
- <a class="active">IT</a>
+ <span class="active" aria-current="true">IT</span>
```

```diff
- <li><a class="current" href="index.html">Profilo</a></li>
+ <li><a class="current" href="index.html" aria-current="page">Profilo</a></li>
```

Il CSS è passato da `.top-bar a.active` a `.top-bar .active` per applicarsi allo `<span>`;
il bordo inferiore è ora `box-shadow: inset` per non alterare il box.

### 1.8 Etichette e lingua dei link

`aria-label="Language"` era in inglese anche sulle pagine italiane e spagnole.

```diff
- <nav class="top-bar" aria-label="Language">
+ <nav class="top-bar" aria-label="Lingua">        <!-- Language / Idioma -->
- <a href="../en/index.html">EN</a>
+ <a href="../en/index.html" hreflang="en" lang="en">EN</a>
```

`lang` fa sì che lo screen reader pronunci "EN" e "ES" con la fonetica giusta.

### 1.9 Movimento ridotto — *2.3.3 Animation from Interactions*

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 2. Struttura semantica

### 2.1 Un solo `<h1>` per pagina — *1.3.1 Info and Relationships*

Ogni pagina ne aveva due: il nome nella sidebar e il titolo di pagina. Per uno screen reader
la pagina aveva due titoli e non era chiaro dove ci si trovasse.

```diff
- <h1 class="name">Agapito E.<br>Santangelo, PhD</h1>
+ <p class="name">Agapito E.<br>Santangelo, PhD</p>
```

La classe `.name` definisce già font, corpo, peso e margini: l'aspetto non cambia.

### 2.2 Gerarchia dei titoli in `projects.html`

La pagina non aveva alcun `<h2>`: passava da `<h1>` a cinque `<h3>`. I `<h3 class="project-title">`
sono diventati `<h2>`, e il CSS annulla le decorazioni che `h2` porta con sé:

```css
.project-title { border-bottom: none; padding-bottom: 0; }
.project-title::before { content: none; }   /* il "§ " dei titoli di sezione */
```

Verificato su tutte le pagine: nessun salto di livello residuo.

### 2.3 Landmark mancanti

Erano esposti solo `nav` (barra lingua), `aside` e `main`. Il menu era una `<ul>` nuda e il
footer un `<div>`.

```diff
+ <nav class="site-nav" aria-label="Navigazione del sito">
    <ul class="nav"> … </ul>
+ </nav>
```

```diff
- <div class="foot"> … </div>
+ <footer class="foot"> … </footer>
```

Ora: `nav[Lingua]`, `aside`, `nav[Navigazione del sito]`, `main`, `footer`.

> **Nota tecnica.** Il wrapper `.site-nav` usa `margin: 0; padding: 0`, **non**
> `display: contents`. Quest'ultima proprietà rimuove storicamente l'elemento dall'albero di
> accessibilità — cancellerebbe proprio il landmark che si vuole esporre. La sidebar è un
> blocco, quindi il wrapper è già neutro rispetto al layout.

> **Limite noto.** `<footer>` è dentro `<main>`, quindi non produce un landmark `contentinfo`.
> Spostarlo fuori richiederebbe di renderlo un elemento della griglia `.shell` con
> `grid-column: 2`. Non fatto: l'elemento semantico è comunque meglio del `<div>`.

### 2.4 Link esterno che apre una nuova scheda

```diff
- <a class="cv-button" href="../assets/cv.pdf" target="_blank">Scarica il CV (PDF)</a>
+ <a class="cv-button" href="../assets/cv.pdf" target="_blank" rel="noopener">Scarica il CV (PDF)<span class="sr-only"> (si apre in una nuova scheda)</span></a>
```

---

## 3. Tipografia e responsività

### 3.1 Lunghezza di riga

`p { max-width: 70ch }` produceva righe piene da **~101 caratteri**; l'intervallo comodo è 45–75.

L'unità `ch` è la larghezza dello zero. Crimson Pro ha lo zero largo ma il carattere medio
stretto, quindi `ch` **sovrastima parecchio**: misurato sul testo reale, 70ch = 101 caratteri,
54ch = 79.

```diff
- p { max-width: 70ch; }
+ p { max-width: 54ch; }
- .lead { max-width: 64ch; }
+ .lead { max-width: 50ch; }
```

### 3.2 Sidebar tagliata sui portatili

`height: 100vh` + `overflow-y: auto`: su un viewport da 720px il contenuto della sidebar è
alto 1012px, quindi **292px finivano in una seconda barra di scorrimento** e le voci
*Divulgazione* e *Contatti* sparivano sotto.

```diff
- height: 100vh;
- overflow-y: auto;
```

Senza vincolo di altezza la sidebar resta sticky quando ci sta nel viewport e scorre con la
pagina quando non ci sta: nulla è mai nascosto.

### 3.3 Scaglione intermedio mancante

C'era un solo breakpoint, a 880px. Fra 881 e ~1100px la colonna di testo scendeva a 441px
(~63 caratteri) contro i ~101 del desktop.

```css
@media (min-width: 881px) and (max-width: 1100px) {
  .shell { grid-template-columns: 250px 1fr; }
  .sidebar { padding: 2.5rem 1.5rem 2rem 1.5rem; }
  .main { padding: 3rem 2.25rem; }
  .page-title { font-size: 2.2rem; }
  .profile-img { width: 104px; height: 104px; }
}
```

### 3.4 Sidebar compressa su mobile

La sidebar precede `<main>` nel DOM, quindi su mobile occupava **1027px — 1,27 schermate di
scroll** prima di una riga di contenuto, su ogni pagina.

Nella media query `max-width: 880px` la sidebar diventa una fascia d'intestazione: foto a
68px accanto al nome, tagline di fianco, menu su righe orizzontali.

> **Perché non `order`.** Invertire sidebar e contenuto con `order` avrebbe disallineato
> l'ordine visivo da quello di tabulazione, violando *1.3.2 Meaningful Sequence* e
> *2.4.3 Focus Order*. La sidebar è stata compressa, non spostata.

Risultato: **da 1027 a 648px, −37%**, da 1,27 a 0,80 schermate.

### 3.5 Nessuno spostamento all'hover

```diff
- .nav a { transition: color 0.18s, padding 0.18s; }
- .nav a:hover { padding-left: 6px; }
+ .nav a { transition: color 0.18s; }
```

Il testo saltava sotto il cursore.

### 3.6 Allineamento della barra lingua

`.top-bar-inner` usava `max-width: 1400px` mentre `.shell` usa `1180px`: `EN IT ES` non
stavano sulla verticale della colonna.

```diff
- .top-bar-inner { max-width: 1400px; }
+ .top-bar-inner { max-width: var(--maxw); }
```

---

## 4. Metadati e SEO

### 4.1 Una sola richiesta a Google Fonts

```diff
- <link href="…css2?family=Crimson+Pro:ital,wght@0,400;…&display=swap" rel="stylesheet">
- <link href="…css2?family=Geist:wght@400;500;600&display=swap" rel="stylesheet">
+ <link href="…css2?family=Crimson+Pro:ital,wght@0,400;…&family=Geist:wght@400;500;600&display=swap" rel="stylesheet">
```

Un round-trip in meno sul percorso critico. Verificato che tutti e 17 i tagli di Crimson Pro
e Geist si carichino ancora.

### 4.2 Canonical

Assente su tutte e 21 le pagine (l'unico stava sulla root e puntava a `/en/`). Aggiunto su
ciascuna, nella forma `…/it/index.html` — **coerente con `sitemap.xml` e con i
`rel="alternate"` già presenti**.

### 4.3 Open Graph e Twitter card

Assenti: condividendo una pagina su LinkedIn o Bluesky usciva un'anteprima nuda. Aggiunti su
tutte e 21 le pagine, con `og:title` e `og:description` presi dal `<title>` e dalla
`<meta name="description">` già esistenti:

`og:type`, `og:site_name`, `og:locale` (+ due `og:locale:alternate`), `og:title`,
`og:description`, `og:url`, `og:image` (720×720, con `width`/`height`/`alt`),
`twitter:card = summary`.

### 4.4 JSON-LD `Person`

Aggiunto sulle tre home (`en/`, `it/`, `es/`): nome, titolo, affiliazione, `alumniOf`,
`knowsAbout`, ORCID come `identifier` di tipo `PropertyValue`, e `sameAs` verso ORCID,
Google Scholar, ResearchGate e LinkedIn.

---

## 5. Pulizia del CSS

**185 righe di regole morte rimosse** (verificato: zero occorrenze delle classi nell'HTML):

| Blocco | Righe | Nota |
|---|---|---|
| `.affiliations`, `.affiliations-label`, `.affiliations-list` | 50 | mai usate |
| `.logo-bar`, `.logo-bar-label`, `.logo-bar-items` | 47 | mai usate |
| primo blocco `.latest` / `.latest-label` / `.latest-list` | 46 | **interamente sovrascritto** dal secondo blocco più in basso; conteneva `.latest-list .when`, orfano perché l'HTML usa `.latest-date` |
| `.lang-switch` e varianti | 34 | mai usata (la barra lingua usa `.top-bar`) |
| `.entry-meta` | 8 | mai usata |
| variabile `--mono` | 1 | dichiarata, nessun font mono caricato, mai usata |

Il file passa da **943 a 916 righe**. Il diff complessivo è `+177 / −204`: delle 204 righe
rimosse, **185 sono i blocchi morti** qui sopra, le altre 19 sono righe riscritte. Le 177
aggiunte sono nuove regole e commenti che spiegano il perché di ogni scelta.

---

## 6. Cambiamenti visibili

L'aspetto è invariato tranne che in tre punti, tutti voluti:

1. **Le righe di testo sono più corte** (da ~101 a ~79 caratteri). È la modifica più
   percepibile: la colonna appare più stretta e con più margine a destra.
2. **`EN IT ES` sono pillole più grandi** e allineate alla colonna anziché al bordo pagina.
3. **Su mobile l'intestazione è compatta**: foto piccola accanto al nome, menu su due righe.

Non cambiano: font, palette, impaginato a due colonne, spaziature del contenuto, colori
degli accenti. Il testo secondario è appena più scuro (impercettibile, ma a norma).

---

## 7. Misure prima/dopo

Rilevate sulla pagina `it/index.html` a 1280×720, salvo dove indicato.

| | prima | dopo |
|---|---|---|
| Contrasto testo secondario (crema) | 4,30:1 ❌ | **5,36:1** ✅ |
| Contrasto testo secondario (bianco) | 4,50:1 ❌ | **5,60:1** ✅ |
| Contrasto pallino "in corso" | 3,81:1 ❌ | **5,93:1** ✅ |
| Bersaglio link lingua | 15×27 px ❌ | **45×32 px** ✅ |
| `<h1>` per pagina | 2 ❌ | **1** ✅ |
| Salti di livello nei titoli | h1→h3 in `projects` ❌ | **nessuno** ✅ |
| Landmark esposti | 3 | **5** ✅ |
| Skip link | assente ❌ | **presente, testato** ✅ |
| Sidebar nascosta a 1280×720 | 292 px ❌ | **0 px** ✅ |
| Riga di testo (riga piena) | ~101 caratteri | **~79** ✅ |
| Colonna di testo a 920px | 441 px | **550 px** ✅ |
| Mobile: scroll prima del contenuto | 1027 px (1,27 schermate) | **648 px (0,80)** ✅ |
| Richieste a Google Fonts | 2 | **1** |
| Righe di CSS | 943 | 916 (**−185 morte**) |

---

## 8. Cosa resta aperto

- **Mobile, ultimo tratto.** Scendere sotto i 648px richiede di spostare il blocco contatti
  dopo `<main>` nell'HTML di 21 pagine. Non fatto: cambia la struttura, va deciso a parte.
- **Font self-hosted.** Le due richieste sono state accorpate, ma i font restano serviti da
  Google. Ospitarli nel repo (~8 file `woff2`) toglierebbe il trasferimento di IP verso
  Google — rilevante per un pubblico europeo — e un round-trip.
- **`<footer>` come landmark `contentinfo`** (vedi § 2.3).
- **Tema scuro.** Il sito non ha `prefers-color-scheme`: chi ha il sistema in modalità scura
  vede comunque il fondo crema. Scelta legittima per un impaginato che imita la carta, ma
  non è mai stata una decisione esplicita.

---

## 9. Come verificare

```bash
git diff --stat
git diff assets/style.css
```

Anteprima locale:

```bash
python3 -m http.server 8765 --directory .
```

Poi aprire <http://localhost:8765/it/index.html> e controllare:

- **Tab** come primo tasto → compare *Salta al contenuto*; **Invio** porta il focus al contenuto.
- Ridurre la finestra a 720px di altezza → il menu della sidebar resta raggiungibile senza
  una seconda barra di scorrimento.
- Larghezza 920px → la colonna di testo resta a 550px.
- Larghezza 375px → il contenuto comincia entro la prima schermata.

Per annullare tutto:

```bash
git checkout -- .
```
