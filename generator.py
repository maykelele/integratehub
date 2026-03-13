import os
import html
import json
import re
import math

INLINE_LINK_RE = re.compile(r'\[([^\]]+)]\(([^)]+)\)')


def process_inline_links(text):
    """
    Converts inline markdown-style links [text](url) into HTML <a> tags with rel="noopener".
    Non-link parts are HTML-escaped, while generated <a> tags are preserved.
    """
    result_parts = []
    last_index = 0

    for match in INLINE_LINK_RE.finditer(text):
        start, end = match.span()
        # Escape text before the link
        if start > last_index:
            result_parts.append(html.escape(text[last_index:start]))

        link_text = match.group(1)
        url = match.group(2)

        escaped_url = html.escape(url, quote=True)
        escaped_text = html.escape(link_text)

        if url.startswith('http://') or url.startswith('https://'):
            # External link: open in new tab
            result_parts.append(
                f'<a href="{escaped_url}" target="_blank" rel="noopener">{escaped_text}</a>'
            )
        else:
            # Internal link: same tab
            result_parts.append(
                f'<a href="{escaped_url}" rel="noopener">{escaped_text}</a>'
            )
        last_index = end

    # No matches — escape whole string
    if last_index == 0:
        return html.escape(text)

    # Trailing text after last match
    if last_index < len(text):
        result_parts.append(html.escape(text[last_index:]))

    return ''.join(result_parts)


TEMPLATE_FILE = 'templates/template.html'
CONTENT_FILE = 'content/input.txt'
OUTPUT_DIR = 'public'
MAKE_AFFILIATE_LINK = "https://www.make.com/en/register?pc=integratehub"

# -----------------------------------------------------------------------
# AFFILIATE LINKS — koristi se sa CTA[key]: tagom u input.txt
# Format u input.txt:  CTA[make]: Tekst poruke ovde.
#                      CTA[typeform]: Tekst poruke ovde.
#                      CTA: Tekst poruke ovde.  (default → make)
# -----------------------------------------------------------------------
AFFILIATE_LINKS = {
    "make": {
        "url": "https://www.make.com/en/register?pc=integratehub",
        "cta_text": "Start free on Make.com →",
    },
    "typeform": {
        "url": "https://typeform.cello.so/vGdCoE97A4Z",
        "cta_text": "Try Typeform free →",
    },
    # --- Newsletter opt-in (not an affiliate — uses CTA[newsletter]: tag) ---
    "newsletter": {
        "url": "https://automationfix.beehiiv.com/subscribe?utm_source=integratehub&utm_medium=inline_cta",
        "cta_text": "Subscribe free →",
    },
    "airtable": {
        "url": "https://airtable.com/invite/r/wuQK7yct",
        "cta_text": "Try Airtable free →",
    },
    # Dodaj nove affiliate partnere ovde:
    # "calendly": {
    #     "url": "https://calendly.com/?ref=integratehub",
    #     "cta_text": "Try Calendly free →",
    # },
    # "pipedrive": {
    #     "url": "https://pipedrive.com/?ref=integratehub",
    #     "cta_text": "Try Pipedrive free →",
    # },
}

# -----------------------------------------------------------------------
# KATEGORIJE — mapiranje slug → display name
# Koristi se za breadcrumb i buduće category stranice
# -----------------------------------------------------------------------
CATEGORIES = {
    "lead-capture": {
        "name": "Lead Capture",
        "description": "Automate how you capture, qualify, and route leads from forms, ads, and landing pages.",
    },
    "payments": {
        "name": "Payments & Invoicing",
        "description": "Automate payment tracking, failed payment alerts, and invoice workflows.",
    },
    "onboarding": {
        "name": "Client Onboarding",
        "description": "Automate client intake, welcome sequences, and project setup after signing.",
    },
    "comparisons": {
        "name": "Comparisons",
        "description": "Side-by-side comparisons of automation tools — pricing, features, and real trade-offs.",
    },
    "automation-strategy": {
        "name": "Automation Strategy",
        "description": "Strategic guides on when, why, and how to automate your business workflows.",
    },
    # Dodaj nove kategorije ovde — format:
    # "slug": { "name": "Display Name", "description": "Opis za category page." },
}

# Minimum broj članaka da bi kategorija dobila svoju stranicu i pojavila se u navigaciji
CATEGORY_MIN_ARTICLES = 3

