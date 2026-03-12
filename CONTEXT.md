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
- **Example emails in tables:** use [at] instead of @ (e.g. sarah[at]brightwave.co) to avoid Cloudflare Email Obfuscation ghost links.
- **Page titles:** no brand suffix on articles. Only homepage keeps " | IntegrateHub.io". Aim for under 60 chars but don't sacrifice keywords.
- **Standalone pages** (about, privacy-policy, affiliate-disclosure): now go through generator.py as `Type: page` entries. No longer manually maintained.
- **Sitemap lastmod:** only update for substantial content changes, NOT for internal link additions or typo fixes.
- **Internal linking:** add links to related articles on every new publish.
- **Screenshots:** screenshot-[topic]-[number].png. When cloning similar scenarios, screenshot only differences.
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
- Navigation: "Topics ▾" dropdown (pill button, click-to-open, lists all categories), "Comparisons" shortcut pill, search icon (placeholder — goes to `/` until search is implemented)
- On desktop (900px+): nav visible, "← All Guides" hidden
- On mobile (<900px): nav hidden, "← All Guides" visible

### Reading Progress Bar
- Thin blue bar directly under sticky header
- Tracks scroll position automatically
- Only visible on scroll (starts at 0% width)

### Scroll-to-Top Button
- Position: fixed, top center (below header)
- Behavior: appears only on scroll-up, hides on scroll-down
- Disappears when near top of page (scrollY < 400)

### Footer
- 3 columns: Browse by Topic, Site, Stay Updated
- Browse by Topic links currently go to `/` — update when category pages are built
- Newsletter link goes to Beehiiv subscribe with UTM

### Meta Tags
- `og:image` → `/assets/branding/og-default.png`
- Favicon: PNG (32px) + apple-touch-icon (192px)
- Canonical URLs use clean paths (no .html)

## Generator Features (generator.py)

### Page Types
- `Type: how-to` (default) — full article with TOC, meta, schema (Article + HowTo)
- `Type: comparison` — full article with TOC, meta, schema (Article only, no HowTo)
- `Type: page` — standalone pages (about, privacy, disclosure). No article meta, no TOC, no newsletter CTA, no banner CTA. Breadcrumb: Home › Title only. Schema: WebPage.

### Supported Tags
`Slug:`, `Title:`, `Type:`, `Date:`, `Updated:`, `Build Time:`, `Category:`, `Meta:`, `Introduction:`, `H2:`, `H3:`, `Image:`, `Table:`, `Tech Tip:`, `CTA:`, `CTA[key]:`, `Workflow Steps:`, `Verdict:`, `FAQ:`, `Internal Links:`, `Python Snippet:`

### Categories
```
CATEGORIES = {
    "lead-capture": "Lead Capture",
    "payments": "Payments & Invoicing",
    "onboarding": "Client Onboarding",
    "comparisons": "Comparisons",
    "automation-strategy": "Automation Strategy",
}
```

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
- **www-to-non-www:** Cloudflare redirect rule active (301).

## Generator Backlog (all resolved)
1. ~~Image alt tag fix~~ — FIXED.
2. ~~Build time badge~~ — FIXED. `Build Time: 25` → `🛠 ~25 min`.
3. ~~rel="noopener" on internal links~~ — SKIPPED (cosmetic, zero SEO/UX impact).
4. ~~HowTo schema truncation~~ — FIXED. Tech Tip and CTA tags render inline in step lists.
5. ~~Article schema enrichment~~ — FIXED. Author (Organization) + image (first Image tag).

## Key Decisions Log
- Homepage stays Make.com focused until 15+ articles.
- Comparison articles convert better than how-to (higher buyer intent).
- Content plan and article tracking live in CONTENT.md.
- Cornerstone article (#9 make-com-free-plan) published early (at 9 articles instead of 10+) because research was thorough and content quality justified it.
- Pricing verification workflow: check official pricing page + own dashboard screenshot before publishing any pricing claims. Third-party sources often have outdated data.
- Business-themed categories (by function, not by tool) — matches search intent better.
- "comparisons" kept as category despite not being a business function — "I want to compare tools" is a valid use case.
- External AI reviews (Gemini, ChatGPT) useful for article feedback but require critical filtering — Gemini incorrectly claimed Google Forms uses instant webhook triggers.

## Planned Architecture Changes

### Near-term (15-18 articles)
- **Category pages:** `/category/[slug]` with filtered card grid — generator.py new function. Header dropdown, footer, and breadcrumb links all point to these.
- **Homepage redesign:** Hero section + "Browse by Topic" category cards + "Latest Tutorials" grid.
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
