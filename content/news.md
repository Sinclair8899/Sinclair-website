---
title: "Industry News"
---

# Latest Industry News

<div id="news-feed">Loading news...</div>

<script>
async function loadNews() {
  const container = document.getElementById('news-feed');
  const apiUrl = 'https://api.rss2json.com/v1/api.json?rss_url=';
  const feedUrl = 'https://news.google.com/rss/search?q=semiconductor+AI+chip&hl=en-US';
  
  try {
    const response = await fetch(apiUrl + encodeURIComponent(feedUrl) + '&count=10');
    const data = await response.json();
    
    if (data.status === 'ok') {
      let html = '<h2>AI & Semiconductors</h2>';
      data.items.forEach(item => {
        html += '<div style="margin: 1rem 0; padding: 1rem; border-left: 3px solid #2563eb; background: #f8fafc;">';
        html += '<div><a href="' + item.link + '" target="_blank" style="color: #1e40af; font-weight: 600;">' + item.title + '</a></div>';
        html += '<div style="font-size: 0.875rem; color: #64748b; margin-top: 0.5rem;">' + new Date(item.pubDate).toLocaleDateString() + '</div>';
        html += '</div>';
      });
      container.innerHTML = html;
    }
  } catch (error) {
    container.innerHTML = '<p>Loading news...</p>';
  }
}

document.addEventListener('DOMContentLoaded', loadNews);
</script>
