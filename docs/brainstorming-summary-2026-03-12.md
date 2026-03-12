# IntegrateHub.io — Brainstorming Summary
**Date:** March 12, 2026
**Context:** 13 articles published, approaching article #15 milestone

---

## 1. Kategorije — Strategija

**Odluka:** Zadržati business-tematske kategorije (po funkciji, ne po alatu).

**Razlog:** Čitaoci razmišljaju u terminima problema ("kako da automatizujem onboarding"), ne alata ("Typeform automation"). Business kategorije se poklapaju sa search intent-om i prirodno grupišu članke za internal linking.

**Trenutne kategorije:**
- lead-capture (4 članka)
- onboarding (3 članka)
- payments (2 članka)
- comparisons (2 članka)
- automation-strategy (1 članak)

**Buduće kategorije** (dodati kad imaju 3+ članka): reporting, invoicing, client-communication, project-management.

**"comparisons" outlier:** Zadržati kao kategoriju uprkos tome što nije poslovna funkcija — "hoću da uporedim alate" je validan use case.

**Odloženo:** Alat-bazirani tag sistem (sekundarna taksonomija) — razmotriti na 25-30 članaka.

---

## 2. input.txt — Razdvajanje na pojedinačne fajlove

**Problem:** 1.776 linija, 13 članaka, 77 internal link linija. Svaki novi članak zahteva editovanje 3-8 starijih članaka za internal linkove.

**Odluka:** Opcija A — razbiti na `content/[slug].txt` fajlove.

**Implementacija:**
- `content/` folder sa po jednim `.txt` fajlom po članku
- Generator čita sve `.txt` fajlove iz foldera umesto jednog input.txt
- Separator `---` više nije potreban
- Format unutar fajla ostaje identičan (isti tagovi)
- Jednom podeliti postojeći input.txt na 13 fajlova (trivijalan skript)

**Automatski internal linkovi:** Odloženi do 25-30 članaka. Za sad ručno kuriranje je bolje za SEO.

**Timeline:** Na 15-18 članaka.

---

## 3. Baza podataka — Supabase migracija

**Problem:** File-based pristup puca na ~25-30 članaka (maintenance, internal link graf, stale pricing tracking).

**Odluka:** Supabase (Postgres) umesto SQLite.

**Zašto Supabase:**
- Table Editor = besplatan CRUD UI out of the box (zamenjuje custom editing tool u ranoj fazi)
- REST API automatski generisan
- Free tier (500MB) — nikad nećeš probiti sa 100 članaka

**Shema (pojednostavljena, body ostaje text blob):**
```
articles        → slug, title, type, category, status, date, meta, intro, body, build_time
internal_links  → source_id, target_id
screenshots     → article_id, filename, date_captured
pricing_claims  → article_id, tool_name, last_verified
faq_items       → article_id, question, answer
```

**Workflow promena:** Supabase (edit u browseru) → generator.py (čita iz Supabase API) → HTML → Cloudflare

**Timeline:**
| Milestone | Akcija |
|---|---|
| 15-18 članaka | Split input.txt na pojedinačne fajlove |
| ~20 članaka | Kreiraj Supabase tabele, migriraj podatke |
| ~20-25 članaka | Preradi generator.py da čita iz Supabase API |
| 25-30 članaka | Po potrebi: custom dashboard za link graf i alerts |

---

## 4. Sajt redesign — Inspiracija i plan

**Referentni sajt:** ainalysis.pro — čist layout, kategorijske kartice, sticky TOC, progress bar.

### Elementi za implementaciju

**Faza 1 (~15 članaka, uz category pages):**
- Homepage hero tekst + CTA
- Kategorijske kartice ispod hero-a ("Browse by Topic" sa brojem članaka)
- "Latest tutorials" sekcija (poslednih 4-6 članaka kao card grid)
- Navigacija: kategorije u headeru (flat linkovi ili dropdown)
- Puniji footer (kategorije + site linkovi + newsletter)
- Reading progress bar (trivijalna implementacija, ~15 linija CSS/JS)
- Header sa logomark + tekst umesto plain text

