import feedparser
import requests
import os
import re
import json
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Transform layer is stdlib-only and offline-tested (test_import_medium.py
# runs BEFORE feedparser/requests are installed in the workflow).
from medium_transform import DescriptionError, description_from_html, front_matter

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
    """Build a URL slug, keeping CJK characters.

    Stripping every non-ASCII character collapsed every Chinese title to the
    same slug (e.g. both "AI離開螢幕之後…" and "從結構到行為…" became "ai"),
    so Chinese posts collided with each other and with the existing
    2026-06-29-ai.md. The site already serves CJK URLs (e.g. /categories/半導體/),
    so keeping those characters is both safe and more meaningful.
    """
    slug = title.lower()
    # keep ASCII alphanumerics, whitespace, hyphens, and CJK ideographs
    slug = re.sub(r'[^a-z0-9\s\-㐀-䶿一-鿿豈-﫿]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)
    return slug[:60].rstrip('-')

def find_existing_by_slug(slug):
    """Return an existing post with this slug under ANY date, or None.

    Cross-posting means the same article arrives from both Medium and Substack
    under different URLs and often a different publication date. Matching on
    "{date}-{slug}.md" alone therefore lets a same-day repost through as a
    duplicate post. Matching on the slug regardless of date closes that hole.
    """
    # A very short slug is not distinctive enough to prove two posts are the
    # same article; blocking on it would silently drop legitimate new posts.
    if not slug or len(slug) < 8 or not os.path.isdir(BLOG_DIR):
        return None
    for name in os.listdir(BLOG_DIR):
        if not name.endswith('.md'):
            continue
        stem = name[:-3]
        # strip a leading YYYY-MM-DD- date prefix, if present
        body = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', stem)
        # tolerate Finder-style " 2" copy suffixes already present in the repo
        body = re.sub(r' \d+$', '', body)
        if body == slug:
            return name
    return None

def extract_tags(entry):
    tags = []
    if hasattr(entry, 'tags'):
        for tag in entry.tags:
            term = tag.get('term', '')
            if term:
                tags.append(term.replace('#', '').strip())
    return tags[:6]

def process_feed(source_name, feed_url, imported):
    """Fetch layer only — parsing/writing is process_entries (testable offline)."""
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
        return 0, 0
    return process_entries(source_name, feed.entries, imported)


def process_entries(source_name, entries, imported, blog_dir=None):
    """Returns (new_count, failed_count). A DescriptionError article is a
    FAILURE of the run: it is not written, and its URL is NOT recorded in
    imported_medium.json, so the whole batch retries after a fix."""
    blog_dir = blog_dir or BLOG_DIR
    new_count = 0
    failed_count = 0
    for entry in entries:
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
        # Description comes from the offline transform layer: 1-2 complete
        # body sentences in 120-160 code points, never a [:200] cut. A
        # non-compliant article FAILS this import run and is NOT recorded
        # as imported, so it retries after a fix instead of vanishing.
        try:
            description = description_from_html(content_html)
        except DescriptionError as exc:
            print(f"FAILED (no compliant description, not recorded): {title} — {exc}")
            failed_count += 1
            continue
        tags = extract_tags(entry)
        slug = title_to_slug(title)
        filename = f"{date_str}-{slug}.md"
        filepath = os.path.join(blog_dir, filename)
        if os.path.exists(filepath):
            print(f"File exists: {filename}")
            imported.append(link)
            continue
        existing = find_existing_by_slug(slug)
        if existing:
            print(f"Cross-post of an existing article, skipping: {title} (already at {existing})")
            imported.append(link)
            continue
        if source_name == "Medium":
            footer = f"\n\n---\n\n*This article was originally published on Medium. [Read the full version with charts and figures \u2192]({link})*"
        else:
            footer = f"\n\n---\n\n*This article was originally published on Substack. [Read the full version with charts and figures \u2192]({link})*"
        # front_matter() writes cta: "subscribe" explicitly (the dispatcher
        # fails builds on missing cta) and never guesses primary_cluster.
        fm = front_matter(title, date_str, tags, description, link)
        with open(filepath, 'w') as f:
            f.write(fm + content_md + footer)
        imported.append(link)
        new_count += 1
        print(f"Imported: {title} -> {filename}")
    return new_count, failed_count

def exit_code(total_failed):
    """A run with any non-compliant article stops NONZERO: the CI job fails,
    nothing is committed, and the unrecorded URLs retry next run."""
    return 1 if total_failed else 0

def main():
    os.makedirs(BLOG_DIR, exist_ok=True)
    imported = load_imported()
    total = 0
    failed = 0
    for source_name, feed_url in SOURCES:
        n, f = process_feed(source_name, feed_url, imported)
        total += n
        failed += f
    save_imported(imported)
    print(f"\nDone: {total} new articles imported, {failed} failed")
    sys.exit(exit_code(failed))

if __name__ == '__main__':
    main()