# -----------------------------------------------------------------------
# PODRŽANI TAGOVI U input.txt:
#
#   Slug:           URL stranice (obavezno)
#                   Primer: Slug: stripe-payment-failed-automation
#
#   Title:          Naslov stranice — koristi se kao <h1> i <title> tag (obavezno)
#                   Primer: Title: Stripe Payment Failed? Automate Alerts with Make.com
#
#   Type:           Tip stranice — utiče na schema markup (default: how-to)
#                   Vrednosti: how-to | comparison
#
#   Date:           Datum objave — format YYYY-MM-DD (preporučeno)
#                   Koristi se za article meta, schema datePublished, i index sortiranje
#                   Primer: Date: 2026-02-15
#
#   Updated:        Datum poslednjeg update-a — format YYYY-MM-DD (opciono)
#                   Koristi se za schema dateModified i "(Updated)" oznaku
#                   Samo za substantial content promene, NE za typo/link fix
#                   Primer: Updated: 2026-03-01
#
#   Build Time:     Procenjeno vreme izgradnje automatizacije u minutima (opciono)
#                   Prikazuje se kao 🛠 ~XX min pored reading time u article meta
#                   Za comparison članke obično se ne koristi
#                   Primer: Build Time: 25
#
#   Category:       Kategorija članka — koristi se za breadcrumb i buduće filtriranje
#                   Dostupne: lead-capture, payments, onboarding, comparisons, automation-strategy
#                   Primer: Category: lead-capture
#
#   Meta:           SEO meta description — preporučeno, max 155 karaktera
#                   Keyword treba biti u prvih 60 karaktera
#                   Ako nije postavljen, koristi se Introduction kao fallback
#                   Primer: Meta: Make.com vs Zapier for small business — honest pricing comparison.
#
#   Introduction:   Uvodni paragraf — prikazuje se kao istaknuti blok sa lijevom bordurom
#                   Ako Meta: nije postavljen, prvih 155 karaktera postaje meta description
#                   Primer: Introduction: Every time someone fills out your lead form...
#
#   H2:             Sekcijski naslov — zatvara otvorenu listu koraka
#                   Primer: H2: Why Zapier Gets Expensive for Small Business
#
#   H3:             Podsekcijski naslov (unutar H2 sekcije) — NE zatvara listu koraka
#                   Primer: H3: On Make.com
#
#   Tech Tip:       Žuti info box sa praktičnim savetom
#                   Unutar Workflow Steps: prikazuje se inline između koraka (ne zatvara listu)
#                   Izvan Workflow Steps: prikazuje se kao standalone blok
#                   Primer: Tech Tip: Add a Slack notification as a third step...
#
#   CTA:            Inline poziv na akciju sa default (Make.com) affiliate linkom
#                   Unutar Workflow Steps: prikazuje se inline između koraka (ne zatvara listu)
#                   Izvan Workflow Steps: prikazuje se kao standalone blok
#                   Primer: CTA: Build this automation for free — no credit card required.
#
#   CTA[key]:       Inline poziv na akciju sa specifičnim affiliate linkom
#                   Dostupni ključevi: make, typeform, airtable, newsletter
#                   (dodaj nove u AFFILIATE_LINKS dict iznad)
#                   Unutar Workflow Steps: prikazuje se inline između koraka (ne zatvara listu)
#                   Primer: CTA[typeform]: Build your intake form for free.
#                   Primer: CTA[make]: Build this automation on Make.com's free plan.
#                   Primer: CTA[newsletter]: Get one tested automation tutorial per week.
#                   Napomena: newsletter nije affiliate — koristi se za Beehiiv opt-in CTA.
#
#   Workflow Steps: Otvara numerisanu listu koraka sa H2 naslovom iznad
#                   Tekst posle taga postaje naslov sekcije
#                   Lista se zatvara na: Verdict, H2, Table, FAQ, Internal Links,
#                   Workflow Steps, Python Snippet, Introduction, ili novi page separator (---)
#                   NE zatvara se na: Image, Screenshot, Tech Tip, CTA, H3 — ovi se
#                   prikazuju inline između koraka
#                   Primer: Workflow Steps: How to Connect Facebook Leads to Google Sheets
#
#   Verdict:        Završni zaključni blok — zatvara listu koraka ako je otvorena
#                   Primer: Verdict: This automation takes 20 minutes to build and runs forever.
#
#   Table:          Comparison tabela — tekst posle taga postaje naslov tabele
#                   Format zaglavlja: Kolona1|Kolona2|Kolona3
#                   Format redova:    vrednost1|vrednost2|vrednost3
#                   Kraj tabele: prazna linija ili novi tag
#                   Primer: Table: Real Cost Comparison: Zapier vs Make.com
#
#   FAQ:            FAQ sekcija sa schema markup
#                   Format: Q: pitanje (novi red) A: odgovor
#                   Kraj FAQ: prazna linija ili novi tag
#
#   Internal Links: Linkovi na druge članke — prikazuje se kao "Related Guides" box
#                   Format: Tekst linka|slug.html
#                   Svaki link u novom redu, kraj bloka: prazna linija ili novi tag
#
#   Screenshot:     Placeholder box dok nemaš pravu sliku
#                   Zameni sa Image: kada imaš screenshot
#                   Unutar Workflow Steps: prikazuje se inline između koraka (ne zatvara listu)
#                   Primer: Screenshot: Make.com canvas with Stripe trigger
#
#   Image:          Prava slika — format: putanja|Caption tekst
#                   Caption postaje i alt attribute (max 125 karaktera)
#                   SEO best practice: počni caption sa "Make.com [tema] —"
#                   Unutar Workflow Steps: prikazuje se inline između koraka (ne zatvara listu)
#                   Prva Image: u članku se koristi za Article schema "image" polje
#                   Primer: Image: assets/screenshots/make-trigger.png|Make.com Stripe automation — Watch Events trigger setup
#
#   Python Snippet: Code blok sa sintax highlightom
#                   Tekst u sledećim redovima do sledećeg taga postaje kod
#
#   ---             Separator između stranica u input.txt
#
#   Sve ostale linije → <p> paragraf
#
# SCHEMA MARKUP:
#   Article schema:  Uvek se generiše. Uključuje author (Organization: IntegrateHub.io)
#                    i image (prva Image: iz članka, apsolutni URL) za rich result eligibility.
#   HowTo schema:    Generiše se za Type: how-to stranice. Sakuplja sve korake iz
#                    Workflow Steps bloka (Image/Tech Tip/CTA ne prekidaju brojanje).
#   FAQ schema:      Generiše se ako postoji FAQ: blok.
# -----------------------------------------------------------------------


