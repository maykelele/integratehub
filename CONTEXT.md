# IntegrateHub.io — Project Context

## Stack
- Cloudflare Pages hosting
- Static HTML generator (generator.py)
- Template: templates/template.html
- Content: content/input.txt (separator: ---)
- Screenshots: public/assets/screenshots/
- Compression: compress.py (JPEG, quality=70)

## Generator Features
- Tags: Slug, Title, Type, Meta, Date, Category, Introduction, H2, H3, Tech Tip, CTA[key], Workflow Steps, Verdict, Table, FAQ, Image, Screenshot, Internal Links, Python Snippet
- CTA system: CTA[make], CTA[typeform], plain CTA: (defaults to make). AFFILIATE_LINKS dict in generator.py
- Inline links: [text](url) markdown syntax supported in Introduction, Tech Tip, Verdict, CTA, FAQ answers, paragraphs, and workflow steps. External links get target="_blank" rel="noopener". Internal links get rel="noopener" only.
- Schema markup: HowTo + FAQ (auto-generated)
- Article meta: reading time, date, category badge
- TOC: auto-generated from H2 headings (3+ H2)
- Index: card grid sorted by date (newest first)

## Generator Improvements Backlog
1. **Image alt tag fix** — alt_attr is always empty string, should use alt_text from caption. SEO impact: missing alt text on all article images. Priority: high.
2. **Build time badge** — add estimated build/implementation time to article meta for how-to articles. Requires new tag in input.txt (e.g. `Build Time: 25`) and generator update. Display: `🛠 ~25 min to build` next to reading time. Priority: medium.
3. **Cleanup rel="noopener" on internal/anchor links** — TOC anchor links and index card links have unnecessary rel="noopener". Cosmetic, no functional impact. Priority: low.
4. **Error handling article** — potential standalone how-to covering Make.com error handling patterns (partial execution, retry duplicates, Break/Resume/Rollback handlers, data store idempotency). Learned from real Google Drive folder duplication issue during Typeform welcome email build. Priority: future content.

## Affiliate Programs
- Make.com: ACTIVE — https://www.make.com/en/register?pc=integratehub
- Typeform: ACTIVE (reward/referral) — https://typeform.cello.so/vGdCoE97A4Z
- Calendly: NO affiliate program available
- Pipedrive: planned (week 4)
- HubSpot: planned (week 4)
- Airtable: planned (week 6)

## Objavljeni članci (7)
1. zapier-too-expensive-make-com-alternative.html (comparison)
2. facebook-instagram-leads-google-sheets-automation.html (how-to)
3. stripe-payment-failed-automation.html (how-to)
4. calendly-booking-onboarding-checklist-automation.html (how-to)
5. make-com-vs-n8n-small-business.html (comparison)
6. typeform-client-intake-google-sheets-automation.html (how-to)
7. typeform-welcome-email-google-drive-automation.html (how-to) — NEW

## Positioning
Vertikala: client acquisition and onboarding automation for service-based businesses (freelancers, agencies, consultants).
Primary tools: Make.com, Calendly, Typeform, Stripe, Google Sheets, Slack, Google Drive.
Approach: build real automations, screenshot every step, write for non-technical readers.
Expand to broader automation topics only after this cluster is strong (15+ articles).
Transform from "Make.com Integration Guides | IntegrateHub.io" to "Workflow automation tutorials for small business — step-by-step guides for Make.com, Airtable, HubSpot, and the tools your business runs on."? 

## Content Plan

### Near-term (next articles)
- Multi-source lead tracking (FB + Typeform + website) → Google Sheets (Masterclass-level, Upsert logic)
- Filter Calendly bookings → only qualified leads to CRM
- Lead goes cold → automatic 24h Slack reminder
- Make.com Free Plan: What You Can Actually Build (cornerstone — write after 8+ how-to articles exist)
- Make.com Error Handling: How to Prevent Duplicate Data and Partial Failures (from real experience)

### Month 2
- Stripe new customer → Google Drive folder + welcome email + Slack
- Weekly client report → Google Sheets + email every Monday
- HubSpot free → Google Sheets real-time sync
- Auto-assign leads from contact form + same-day follow-up
- Typeform → AI Agent lead qualification → Slack (advanced)
- Make.com vs Zapier Professional plan — specific pricing breakdown

### Authority series (later)
- Why Most Automations Break After 3-6 Months
- How to Make Automations Maintainable
- Duplicate Data & Partial Failures
- The Status Table Pattern
- When to Use AI in Automation

## SEO Status
- Google Search Console: indexed and receiving impressions
- Early signals: 46 impressions, 1 click, avg position 23.8 (as of Feb 27, 2026)
- Sitemap: public/sitemap.xml — update lastmod only for substantial content changes

## Technical Learnings
- Google Drive is a restricted Google API — requires custom OAuth client in Google Cloud Console for personal Gmail accounts. Google Sheets works with default Make.com OAuth. Free setup, one-time only.
- Google Cloud Console OAuth setup is free forever (no trial expiry). Only compute/storage resources cost money.
- Redirect URI exact match is critical — trailing slash difference causes OAuth errors. Both with and without slash should be registered.
- Google Drive Share by email fails for non-Google account users — use "Anyone with the link" instead.
- Make.com partial execution: if a later module fails, earlier modules (like Create Folder) have already executed. Retries create duplicates without idempotency logic.

## Content Rules (enforced via memory)
- Title: primary keyword in first 60 chars, include Slack/notifications if part of workflow
- Meta: primary keyword in first 60 chars, max 155 chars
- Intro: weave exact-match keyword naturally, not keyword-stuffed
- H2: include keyword where possible ("How the X to Y Automation Works")
- Verdict: end with actionable CTA mentioning Make.com free plan
- INSTANT modules: always recommend over polling, explain difference
- Screenshots: screenshot-[topic]-[number].png in public/assets/screenshots/
- Inline links: use [text](url) for external references in Tech Tips and paragraphs

## Key Decisions
- Anonymity is a hard constraint — no personal branding
- Homepage stays Make.com focused until content justifies broader positioning (15+ articles)
- 1 quality article/week > 3 mediocre ones
- Comparison articles convert better than how-to (higher buyer intent)
- Internal linking: add to related articles on every new publish, don't update lastmod for link-only changes