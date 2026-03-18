# IntegrateHub.io — Project Context

## Stack
- Cloudflare Pages hosting
- Static HTML generator (generator.py)
- Template: templates/template.html
- Content: content/input.txt (separator: ---)
- Screenshots: public/assets/screenshots/
- Compression: compress.py (JPEG, quality=70)

## Working Rules
- **Generator/template changes:** Provide patches (find → replace) for Sasa to apply to local files. No direct file editing.
- **Anonymity:** hard constraint — no personal branding anywhere.
- **URLs:** no .html extensions anywhere — canonicals, internal links, sitemap, index cards all use clean URLs (e.g. /slug not /slug.html). Cloudflare Pages redirects .html to clean URLs.
- **Category page URLs:** use trailing slash in canonicals (`/category/lead-capture/`) because Cloudflare serves folder/index.html with trailing slash.
- **Example emails in tables:** use [at] instead of @ (e.g. sarah[at]brightwave.co) to avoid Cloudflare Email Obfuscation ghost links.
- **Page titles:** no brand suffix on articles. Only homepage keeps " | IntegrateHub.io". Aim for under 60 chars but don't sacrifice keywords.
- **Standalone pages** (about, privacy-policy, affiliate-disclosure): now go through generator.py as `Type: page` entries. No longer manually maintained.
- **Sitemap:** manually maintained. Only update lastmod for substantial content changes, NOT for internal link additions, typo fixes, or design/template changes. Category pages added manually without lastmod.
- **Internal linking:** add links to related articles on every new publish.
- **Screenshots:** screenshot-[topic]-[number].png. When cloning similar scenarios, screenshot only differences.
- **Banner images:** use absolute paths (`/assets/banners/...`) in template — relative paths break on nested pages like `/category/[slug]/`.
- **1 quality article/week > 3 mediocre ones.**

## Content Rules
- Title: primary keyword in first 60 chars, include Make.com. Include Slack/notifications if part of workflow.
- Meta: primary keyword in first 60 chars, max 155 chars.
- Intro: weave exact-match keyword naturally. No keyword-stuffed sentences. No affiliate links in intro.
- H2: include keyword where possible ("How the X to Y Automation Works").
- Verdict: end with actionable CTA mentioning Make.com free plan.
- INSTANT modules: always recommend over polling, explain difference.
- CTA tags: use CTA[key]: format. Plain CTA: defaults to Make.com. Place at natural points, not aggressively.
- CTA[newsletter]: use sparingly in cornerstone/pillar articles and high-engagement tutorials. Not an affiliate — drives Beehiiv opt-in. Don't put in every article, only where reader is most engaged.
- Inline links: [text](url) for external references in Tech Tips and paragraphs.
- **Cornerstone/pillar articles:** no screenshots needed. Focus on math, tables, internal links to how-to tutorials. Type stays `how-to` in generator for schema purposes.
- **Pricing claims:** always add "(annual billing)" on first mention. Include monthly price if known. Verify against official pricing page before publish.

## Branding & Visual Identity

### Logo Package
Logomark: Variation 6C — central hub circle + 4 connected endpoint nodes (rounded squares). Developed through iterative AI process (Gemini).

| File | Location | Purpose |
|------|----------|---------|
| favicon.png (32px) | `public/` | Browser tab |
| apple-touch-icon.png (192px) | `public/` | iOS/Android |
| favicon-512.png | `public/assets/branding/` | PWA |
| logomark-blue.svg | `public/assets/branding/` | Primary mark, blue on transparent |
| logomark-black.svg | `public/assets/branding/` | Monochrome version |
| logomark-white.svg | `public/assets/branding/` | For dark/blue backgrounds |
| favicon.svg | `public/assets/branding/` | White on blue, rounded square |
| logo-full-horizontal.svg | `public/assets/branding/` | Mark + text for header |
| logo-full-horizontal.png | `public/assets/branding/` | Raster version — deployed in header |
| og-default.png (1200x630) | `public/assets/branding/` | Social sharing default |

