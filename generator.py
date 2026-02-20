import os
import html

TEMPLATE_FILE = 'templates/template.html'
CONTENT_FILE = 'content/input.txt'
OUTPUT_DIR = 'public'
MAKE_AFFILIATE_LINK = "https://www.make.com/en/register?pc=integratehub"

# -----------------------------------------------------------------------
# PODRŽANI TAGOVI U input.txt:
#
#   Slug:           URL stranice (obavezno)
#   Title:          Naslov stranice (obavezno)
#   Type:           Tip stranice — how-to | comparison (default: how-to)
#   Introduction:   Uvodni paragraf + automatski meta description
#   Tech Tip:       Žuti info box sa savetom
#   Workflow Steps: Otvara numerisanu listu koraka
#   Verdict:        Završni paragraf — zatvara listu ako je otvorena
#   Python Snippet: Code blok
#   Table:          Comparison tabela — format: Header1|Header2|Header3
#                   Svaki red: vrednost1|vrednost2|vrednost3
#                   Kraj tabele: prazna linija ili novi tag
#   FAQ:            FAQ sekcija — format: Q: pitanje / A: odgovor
#                   Kraj FAQ: prazna linija ili novi tag
#   Internal Links: Linkovi na druge stranice — format: Tekst|slug.html
#                   Svaki link u novom redu
#   Screenshot:     Placeholder box dok nemaš pravu sliku
#                   Format: Screenshot: Opis šta treba da prikazuje
#                   Zameni sa Image: kada imaš pravi fajl
#   Image:          Prava slika — format: putanja/do/slike.png|Alt tekst
#                   Primer: Image: assets/screenshots/make-trigger.png|Make.com trigger setup
#   ---             Separator između stranica
#
#   Sve ostale linije → <p> paragraf
# -----------------------------------------------------------------------


def extract_field(lines, prefix):
    """Izvlači vrednost polja po prefiksu."""
    return next(
        (l.replace(prefix, '').strip() for l in lines if l.startswith(prefix)), ""
    )


def format_content(text):
    """Parsira strukturirani tekst i generiše semantički HTML."""
    lines = text.split('\n')
    html_parts = []

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

    def close_open_blocks():
        """Zatvara sve otvorene blokove."""
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
        """Renderuje HTML tabelu iz sakupljenih redova."""
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
        """Renderuje FAQ sekciju iz sakupljenih pitanja."""
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

    def _flush_internal_links(links):
        """Renderuje 'Related guides' sekciju."""
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

        # Detektujemo novi tag — zatvara prethodni blok
        is_new_tag = any(line_stripped.startswith(tag) for tag in [
            'Introduction:', 'Tech Tip:', 'Workflow Steps:', 'Verdict:',
            'Python Snippet:', 'Table:', 'FAQ:', 'Internal Links:',
            'Screenshot:', 'Image:',
            'Slug:', 'Title:', 'Type:', '---'
        ])

        if is_new_tag and (in_table or in_faq or in_internal_links):
            close_open_blocks()

        # Preskači prazne linije i meta polja
        if not line_stripped:
            if in_table:
                close_open_blocks()
            elif in_faq:
                pass  # FAQ dozvoljava prazne linije između Q/A
            continue

        if line_stripped.startswith(('Slug:', 'Title:', 'Type:', '---')):
            continue

        # --- Introduction ---
        if line_stripped.startswith('Introduction:'):
            intro_text = line_stripped.replace('Introduction:', '').strip()
            meta_description = intro_text[:155]
            html_parts.append(f'<p class="intro">{html.escape(intro_text)}</p>')

        # --- Tech Tip ---
        elif line_stripped.startswith('Tech Tip:'):
            close_open_blocks()
            tip_text = line_stripped.replace('Tech Tip:', '').strip()
            html_parts.append(
                f'<div class="tech-tip">'
                f'<strong>💡 Pro Tip:</strong> {html.escape(tip_text)}'
                f'</div>'
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

        # --- Image (prava slika) ---
        elif line_stripped.startswith('Image:'):
            close_open_blocks()
            image_data = line_stripped.replace('Image:', '').strip()
            if '|' in image_data:
                img_path, alt_text = image_data.split('|', 1)
                img_path = img_path.strip()
                alt_text = alt_text.strip()
            else:
                img_path = image_data.strip()
                alt_text = ''
            html_parts.append(
                f'<figure class="screenshot">'
                f'<img src="{html.escape(img_path)}" alt="{html.escape(alt_text)}" loading="lazy">'
                f'<figcaption>{html.escape(alt_text)}</figcaption>'
                f'</figure>'
            )

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
            html_parts.append(f'<li>{html.escape(clean)}</li>')

        # --- Regularni paragraf ---
        else:
            html_parts.append(f'<p>{html.escape(line_stripped)}</p>')

    # Zatvaranje svih otvorenih blokova na kraju entry-ja
    close_open_blocks()

    if in_code_block and code_lines:
        escaped_code = html.escape('\n'.join(code_lines))
        html_parts.append(f'<pre><code>{escaped_code}</code></pre>')

    return '\n'.join(html_parts), meta_description


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

    page = page.replace(
        '<p class="reading-time">⏱ 5 min read · Make.com Integration Guide</p>', '')
    page = page.replace(
        '<a href="index.html" class="back-link">← All Integrations</a>', '')
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

        main_body, meta_desc = format_content(entry)

        page = template_html.replace('{{TITLE}}', title)
        page = page.replace('{{META_DESCRIPTION}}', meta_desc)
        page = page.replace('{{MAIN_CONTENT}}', main_body)
        page = page.replace('{{AFFILIATE_LINK}}', MAKE_AFFILIATE_LINK)

        output_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(page)

        links.append({
            'slug': slug,
            'title': title,
            'type': page_type,
            'description': meta_desc[:150] + '...' if len(meta_desc) > 150 else meta_desc
        })

        print(f"✅ Generisano [{page_type}]: {slug}.html")

    index_html = generate_index(template_html, links)
    index_html = index_html.replace('{{AFFILIATE_LINK}}', MAKE_AFFILIATE_LINK)
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print(f"\n🚀 Gotovo! Generisano {len(links)} stranica + index.html")


if __name__ == "__main__":
    generate_site()