def extract_field(lines, prefix):
    """Izvlači vrednost polja po prefiksu."""
    return next(
        (l.replace(prefix, '').strip() for l in lines if l.startswith(prefix)), ""
    )


def cat_name(slug):
    """Vraća display name kategorije iz CATEGORIES dict-a."""
    cat = CATEGORIES.get(slug)
    if not cat:
        return slug.replace('-', ' ').title()
    return cat["name"] if isinstance(cat, dict) else cat


def estimate_reading_time(text):
    """Procenjuje vreme čitanja na osnovu broja reči (200 wpm avg)."""
    # Ukloni tagove/metapodatke za tačniji count
    content_lines = []
    skip_prefixes = ('Slug:', 'Title:', 'Type:', 'Date:', 'Updated:', 'Category:',
                     'Build Time:', 'Meta:', 'Image:', 'Screenshot:', 'Internal Links:', '---')
    for line in text.split('\n'):
        stripped = line.strip()
        if not stripped:
            continue
        if any(stripped.startswith(p) for p in skip_prefixes):
            continue
        # Ukloni tag prefiks ali zadrži tekst
        for tag in ('Introduction:', 'H2:', 'H3:', 'Tech Tip:', 'Verdict:',
                     'Workflow Steps:', 'Table:', 'FAQ:', 'Q:', 'A:', 'CTA:'):
            if stripped.startswith(tag):
                stripped = stripped[len(tag):]
                break
        content_lines.append(stripped)
    word_count = len(' '.join(content_lines).split())
    minutes = max(1, math.ceil(word_count / 200))
    return minutes


def format_date_display(date_str):
    """Formatira YYYY-MM-DD u human-readable format (Feb 15, 2026)."""
    if not date_str:
        return ""
    try:
        from datetime import datetime
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%b %d, %Y')
    except ValueError:
        return date_str


def build_article_schema(title, meta_desc, date_published, date_modified=None, image_path=None):
    """Generiše Article schema markup."""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": meta_desc,
        "author": {
            "@type": "Organization",
            "name": "IntegrateHub.io",
            "url": "https://integratehub.io"
        },
        "publisher": {
            "@type": "Organization",
            "name": "IntegrateHub.io",
            "url": "https://integratehub.io"
        }
    }
    if image_path:
        # Ensure absolute URL for schema
        if not image_path.startswith('http'):
            schema["image"] = f"https://integratehub.io/{image_path.lstrip('/')}"
        else:
            schema["image"] = image_path
    if date_published:
        schema["datePublished"] = date_published
    if date_modified:
        schema["dateModified"] = date_modified
    elif date_published:
        schema["dateModified"] = date_published

    return (
        f'<script type="application/ld+json">\n'
        f'{json.dumps(schema, indent=2, ensure_ascii=False)}\n'
        f'</script>'
    )


def build_howto_schema(title, steps):
    """Generiše HowTo schema markup za how-to stranice."""
    if not steps:
        return ""

    schema_steps = []
    for i, step_text in enumerate(steps, 1):
        clean_text = step_text[:200] + "..." if len(step_text) > 200 else step_text
        schema_steps.append({
            "@type": "HowToStep",
            "position": i,
            "name": f"Step {i}",
            "text": clean_text
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": title,
        "step": schema_steps
    }

    return (
        f'<script type="application/ld+json">\n'
        f'{json.dumps(schema, indent=2, ensure_ascii=False)}\n'
        f'</script>'
    )


def build_faq_schema(faq_items):
    """Generiše FAQ schema markup."""
    if not faq_items:
        return ""

    entities = []
    for q, a in faq_items:
        entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }

    return (
        f'<script type="application/ld+json">\n'
        f'{json.dumps(schema, indent=2, ensure_ascii=False)}\n'
        f'</script>'
    )


def build_toc(h2_headings):
    """Generiše Table of Contents HTML iz liste H2 naslova."""
    if len(h2_headings) < 3:
        return ""  # Ne prikazuj TOC za kratke članke

    items = ""
    for i, heading in enumerate(h2_headings):
        anchor = re.sub(r'[^a-z0-9]+', '-', heading.lower()).strip('-')
        items += (
            f'<li><a href="#{html.escape(anchor)}" rel="noopener">'
            f'{html.escape(heading)}</a></li>\n'
        )

    return (
        f'<nav class="toc">\n'
        f'<p class="toc-title">In This Guide</p>\n'
        f'<ol>{items}</ol>\n'
        f'</nav>'
    )


