import feedparser
import requests
import os
import re
import json
from datetime import datetime, timedelta

SOURCES = [
    ("Medium", "https://medium.com/feed/@sinclairhuang"),
    ("Substack", "https://sinclairhuang.substack.com/feed"),
]
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
    text = re.sub('<[^<]+?>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def html_to_markdown(html):
    html = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', html, flags=re.DOTALL)
    html = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', html, flags=re.DOTALL)
    html = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', html, flags=re.DOTALL)
    html = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', html, flags=re.DOTALL)
    html = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', html, flags=re.DOTALL)
    html = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', html, flags=re.DOTALL)
    html = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', html, flags=re.DOTALL)
    html = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: '\n> ' + strip_html(m.group(1)).replace('\n', '\n> ') + '\n', html, flags=re.DOTALL)
    html = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', html, flags=re.DOTALL)
    html = re.sub(r'<[ou]l[^>]*>', '', html)
    html = re.sub(r'</[ou]l>', '', html)
    html = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html, flags=re.DOTALL)
    html = re.sub(r'<br\s*/?>', '\n', html)
    html = re.sub(r'<hr\s*/?>', '\n---\n', html)
    html = re.sub(r'<img[^>]*>', '', html)
    html = re.sub(r'<figure[^>]*>.*?</figure>', '', html, flags=re.DOTALL)
    html = re.sub('<[^<]+?>', '', html)
    html = re.sub(r'\n{4,}', '\n\n\n', html)
    return html.strip()

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
    return tags[:6]

def process_feed(source_name, feed_url, imported):
    print(f"Fetching {source_name} RSS: {feed_url}")
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
    try:
        resp = requests.get(feed_url, headers=headers, timeout=30)
        print(f"  HTTP status: {resp.status_code}, content length: {len(resp.content)}")
        feed = feedparser.parse(resp.content)
        print(f"  Parsed entries: {len(feed.entries)}, feed title: {feed.feed.get('title', 'N/A')}")
    except Exception as e:
        print(f"Error fetching {source_name}: {e}")
        feed = feedparser.parse(feed_url)
    if not feed.entries:
        print(f"No entries found in {source_name} RSS feed")
        return 0
    new_count = 0
    for entry in feed.entries:
        link = entry.get('link', '')
        title = entry.get('title', 'Untitled').lstrip('# ')
        if link in imported:
            print(f"Already imported: {title}")
            continue
        content_html = ''
        if hasattr(entry, 'content') and entry.content:
            content_html = entry.content[0].get('value', '')
        elif hasattr(entry, 'summary'):
            content_html = entry.summary
        if not content_html:
            print(f"No content for: {title}")
            continue
        content_md = html_to_markdown(content_html)
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            pub_date = datetime(*entry.published_parsed[:6])
            if pub_date.date() >= datetime.now().date():
                pub_date = datetime.now() - timedelta(days=1)
        else:
            pub_date = datetime.now() - timedelta(days=1)
        date_str = pub_date.strftime('%Y-%m-%d')
        description = strip_html(entry.get('summary', ''))[:200].replace('"', "'")
        tags = extract_tags(entry)
        tags_str = ', '.join([f'"{t}"' for t in tags]) if tags else '"AI", "Research"'
        slug = title_to_slug(title)
        filename = f"{date_str}-{slug}.md"
        filepath = os.path.join(BLOG_DIR, filename)
        if os.path.exists(filepath):
            print(f"File exists: {filename}")
            imported.append(link)
            continue
        title_escaped = title.replace('"', '\\"')
        if source_name == "Medium":
            footer = f"\n\n---\n\n*This article was originally published on Medium. [Read the full version with charts and figures \u2192]({link})*"
        else:
            footer = f"\n\n---\n\n*This article was originally published on Substack. [Read the full version with charts and figures \u2192]({link})*"
        front_matter = f"""---
title: "{title_escaped}"
date: {date_str}
draft: false
tags: [{tags_str}]
description: "{description}"
canonical: "{link}"
---

"""
        with open(filepath, 'w') as f:
            f.write(front_matter + content_md + footer)
        imported.append(link)
        new_count += 1
        print(f"Imported: {title} -> {filename}")
    return new_count

def main():
    os.makedirs(BLOG_DIR, exist_ok=True)
    imported = load_imported()
    total = 0
    for source_name, feed_url in SOURCES:
        total += process_feed(source_name, feed_url, imported)
    save_imported(imported)
    print(f"\nDone: {total} new articles imported")

if __name__ == '__main__':
    main()
