import feedparser
from bs4 import BeautifulSoup
import datetime
import os

# 設定您的新聞頁面路徑 (假設是 docs/news/index.html)
# 如果程式說找不到，請確認實際路徑
TARGET_FILE = 'docs/news/index.html'

RSS_FEEDS = [
    {
        "category": "AI & Semiconductors",
        "url": "https://news.google.com/rss/search?q=Semiconductor+OR+Nvidia+OR+TSMC+OR+AI+Chip+when:7d&hl=en-US&gl=US&ceid=US:en"
    },
    {
        "category": "Biotech & AI",
        "url": "https://news.google.com/rss/search?q=Biotech+AI+OR+AlphaFold+OR+Generative+Biology+when:7d&hl=en-US&gl=US&ceid=US:en"
    }
]

def update_news_page():
    if not os.path.exists(TARGET_FILE):
        print(f"❌ 找不到目標檔案：{TARGET_FILE}")
        print("請檢查您的新聞頁面 index.html 到底在哪個資料夾？(例如 docs/ 還是 content/？)")
        return

    print("📡 正在從 Google News 抓取最新標題...")
    news_items = []
    
    for feed in RSS_FEEDS:
        print(f"   - 讀取: {feed['category']} ...")
        d = feedparser.parse(feed['url'])
        for entry in d.entries[:3]:
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "source": entry.source.title if 'source' in entry else "Google News"
            })

    with open(TARGET_FILE, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # 尋找新聞區塊 (標題含有 Industry News 或 Latest)
    news_header = None
    for h in soup.find_all(['h1', 'h2', 'h3', 'div']):
        if 'Industry News' in h.get_text() or 'Latest Industry News' in h.get_text():
            news_header = h
            break
    
    if not news_header:
        print("❌ 找不到 'Industry News' 標題，無法定位插入點。")
        return

    # 嘗試找到標題後的列表容器
    news_container = news_header.find_next(['ul', 'div'])
    
    if not news_container:
        news_container = soup.new_tag('ul')
        news_header.insert_after(news_container)
    else:
        news_container.clear() # 清空舊新聞

    print(f"📝 正在寫入 {len(news_items)} 則最新新聞...")
    
    if news_container.name != 'ul':
        new_ul = soup.new_tag('ul')
        news_container.append(new_ul)
        news_container = new_ul

    for item in news_items:
        li = soup.new_tag('li')
        li['style'] = "margin-bottom: 20px; list-style: none;"
        
        a = soup.new_tag('a', href=item['link'], target="_blank")
        a.string = item['title']
        a['style'] = "font-weight: 600; color: #2c3e50; text-decoration: none; font-size: 1.1em;"
        
        meta = soup.new_tag('div')
        meta.string = f"{item['source']} • {item['date']}"
        meta['style'] = "font-size: 0.85em; color: #7f8c8d; margin-top: 4px;"

        li.append(a)
        li.append(meta)
        news_container.append(li)

    with open(TARGET_FILE, 'w', encoding='utf-8') as file:
        file.write(str(soup.prettify()))

    print("🎉 新聞頁面更新成功！")

if __name__ == "__main__":
    update_news_page()
