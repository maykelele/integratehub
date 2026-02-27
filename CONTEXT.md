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
- Schema markup: HowTo + FAQ (auto-generated)
- Article meta: reading time, date, category badge
- TOC: auto-generated from H2 headings (3+ H2)
- Index: card grid sorted by date (newest first)

## Affiliate Programs
- Make.com: ACTIVE — https://www.make.com/en/register?pc=integratehub
- Typeform: ACTIVE (reward/referral) — https://typeform.cello.so/vGdCoE97A4Z
- Calendly: NO affiliate program available
- Pipedrive: planned (week 4)
- HubSpot: planned (week 4)
- Airtable: planned (week 6)

## Objavljeni članci (6)
1. zapier-too-expensive-make-com-alternative.html (comparison)
2. facebook-instagram-leads-google-sheets-automation.html (how-to)
3. stripe-payment-failed-automation.html (how-to)
4. calendly-booking-onboarding-checklist-automation.html (how-to)
5. make-com-vs-n8n-small-business.html (comparison)
6. typeform-client-intake-google-sheets-automation.html (how-to)

## Positioning
Vertikala: client acquisition and onboarding automation for service-based businesses (freelancers, agencies, consultants).
Primary tools: Make.com, Calendly, Typeform, Stripe, Google Sheets, Slack.
Approach: build real automations, screenshot every step, write for non-technical readers.
Expand to broader automation topics only after this cluster is strong (15+ articles).
Transform from "Make.com Integration Guides | IntegrateHub.io" to "Workflow automation tutorials for small business — step-by-step guides for Make.com, Airtable, HubSpot, and the tools your business runs on."? 

## Content Plan

### Near-term (next articles)
- Typeform → email welcome + Google Drive folder creation
- Multi-source lead tracking (FB + Typeform + website) → Google Sheets (Masterclass-level, Upsert logic)
- Filter Calendly bookings → only qualified leads to CRM
- Lead goes cold → automatic 24h Slack reminder
- Make.com Free Plan: What You Can Actually Build (cornerstone — write after 8+ how-to articles exist)

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

## Content Rules (enforced via memory)
- Title: primary keyword in first 60 chars, include Slack/notifications if part of workflow
- Meta: primary keyword in first 60 chars, max 155 chars
- Intro: weave exact-match keyword naturally, not keyword-stuffed
- H2: include keyword where possible ("How the X to Y Automation Works")
- Verdict: end with actionable CTA mentioning Make.com free plan
- INSTANT modules: always recommend over polling, explain difference
- Screenshots: screenshot-[topic]-[number].png in public/assets/screenshots/

## Key Decisions
- Anonymity is a hard constraint — no personal branding
- Homepage stays Make.com focused until content justifies broader positioning (15+ articles)
- 1 quality article/week > 3 mediocre ones
- Comparison articles convert better than how-to (higher buyer intent)
- Internal linking: add to related articles on every new publish, don't update lastmod for link-only changes