**Faza 2 (~20-25 članaka):**
- Sticky sidebar TOC (zahteva layout promenu na dvostubačni)
- Active section highlighting u TOC (IntersectionObserver)
- "Continue reading" kartice na dnu svakog članka
- Featured section na homepage za cornerstone članke

**Ne dirati:** članak layout (funkcionalan), boje/tipografija (rade), newsletter CTA pozicija.

**Trade-off za sticky sidebar TOC:** Smanjuje content width sa 1060px na ~750px — screenshotovi postaju manji. Razmotriti floating TOC kao alternativu.

---

## 5. Branding

**Ime:** IntegrateHub.io ostaje. Generično ali za anonymous affiliate sajt ime nije bitno — čitaoci dolaze sa Google-a, ne po imenu. Newsletter ime "The Automation Fix" je pamtljivije — razmotriti kao primarni brand na Checkpoint 2.

**Ne menjati domen** — 13 indeksiranih članaka, rani page 1 rankovi.

### Vizuelni identitet — šta je napravljeno

**Novi logomark:** Variation 6C — centralni hub krug + 4 connected endpoint čvora (zaobljeni kvadrati). Razvijen kroz iterativan AI process (Gemini) od koncepta do finalnog marka.

**Logo paket (SVG + PNG):**

| Fajl | Lokacija | Namena |
|---|---|---|
| favicon.png (32px) | `public/` | Browser tab |
| apple-touch-icon.png (192px) | `public/` | iOS/Android |
| favicon-512.png | `public/assets/branding/` | PWA |
| logomark-blue.svg | `public/assets/branding/` | Primarni mark, plavi na transparentnom |
| logomark-black.svg | `public/assets/branding/` | Monochrome verzija |
| logomark-white.svg | `public/assets/branding/` | Za tamne/plave pozadine |
| favicon.svg | `public/assets/branding/` | White on blue, rounded square |
| logo-full-horizontal.svg | `public/assets/branding/` | Mark + tekst za header |
| logo-full-horizontal.png | `public/assets/branding/` | Raster verzija (napraviti u Figmi) |
| og-default.png (1200x630) | `public/assets/branding/` | Social sharing default |

**Template promene (za sledeći deploy):**
```html
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:image" content="https://integratehub.io/assets/branding/og-default.png">
```

---

## 6. Prioritizovani akcioni plan

### Odmah (sledeći deploy)
- [ ] Sačuvaj logo paket u `public/assets/branding/`
- [ ] favicon.png i apple-touch-icon.png u `public/` root
- [ ] Zameni stari inline SVG favicon u template.html
- [ ] Dodaj og:image meta tag u template.html
- [ ] Dodaj reading progress bar u template.html

### Narednih 30 dana
- [ ] Završi članak #14 (Make.com vs Zapier comparison)
- [ ] Završi članak #15 (weekly client report automation)
- [ ] Homepage redesign: hero + kategorijske kartice + latest tutorials
- [ ] Navigacija: kategorije u headeru
- [ ] Header: logomark + tekst umesto plain text
- [ ] Puniji footer
- [ ] Welcome email sequence u Beehiivu
- [ ] logo-full-horizontal.png napraviti u Figmi

### Na 15-18 članaka
- [ ] Split input.txt na pojedinačne `content/[slug].txt` fajlove
- [ ] Generator.py refactor: čita direktorijum umesto jednog fajla
- [ ] Category pages u generator.py

### Na 20-25 članaka
- [ ] Supabase tabele + migracija
- [ ] Generator.py: čita iz Supabase API
- [ ] Sticky TOC + "Continue reading" sekcija
- [ ] Article card baner template (Canva/Figma) za thumbnailove

### Na 25-30 članaka
- [ ] Custom dashboard za stale content alerts
- [ ] Automatski internal linkovi (hibrid: ručni + auto-dopuna)

---

## Ažuriranja za projektne fajlove

**CONTEXT.md — dodati:**
- Logo paket lokacija i naming convention
- Favicon/og:image meta tagovi
- Progress bar implementacija
- Category pages kao generator feature

**CONTENT.md — dodati:**
- Napomena o nadolazećem input.txt split-u
- Kategorizacija sa brojem članaka

**STRATEGY-v2.md — ne menjati sad** (sledeći review: Checkpoint 1, September 2026)
