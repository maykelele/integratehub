# IntegrateHub.io — Living Strategy Document
**Version:** 2.0
**Created:** March 2026
**Last Updated:** March 2026 (post external AI verification)
**Next Review:** September 2026
**Review Cadence:** Every 6 months — update version, date, and checkpoint results

---

## Change Log
- v1.0 (March 2026): Initial strategy document
- v2.0 (March 2026): Revised after external verification by 3 independent AI models. Key changes: added unit economics model, revised financial projections downward, added maintenance budget to time allocation, modified affiliate content rule, added maintenance trap to risk register, reframed blueprint monetization.

---

## Core Thesis

Build an anonymous, SEO-driven affiliate website targeting small business owners, freelancers, and agencies who need workflow automation. Monetize through recurring affiliate commissions and supplementary revenue streams. Defend against AI search erosion through visual proof, verified data, downloadable assets, and newsletter audience ownership.

The primary moat is not screenshots or blueprints in isolation — it is the combination of verified, current, visual, and functional content that AI cannot reliably replicate in real-time. This moat degrades over time and must be actively maintained.

**Hard constraints:**
- Full anonymity — no personal branding anywhere
- No paid acquisition in phase 1
- Quality over quantity — one deep article over three shallow ones
- Primary content has active affiliate program. Max 20% of content is authority/infrastructure content without direct monetization (beginner guides, error handling, webhook concepts) — this builds domain authority and internal link structure.

---

## Current State (March 2026)

| Metric | Status |
|---|---|
| Published articles | 8 |
| Active affiliate programs | Make.com (35% recurring, 12 months), Typeform |
| Content mix | 6 how-to / 2 comparison (75/25) ✅ |
| SEO traction | Early page 1 signals confirmed |
| Newsletter | Not yet launched |
| Monthly revenue | Pre-revenue |
| Tech stack | Custom Python generator, Cloudflare Pages |

---

## Unit Economics Model

**Why this exists:** Revenue projections are meaningless without understanding the funnel. This model defines exactly what traffic and conversion you need to hit each milestone.

### Make.com Commission Structure
- Commission rate: 35% recurring
- Commission period: 12 months per referred customer (not lifetime)
- Average referred customer plan: ~€20-30/month
- Commission per active customer per month: €7-10.50
- Average SMB retention: 6 months (conservative)
- Effective revenue per referred customer (lifetime): ~€42-63

### Required Referrals Per Revenue Target

| Monthly Revenue Target | Active Referred Customers Needed | New Paying Customers/Month Needed |
|---|---|---|
| €300/mo | ~35 | ~6 |
| €500/mo | ~60 | ~10 |
| €1,000/mo | ~120 | ~20 |
| €2,000/mo | ~240 | ~42 |
| €3,500/mo | ~420 | ~70 |

### Traffic Required (Working Backward)

Assumptions: 1-2% affiliate click-through rate on articles, 2-4% trial conversion, 40-60% trial-to-paid conversion.

| Monthly Revenue Target | Monthly Sessions Needed (conservative) | Monthly Sessions Needed (optimistic) |
|---|---|---|
| €300/mo | 15,000-25,000 | 8,000-15,000 |
| €500/mo | 25,000-40,000 | 12,000-25,000 |
| €1,000/mo | 50,000-80,000 | 25,000-50,000 |
| €2,000/mo | 100,000-160,000 | 50,000-100,000 |

**Key insight:** €2,000/month requires either very high traffic OR significantly above-average conversion. At 15h/week with SEO-only acquisition, €1,000-1,500/month is a realistic ceiling for month 36 unless a distribution wedge is found.

### Multi-Affiliate Adjustment
With 4+ affiliate programs active, total revenue potential increases without proportional traffic increase — different articles convert different programs. Target: by month 18, no single affiliate represents more than 50% of total affiliate revenue.

---

## Strategic Pillars

### Pillar 1: AI-Resistant Content
Every article must include at least two of:
- Real screenshots of current UI (not stock, not AI-generated)
- "Last verified: [date]" on all pricing claims
- Specific error or edge case from real implementation
- Downloadable blueprint/template

**Important caveat:** These defenses improve post-click conversion and trust. They do not prevent pre-click CTR compression from AI Overviews. The real defense against AI is diversified traffic sources, not just content format.