def format_content(text, page_type='how-to'):
    """Parsira strukturirani tekst i generiše semantički HTML."""
    lines = text.split('\n')
    html_parts = []
    schema_parts = []

    in_code_block = False
    in_list = False
    in_table = False
    in_faq = False
    in_internal_links = False
    code_lines = []
    table_rows = []
    faq_items = []
    internal_links = []
    current_faq_q = None
    meta_description = ""
    first_image = ""  # Za Article schema image
    howto_steps = []  # Za HowTo schema
    h2_headings = []  # Za TOC generaciju

    def close_open_blocks():
        nonlocal in_list, in_table, in_faq, in_internal_links
        nonlocal table_rows, faq_items, internal_links, current_faq_q

        if in_list:
            html_parts.append('</ol>')
            in_list = False

        if in_table and table_rows:
            _flush_table(table_rows)
            table_rows = []
            in_table = False

        if in_faq and faq_items:
            _flush_faq(faq_items)
            faq_items = []
            in_faq = False

        if in_internal_links and internal_links:
            _flush_internal_links(internal_links)
            internal_links = []
            in_internal_links = False

    def _flush_table(rows):
        if not rows:
            return
        header = rows[0]
        body = rows[1:]
        header_html = ''.join(f'<th>{html.escape(h.strip())}</th>' for h in header)
        body_html = ''
        for row in body:
            cells = ''.join(f'<td>{html.escape(c.strip())}</td>' for c in row)
            body_html += f'<tr>{cells}</tr>'
        html_parts.append(
            f'<div class="table-wrapper">'
            f'<table class="comparison-table">'
            f'<thead><tr>{header_html}</tr></thead>'
            f'<tbody>{body_html}</tbody>'
            f'</table></div>'
        )

    def _flush_faq(items):
        if not items:
            return
        html_parts.append('<div class="faq-section"><h2 id="frequently-asked-questions">Frequently Asked Questions</h2>')
        h2_headings.append('Frequently Asked Questions')
        for q, a in items:
            html_parts.append(
                f'<div class="faq-item">'
                f'<h3 class="faq-q">{html.escape(q)}</h3>'
                f'<p class="faq-a">{process_inline_links(a)}</p>'
                f'</div>'
            )
        html_parts.append('</div>')
        schema_parts.append(build_faq_schema(items))

    def _flush_internal_links(links):
        if not links:
            return
        items_html = ''
        for text, href in links:
            items_html += (
                f'<li><a href="{html.escape(href)}" rel="noopener">'
                f'{html.escape(text)}</a></li>'
            )
        html_parts.append(
            f'<div class="related-guides">'
            f'<h3>Related Guides</h3>'
            f'<ul>{items_html}</ul>'
            f'</div>'
        )

    for line in lines:
        line_stripped = line.strip()

        is_new_tag = any(line_stripped.startswith(tag) for tag in [
            'Introduction:', 'Meta:', 'Tech Tip:', 'CTA', 'Workflow Steps:', 'Verdict:',
            'Python Snippet:', 'Table:', 'FAQ:', 'Internal Links:',
            'Screenshot:', 'Image:', 'H2:', 'H3:',
            'Slug:', 'Title:', 'Type:', 'Date:', 'Updated:', 'Category:', 'Build Time:', '---'
        ])

        if is_new_tag and (in_table or in_faq or in_internal_links):
            close_open_blocks()

        if not line_stripped:
            if in_table:
                close_open_blocks()
            continue

        if line_stripped.startswith(('Slug:', 'Title:', 'Type:', 'Date:', 'Updated:', 'Category:', 'Build Time:', '---')):
            continue

        # --- Meta description (optional override) ---
        if line_stripped.startswith('Meta:'):
            meta_text = line_stripped.replace('Meta:', '').strip()
            if len(meta_text) > 155:
                meta_description = meta_text[:155].rsplit(' ', 1)[0] + "..."
            else:
                meta_description = meta_text

        # --- Introduction ---
        elif line_stripped.startswith('Introduction:'):
            intro_text = line_stripped.replace('Introduction:', '').strip()
            if not meta_description:
                meta_limit = 155
                if len(intro_text) > meta_limit:
                    meta_description = intro_text[:meta_limit].rsplit(' ', 1)[0] + "..."
                else:
                    meta_description = intro_text
            html_parts.append(f'<p class="intro">{process_inline_links(intro_text)}</p>')

        # --- H2 ---
        elif line_stripped.startswith('H2:'):
            close_open_blocks()
            h2_text = line_stripped.replace('H2:', '').strip()
            anchor = re.sub(r'[^a-z0-9]+', '-', h2_text.lower()).strip('-')
            h2_headings.append(h2_text)
            html_parts.append(f'<h2 id="{html.escape(anchor)}">{html.escape(h2_text)}</h2>')

        # --- H3 ---
        elif line_stripped.startswith('H3:'):
            h3_text = line_stripped.replace('H3:', '').strip()
            html_parts.append(f'<h3>{html.escape(h3_text)}</h3>')

        # --- Tech Tip (list-safe: does NOT close Workflow Steps) ---
        elif line_stripped.startswith('Tech Tip:'):
            if not in_list:
                close_open_blocks()
            tip_text = line_stripped.replace('Tech Tip:', '').strip()
            tip_html = (
                f'<div class="tech-tip">'
                f'<strong>💡 Pro Tip:</strong> {process_inline_links(tip_text)}'
                f'</div>'
            )
            if in_list:
                html_parts.append(f'<li class="step-image">{tip_html}</li>')
            else:
                html_parts.append(tip_html)

        # --- CTA (supports CTA: and CTA[key]:) (list-safe: does NOT close Workflow Steps) ---
        elif line_stripped.startswith('CTA'):
            if not in_list:
                close_open_blocks()
            cta_match = re.match(r'^CTA\[(\w+)\]:\s*(.*)', line_stripped)
            if cta_match:
                affiliate_key = cta_match.group(1).lower()
                cta_text = cta_match.group(2).strip()
            else:
                affiliate_key = "make"
                cta_text = line_stripped.replace('CTA:', '').strip()
            affiliate = AFFILIATE_LINKS.get(affiliate_key, AFFILIATE_LINKS["make"])
            cta_html = (
                f'<p class="inline-cta">{process_inline_links(cta_text)} '
                f'<a href="{affiliate["url"]}" rel="sponsored noopener">{affiliate["cta_text"]}</a></p>'
            )
            if in_list:
                html_parts.append(f'<li class="step-image">{cta_html}</li>')
            else:
                html_parts.append(cta_html)

        # --- Workflow Steps ---
        elif line_stripped.startswith('Workflow Steps:'):
            close_open_blocks()
            section_title = line_stripped.replace('Workflow Steps:', '').strip()
            heading = section_title if section_title else 'Implementation Steps'
            anchor = re.sub(r'[^a-z0-9]+', '-', heading.lower()).strip('-')
            h2_headings.append(heading)
            html_parts.append(f'<h2 id="{html.escape(anchor)}">{html.escape(heading)}</h2>')
            html_parts.append('<ol class="steps">')
            in_list = True

        # --- Verdict ---
        elif line_stripped.startswith('Verdict:'):
            close_open_blocks()
            verdict_text = line_stripped.replace('Verdict:', '').strip()
            html_parts.append(
                f'<div class="verdict">'
                f'<strong>Bottom line:</strong> {process_inline_links(verdict_text)}'
                f'</div>'
            )

        # --- Table ---
        elif line_stripped.startswith('Table:'):
            close_open_blocks()
            table_title = line_stripped.replace('Table:', '').strip()
            if table_title:
                html_parts.append(f'<h2>{html.escape(table_title)}</h2>')
            in_table = True
            table_rows = []

        # --- FAQ ---
        elif line_stripped.startswith('FAQ:'):
            close_open_blocks()
            in_faq = True
            faq_items = []
            current_faq_q = None

        # --- Internal Links ---
        elif line_stripped.startswith('Internal Links:'):
            close_open_blocks()
            in_internal_links = True
            internal_links = []

        # --- Screenshot placeholder (list-safe) ---
        elif line_stripped.startswith('Screenshot:'):
            if not in_list:
                close_open_blocks()
            caption = line_stripped.replace('Screenshot:', '').strip()
            html_parts.append(
                f'<div class="screenshot-placeholder">'
                f'<div class="screenshot-placeholder-inner">'
                f'<span class="screenshot-icon">📷</span>'
                f'<span class="screenshot-label">Screenshot: {html.escape(caption)}</span>'
                f'</div>'
                f'</div>'
            )

        # --- Image (list-safe) ---
        elif line_stripped.startswith('Image:'):
            if not in_list:
                close_open_blocks()
            image_data = line_stripped.replace('Image:', '').strip()
            if '|' in image_data:
                img_path, alt_text = image_data.split('|', 1)
                img_path = img_path.strip()
                alt_text = alt_text.strip()
            else:
                img_path = image_data.strip()
                alt_text = ''
            if not first_image:
                first_image = img_path
            alt_attr = alt_text[:125] if alt_text else ''
            figure_html = (
                f'<figure class="screenshot">'
                f'<img src="{html.escape(img_path)}" alt="{html.escape(alt_attr)}" width="1060" loading="lazy">'
                f'<figcaption>{html.escape(alt_text)}</figcaption>'
                f'</figure>'
            )
            if in_list:
                html_parts.append(f'<li class="step-image">{figure_html}</li>')
            else:
                html_parts.append(figure_html)

        # --- Python Snippet ---
        elif line_stripped.startswith('Python Snippet:'):
            close_open_blocks()
            html_parts.append('<h2>Code Snippet</h2>')
            in_code_block = True
            code_lines = []

        # --- Unutar code bloka ---
        elif in_code_block:
            code_lines.append(line)

        # --- Unutar table bloka ---
        elif in_table:
            if '|' in line_stripped:
                table_rows.append(line_stripped.split('|'))

        # --- Unutar FAQ bloka ---
        elif in_faq:
            if line_stripped.startswith('Q:'):
                current_faq_q = line_stripped.replace('Q:', '').strip()
            elif line_stripped.startswith('A:') and current_faq_q:
                answer = line_stripped.replace('A:', '').strip()
                faq_items.append((current_faq_q, answer))
                current_faq_q = None

        # --- Unutar Internal Links bloka ---
        elif in_internal_links:
            if '|' in line_stripped:
                parts = line_stripped.split('|', 1)
                if len(parts) == 2:
                    internal_links.append((parts[0].strip(), parts[1].strip()))

        # --- Unutar liste koraka ---
        elif in_list:
            clean = line_stripped
            if len(clean) > 2 and clean[0].isdigit() and clean[1] in '.):':
                clean = clean[2:].strip()
            elif len(clean) > 3 and clean[0].isdigit() and clean[2] in '.):':
                clean = clean[3:].strip()
            howto_steps.append(clean)
            html_parts.append(f'<li>{process_inline_links(clean)}</li>')

        # --- Regularni paragraf ---
        else:
            html_parts.append(f'<p>{process_inline_links(line_stripped)}</p>')

    # Zatvaranje svih otvorenih blokova
    close_open_blocks()

    if in_code_block and code_lines:
        escaped_code = html.escape('\n'.join(code_lines))
        html_parts.append(f'<pre><code>{escaped_code}</code></pre>')

    # HowTo schema za how-to stranice
    if page_type == 'how-to' and howto_steps:
        schema_parts.insert(0, None)  # Placeholder — title dolazi iz generate_site

    return '\n'.join(html_parts), meta_description, schema_parts, howto_steps, h2_headings, first_image


