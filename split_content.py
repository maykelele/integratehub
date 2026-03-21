"""
Split input.txt into individual files:
  - Articles (Type: how-to, comparison) → content/NNN-slug.txt (numbered by Date)
  - Pages (Type: page) → pages/slug.txt (no numbering)

Run from project root: python split_content.py
"""

import os
import re

INPUT_FILE = 'content/input.txt'
CONTENT_DIR = 'content'
PAGES_DIR = 'pages'


def extract_field(text, field):
    """Extract a field value from article text."""
    for line in text.split('\n'):
        if line.startswith(field):
            return line[len(field):].strip()
    return None


def split_input():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw = f.read()

    entries = [e.strip() for e in raw.split('---') if e.strip()]

    articles = []
    pages = []

    for entry in entries:
        slug = extract_field(entry, 'Slug:')
        page_type = extract_field(entry, 'Type:') or 'how-to'
        date = extract_field(entry, 'Date:')

        if not slug:
            print(f"⚠️  Skipping entry without slug")
            continue

        if page_type == 'page':
            pages.append({'slug': slug, 'content': entry})
        else:
            articles.append({
                'slug': slug,
                'date': date or '9999-99-99',  # no-date fallback sorts last
                'content': entry
            })

    # Sort articles by date (chronological)
    articles.sort(key=lambda a: a['date'])

    # Create directories
    os.makedirs(CONTENT_DIR, exist_ok=True)
    os.makedirs(PAGES_DIR, exist_ok=True)

    # Write article files
    print(f"\n📄 Articles ({len(articles)}):")
    for i, article in enumerate(articles, start=1):
        filename = f"{i:03d}-{article['slug']}.txt"
        filepath = os.path.join(CONTENT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(article['content'] + '\n')
        print(f"  ✅ {filename}  (Date: {article['date']})")

    # Write page files
    print(f"\n📁 Pages ({len(pages)}):")
    for page in pages:
        filename = f"{page['slug']}.txt"
        filepath = os.path.join(PAGES_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page['content'] + '\n')
        print(f"  ✅ {filename}")

    print(f"\n✅ Done. {len(articles)} articles + {len(pages)} pages.")
    print(f"   input.txt preserved as backup.")


if __name__ == '__main__':
    split_input()