### Pillar 2: Affiliate Diversification
Never depend on a single affiliate program. Target 4-6 active programs by month 12.

**Priority pipeline:**

| Partner | Commission | Status | Action |
|---|---|---|---|
| Make.com | 35% recurring (12mo) | ✅ Active | — |
| Typeform | Recurring | ✅ Active | — |
| n8n Cloud | Exists | 🔜 Apply now | Before first n8n article |
| Airtable | Exists | 🔜 Apply now | Before first Airtable article |
| Pipedrive | 20-33% recurring | 🔜 Apply | Before first Pipedrive article |
| HubSpot | 30% recurring | 🔜 Apply | High priority — large TAM |
| Zapier | Exists | 🔜 Consider | Useful for comparison articles |

**Rule:** No article for a tool without approved affiliate. Exception: up to 20% of content can be authority/infrastructure content (error handling, webhook concepts, beginner guides) that builds domain authority without direct monetization.

**Risk note:** Affiliate programs can change terms, reduce commissions, or close without warning. Monitor Make.com affiliate terms page quarterly.

### Pillar 3: Blueprint Ecosystem (Conversion Tool First, Revenue Second)
Starting from article #9, every how-to tutorial gets a companion Make.com blueprint (`.json`) for download.

- **Primary purpose:** Conversion optimization and email opt-in (lead magnet)
- **Secondary purpose:** Newsletter growth
- **Tertiary purpose (month 18+):** Premium bundles ($29-49) only after list exceeds 3,000 subscribers and traffic proves demand
- **Not a standalone business line** until proven at scale

**Why:** At current scale, paid blueprint bundles will generate low volume, create support burden, and distract from core affiliate model. Treat as conversion enhancer, not revenue pillar.

### Pillar 4: Newsletter as Owned Audience
Platform: Beehiiv

- **Not a separate workload** — each article repurposed as newsletter issue (~45 min/week)
- **Monetization layers:** Beehiiv Boost + direct newsletter ads
- **Realistic CPM:** $10-30 for network ads, $30-50 only for direct sponsorships (harder to secure at <5K subscribers)
- **Goal:** audience ownership that survives Google algorithm changes

**Realistic newsletter revenue timeline:**
- 1,000 subscribers: €50-100/month (network ads only)
- 3,000 subscribers: €150-300/month
- 5,000 subscribers: €300-600/month (mix of network + occasional direct)

### Pillar 5: Maintenance Budget
**This is the pillar most affiliate strategies ignore.**

As content library grows, maintenance competes with new content production:

| Articles Published | Estimated Monthly Maintenance | Impact on New Content |
|---|---|---|
| 1-20 | 1-2h/week | Minimal |
| 20-40 | 2-3h/week | Slight reduction |
| 40-60 | 3-4h/week | One fewer article per month |
| 60-100 | 4-6h/week | Significant — may need to prioritize updates over new |

**Rule:** Every article that gets a UI update screenshot must be updated within 30 days or marked "screenshots may be outdated." Letting broken screenshots accumulate destroys trust faster than any other factor.

### Pillar 6: Strategic Review Discipline
Every 6 months: review metrics, kill what doesn't work, double down on what does. This document gets updated at every checkpoint.

---

## Content Strategy

### Target Mix
- 70% how-to tutorials (affiliate conversion)
- 20% comparison articles (higher buyer intent)
- 10% authority/infrastructure content (domain authority, internal links, no direct monetization)

### AI-Erosion Defense by Content Type

| Content Type | AI Risk | Defense |
|---|---|---|
| Generic "how to connect X to Y" | High | Add screenshots + blueprint + edge cases |
| Pricing comparisons | Medium | Verified date + fresh data, update quarterly |
| Error troubleshooting | Low | Real edge cases from implementation |
| Tool comparisons with fresh date | Medium | Update every 3-6 months |
| Blueprint/template downloads | Low-Medium | Functional value, but commoditization risk grows |
| Authority/concept content | Low | Builds links, not directly AI-threatened |

### Content Velocity and Time Budget

**15h/week allocation:**