def generate_index(template_html, links, active_categories=None, category_counts=None):
    """Generiše index.html sa hero, category karticama, latest tutorials, i svim člancima."""
    if active_categories is None:
        active_categories = []
    if category_counts is None:
        category_counts = {}

    sorted_links = sorted(links, key=lambda x: x.get('date', ''), reverse=True)

    def build_card(l, show_category=True):
        description = l.get('description', '')
        if len(description) > 150:
            description = description[:150] + '...'
        date_display = format_date_display(l.get('date', ''))
        category_name = cat_name(l.get('category', '')) if l.get('category') and show_category else ''
        meta_parts = []
        if date_display:
            meta_parts.append(date_display)
        if category_name:
            meta_parts.append(category_name)
        meta_line = ' · '.join(meta_parts)
        return f"""
        <div class="card">
            <a href="/{l['slug']}" rel="noopener">
                {'<p class="card-meta">' + html.escape(meta_line) + '</p>' if meta_line else ''}
                <h2>{html.escape(l['title'])}</h2>
                <p>{html.escape(description)}</p>
                <span class="read-more">Read guide →</span>
            </a>
        </div>"""

    # --- Hero ---
    hero_html = f"""
        <div class="hero">
            <h1>Automate Your Business with Make.com</h1>
            <p>Step-by-step tutorials for service businesses, freelancers, and agencies. Build real workflows — no code required.</p>
            <a href="{MAKE_AFFILIATE_LINK}" target="_blank" rel="sponsored noopener" class="btn">Start free on Make.com →</a>
        </div>
    """

    # --- Browse by Topic ---
    category_cards_html = ""
    if active_categories:
        cat_cards = ""
        for slug in active_categories:
            count = category_counts.get(slug, 0)
            display = cat_name(slug)
            cat_cards += f"""
            <a href="/category/{slug}" class="category-card">
                <h3>{html.escape(display)}</h3>
                <span class="cat-count">{count} guide{'s' if count != 1 else ''}</span>
            </a>"""

        category_cards_html = f"""
        <div class="home-section">
            <p class="section-label">Browse by Topic</p>
            <div class="category-grid">
                {cat_cards}
            </div>
        </div>
        """

    # --- Latest Tutorials (6 najnovijih) ---
    latest_cards = ''.join(build_card(l) for l in sorted_links[:6])
    latest_html = f"""
        <div class="home-section">
            <p class="section-label">Latest Tutorials</p>
            <div class="card-grid">
                {latest_cards}
            </div>
        </div>
    """

    # --- All Guides ---
    all_cards = ''.join(build_card(l) for l in sorted_links)
    all_guides_html = f"""
        <hr class="home-divider">
        <div class="home-section">
            <p class="section-label">All Guides</p>
            <div class="card-grid">
                {all_cards}
            </div>
        </div>
    """

    index_content = hero_html + category_cards_html + latest_html + all_guides_html

    page = template_html.replace('{{TITLE}}', 'Make.com Integration Guides | IntegrateHub.io')
    page = page.replace('{{META_DESCRIPTION}}',
        'Free step-by-step Make.com integration guides. '
        'Automate your business workflows and save hours every week.')
    page = page.replace('{{MAIN_CONTENT}}', index_content)
    page = page.replace('{{SCHEMA_MARKUP}}', '')
    page = page.replace('{{SLUG}}', 'index')
    page = page.replace('{{CANONICAL_URL}}', '')

    page = page.replace('{{ARTICLE_META}}', '')
    page = page.replace('{{TOC}}', '')
    page = page.replace('{{BREADCRUMB}}', '')

    page = page.replace(
        '<a href="/" class="back-link">← All Guides</a>', '')
    page = page.replace(
        '<div class="breadcrumb">\n        \n    </div>', '')

    page = page.replace('{{AFFILIATE_LINK}}', MAKE_AFFILIATE_LINK)
    # Newsletter CTA je VIDLJIV na homepage-u (ne sakrivamo ga)
    return page