### Site Identity
- **Site name:** IntegrateHub.io (stays — generic but fine for anonymous affiliate site)
- **Newsletter brand:** "The Automation Fix" (more memorable — consider as primary brand later)
- **Domain:** don't change — 13 indexed articles, early page 1 ranks

## Template Features (template.html)

### Header
- Logo: `logo-full-horizontal.png` (height: 32px, width: 208px)
- Navigation: "Topics ▾" dropdown (pill button, click-to-open, lists active categories dynamically), "Comparisons" shortcut pill (links to `/category/comparisons` when active, otherwise `/`), search icon (placeholder — goes to `/` until search is implemented)
- On desktop (900px+): nav visible, "← All Guides" hidden
- On mobile (<900px): nav hidden, "← All Guides" visible
- Nav content is dynamically injected by `inject_dynamic_nav()` — only categories with 3+ articles appear

### Homepage Layout
- Hero: centered title + tagline + affiliate CTA button, subtle blue gradient background
- Browse by Topic: category cards with description + article count (only active categories)
- Latest Tutorials: 6 most recent articles as card grid
- More Guides: remaining articles (no duplicates with Latest)
- Newsletter CTA: visible at bottom
- H1 from template hidden — hero provides the page heading

### Reading Progress Bar
- Thin blue bar directly under sticky header
- Tracks scroll position automatically
- Only visible on scroll (starts at 0% width)

### Scroll-to-Top Button
- Position: fixed, top center (below header)
- Behavior: appears only on scroll-up, hides on scroll-down
- Disappears when near top of page (scrollY < 400)

### Footer
- 3 columns: Site, Browse by Topic, Stay Updated
- Browse by Topic links dynamically injected — only active categories (3+) shown
- Newsletter link goes to Beehiiv subscribe with UTM

### Meta Tags
- `og:image` → `/assets/branding/og-default.png`
- Favicon: PNG (32px) + apple-touch-icon (192px)
- Canonical URLs use clean paths (no .html); category pages use trailing slash

## Generator Features (generator.py)

### Page Types
- `Type: how-to` (default) — full article with TOC, meta, schema (Article + HowTo)
- `Type: comparison` — full article with TOC, meta, schema (Article only, no HowTo)
- `Type: page` — standalone pages (about, privacy, disclosure). No article meta, no TOC, no newsletter CTA, no banner CTA. Breadcrumb: Home › Title only. Schema: WebPage.

### Supported Tags
`Slug:`, `Title:`, `Type:`, `Date:`, `Updated:`, `Build Time:`, `Category:`, `Meta:`, `Introduction:`, `H2:`, `H3:`, `Image:`, `Table:`, `Tech Tip:`, `CTA:`, `CTA[key]:`, `Workflow Steps:`, `Verdict:`, `FAQ:`, `Internal Links:`, `Python Snippet:`, `Code Block:`

### Categories
```
CATEGORIES = {
    "lead-capture": { "name": "Lead Capture", "description": "..." },
    "payments": { "name": "Payments & Invoicing", "description": "..." },
    "onboarding": { "name": "Client Onboarding", "description": "..." },
    "comparisons": { "name": "Comparisons", "description": "..." },
    "automation-strategy": { "name": "Automation Strategy", "description": "..." },
    "reporting": { "name": "Reporting", "description": "..." },
}
CATEGORY_MIN_ARTICLES = 3
```

Category pages are auto-generated at `/category/[slug]/index.html` only when a category reaches 3+ articles. The `description` field is displayed on the category page intro and in homepage category cards.

### Category System Flow
1. Generator counts articles per category from input.txt
2. Categories with 3+ articles become "active"
3. Active categories get: category page, header dropdown link, footer link, breadcrumb link
4. Inactive categories: breadcrumb links to `/`, no nav presence, no category page
5. `inject_dynamic_nav()` replaces hardcoded template links with dynamic ones on every build
6. Adding a new category: add to CATEGORIES dict + use in articles → auto-activates at 3+

### Affiliate Links
```
AFFILIATE_LINKS = {
    "make": url + "Start free on Make.com →",
    "typeform": url + "Try Typeform free →",
    "airtable": url + "Try Airtable free →",
    "newsletter": url + "Subscribe free →",
}
```