| Activity | Hours/Week (Phase 1) | Hours/Week (Phase 2, Month 12+) |
|---|---|---|
| Build + test automation | 3-4h | 2-3h |
| Write + screenshots + formatting | 5-6h | 4-5h |
| SEO research | 1-2h | 1h |
| Tech + maintenance | 1-2h | 3-4h |
| Newsletter | 1h | 1h |
| **New articles per month** | **~4** | **~3** |

**Important:** By month 12-15, maintenance starts consuming production time. Plan for reduced content velocity, not failure.

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Google algorithm update | Medium | High | Diversify to newsletter + blueprints + non-Google content |
| Make.com changes affiliate terms | Medium | High | 4+ affiliate programs by M12, monitor quarterly |
| AI erodes 40-60% of SEO traffic | High (3-5yr) | High | Newsletter ownership, blueprint ecosystem, consider YouTube |
| Execution fatigue / burnout | Medium | Fatal | Checkpoint system, realistic pace, maintenance budget |
| Competitor with more resources | Medium | Medium | Depth over breadth, moat content |
| Single affiliate dependency | High currently | High | Priority: diversify in next 60 days |
| Maintenance trap | High (M12+) | Medium | Budget maintenance hours explicitly, prioritize evergreen content |
| Affiliate approval rejections | Medium | Medium | Apply early, build traffic first for programs with traffic requirements |
| Make.com platform commoditization | Medium (2-3yr) | High | Expand beyond Make.com to broader automation niche |

---

## Financial Projections (Revised)

**Assumptions:** 15h/week, SEO-only acquisition, 4+ affiliate programs by month 12, newsletter ads from month 12, blueprint sales tested from month 18.

*Conservative = no major Google updates, slow affiliate approval. Realistic = 4 affiliate programs active, steady SEO growth. These replace the previous "optimistic" scenario which required traffic volumes not achievable at 15h/week SEO-only.*

| Timeframe | Conservative | Realistic |
|---|---|---|
| Month 12 | 100-300 EUR/mo | 400-700 EUR/mo |
| Month 18 | 300-600 EUR/mo | 700-1,200 EUR/mo |
| Month 24 | 600-1,000 EUR/mo | 1,200-2,000 EUR/mo |
| Month 36 | 1,000-1,800 EUR/mo | 2,000-3,500 EUR/mo |

**Why the previous optimistic scenario (€5,500/mo) was removed:** Reaching €5,500/month requires ~115 new paying Make.com customers per month, implying 80,000-150,000+ monthly sessions with above-average conversion. This is not consistent with a 15h/week, SEO-only, anonymous site profile.

**Exit potential:** Content affiliate sites sell at 30-40x monthly revenue. At month 36 realistic scenario: potential asset value of €60,000-140,000. Not a primary goal — a real option.

---

## Checkpoint Framework

### Checkpoint 1 — Month 6 (September 2026)
**Validation checkpoint — is the foundation working?**

Metrics to review:
- [ ] Minimum 20-25 published articles
- [ ] 3+ articles ranking page 1 for target keywords
- [ ] At least 1 confirmed affiliate conversion
- [ ] Newsletter launched with 150+ subscribers
- [ ] First blueprint available for download
- [ ] 3+ active affiliate programs approved
- [ ] Search Console: impressions growing month-over-month
- [ ] AI Overviews: note which target keywords now show AI snippets (baseline for future comparison)

**Decision gate:**
- All green → continue, accelerate blueprint opt-in
- 2-3 red → diagnose root cause before investing another 6 months
- 4+ red → strategic pivot required

---

### Checkpoint 2 — Month 12 (March 2027)
**Monetization checkpoint — is revenue real?**

Metrics to review:
- [ ] 40-50 published articles
- [ ] Monthly revenue >200 EUR (any source)
- [ ] Newsletter at 400+ subscribers
- [ ] 4+ active affiliate programs
- [ ] Search Console: no major impression drops vs month 6
- [ ] AI Overview presence — quantify how many target keywords have AI snippets vs month 6
- [ ] Maintenance hours: how much of 15h/week is now going to updates?
- [ ] Top 3 revenue-generating articles identified

**Decision gate:**
- Revenue growing + traffic stable → scale content, test blueprint bundle
- Revenue flat despite traffic → conversion problem, audit CTAs and affiliate placement
- Traffic dropping → SEO problem or AI erosion starting, accelerate newsletter growth
- Maintenance consuming >4h/week → adjust content strategy toward more evergreen topics

