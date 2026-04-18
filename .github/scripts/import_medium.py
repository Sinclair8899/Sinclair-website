import feedparser
import os
import re
import json
from datetime import datetime, timedelta

MEDIUM_RSS = "https://medium.com/feed/@sinclairhuang"
BLOG_DIR = "content/blog"
IMPORTED_LOG = ".github/scripts/imported_medium.json"

def load_imported():
    if os.path.exists(IMPORTED_LOG):
        with open(IMPORTED_LOG) as f:
            return json.load(f)
    return []

def save_imported(imported):
    os.makedirs(os.path.dirname(IMPORTED_LOG), exist_ok=True)
    with open(IMPORTED_LOG, "w") as f:
        json.dump(imported, f, indent=2)

def strip_html(text):
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', text)
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def html_to_markdown(html):
    """Basic HTML to Markdown conversion"""
    # Headers
    html = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', html, flags=re.DOTALL)
    html = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', html, flags=re.DOTALL)
    html = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', html, flags=re.DOTALL)
    html = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', html, flags=re.DOTALL)

    # Bold and italic
    html = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', html, flags=re.DOTALL)
    html = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', html, flags=re.DOTALL)

    # Links
    html = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', html, flags=re.DOTALL)

    # Blockquotes
    html = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: '\n> ' + strip_html(m.group(1)).replace('\n', '\n> ') + '\n', html, flags=re.DOTALL)

    # Lists
    html = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', html, flags=re.DOTALL)
    html = re.sub(r'<[ou]l[^>]*>', '', html)
    html = re.sub(r'</[ou]l>', '', html)

    # Paragraphs and line breaks
    html = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html, flags=re.DOTALL)
    html = re.sub(r'<br\s*/?>', '\n', html)
    html = re.sub(r'<hr\s*/?>', '\n---\n', html)

    # Images (skip Medium's CDN images to avoid copyright issues)
    html = re.sub(r'<img[^>]*>', '', html)
    html = re.sub(r'<figure[^>]*>.*?</figure>', '', html, flags=re.DOTALL)

    # Remove remaining HTML tags
    html = re.sub('<[^<]+?>', '', html)

    # Clean up whitespace
    html = re.sub(r'\n{4,}', '\n\n\n', html)
    html = html.strip()

    return html

def title_to_slug(title):
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)
    return slug[:60].rstrip('-')

def extract_tags(entry):
    tags = []
    if hasattr(entry, 'tags'):
        for tag in entry.tags:
            term = tag.get('term', '')
            if term:
                tags.append(term.replace('#', '').strip())
    return tags[:6]  # Max 6 tags

def main():
    os.makedirs(BLOG_DIR, exist_ok=True)
    imported = load_imported()

    print(f"Fetching Medium RSS: {MEDIUM_RSS}")
    feed = feedparser.parse(MEDIUM_RSS)

    if not feed.entries:
        print("No entries found in RSS feed")
        return

    new_count = 0

    for entry in feed.entries:
        link = entry.get('link', '')
        title = entry.get('title', 'Untitled')

        # Skip if already imported
        if link in imported:
            print(f"Already imported: {title}")
            continue

        # Get content
        content_html = ''
        if hasattr(entry, 'content') and entry.content:
            content_html = entry.content[0].get('value', '')
        elif hasattr(entry, 'summary'):
            content_html = entry.summary

        if not content_html:
            print(f"No content for: {title}")
            continue

        # Convert to markdown
        content_md = html_to_markdown(content_html)

        # Get date (use yesterday to avoid Hugo future-date issue)
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            pub_date = datetime(*entry.published_parsed[:6])
            # Use yesterday if published today
            if pub_date.date() >= datetime.now().date():
                pub_date = datetime.now() - timedelta(days=1)
        else:
            pub_date = datetime.now() - timedelta(days=1)

        date_str = pub_date.strftime('%Y-%m-%d')

        # Get description from summary
        description = strip_html(entry.get('summary', ''))[:200].replace('"', "'")

        # Get tags
        tags = extract_tags(entry)
        tags_str = ', '.join([f'"{t}"' for t in tags]) if tags else '"AI", "Research"'

        # Create slug
        slug = title_to_slug(title)
        filename = f"{date_str}-{slug}.md"
        filepath = os.path.join(BLOG_DIR, filename)

        # Skip if file already exists
        if os.path.exists(filepath):
            print(f"File exists: {filename}")
            imported.append(link)
            continue

        # Build front matter
        title_escaped = title.replace('"', '\\"')
        front_matter = f"""---
title: "{title_escaped}"
date: {date_str}
draft: false
tags: [{tags_str}]
description: "{description}"
canonical: "{link}"
---

"""

        # Write file
        with open(filepath, 'w') as f:
            f.write(front_matter + content_md)

        imported.append(link)
        new_count += 1
        print(f"✅ Imported: {title} -> {filename}")

    save_imported(imported)
    print(f"\nDone: {new_count} new articles imported")

if __name__ == '__main__':
    main()
