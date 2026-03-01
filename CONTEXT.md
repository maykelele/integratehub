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
- **Cornerstone/pillar articles:** no screenshots needed. Focus on math, tables, internal links to how-to tutorials. Type stays `how-to` in generator for schema purposes.
- **Pricing claims:** always add "(annual billing)" on first mention. Include monthly price if known. Verify against official pricing page before publish.

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
- **Make.com credits vs operations:** Make rebranded operations → credits (mid-2025). Standard modules = 1 credit. AI modules and Code module can consume >1 credit. For free plan articles, this distinction matters less because AI Tools aren't available on free.
- **Make.com polling cost:** Trigger modules consume 1 credit per run even when no new data is found. Webhook (INSTANT) triggers consume 0 credits while idle. On free plan (15-min interval), one polling trigger burns ~2,880 credits/month — 3x the entire budget.
- **Make.com free plan limits (verified March 2026):** 1,000 credits/mo, 2 active scenarios, 15-min polling, 0.5 GB transfer, 5 MB max file size. No AI Tools, no AI Agents. Credits don't roll over.
- **Make.com Core plan ($9/mo annual, ~$10.59 monthly):** 10,000 credits, unlimited scenarios, 1-min polling, 5 GB transfer, 100 MB file size, AI Tools + Agents included, API access (60 calls/min).

## Generator Backlog
1. ~~Image alt tag fix~~ — FIXED. Cursor prompt: `In generator.py, find alt_attr = '' inside Image handler. Change to alt_attr = alt_text[:125] if alt_text else ''`
2. Build time badge — new tag `Build Time: 25`, display `🛠 ~25 min` next to reading time. Priority: medium.
3. Cleanup rel="noopener" on internal/anchor links — cosmetic. Priority: low.

## Key Decisions Log
- Homepage stays Make.com focused until 15+ articles.
- Comparison articles convert better than how-to (higher buyer intent).
- Content plan and article tracking live in CONTENT.md.
- Cornerstone article (#9 make-com-free-plan) published early (at 9 articles instead of 10+) because research was thorough and content quality justified it.
- Pricing verification workflow: check official pricing page + own dashboard screenshot before publishing any pricing claims. Third-party sources often have outdated data.
