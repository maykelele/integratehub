import os
import html
import json
import re

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
#   Meta:           SEO meta description — preporučeno, max 155 karaktera
#                   Keyword treba biti u prvih 60 karaktera
#                   Ako nije postavljen, koristi se Introduction kao fallback
#                   Primer: Meta: Make.com vs Zapier for small business — honest pricing comparison.
#
#   Introduction:   Uvodni paragraf — prikazuje se kao istaknuti blok sa lijevom bordurom
#                   Ako Meta: nije postavljen, prvih 155 karaktera postaje meta description
#                   Primer: Introduction: Every time someone fills out your lead form...
#
#   H2:             Sekcijski naslov
#                   Primer: H2: Why Zapier Gets Expensive for Small Business
#
#   H3:             Podsekcijski naslov (unutar H2 sekcije)
#                   Primer: H3: On Make.com
#
#   Tech Tip:       Žuti info box sa praktičnim savetom
#                   Primer: Tech Tip: Add a Slack notification as a third step...
#
#   CTA:            Inline poziv na akciju sa default (Make.com) affiliate linkom
#                   Primer: CTA: Build this automation for free — no credit card required.
#
#   CTA[key]:       Inline poziv na akciju sa specifičnim affiliate linkom
#                   Dostupni ključevi: make, typeform (dodaj nove u AFFILIATE_LINKS)
#                   Primer: CTA[typeform]: Build your intake form for free.
#                   Primer: CTA[make]: Build this automation on Make.com's free plan.
#
#   Workflow Steps: Otvara numerisanu listu koraka sa H2 naslovom iznad
#                   Tekst posle taga postaje naslov sekcije
#                   Lista se zatvara na prvom sledećem tagu (Verdict, H2, itd.)
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
#                   Primer: Screenshot: Make.com canvas with Stripe trigger
#
#   Image:          Prava slika — format: putanja|Caption tekst
#                   Caption postaje i alt attribute (max 125 karaktera)
#                   SEO best practice: počni caption sa "Make.com [tema] —"
#                   Unutar Workflow Steps: automatski se prikazuje između koraka
#                   Primer: Image: assets/screenshots/make-trigger.png|Make.com Stripe automation — Watch Events trigger setup
#
#   Python Snippet: Code blok sa sintax highlightom
#                   Tekst u sledećim redovima do sledećeg taga postaje kod
#
#   ---             Separator između stranica u input.txt
#
#   Sve ostale linije → <p> paragraf
# -----------------------------------------------------------------------


def extract_field(lines, prefix):
    """Izvlači vrednost polja po prefiksu."""
    return next(
        (l.replace(prefix, '').strip() for l in lines if l.startswith(prefix)), ""
    )


