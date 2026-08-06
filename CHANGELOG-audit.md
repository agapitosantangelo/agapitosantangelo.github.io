# Audit di accessibilità e design — modifiche applicate

**Branch:** `audit-accessibilita-design`
**Riferimento:** commit `ad6b055` (stato di `main` prima dell'audit)
**Ambito:** le 21 pagine di contenuto (`en/`, `it/`, `es/` × 7) e `assets/style.css`

Nessun contenuto testuale è stato riscritto: le modifiche riguardano struttura semantica,
accessibilità, tipografia, responsività e metadati.

> **Come leggere questo documento.** I blocchi `diff` sono **estratti illustrativi**, non
> l'output letterale di `git diff`: omettono righe di contesto e i commenti aggiunti al CSS.
> Il diff autorevole è `git diff ad6b055`.

> **Sulle citazioni WCAG.** Solo due modifiche sanano una non conformità reale (§ 1.1 e § 1.2).
> Le altre sono miglioramenti di usabilità, di supporto alle tecnologie assistive o di buona
> pratica, e sono classificate come tali: dove un criterio è di livello AAA, o dove non è
> tecnicamente violato, è detto esplicitamente. Vedi § 2.

> ⚠️ **Stato del repository.** Parte di queste modifiche è già stata committata nel commit
> `6f5456c`, che le ha impacchettate insieme a un aggiornamento di contenuti indipendente. In
> quell'operazione le tre pagine `research.html` hanno **perso** le correzioni dell'audit; sono
> state riapplicate e sono fra le modifiche non ancora committate. Vedi § 11.

---

## Indice

1. [Non conformità sanate](#1-non-conformità-sanate)
2. [Miglioramenti di accessibilità (non correzioni di conformità)](#2-miglioramenti-di-accessibilità-non-correzioni-di-conformità)
3. [Struttura semantica](#3-struttura-semantica)
4. [Tipografia e responsività](#4-tipografia-e-responsività)
5. [Metadati e SEO](#5-metadati-e-seo)
6. [Pulizia del CSS](#6-pulizia-del-css)
7. [Un bug di specificità risolto](#7-un-bug-di-specificità-risolto)
8. [Una regressione introdotta e corretta](#8-una-regressione-introdotta-e-corretta)
9. [Cambiamenti visibili](#9-cambiamenti-visibili)
10. [Misure prima/dopo](#10-misure-primadopo)
11. [Stato del repository e come verificare](#11-stato-del-repository-e-come-verificare)
12. [Cosa resta aperto](#12-cosa-resta-aperto)

---

## 1. Non conformità sanate

### 1.1 Contrasto del testo secondario — *1.4.3 Contrast (Minimum)*, **AA** ✔ violazione reale

`--ink-mute` valeva `#7a7674`: **4,30:1** su crema e **4,4957:1** su bianco. Il colore è usato su
testo che va da **11,9 a 15,3 px**, quindi testo *normale* per WCAG, soglia 4,5:1. Falliva su
45 elementi della sola home: date, `entry-venue`, `exp-keywords`, `skills-grid dt`, footer,
barra lingua, `project-meta`, didascalie.

```diff
- --ink-mute: #7a7674;
+ --ink-mute: #6b6764;
```

Risultato: **5,36:1** su crema, **5,60:1** su bianco. La tinta si sposta leggermente
(20,0° → 25,7° in HSL): scostamento non percepibile, ma non è lo stesso colore solo più scuro.

### 1.2 Scorciatoia al contenuto — *2.4.1 Bypass Blocks*, **A** ✔ violazione reale

Su ogni pagina **16 link precedevano `<main>`**: 2 di lingua, dipartimento, email, CV, 4 social,
7 voci di menu — un blocco ripetuto identico su tutte le pagine, da riattraversare ogni volta,
senza alcun meccanismo per saltarlo. (Foto e nome non sono focalizzabili e non contano.)

```diff
  <body>
+ <a class="skip-link" href="#contenuto">Salta al contenuto</a>
...
- <main class="main">
+ <main class="main" id="contenuto" tabindex="-1">
```

`tabindex="-1"` serve perché il focus si sposti davvero su `<main>`, non solo il punto di
ripartenza della tabulazione. Testato: il focus atterra su `<main>` e il Tab successivo è già
dentro il contenuto. Etichette localizzate (*Salta al contenuto* / *Skip to content* /
*Saltar al contenido*); l'ancora resta `#contenuto` in tutte le lingue perché è un
identificatore interno, non visibile.

---

## 2. Miglioramenti di accessibilità (non correzioni di conformità)

Tutto ciò che segue migliora l'esperienza, ma **non** sanava una non conformità AA. Lo dico
esplicitamente perché la prima stesura di questo documento citava criteri sbagliati.

### 2.1 Dimensione dei bersagli nella barra lingua

Misure sul commit base a 1280×720: **EN 22,8×27,2 · IT 15,3×28,2 · ES 21,7×27,2 px**
(`IT` è il più stretto perché è la lingua attiva e ha 1px di `border-bottom` in più).

> **Non era una violazione di 2.5.8 Target Size (Minimum).** Il criterio prevede l'eccezione
> *Spacing*: i bersagli sottodimensionati sono ammessi se un cerchio di 24px di diametro
> centrato su ciascuno non interseca gli altri. I centri distavano 37,1px e 36,5px — ben oltre
> i 24 richiesti. L'ingrandimento resta un miglioramento d'uso, soprattutto da mobile.

```diff
  .top-bar a,
  .top-bar .active {
+   display: inline-flex;
+   align-items: center;
+   justify-content: center;
+   min-width: 2.5rem;
+   min-height: 1.75rem;
-   padding: 0.15rem 0;
+   padding: 0.25rem 0.5rem;
  }
```

Ora tutti e tre misurano **45 × 31,5 px**.

### 2.2 Dimensione del carattere rispettosa delle preferenze

`html, body { font-size: 18px }` ignorava la dimensione di carattere predefinita impostata
dall'utente nel browser.

> **Non era una violazione di 1.4.4 Resize Text.** Quel criterio chiede solo che il testo possa
> essere ingrandito fino al 200%, e lo zoom del browser lo soddisfa comunque. Usare unità
> relative sulla root resta buona pratica, ma nessun criterio AA la impone.

```diff
+ html {
+   font-size: 112.5%;
+ }
  html, body {
-   font-size: 18px;
  }
  body {
+   font-size: 1rem;
```

> ⚠️ **Trappola.** La percentuale deve stare **solo su `html`**. Su `html, body` si compone:
> `html` diventa 18px e `body` 112,5% *di 18* = 20,25px, ingrandendo tutto il sito del 12,5%.
> È l'errore che ho commesso al primo tentativo; per questo `body` riceve `font-size: 1rem`.

### 2.3 Focus visibile esplicito

Non era mai definito: si ereditava l'anello di default del browser — **presente e quindi
conforme a 2.4.7 Focus Visible**, ma sottile e quasi invisibile sul bottone CV nero.

```css
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
  border-radius: 1px;
}
.cv-button:focus-visible { outline-color: var(--accent-h); outline-offset: 3px; }
main:focus, main:focus-visible { outline: none; }
```

### 2.4 Il pallino "posizione attuale"

Il pallino verde davanti alle date significava "posizione attuale". Il contenuto generato
`"● "` veniva letto dagli screen reader come glifo, senza spiegare cosa volesse dire.

> **Non era una violazione di 1.4.1 Use of Color.** L'informazione era veicolata dalla
> *presenza di una forma*, non dalla tinta, quindi 1.4.1 non era in gioco. E un testo
> `.sr-only` è invisibile per costruzione: non avrebbe potuto sanarla comunque. Ciò che si
> corregge davvero è l'informazione non testuale per le tecnologie assistive, più il contrasto.

```diff
  .exp-date.current::before {
-   content: "● ";
-   color: #6a8859;
-   font-size: 0.7em;
-   vertical-align: 1px;
+   content: "";
+   display: inline-block;
+   width: 0.45em; height: 0.45em;
+   border-radius: 50%;
+   background: #4f6841;
+   margin-right: 0.4em;
+   vertical-align: 0.08em;
  }
```

```diff
- <div class="exp-date current">Set 2024 — In corso</div>
+ <div class="exp-date current"><span class="sr-only">Posizione attuale — </span>Set 2024 — In corso</div>
```

Il verde passa da 3,81:1 a **5,93:1**. Aggiunta l'utility `.sr-only`.

**Effetto collaterale coperto:** un disco disegnato con `background` sparirebbe in modalità a
colori forzati (Contrasto elevato di Windows), dove gli sfondi vengono sovrascritti dal sistema
— cosa che il vecchio glifo di testo non faceva. Aggiunta quindi:

```css
@media (forced-colors: active) {
  .exp-date.current::before { background: CanvasText; }
  :focus-visible { outline-color: Highlight; }
}
```

### 2.5 Lingua corrente esposta alle tecnologie assistive

La lingua attiva era `<a class="active">IT</a>`: un'ancora senza `href`, quindi non
focalizzabile e non annunciata come link, e senza indicazione di stato.

```diff
- <a class="active">IT</a>
+ <a class="active" href="index.html" hreflang="it" lang="it" aria-current="true">IT</a>
```

Un **link a se stesso**, come già fa la voce di menu attiva (`<a class="current" href="…"
aria-current="page">`). Il primo tentativo usava uno `<span aria-current="true">`: risolveva
metà del problema, perché uno `<span>` senza `role` mappa su `generic` e gli screen reader non
annunciano `aria-current` in modo affidabile sui contenitori generici. Il link lo garantisce.

Il selettore CSS passa da `.top-bar a.active` a `.top-bar .active`; il bordo inferiore diventa
`box-shadow: inset` per non alterare il box ora che l'elemento ha dimensioni minime.

### 2.6 Etichette e lingua dei link

`aria-label="Language"` era in inglese anche sulle pagine italiane e spagnole.

```diff
- <nav class="top-bar" aria-label="Language">
+ <nav class="top-bar" aria-label="Lingua">        <!-- Language / Idioma -->
- <a href="../en/index.html">EN</a>
+ <a href="../en/index.html" hreflang="en" lang="en">EN</a>
```

`lang` fa sì che lo screen reader pronunci "EN" e "ES" con la fonetica giusta.

### 2.7 Link esterno che apre una nuova scheda

```diff
- <a class="cv-button" href="../assets/cv.pdf" target="_blank">Scarica il CV (PDF)</a>
+ <a class="cv-button" href="../assets/cv.pdf" target="_blank" rel="noopener">Scarica il CV (PDF)<span class="sr-only"> (si apre in una nuova scheda)</span></a>
```

### 2.8 Movimento ridotto — *2.3.3*, livello **AAA**

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Criterio **AAA**, non AA. E nel foglio di stile non ci sono animazioni né `scroll-behavior`:
due delle tre dichiarazioni sono oggi inerti, e restano come rete per aggiunte future.

---

## 3. Struttura semantica

### 3.1 Un solo `<h1>` per pagina

Ogni pagina ne aveva due: il nome nella sidebar e il titolo di pagina.

```diff
- <h1 class="name">Agapito E.<br>Santangelo, PhD</h1>
+ <p class="name">Agapito E.<br>Santangelo, PhD</p>
```

> Due `<h1>` **non** violano 1.3.1: HTML li ammette e la struttura resta determinabile
> programmaticamente. È buona pratica di navigazione — con un solo `h1` chi usa uno screen
> reader capisce subito su quale pagina si trova.

La classe `.name` definisce già font, corpo, peso e margini: l'aspetto non cambia.

### 3.2 Gerarchia dei titoli in `projects.html`

La pagina non aveva alcun `<h2>`: passava da `<h1>` a cinque `<h3>`. I `<h3 class="project-title">`
sono diventati `<h2>`, e il CSS annulla le decorazioni che `h2` porta con sé:

```css
.project-title { border-bottom: none; padding-bottom: 0; }
.project-title::before { content: none; }   /* il "§ " dei titoli di sezione */
```

Verificato su tutte e 21 le pagine: un solo `h1` ciascuna, nessun salto di livello.

### 3.3 Landmark

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

**I landmark passano da 3 a 4**: `nav[Lingua]`, `aside`, `nav[Navigazione del sito]`, `main`.
Il `<footer>` **non** aggiunge un landmark: si trova dentro `<main>`, e per la mappatura
HTML-AAM assume il ruolo `contentinfo` solo quando ha come scope il `<body>`. Il guadagno è di
semantica dell'elemento, non di navigazione per landmark.

> **Nota su `display: contents`.** Il wrapper `.site-nav` usa `margin: 0; padding: 0`, non
> `display: contents`. Il motivo storico — che quella proprietà cancella l'elemento dall'albero
> di accessibilità — **non è più attuale**: il bug è stato corretto in Firefox nel 2019 e in
> Chrome nel 2021, e su un `<nav>` wrapper oggi il landmark sopravvive. Restano regressioni note
> in Safari su tabelle e web component, quindi la scelta conservativa resta ragionevole, ma non
> per la ragione che avevo scritto inizialmente.

---

## 4. Tipografia e responsività

### 4.1 Lunghezza di riga

`p { max-width: 70ch }` produceva righe piene con una media di **97 caratteri** (massimo 110);
l'intervallo comodo è 45–75.

L'unità `ch` è la larghezza dello zero. Crimson Pro ha lo zero largo ma il carattere medio
stretto, quindi `ch` **sovrastima parecchio**.

```diff
- p     { max-width: 70ch; }
+ p     { max-width: 54ch; }
- .lead { max-width: 64ch; }
+ .lead { max-width: 50ch; }
```

Misurato dopo: media **78 caratteri**, massimo 89.

### 4.2 Sidebar tagliata sui portatili

`height: 100vh` + `overflow-y: auto`: il contenuto della sidebar è alto **1012px**, quindi su un
viewport da 720px **292px finivano in una seconda barra di scorrimento** e le voci
*Divulgazione* e *Contatti* sparivano sotto.

```diff
- position: sticky;
- top: 0;
- height: 100vh;
- overflow-y: auto;
```

Va tolto **anche lo sticky**, non solo il vincolo di altezza — vedi § 8, dove è spiegato perché.
Ora la sidebar scorre con la pagina e tutto resta raggiungibile e visibile.

Effetto collaterale accettato: il filetto verticale e la sfumatura di sfondo non arrivano più
in fondo alla finestra, ma finiscono dove finisce il contenuto.

### 4.3 Scaglione intermedio mancante

C'era un solo breakpoint, a 880px. Fra 881 e ~1100px la colonna di testo si stringeva molto:
**417px a 881px di finestra**, 441px a 920px, 636px a 1100px — contro i 712px del desktop.

```css
@media (min-width: 881px) and (max-width: 1100px) {
  .shell   { grid-template-columns: 250px 1fr; }
  .sidebar { padding: 2.5rem 1.5rem 2rem 1.5rem; }
  .main    { padding: 3rem 2.25rem; }
  .page-title { font-size: 2.2rem; }
  .profile-img { width: 104px; height: 104px; }
}
```

Con questo scaglione la colonna resta **≥ 550px** in tutta la fascia, cioè al valore imposto dal
`max-width: 54ch`: la misura di riga è la stessa del desktop a qualunque larghezza.

### 4.4 Sidebar compressa su mobile

La sidebar precede `<main>` nel DOM, quindi su mobile occupava **1027px** prima di una riga di
contenuto, su ogni pagina — circa 1,26 schermate su un 375×812.

Nella media query `max-width: 880px` diventa una fascia d'intestazione:

- foto ridotta a 68px e affiancata al nome, con la tagline di fianco;
- `.name` da 1,55rem a 1,3rem, `.tagline` da 0,85rem a 0,8rem;
- padding della sidebar da `2rem 1.5rem` a `1.5rem 1.5rem 1.25rem`;
- blocchi contatti/CV/social a tutta larghezza con margini più stretti;
- menu su righe orizzontali invece che su sette righe, con `.nav a { padding: 0.45rem 0 }`
  che porta il bersaglio tattile a 42px di altezza.

> **Perché non `order`.** Invertire sidebar e contenuto con `order` avrebbe disallineato
> l'ordine visivo da quello di tabulazione, violando *1.3.2 Meaningful Sequence* e
> *2.4.3 Focus Order*. La sidebar è stata compressa, non spostata.

Risultato: **da 1027 a 648px, −37%** (da ~1,26 a ~0,80 schermate a 812px di altezza).

### 4.5 Nessuno spostamento all'hover

```diff
- .nav a       { transition: color 0.18s, padding 0.18s; }
- .nav a:hover { padding-left: 6px; }
+ .nav a       { transition: color 0.18s; }
```

Il testo saltava sotto il cursore.

### 4.6 Allineamento della barra lingua

```diff
- .top-bar-inner { max-width: 1400px; }
+ .top-bar-inner { max-width: var(--maxw); }
```

`.shell` usa `1180px`: `EN IT ES` non stavano sulla verticale della colonna.

---

## 5. Metadati e SEO

### 5.1 Una sola richiesta a Google Fonts

```diff
- <link href="…css2?family=Crimson+Pro:ital,wght@0,400;…&display=swap" rel="stylesheet">
- <link href="…css2?family=Geist:wght@400;500;600&display=swap" rel="stylesheet">
+ <link href="…css2?family=Crimson+Pro:ital,wght@0,400;…&family=Geist:wght@400;500;600&display=swap" rel="stylesheet">
```

Una richiesta HTTP in meno — **non** un round-trip: le due partivano già in parallelo sulla
stessa connessione HTTP/2, e i `preconnect` erano e restano invariati. Verificato che i
**9 tagli** richiesti (6 di Crimson Pro, 3 di Geist) continuino a caricarsi.

### 5.2 Canonical

Assente su tutte e 21 le pagine. Aggiunto su ciascuna nella forma `…/it/index.html`, **coerente
con i `<loc>` di `sitemap.xml`** e con i `rel="alternate"` già presenti.

*Residuo noto:* la `index.html` di root non è stata toccata e mantiene il suo `canonical`
verso `/en/`.

### 5.3 Open Graph e Twitter card

Assenti: condividendo una pagina su LinkedIn o Bluesky usciva un'anteprima nuda. Aggiunti su
tutte e 21 le pagine, con `og:title` e `og:description` presi dal `<title>` e dalla
`<meta name="description">` già esistenti: `og:type`, `og:site_name`, `og:locale` (+ due
`og:locale:alternate`), `og:title`, `og:description`, `og:url`, `og:image` (720×720, con
`width`/`height`/`alt`), `twitter:card = summary`.

*Semplificazione nota:* `og:type` è `profile` su tutte le pagine, anche quelle che profilo non
sono, e senza le proprietà `profile:*` che la specifica associa a quel tipo. Nessun crawler lo
penalizza, ma `website` sarebbe più corretto sulle pagine non-profilo.

### 5.4 JSON-LD `Person`

Aggiunto sulle tre home: nome, titolo, affiliazione, `alumniOf`, `knowsAbout`, ORCID come
`identifier`, e `sameAs` verso ORCID, Google Scholar, ResearchGate e LinkedIn. Verificato che il
JSON sia sintatticamente valido in tutte e tre.

---

## 6. Pulizia del CSS

**140 righe di regole realmente morte rimosse** (zero occorrenze delle classi in tutto l'HTML
del repository, incluse la root e `mondiale2026/`):

| Blocco | Righe |
|---|---|
| `.affiliations`, `.affiliations-label`, `.affiliations-list` | 50 |
| `.logo-bar`, `.logo-bar-label`, `.logo-bar-items` | 47 |
| `.lang-switch` e varianti | 34 |
| `.entry-meta` | 8 |
| variabile `--mono` (dichiarata, nessun font mono caricato) | 1 |

A queste si aggiungono le **46 righe del primo blocco `.latest`**, che però *non* erano morte:
vedi § 7.

Il file passa da **943 a 929 righe**; il diff è `+192 / −206`.

---

## 7. Un bug di specificità risolto

Il primo dei due blocchi `.latest` **non era codice morto**, ed è giusto dirlo apertamente:
inizialmente l'avevo classificato così.

L'HTML è `<ul class="latest-list"><li class="latest-item">`. Il foglio di stile conteneva due
serie di regole in conflitto:

| | specificità | padding | gap | separatore |
|---|---|---|---|---|
| `.latest-list li` (primo blocco) | 0-1-1 | `0.35rem 0` | `0.8rem` | `dotted` |
| `.latest-item` (secondo blocco) | 0-1-0 | `0.7rem 0` | `1rem` | `dashed` |

`.latest-list li` vinceva per specificità, **indipendentemente dall'ordine**. Le regole
`.latest-item` — evidentemente le più recenti, visto che è la classe usata nell'HTML, ed
equipaggiate di `:first-child` / `:last-child` — erano silenziosamente annullate.

Rimuovere il primo blocco risolve il conflitto a favore delle seconde. Conseguenze:

- nel riquadro **Aggiornamenti** delle tre home ogni voce guadagna spazio verticale e il
  separatore passa da punteggiato a tratteggiato;
- su mobile si attiva la media query `.latest-item { grid-template-columns: 1fr }`, prima
  inefficace per lo stesso motivo: la data non occupa più una colonna fissa da 90px su uno
  schermo da 375px.

Entrambe sono migliorie, ma sono **cambiamenti di aspetto**, non pulizia. Se preferisci
l'aspetto precedente, la strada corretta non è ripristinare il blocco rimosso ma alzare la
specificità delle regole che vuoi far vincere.

---

## 8. Una regressione introdotta e corretta

Vale la pena documentarla, perché è controintuitiva.

Per risolvere la sidebar tagliata (§ 4.2) il primo tentativo è stato togliere `height: 100vh` e
`overflow-y: auto`, **lasciando `position: sticky; top: 0`**. Ragionamento: senza vincolo di
altezza la sidebar scorre con la pagina.

**Sbagliato.** Un elemento `sticky` più alto del viewport si blocca a `top: 0` e la sua parte
bassa resta permanentemente fuori schermo. Peggio: senza più il contenitore scrollabile, il
browser non riesce nemmeno a portare in vista la voce che riceve il focus da tastiera.

Misurato a 1280×720, portando il focus su *Contatti*:

| | risultato |
|---|---|
| Prima (`height:100vh` + `overflow-y:auto`) | il contenitore si auto-scrolla → voce **visibile** |
| Primo tentativo (solo sticky) | pagina scrollata a 653px, voce a top **936** → **fuori schermo** |
| Correzione (`position: static`) | pagina scrollata a 653px, voce a top **340** → **visibile** |

Il vecchio CSS nascondeva 292px dietro una seconda barra, ma li rendeva raggiungibili. Il primo
tentativo li rendeva irraggiungibili. Solo togliendo anche lo sticky il problema è risolto
davvero.

Costo: sopra i 1100px la sidebar non resta più agganciata in cima durante lo scorrimento.

---

## 9. Cambiamenti visibili

1. **Le righe di testo sono più corte** — da ~97 a ~78 caratteri di media. È la modifica più
   percepibile: la colonna appare più stretta, con più margine a destra.
2. **`EN IT ES` sono pillole più grandi** e allineate alla colonna anziché al bordo pagina.
3. **Su mobile l'intestazione è compatta**: foto piccola accanto al nome, nome e tagline
   rimpiccioliti, menu su due righe.
4. **Il riquadro Aggiornamenti è più arioso**, col separatore tratteggiato (§ 7).
5. **Fra 881 e 1100px** la sidebar è più stretta (250px invece di 320) e il contenuto ha meno
   padding (40,5px invece di 72 per lato).
6. **La sidebar non resta più agganciata in cima** durante lo scorrimento (§ 8).
7. **Il pallino "in corso"** è un disco leggermente più piccolo, più scuro e più distanziato.
8. **Le voci di menu non si spostano più** al passaggio del cursore.
9. **Il filetto verticale della sidebar** finisce dove finisce il suo contenuto, non più in
   fondo alla finestra.

Non cambiano: i font, la palette di base, l'impaginato a due colonne sopra i 1100px, il colore
d'accento dei link. Il testo secondario è appena più scuro — impercettibile, ma a norma.

---

## 10. Misure prima/dopo

Rilevate su `it/index.html` a 1280×720, salvo dove indicato.

| | prima | dopo |
|---|---|---|
| Contrasto testo secondario (crema) | 4,30:1 ❌ | **5,36:1** ✅ |
| Contrasto testo secondario (bianco) | 4,496:1 ❌ | **5,60:1** ✅ |
| Contrasto pallino "in corso" | 3,81:1 | **5,93:1** ✅ |
| Bersaglio link lingua (il più stretto, `IT`) | 15,3×28,2 px | **45×31,5 px** |
| `<h1>` per pagina | 2 | **1** |
| Salti di livello nei titoli | h1→h3 in `projects` | **nessuno** |
| Landmark esposti | 3 | **4** |
| Skip link | assente ❌ | **presente, testato** ✅ |
| Voce di menu «Contatti» raggiunta col Tab, a 720px | visibile solo dentro uno scroller annidato | **visibile nella pagina** |
| Riga di testo (media / massimo) | 97 / 110 caratteri | **78 / 89** |
| Colonna di testo a 920px | 441 px | **550 px** |
| Mobile (375×812): scroll prima del contenuto | 1027 px (~1,26 schermate) | **648 px (~0,80)** |
| Richieste a Google Fonts | 2 | **1** |
| Righe di CSS | 943 | 929 (**−140 morte**) |

❌ = non conformità WCAG AA sanata. Le altre righe sono miglioramenti (§ 2).

---

## 11. Stato del repository e come verificare

Sul branch `audit-accessibilita-design`:

| Commit | Contenuto |
|---|---|
| `ad6b055` | stato di `main`, prima dell'audit |
| `6f5456c` | aggiornamento contenuti dal CV **+ gran parte dell'audit**, impacchettati insieme |
| `e32367f` | link contestuali ricerca ↔ progetti |
| *non committato* | `assets/style.css`, tutte e 21 le pagine, questo file |

⚠️ Il commit `6f5456c` ha sovrascritto le tre `research.html` con la versione precedente
all'audit, facendo perdere loro tutte le correzioni. Sono state riapplicate e sono fra le
modifiche non committate. **Non fare il push senza includerle**, o `research.html` resterà
l'unica pagina non conforme in tutte e tre le lingue.

Verifica strutturale — non deve stampare nulla:

```bash
for f in en/*.html it/*.html es/*.html; do
  for k in 'class="skip-link"' 'id="contenuto"' '<nav class="site-nav"' \
           '<footer class="foot">' 'rel="canonical"' 'property="og:title"' 'aria-current'; do
    grep -q "$k" "$f" || echo "MANCA $k in $f"
  done
done
```

Anteprima locale:

```bash
python3 -m http.server 8765 --directory .
```

Su <http://localhost:8765/it/index.html> controllare:

- **Tab** come primo tasto → compare *Salta al contenuto*; **Invio** porta il focus al contenuto.
- Finestra alta 720px, poi Tab fino a *Contatti* → la voce deve essere **visibile**, senza
  seconda barra di scorrimento.
- Larghezza 920px → la colonna di testo resta a 550px.
- Larghezza 375px → il contenuto comincia entro la prima schermata.

Per annullare le sole modifiche non committate:

```bash
git checkout -- .
```

---

## 12. Cosa resta aperto

- **Mobile, ultimo tratto.** Scendere sotto i 648px richiede di spostare il blocco contatti dopo
  `<main>` nell'HTML di 21 pagine. Cambia la struttura, va deciso a parte.
- **Font self-hosted.** Le due richieste sono state accorpate, ma i font restano serviti da
  Google. Ospitarli nel repo (~8 file `woff2`) toglierebbe il trasferimento di IP verso Google
  — rilevante per un pubblico europeo — e una richiesta di rete.
- **Sidebar agganciata.** Sopra i 1100px, dove ci starebbe nel viewport, si potrebbe
  reintrodurre lo sticky con una media query dedicata sull'altezza (`@media (min-height: 1100px)`).
- **`<footer>` come landmark `contentinfo`** (§ 3.3).
- **`canonical` della root** che punta ancora a `/en/` (§ 5.2).
- **`og:type`** uniforme a `profile` anche sulle pagine non-profilo (§ 5.3).
- **Tema scuro.** Il sito non ha `prefers-color-scheme`: chi ha il sistema in modalità scura
  vede comunque il fondo crema. Scelta legittima per un impaginato che imita la carta, ma non è
  mai stata una decisione esplicita.
