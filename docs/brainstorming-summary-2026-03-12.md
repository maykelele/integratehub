# IntegrateHub.io — Brainstorming Summary
**Date:** March 13, 2026 (updated after design/category implementation session)
**Context:** 13 articles published, approaching article #15 milestone

---

## 1. Kategorije — Strategija

**Odluka:** Zadržati business-tematske kategorije (po funkciji, ne po alatu).

**Razlog:** Čitaoci razmišljaju u terminima problema ("kako da automatizujem onboarding"), ne alata ("Typeform automation"). Business kategorije se poklapaju sa search intent-om i prirodno grupišu članke za internal linking.

**Trenutne kategorije:**
- lead-capture (4 članka) ✅ aktivna (category page generisan)
- onboarding (4 članka) ✅ aktivna (category page generisan)
- payments (2 članka) — ispod praga
- comparisons (2 članka) — ispod praga (dodaj #14 Make.com vs Zapier → aktivira se)
- automation-strategy (1 članak) — ispod praga

**Prag za aktivaciju:** 3+ članaka (konfigurisano u `CATEGORY_MIN_ARTICLES` u generator.py). Kategorija sa <3 članaka i dalje radi u breadcrumbu i article meta, ali nema svoju stranicu niti se pojavljuje u navigaciji.

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
- ~~Reading progress bar~~ ✅ Implementiran (ispod sticky headera, prati header automatski)
- ~~Header sa logomark + tekst umesto plain text~~ ✅ Implementiran (logo-full-horizontal.png, height: 32px)
- ~~Puniji footer~~ ✅ Implementiran (3 kolone: Site, Browse by Topic, Stay Updated)
- ~~Scroll-to-top dugme~~ ✅ Implementirano (gornji centar, pojavljuje se samo pri scroll-up, nestaje pri scroll-down)
- ~~Header navigacija~~ ✅ Implementirano (March 12): "Topics ▾" dropdown pill + "Comparisons" shortcut pill + search icon (placeholder). Desktop-only — mobile zadržava "← All Guides".
- ~~Category pages~~ ✅ Implementirano (March 13): `/category/[slug]/index.html`, dinamički generisane samo za kategorije sa 3+ članaka. Filtrirani card grid, intro opis iz CATEGORIES dict-a, breadcrumb Home › Category.
- ~~Homepage redesign~~ ✅ Implementirano (March 13): Hero (naslov + tagline + CTA) → Browse by Topic kartice (sa opisom i brojem članaka) → Latest Tutorials (6) → More Guides (preostali). Hero ima blagi plavi gradijent. Newsletter CTA vidljiv na homepage-u.
- ~~Dinamički nav/footer~~ ✅ Implementirano (March 13): `inject_dynamic_nav()` zamenjuje hardkodirane linkove u header dropdown i footer sa pravim `/category/[slug]` URL-ovima. Samo aktivne kategorije (3+) se prikazuju. Comparisons pill automatski linkuje kad comparisons dostigne 3+.
- ~~Breadcrumb linkovi~~ ✅ Implementirano (March 13): Breadcrumb kategorija linkuje na `/category/[slug]` ako category page postoji, inače na `/`.

**Faza 2 (~20-25 članaka):**
- Sticky sidebar TOC (zahteva layout promenu na dvostubačni)
- Active section highlighting u TOC (IntersectionObserver)
- "Continue reading" kartice na dnu svakog članka
- Featured section na homepage za cornerstone članke

**Ne dirati:** članak layout (funkcionalan), boje/tipografija (rade), newsletter CTA pozicija.

**Trade-off za sticky sidebar TOC:** Smanjuje content width sa 1060px na ~750px — screenshotovi postaju manji. Razmotriti floating TOC kao alternativu.

### Header nav skaliranje
- **Trenutno (5 kategorija):** pill-ovi + dropdown rade
- **Na 7-8 kategorija:** dropdown skalira bez problema (samo dodaj linkove u listu)
- **Na 10+ kategorija:** i dalje OK — dropdown je neograničen
- Search ikona je placeholder — aktivirati kad search funkcionalnost bude implementirana

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
| logo-full-horizontal.png | `public/assets/branding/` | Raster verzija — **deployed u headeru** |
| og-default.png (1200x630) | `public/assets/branding/` | Social sharing default |

---

## 6. Generator — nove funkcionalnosti

### Implementirano (March 12, 2026)

**`Type: page` podrška:**
- Standalone stranice (about, affiliate-disclosure, privacy-policy) sada idu kroz generator
- `Type: page` u input.txt → generiše stranicu bez: article meta, TOC, newsletter CTA, banner CTA
- Breadcrumb: samo Home › Title (bez kategorije)
- Schema: WebPage umesto Article/HowTo
- Ne pojavljuje se u index card gridu
- Stare ručno održavane HTML fajlove obrisati iz `public/`

### Implementirano (March 13, 2026)

**Category pages (`/category/[slug]`):**
- `CATEGORIES` dict proširen sa `description` poljem za svaku kategoriju
- `CATEGORY_MIN_ARTICLES = 3` — prag za generisanje category page
- `generate_category_pages()` — kreira `/category/[slug]/index.html` sa filtriranim card gridom
- Canonical URL-ovi sa trailing slash (`/category/lead-capture/`) — matcha Cloudflare serving
- Kategorije sa <3 članaka rade u breadcrumbu/meta ali nemaju stranicu

**Dinamička navigacija:**
- `inject_dynamic_nav()` — regex zamenjuje hardkodirane linkove u header dropdown i footer
- Samo aktivne kategorije (3+) prikazane u navigaciji
- Comparisons pill automatski linkuje kad comparisons dostigne 3+ članaka
- Breadcrumb placeholder sistem: `{{CAT_LINK_[slug]}}` zamenjuje se sa `/category/[slug]` ili `/`

**Homepage redesign:**
- Hero sekcija: naslov + tagline + affiliate CTA dugme, blagi plavi gradijent pozadina
- Browse by Topic: category kartice sa opisom i brojem članaka
- Latest Tutorials: 6 najnovijih članaka
- More Guides: preostali članci (bez duplikata)
- Newsletter CTA vidljiv na homepage-u
- `<h1>` title uklonjen sa homepage-a (hero ga zamenjuje)

**Footer:**
- Redosled kolona: Site → Browse by Topic → Stay Updated

**Banner fix:**
- `src="/assets/banners/..."` (apsolutna putanja) umesto relativne — rešava broken slike na nested stranicama

### Za budućnost
- Automatsko generisanje sitemap.xml — odloženo (lastmod problem: design promene ne smeju ažurirati lastmod, a detekcija content-only promena zahteva hash/diff logiku)
- Category pages za preostale kategorije — automatski kad dostignu 3+ članaka

---

## 7. Prioritizovani akcioni plan

### ~~Odmah (sledeći deploy)~~ ✅ ZAVRŠENO (March 12, 2026)
- [x] Sačuvaj logo paket u `public/assets/branding/`
- [x] favicon.png i apple-touch-icon.png u `public/` root
- [x] Zameni stari inline SVG favicon u template.html
- [x] Dodaj og:image meta tag u template.html
- [x] Dodaj reading progress bar u template.html
- [x] Header: logomark + tekst umesto plain text
- [x] Puniji footer (3 kolone)
- [x] Scroll-to-top dugme (scroll-up only, gornji centar)
- [x] `Type: page` podrška u generator.py
- [x] About, Affiliate Disclosure, Privacy Policy prebačeni u input.txt
- [x] Header navigacija: Topics ▾ dropdown + Comparisons pill + search icon

### ~~Sledeći korak~~ ✅ ZAVRŠENO (March 13, 2026)
- [x] Category pages u generator.py (`/category/[slug]`)
- [x] Homepage redesign: hero + kategorijske kartice + latest tutorials
- [x] Linkovi profunkcionišu: header dropdown, footer, breadcrumb → prave category URL-ove
- [x] Comparisons pill u headeru → automatski kad dostigne 3+
- [x] Ažuriraj CONTEXT.md i CONTENT.md
- [x] Canonical trailing slash fix za category pages
- [x] Banner apsolutna putanja fix
- [x] Footer kolone reorder (Site prvo)
- [x] Ručno dodati category pages u sitemap.xml (bez lastmod)

### Narednih 30 dana
- [ ] Završi članak #14 (Make.com vs Zapier comparison) → aktivira comparisons kategoriju
- [ ] Završi članak #15 (weekly client report automation)
- [ ] Welcome email sequence u Beehiivu

### Na 15-18 članaka
- [ ] Split input.txt na pojedinačne `content/[slug].txt` fajlove
- [ ] Generator.py refactor: čita direktorijum umesto jednog fajla

### Na 20-25 članaka
- [ ] Supabase tabele + migracija
- [ ] Generator.py: čita iz Supabase API
- [ ] Sticky TOC + "Continue reading" sekcija
- [ ] Article card baner template (Canva/Figma) za thumbnailove

### Na 25-30 članaka
- [ ] Custom dashboard za stale content alerts
- [ ] Automatski internal linkovi (hibrid: ručni + auto-dopuna)