def build_howto_schema(title, steps):
    """Generiše HowTo schema markup za how-to stranice."""
    if not steps:
        return ""

    schema_steps = []
    for i, step_text in enumerate(steps, 1):
        # Skrati tekst koraka na razumnu dužinu
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
    howto_steps = []  # Za HowTo schema

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
        html_parts.append('<div class="faq-section"><h2>Frequently Asked Questions</h2>')
        for q, a in items:
            html_parts.append(
                f'<div class="faq-item">'
                f'<h3 class="faq-q">{html.escape(q)}</h3>'
                f'<p class="faq-a">{html.escape(a)}</p>'
                f'</div>'
            )
        html_parts.append('</div>')
        # Dodaj FAQ schema
        schema_parts.append(build_faq_schema(items))

    def _flush_internal_links(links):
        if not links:
            return
        items_html = ''
        for text, href in links:
            items_html += f'<li><a href="{html.escape(href)}">{html.escape(text)}</a></li>'
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
            'Slug:', 'Title:', 'Type:', '---'
        ])

        if is_new_tag and (in_table or in_faq or in_internal_links):
            close_open_blocks()

        if not line_stripped:
            if in_table:
                close_open_blocks()
            continue

        if line_stripped.startswith(('Slug:', 'Title:', 'Type:', '---')):
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
            # Only use intro as fallback if Meta: not already set
            if not meta_description:
                meta_limit = 155
                if len(intro_text) > meta_limit:
                    meta_description = intro_text[:meta_limit].rsplit(' ', 1)[0] + "..."
                else:
                    meta_description = intro_text
            html_parts.append(f'<p class="intro">{html.escape(intro_text)}</p>')

        # --- H2 ---
        elif line_stripped.startswith('H2:'):
            close_open_blocks()
            h2_text = line_stripped.replace('H2:', '').strip()
            html_parts.append(f'<h2>{html.escape(h2_text)}</h2>')

        # --- H3 ---
        elif line_stripped.startswith('H3:'):
            h3_text = line_stripped.replace('H3:', '').strip()
            html_parts.append(f'<h3>{html.escape(h3_text)}</h3>')

        # --- Tech Tip ---
        elif line_stripped.startswith('Tech Tip:'):
            close_open_blocks()
            tip_text = line_stripped.replace('Tech Tip:', '').strip()
            html_parts.append(
                f'<div class="tech-tip">'
                f'<strong>💡 Pro Tip:</strong> {html.escape(tip_text)}'
                f'</div>'
            )

        # --- CTA (supports CTA: and CTA[key]:) ---
        elif line_stripped.startswith('CTA'):
            close_open_blocks()
            # Parse CTA[key]: or plain CTA:
            cta_match = re.match(r'^CTA\[(\w+)\]:\s*(.*)', line_stripped)
            if cta_match:
                affiliate_key = cta_match.group(1).lower()
                cta_text = cta_match.group(2).strip()
            else:
                affiliate_key = "make"  # default
                cta_text = line_stripped.replace('CTA:', '').strip()
            affiliate = AFFILIATE_LINKS.get(affiliate_key, AFFILIATE_LINKS["make"])
            html_parts.append(
                f'<p class="inline-cta">{html.escape(cta_text)} '
                f'<a href="{affiliate["url"]}" rel="sponsored">{affiliate["cta_text"]}</a></p>'
            )

        # --- Workflow Steps ---
        elif line_stripped.startswith('Workflow Steps:'):
            close_open_blocks()
            section_title = line_stripped.replace('Workflow Steps:', '').strip()
            heading = section_title if section_title else 'Implementation Steps'
            html_parts.append(f'<h2>{html.escape(heading)}</h2>')
            html_parts.append('<ol class="steps">')
            in_list = True

        # --- Verdict ---
        elif line_stripped.startswith('Verdict:'):
            close_open_blocks()
            verdict_text = line_stripped.replace('Verdict:', '').strip()
            html_parts.append(
                f'<div class="verdict">'
                f'<strong>Bottom line:</strong> {html.escape(verdict_text)}'
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

        # --- Screenshot placeholder ---
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

                # --- Image ---
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
            # Use full alt_text for SEO — truncate at 125 chars if needed
            if alt_text:
                if len(alt_text) > 125:
                    alt_attr = alt_text[:125].rsplit(' ', 1)[0]
                else:
                    alt_attr = alt_text
            else:
                alt_attr = ''
            figure_html = (
                f'<figure class="screenshot">'
                f'<img src="{html.escape(img_path)}" alt="{html.escape(alt_attr)}" loading="lazy">'
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
            howto_steps.append(clean)  # Sakupljaj korake za schema
            html_parts.append(f'<li>{html.escape(clean)}</li>')

        # --- Regularni paragraf ---
        else:
            html_parts.append(f'<p>{html.escape(line_stripped)}</p>')

    # Zatvaranje svih otvorenih blokova
    close_open_blocks()

    if in_code_block and code_lines:
        escaped_code = html.escape('\n'.join(code_lines))
        html_parts.append(f'<pre><code>{escaped_code}</code></pre>')

    # HowTo schema za how-to stranice
    if page_type == 'how-to' and howto_steps:
        schema_parts.insert(0, None)  # Placeholder — title dolazi iz generate_site

    return '\n'.join(html_parts), meta_description, schema_parts, howto_steps


def generate_index(template_html, links):
    """Generiše index.html sa listom svih integracija."""
    cards = ""
    for l in links:
        description = l.get('description', '')
        if len(description) > 150:
            description = description[:150] + '...'

        cards += f"""
        <div class="card">
            <a href="{l['slug']}.html">
                <h2>{html.escape(l['title'])}</h2>
                <p>{html.escape(description)}</p>
                <span class="read-more">Read guide →</span>
            </a>
        </div>"""

    index_content = f"""
        <p class="intro">
            Step-by-step automation guides for business owners and operations teams.
            Stop copying data between apps — let Make.com do it automatically.
        </p>
        <div class="card-grid">
            {cards}
        </div>
    """

    page = template_html.replace('{{TITLE}}', 'Make.com Integration Guides')
    page = page.replace('{{META_DESCRIPTION}}',
        'Free step-by-step Make.com integration guides. '
        'Automate your business workflows and save hours every week.')
    page = page.replace('{{MAIN_CONTENT}}', index_content)
    page = page.replace('{{SCHEMA_MARKUP}}', '')

    page = page.replace(
        '<p class="reading-time">⏱ 5 min read · Make.com Integration Guide</p>', '')
    page = page.replace(
        '<a href="/" class="back-link">← All Integrations</a>', '')
    page = page.replace(
        '<div class="breadcrumb">',
        '<div class="breadcrumb" style="display:none">')

    page = page.replace('{{AFFILIATE_LINK}}', MAKE_AFFILIATE_LINK)
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

        if not slug or not title:
            print(f"⚠️  Preskačem entry bez slug/title")
            continue

        main_body, meta_desc, schema_parts, howto_steps = format_content(entry, page_type)

        # Generiši HowTo schema ako je how-to stranica
        all_schemas = []
        if page_type == 'how-to' and howto_steps:
            all_schemas.append(build_howto_schema(title, howto_steps))
        # Dodaj ostale schema (FAQ itd.) — preskači None placeholder
        for s in schema_parts:
            if s is not None:
                all_schemas.append(s)

        schema_html = '\n'.join(all_schemas)

        page = template_html.replace('{{TITLE}}', title)
        page = page.replace('{{META_DESCRIPTION}}', meta_desc)
        page = page.replace('{{MAIN_CONTENT}}', main_body)
        page = page.replace('{{SCHEMA_MARKUP}}', schema_html)
        page = page.replace('{{AFFILIATE_LINK}}', MAKE_AFFILIATE_LINK)

        output_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(page)

        print(f"✅ Generisano [{page_type}]: {slug}.html")
        
        links.append({
            'slug': slug,
            'title': title,
            'type': page_type,
            'description': meta_desc
        })

    index_html = generate_index(template_html, links)
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print(f"\n🚀 Gotovo! Generisano {len(links)} stranica + index.html")


if __name__ == "__main__":
    generate_site()