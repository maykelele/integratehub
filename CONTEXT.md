# IntegrateHub.io — Project Context

## Stack
- Cloudflare Pages hosting
- Static HTML generator (generator.py)
- Template: templates/template.html
- Content: content/input.txt (separator: ---)
- Screenshots: public/assets/screenshots/
- Compression: compress.py (JPEG, quality=70)

## Working Rules
- **Generator/template changes:** NEVER edit files directly. Provide a Cursor AI prompt for every change.
- **Anonymity:** hard constraint — no personal branding anywhere.
- **URLs:** keep .html extensions — static site, removing requires redirect rules for no benefit.
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
- Inline links: [text](url) for external references in Tech Tips and paragraphs.

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

## Generator Backlog
1. ~~Image alt tag fix~~ — FIXED. Cursor prompt: `In generator.py, find alt_attr = '' inside Image handler. Change to alt_attr = alt_text[:125] if alt_text else ''`
2. Build time badge — new tag `Build Time: 25`, display `🛠 ~25 min` next to reading time. Priority: medium.
3. Cleanup rel="noopener" on internal/anchor links — cosmetic. Priority: low.

## Key Decisions Log
- Homepage stays Make.com focused until 15+ articles.
- Comparison articles convert better than how-to (higher buyer intent).
- Content plan and article tracking live in CONTENT.md.