### Schema
- Article schema: always generated for how-to and comparison types. Includes `author` (Organization: IntegrateHub.io) and `image` (first Image: tag as absolute URL).
- HowTo schema: only for `Type: how-to` when Workflow Steps exist. `Tech Tip:` and `CTA:` tags render as `<li class="step-image">` inside step lists (don't break step counting).
- FAQ schema: generated from `FAQ:` blocks.
- WebPage schema: for `Type: page` only.

## Technical Learnings
- Google Drive is a restricted API — requires custom OAuth client (free, one-time). Google Sheets works with default Make.com OAuth.
- Redirect URI exact match critical — trailing slash causes OAuth errors.
- Google Drive Share: use "Anyone with the link" — email sharing fails for non-Google users.
- Make.com partial execution: earlier modules run even if later ones fail. Retries create duplicates without idempotency.
- Make.com formulas: enter through formula editor (press `/`). Typing `{{ }}` directly = literal text.
- Make.com string concat: `concat()` doesn't exist. Use `+` operator.
- Make.com Router fallback: wrench icon → Set as fallback → Yes. Runs when no other branch matches.
- Custom Webhook: no API key, no data structure, no special settings needed. Test by pasting URL with params in browser.
- Facebook Lead Ads testing: Meta testing tool (developers.facebook.com/tools/lead-ads-testing/) sends dummy data. Polling "Watch Leads" with "All" can pick up test leads without running an ad.
- Upsert pattern: Search Rows (by email) → Router → "Lead Exists" (Total bundles > 0) → Update a Row / fallback → Add a Row.
- Google Forms returns nested data structures in Make.com — map via `Answers[].textAnswers.answers[].value` paths, not flat field names.
- Airtable accepted Stripe Unix timestamps directly without `formatDate()` conversion.
- **Make.com credits vs operations:** Make rebranded operations → credits (mid-2025). Standard modules = 1 credit. AI modules and Code module can consume >1 credit. For free plan articles, this distinction matters less because AI Tools aren't available on free.
- **Make.com polling cost:** Trigger modules consume 1 credit per run even when no new data is found. Webhook (INSTANT) triggers consume 0 credits while idle. On free plan (15-min interval), one polling trigger burns ~2,880 credits/month — 3x the entire budget.
- **Make.com free plan limits (verified March 2026):** 1,000 credits/mo, 2 active scenarios, 15-min polling, 0.5 GB transfer, 5 MB max file size. No AI Tools, no AI Agents. Credits don't roll over.
- **Make.com Core plan ($9/mo annual, ~$10.59 monthly):** 10,000 credits, unlimited scenarios, 1-min polling, 5 GB transfer, 100 MB file size, AI Tools + Agents included, API access (60 calls/min).
- **Make.com parseDate for Google Sheets dates:** When a Google Sheets column stores dates as text (e.g. "2026-03-01"), use `parseDate(value; "YYYY-MM-DD")` to convert to a real date before comparing. Without parseDate, filters comparing text to dates fail silently. If the column uses native Google Sheets date format, parseDate is not needed.
- **Polling is correct when "absence of action" is the trigger:** Webhook triggers can't detect that something didn't happen (e.g. no follow-up in 24h). Polling (scheduled check) is the only option for time-based inactivity detection. Cost: ~720 ops/month at 60-min interval.
- **`dateDifference()` doesn't exist in Make.com.** Use `addDays(now; -1)` compared against `parseDate(field; "YYYY-MM-DD")` for date comparisons.
- **`site:` operator in GSC is unreliable.** ~2-week GSC data lag is normal.
- **Make.com Schedule trigger doesn't consume credits.** It's a timer that starts the scenario, not a processing module. Only modules that handle data consume credits.
- **Make.com Iterator consumes 1 credit per bundle (per iteration).** Not free. For N items: N credits. Formula for scenario with Iterator: count fixed modules + (modules-per-iteration × N).
- **Make.com Code Block tag:** `Code Block:` in input.txt renders as `<pre><code>` without an H2 heading. Terminates on empty line. Use for inline code snippets within articles (e.g., HTML templates). `Python Snippet:` still works for code with its own H2.
- **www-to-non-www:** Cloudflare redirect rule active (301).
- **Cloudflare Pages + trailing slash:** Cloudflare serves `/category/slug/index.html` as `/category/slug/` (with trailing slash). Canonical URLs for category pages must include trailing slash to avoid mismatch warnings in Screaming Frog.
- **Sitemap lastmod pitfall:** Automatic sitemap generation would set lastmod on every build (including design-only changes). Detecting content-only changes requires file hashing or git diff — not worth the complexity yet. Keep sitemap manual.
- OpenAI module (Generate a Response) works on Free plan — third-party integration, not Make.com AI Tools/Agents.
- OpenAI module costs exactly 1 Make.com credit per execution.
- JSON Schema output gives directly mappable fields — no Parse JSON needed.
- gpt-5-mini available in Make.com as of March 2026.
- Python Snippet: and Code Block: tags break Workflow Steps <ol>. Never place inside Workflow Steps — use separate H2 section.
- Category "automation-strategy" renamed to "best-practices" (slug + name). 0 articles — no migration needed.
- Category "reporting" added to generator (was missing for Article #15).

## Generator Backlog (all resolved)
1. ~~Image alt tag fix~~ — FIXED.
2. ~~Build time badge~~ — FIXED. `Build Time: 25` → `🛠 ~25 min`.
3. ~~rel="noopener" on internal links~~ — SKIPPED (cosmetic, zero SEO/UX impact).
4. ~~HowTo schema truncation~~ — FIXED. Tech Tip and CTA tags render inline in step lists.
5. ~~Article schema enrichment~~ — FIXED. Author (Organization) + image (first Image tag).
6. Support Code Block: inside Workflow Steps without breaking <ol> — render as <li class="step-code"> similar to Image: handling. Low priority — workaround exists.

## Key Decisions Log
- Homepage stays Make.com focused until 15+ articles.
- Comparison articles convert better than how-to (higher buyer intent).
- Content plan and article tracking live in CONTENT.md.
- Cornerstone article (#9 make-com-free-plan) published early (at 9 articles instead of 10+) because research was thorough and content quality justified it.
- Pricing verification workflow: check official pricing page + own dashboard screenshot before publishing any pricing claims. Third-party sources often have outdated data.
- Business-themed categories (by function, not by tool) — matches search intent better.
- "comparisons" kept as category despite not being a business function — "I want to compare tools" is a valid use case.
- External AI reviews (Gemini, ChatGPT) useful for article feedback but require critical filtering — Gemini incorrectly claimed Google Forms uses instant webhook triggers.
- Category activation threshold set at 3 articles — shows only substantive categories in navigation, avoids sparse pages.
- Header dropdown and footer "Browse by Topic" show only active categories — consistent with threshold, no dead links.
- Automatic sitemap generation deferred — lastmod accuracy problem with design-only rebuilds.
- Homepage "More Guides" section ensures all articles are reachable even if their category isn't active yet.
- Footer column order: Site → Browse by Topic → Stay Updated (Site first for usability).

## Planned Architecture Changes

### Near-term (15-18 articles)
- ~~Category pages~~ ✅ DONE
- ~~Homepage redesign~~ ✅ DONE
- ~~Dynamic nav/footer~~ ✅ DONE
- **Split input.txt:** One `content/[slug].txt` file per article. Generator reads directory instead of single file. Format within files stays identical.

### Medium-term (20-25 articles)
- **Supabase migration:** Postgres DB replaces file-based content. Table Editor as free CRUD UI. REST API auto-generated. Schema: articles, internal_links, screenshots, pricing_claims, faq_items.
- **Sticky sidebar TOC:** Requires layout change to two-column. Trade-off: content width drops from 1060px to ~750px (smaller screenshots). Consider floating TOC alternative.
- **"Continue reading" cards** at bottom of each article.

### Long-term (25-30 articles)
- Custom dashboard for stale content alerts.
- Automatic internal links (hybrid: manual + auto-supplement).
- Tool-based tag system (secondary taxonomy).
- Template ecosystem / downloadable blueprints (AI-resistant content).