---

### Checkpoint 3 — Month 18 (September 2027)
**Scale checkpoint — what's working, what isn't?**

Metrics to review:
- [ ] Monthly revenue >700 EUR
- [ ] Newsletter at 1,500+ subscribers
- [ ] Newsletter ads generating first revenue
- [ ] Top 3 revenue articles — double down on that topic cluster
- [ ] Bottom 3 affiliate programs — cut or replace
- [ ] AI impact quantified: compare impressions to month 12 baseline
- [ ] Maintenance hours tracked: is content velocity sustainable?
- [ ] Blueprint bundle: tested or consciously deferred?

**Decision gate:**
- Revenue scaling → stay course, consider YouTube as second channel
- Revenue plateauing → introduce new revenue stream or distribution channel
- AI erosion >30% of impressions → accelerate YouTube/video or community distribution
- Maintenance >5h/week → consider outsourcing screenshot updates

---

### Checkpoint 4 — Month 24 (March 2028)
**Sustainability checkpoint — is this a real business?**

Metrics to review:
- [ ] Monthly revenue >1,200 EUR consistently (3 months)
- [ ] Newsletter at 3,000+ subscribers
- [ ] 2-3 revenue streams active and contributing
- [ ] Make.com dependency: what % of revenue comes from Make.com affiliate?
- [ ] AI search landscape: what % of target keywords have AI Overviews? (compare to month 6 baseline)
- [ ] Decision: continue to month 36, optimize current state, or explore exit?

**Decision gate:**
- Revenue >1,200 EUR and growing → plan for month 36, consider outsourcing
- Revenue 600-1,200 EUR and stable → optimize, don't expand scope
- Revenue <600 EUR despite consistent work → honest pivot conversation required

---

### Checkpoint 5 — Month 36 (March 2029)
**Exit/scale checkpoint**

Metrics to review:
- [ ] Monthly revenue documented for trailing 12 months (needed for valuation)
- [ ] Newsletter list size and 30-day open rate
- [ ] Total asset value estimate (30-40x monthly revenue)
- [ ] AI search impact: has the erosion scenario materialized, and at what scale?
- [ ] Decision: sell, continue, or pivot to adjacent opportunity (B2B automation services, SaaS tool, community)

---

## Immediate Action Items (Next 30 Days)

- [ ] Apply for n8n Cloud affiliate program
- [ ] Apply for Airtable affiliate program
- [ ] Apply for HubSpot affiliate program
- [ ] Set up Beehiiv newsletter (free plan)
- [ ] Add newsletter opt-in to all existing articles
- [ ] Create first Make.com blueprint for most popular existing article
- [ ] Add "Last verified: [date]" to all pricing claims in existing articles
- [ ] Set Google Search Console monthly review reminder (calendar)
- [ ] Note which target keywords currently show AI Overviews (baseline)
- [ ] Set Make.com affiliate terms monitoring reminder (quarterly)

---

## Strategic Watch List

Topics and signals to monitor at every checkpoint:

- **Google AI Overviews expansion** — track which target keywords get AI snippets (note at each checkpoint)
- **Make.com affiliate program changes** — monitor terms page quarterly
- **Make.com platform changes** — UI updates that break screenshots
- **Competing sites in niche** — track top 3 competitors' content velocity
- **n8n growth trajectory** — may become more important than Make.com in 2-3 years
- **New affiliate opportunities** — automation tools launching programs

---

## Future Options (Not Commitments)

These are not part of the current strategy but become relevant at specific checkpoints:

- **YouTube (faceless screen recordings):** Consider at month 18 if AI erosion >25% of impressions. Second-largest search engine, AI-resistant for visual tutorials.
- **B2B automation setup service:** Consider at month 24 if revenue plateaus. Anonimno, through email, €300-500 per setup. No personal brand required.
- **Vertical specialization:** If one industry cluster converts significantly better, double down and become the automation resource for that vertical.
- **Exit:** At month 36, if trailing 12-month revenue is stable, asset value is €60,000-140,000 at 30-40x multiple.

---

*This document is reviewed and updated every 6 months.*
*Version history: STRATEGY-v1-2026-03.md → STRATEGY-v2-2026-03.md*
*Next version: STRATEGY-v3-2026-09.md (after September 2026 checkpoint)*
