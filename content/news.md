---
title: "Industry News"
---

# Latest Industry News

<div id="news-feed">
  <p style="text-align: center; padding: 2rem;">Loading news from Google...</p>
</div>

<script>
console.log('News page loaded, starting to fetch...');

async function loadNews() {
  const container = document.getElementById('news-feed');
  console.log('Container found:', container);
  
  try {
    const apiUrl = 'https://api.rss2json.com/v1/api.json';
    const feedUrl = 'https://news.google.com/rss/search?q=semiconductor+chip&hl=en-US';
    const fullUrl = apiUrl + '?rss_url=' + encodeURIComponent(feedUrl) + '&count=10';
    
    console.log('Fetching from:', fullUrl);
    
    const response = await fetch(fullUrl);
    console.log('Response received:', response.status);
    
    const data = await response.json();
    console.log('Data:', data);
    
    if (data.status === 'ok' && data.items && data.items.length > 0) {
      let html = '<h2 style="color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem;">Latest News</h2>';
      
      data.items.forEach(item => {
        html += '<div style="margin: 1rem 0; padding: 1rem; border-left: 3px solid #2563eb; background: #f8fafc; border-radius: 0 8px 8px 0;">';
        html += '<div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;"><a href="' + item.link + '" target="_blank" style="color: #1e40af; text-decoration: none;">' + item.title + '</a></div>';
        html += '<div style="font-size: 0.875rem; color: #64748b;">' + new Date(item.pubDate).toLocaleDateString() + '</div>';
        html += '</div>';
      });
      
      container.innerHTML = html;
      console.log('News loaded successfully!');
    } else {
      container.innerHTML = '<p style="color: #dc2626;">No news available. Status: ' + data.status + '</p>';
      console.log('No items in response');
    }
  } catch (error) {
    console.error('Error loading news:', error);
    container.innerHTML = '<p style="color: #dc2626;">Error loading news: ' + error.message + '</p>';
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadNews);
} else {
  loadNews();
}
</script>