def generate_site():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template_html = f.read()

    with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
        raw = f.read()

    integrations = [i.strip() for i in raw.split('---') if i.strip()]
    links = []

    for entry in integrations:
        lines = entry.split('\n')

        slug = extract_field(lines, 'Slug:')
        title = extract_field(lines, 'Title:')
        page_type = extract_field(lines, 'Type:') or 'how-to'
        date_published = extract_field(lines, 'Date:')
        date_updated = extract_field(lines, 'Updated:')
        category = extract_field(lines, 'Category:')
        build_time = extract_field(lines, 'Build Time:')

        if not slug or not title:
            print(f"⚠️  Preskačem entry bez slug/title")
            continue

        main_body, meta_desc, schema_parts, howto_steps, h2_headings, first_image = format_content(entry, page_type)

        # --- Page type: page (standalone pages like About, Privacy, etc.) ---
        is_standalone = (page_type == 'page')

        # --- Reading time ---
        reading_time = estimate_reading_time(entry)

        # --- TOC (skip for standalone pages) ---
        toc_html = '' if is_standalone else build_toc(h2_headings)

        # --- Article meta (skip for standalone pages) ---
        if is_standalone:
            article_meta_html = ''
        else:
            meta_parts = []
            if date_published:
                display_date = format_date_display(date_published)
                meta_parts.append(f'<time datetime="{html.escape(date_published)}">{html.escape(display_date)}</time>')
                if date_updated and date_updated != date_published:
                    updated_display = format_date_display(date_updated)
                    meta_parts.append(f'<span>(Updated {html.escape(updated_display)})</span>')
            meta_parts.append(f'<span class="separator">·</span>')
            meta_parts.append(f'<span>⏱ {reading_time} min read</span>')
            if build_time:
                meta_parts.append(f'<span class="separator">·</span>')
                meta_parts.append(f'<span>🛠 ~{html.escape(build_time)} min build</span>')
            if category and category in CATEGORIES:
                meta_parts.append(f'<span class="separator">·</span>')
                meta_parts.append(f'<span class="category-badge">{html.escape(cat_name(category))}</span>')
            article_meta_html = f'<div class="article-meta">{" ".join(meta_parts)}</div>'

        # --- Breadcrumb (simplified for standalone pages) ---
        breadcrumb_parts = [f'<a href="/" rel="noopener">Home</a>']
        if not is_standalone and category and category in CATEGORIES:
            cat_display = cat_name(category)
            # Link ide na category page samo ako postoji (placeholder se zameni posle)
            breadcrumb_parts.append(
                f'<a href="{{{{CAT_LINK_{category}}}}}" rel="noopener">{html.escape(cat_display)}</a>'
            )
        breadcrumb_parts.append(f'{html.escape(title)}')
        breadcrumb_html = ' › '.join(breadcrumb_parts)

        # --- Schema markup ---
        all_schemas = []
        if is_standalone:
            # WebPage schema for standalone pages
            wp_schema = {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": title,
                "description": meta_desc,
                "publisher": {
                    "@type": "Organization",
                    "name": "IntegrateHub.io",
                    "url": "https://integratehub.io"
                }
            }
            all_schemas.append(
                f'<script type="application/ld+json">\n'
                f'{json.dumps(wp_schema, indent=2, ensure_ascii=False)}\n'
                f'</script>'
            )
        else:
            # Article schema (uvek) — sa author i image
            all_schemas.append(build_article_schema(title, meta_desc, date_published, date_updated, first_image))
            # HowTo schema (samo za how-to)
            if page_type == 'how-to' and howto_steps:
                all_schemas.append(build_howto_schema(title, howto_steps))
        # FAQ i ostali schema
        for s in schema_parts:
            if s is not None:
                all_schemas.append(s)

        schema_html = '\n'.join(all_schemas)

        # --- Popunjavanje template-a ---
        page = template_html.replace('{{TITLE}}', title)
        page = page.replace('{{SLUG}}', slug)
        canonical_url = slug  # clean URL without .html
        page = page.replace('{{CANONICAL_URL}}', canonical_url)
        page = page.replace('{{META_DESCRIPTION}}', meta_desc)
        page = page.replace('{{MAIN_CONTENT}}', main_body)
        page = page.replace('{{SCHEMA_MARKUP}}', schema_html)
        page = page.replace('{{AFFILIATE_LINK}}', MAKE_AFFILIATE_LINK)
        page = page.replace('{{ARTICLE_META}}', article_meta_html)
        page = page.replace('{{TOC}}', toc_html)
        page = page.replace('{{BREADCRUMB}}', breadcrumb_html)

        # Hide newsletter CTA and banner on standalone pages
        if is_standalone:
            page = page.replace(
                '<div class="newsletter-cta"',
                '<!-- newsletter hidden on page --><div class="newsletter-cta" style="display:none"'
            )
            page = page.replace(
                '<div class="cta-card"',
                '<!-- cta hidden on page --><div class="cta-card" style="display:none"'
            )

        output_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(page)

        print(f"✅ Generisano [{page_type}]: {slug}.html — {reading_time} min read, date: {date_published or 'N/A'}, category: {category or 'N/A'}")

        # Standalone pages don't appear in index
        if not is_standalone:
            links.append({
                'slug': slug,
                'title': title,
                'type': page_type,
                'description': meta_desc,
                'date': date_published,
                'category': category,
            })

    # --- Izračunaj koje kategorije imaju dovoljno članaka ---
    category_counts = {}
    for l in links:
        cat = l.get('category')
        if cat:
            category_counts[cat] = category_counts.get(cat, 0) + 1

    active_categories = sorted(
        [slug for slug, count in category_counts.items()
         if count >= CATEGORY_MIN_ARTICLES and slug in CATEGORIES],
        key=lambda s: list(CATEGORIES.keys()).index(s)
    )

    print(f"\n📂 Aktivne kategorije (>={CATEGORY_MIN_ARTICLES} članaka): {active_categories}")
    for slug, count in category_counts.items():
        if count < CATEGORY_MIN_ARTICLES:
            print(f"   ⏳ {slug}: {count} članaka (treba {CATEGORY_MIN_ARTICLES})")

    # --- Zameni breadcrumb category link placeholdere u svim generisanim stranicama ---
    for fname in os.listdir(OUTPUT_DIR):
        fpath = os.path.join(OUTPUT_DIR, fname)
        if not fpath.endswith('.html') or os.path.isdir(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        changed = False
        for cat_slug in CATEGORIES:
            placeholder = f'{{{{CAT_LINK_{cat_slug}}}}}'
            if placeholder in content:
                if cat_slug in active_categories:
                    replacement = f'/category/{cat_slug}'
                else:
                    replacement = '/'
                content = content.replace(placeholder, replacement)
                changed = True
        if changed:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)

    # --- Generiši index ---
    index_html = generate_index(template_html, links, active_categories, category_counts)
    index_html = inject_dynamic_nav(index_html, active_categories)
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    # --- Generiši category pages ---
    generate_category_pages(template_html, links, active_categories)

    # --- Inject dynamic nav u sve article/page HTML fajlove ---
    for fname in os.listdir(OUTPUT_DIR):
        fpath = os.path.join(OUTPUT_DIR, fname)
        if not fname.endswith('.html') or fname == 'index.html' or os.path.isdir(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        content = inject_dynamic_nav(content, active_categories)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

    # --- Inject dynamic nav u category page HTML fajlove ---
    cat_dir = os.path.join(OUTPUT_DIR, 'category')
    if os.path.isdir(cat_dir):
        for cat_slug in os.listdir(cat_dir):
            idx_path = os.path.join(cat_dir, cat_slug, 'index.html')
            if os.path.isfile(idx_path):
                with open(idx_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                content = inject_dynamic_nav(content, active_categories)
                with open(idx_path, 'w', encoding='utf-8') as f:
                    f.write(content)

    total = len(links) + len(active_categories) + 1
    print(f"\n🚀 Gotovo! Generisano {len(links)} članaka + {len(active_categories)} category stranica + index.html")


def inject_dynamic_nav(page_html, active_categories):
    """Zamenjuje hardkodirane header dropdown i footer category linkove sa dinamičkim."""

    # --- Header dropdown menu ---
    dropdown_links = '\n'.join(
        f'                    <a href="/category/{slug}">{html.escape(cat_name(slug))}</a>'
        for slug in active_categories
    )
    page_html = re.sub(
        r'(<div class="nav-dropdown-menu">)\s*.*?\s*(</div>\s*</div>\s*</nav>)',
        rf'\1\n{dropdown_links}\n                \2',
        page_html,
        flags=re.DOTALL
    )

    # --- Header Comparisons pill ---
    if 'comparisons' in active_categories:
        page_html = page_html.replace(
            '<a href="/" class="nav-pill">Comparisons</a>',
            '<a href="/category/comparisons" class="nav-pill">Comparisons</a>'
        )

    # --- Footer "Browse by Topic" ---
    footer_links = '\n'.join(
        f'                    <li><a href="/category/{slug}">{html.escape(cat_name(slug))}</a></li>'
        for slug in active_categories
    )
    page_html = re.sub(
        r'(<h4>Browse by Topic</h4>\s*<ul>)\s*.*?\s*(</ul>)',
        rf'\1\n{footer_links}\n                \2',
        page_html,
        flags=re.DOTALL
    )

    return page_html


def generate_category_pages(template_html, links, active_categories):
    """Generiše /category/[slug]/index.html za svaku aktivnu kategoriju."""
    for cat_slug in active_categories:
        cat_info = CATEGORIES[cat_slug]
        cat_display = cat_info["name"] if isinstance(cat_info, dict) else cat_info
        cat_desc = cat_info.get("description", "") if isinstance(cat_info, dict) else ""

        cat_links = [l for l in links if l.get('category') == cat_slug]
        cat_links_sorted = sorted(cat_links, key=lambda x: x.get('date', ''), reverse=True)

        cards = ""
        for l in cat_links_sorted:
            description = l.get('description', '')
            if len(description) > 150:
                description = description[:150] + '...'
            date_display = format_date_display(l.get('date', ''))
            meta_line = date_display

            cards += f"""
        <div class="card">
            <a href="/{l['slug']}" rel="noopener">
                {'<p class="card-meta">' + html.escape(meta_line) + '</p>' if meta_line else ''}
                <h2>{html.escape(l['title'])}</h2>
                <p>{html.escape(description)}</p>
                <span class="read-more">Read guide →</span>
            </a>
        </div>"""

        cat_content = f"""
        <p class="intro">{html.escape(cat_desc)}</p>
        <div class="card-grid">
            {cards}
        </div>
    """

        page = template_html.replace('{{TITLE}}', f'{cat_display} Guides | IntegrateHub.io')
        page = page.replace('{{META_DESCRIPTION}}', cat_desc[:155])
        page = page.replace('{{MAIN_CONTENT}}', cat_content)
        page = page.replace('{{SCHEMA_MARKUP}}', '')
        page = page.replace('{{SLUG}}', f'category/{cat_slug}')
        page = page.replace('{{CANONICAL_URL}}', f'category/{cat_slug}')
        page = page.replace('{{ARTICLE_META}}', '')
        page = page.replace('{{TOC}}', '')
        page = page.replace('{{BREADCRUMB}}',
            f'<a href="/" rel="noopener">Home</a> › {html.escape(cat_display)}')
        page = page.replace('{{AFFILIATE_LINK}}', MAKE_AFFILIATE_LINK)

        page = page.replace(
            '<a href="/" class="back-link">← All Guides</a>', '')
        page = page.replace(
            '<div class="breadcrumb">\n        \n    </div>', '')
        page = page.replace(
            '<div class="newsletter-cta"',
            '<!-- newsletter hidden on category --><div class="newsletter-cta" style="display:none"'
        )

        cat_dir = os.path.join(OUTPUT_DIR, 'category', cat_slug)
        os.makedirs(cat_dir, exist_ok=True)
        output_path = os.path.join(cat_dir, 'index.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(page)

        print(f"📁 Category page: /category/{cat_slug}/ — {len(cat_links)} članaka")


if __name__ == "__main__":
    generate_site()