import feedparser
import re
from datetime import datetime

today = datetime.now().strftime("%B %Y")

feeds = {
    "AI & Semiconductors": [
        ("Reuters Technology", "https://feeds.reuters.com/reuters/technologyNews"),
        ("The Verge", "https://www.theverge.com/rss/index.xml"),
        ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/technology-lab"),
    ],
    "Biotechnology": [
        ("Nature News", "https://www.nature.com/nature.rss"),
        ("BioSpace", "https://www.biospace.com/rss/news"),
    ]
}

semi_keywords = ["semiconductor", "chip", "AI", "TSMC", "NVIDIA", "HBM", "GPU", "supply chain", "memory", "foundry"]
bio_keywords = ["drug", "biotech", "AlphaFold", "cancer", "therapy", "clinical", "protein", "FDA", "precision medicine"]

def strip_html(text):
    return re.sub('<[^<]+?>', '', text)

def fetch_articles(feed_url, keywords, max_items=3):
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        for entry in feed.entries[:30]:
            title = entry.get("title", "")
            summary = strip_html(entry.get("summary", entry.get("description", "")))[:300]
            link = entry.get("link", "#")
            text = (title + " " + summary).lower()
            if any(kw.lower() in text for kw in keywords):
                articles.append({"title": title, "summary": summary, "link": link})
            if len(articles) >= max_items:
                break
        return articles
    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")
        return []

semi_articles = []
for source_name, url in feeds["AI & Semiconductors"]:
    items = fetch_articles(url, semi_keywords, 2)
    for item in items:
        item["source"] = source_name
        semi_articles.append(item)
    if len(semi_articles) >= 4:
        break

bio_articles = []
for source_name, url in feeds["Biotechnology"]:
    items = fetch_articles(url, bio_keywords, 2)
    for item in items:
        item["source"] = source_name
        bio_articles.append(item)
    if len(bio_articles) >= 3:
        break

def render_article(article, border_color):
    title = article["title"].replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    summary = article.get("summary", "")[:250]
    return f"""  <div style="margin: 1rem 0; padding: 1rem; border-left: 3px solid {border_color}; background: #f8fafc; border-radius: 0 8px 8px 0;">
    <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">
      <a href="{article['link']}" target="_blank" style="color: #1e40af; text-decoration: none;">{title}</a>
    </div>
    <div style="font-size: 0.875rem; color: #64748b; margin-bottom: 0.5rem;">{article['source']} • {today}</div>
    <div style="color: #334155; line-height: 1.6;">{summary}</div>
  </div>"""

semi_html = "\n".join([render_article(a, "#2563eb") for a in semi_articles]) if semi_articles else '  <p style="color:#64748b">No recent articles found.</p>'
bio_html = "\n".join([render_article(a, "#16a34a") for a in bio_articles]) if bio_articles else '  <p style="color:#64748b">No recent articles found.</p>'

content = f"""---
description: "Latest Industry News"
title: "Industry News"
---

# Latest Industry News

*Last updated: {today}*

<div style="margin: 2rem 0;">
  <h2 style="color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; margin-bottom: 1rem;">AI &amp; Semiconductors</h2>

{semi_html}
</div>

<div style="margin: 2rem 0;">
  <h2 style="color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; margin-bottom: 1rem;">Biotechnology</h2>

{bio_html}
</div>

<div style="margin: 3rem 0; padding: 1.5rem; background: #fef3c7; border-radius: 8px;">
  <h3 style="color: #92400e; margin-bottom: 1rem;">📰 News Sources</h3>
  <p style="color: #78350f; line-height: 1.8;">
    For the latest updates, visit:<br>
    • <a href="https://news.google.com/search?q=semiconductor+AI+chip" target="_blank" style="color: #1e40af;">Google News - Semiconductors &amp; AI</a><br>
    • <a href="https://news.google.com/search?q=biotechnology+drug+discovery" target="_blank" style="color: #1e40af;">Google News - Biotechnology</a><br>
    • <a href="https://www.reuters.com/technology/" target="_blank" style="color: #1e40af;">Reuters Technology</a><br>
    • <a href="https://www.bloomberg.com/technology" target="_blank" style="color: #1e40af;">Bloomberg Technology</a>
  </p>
</div>
"""

with open("content/news.md", "w") as f:
    f.write(content)

print(f"Done: {len(semi_articles)} semi + {len(bio_articles)} bio articles")
