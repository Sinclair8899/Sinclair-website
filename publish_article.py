import os
import datetime
from bs4 import BeautifulSoup

# 設定
DRAFT_FILE = 'draft.txt'
DOCS_DIR = 'docs'
BLOG_DIR = os.path.join(DOCS_DIR, 'blog')
BLOG_INDEX_FILE = os.path.join(BLOG_DIR, 'index.html')
HOME_INDEX_FILE = os.path.join(DOCS_DIR, 'index.html')

# 文章頁面的樣式 (Medium 風格)
ARTICLE_STYLE = """
<style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.8; color: #333; max-width: 740px; margin: 0 auto; padding: 40px 20px; }
    h1 { font-size: 2.2em; margin-bottom: 0.2em; font-weight: 700; color: #111; letter-spacing: -0.02em; }
    .meta { color: #757575; font-size: 0.9em; margin-bottom: 30px; }
    p { font-size: 1.15em; margin-bottom: 1.5em; color: #2c3e50; }
    a.back { text-decoration: none; color: #555; border: 1px solid #ddd; padding: 6px 12px; border-radius: 20px; font-size: 0.85em; transition: all 0.2s; }
    a.back:hover { background: #f5f5f5; border-color: #bbb; }
    hr { border: 0; height: 1px; background: #eee; margin: 40px 0; }
</style>
"""

# Blog 列表頁面的樣式
BLOG_INDEX_STYLE = """
<style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 40px 20px; }
    h1 { font-size: 2.5em; font-weight: 800; margin-bottom: 10px; color: #2c3e50; }
    .subtitle { color: #7f8c8d; font-size: 1.2em; margin-bottom: 40px; }
    ul { list-style: none; padding: 0; }
    li { margin-bottom: 25px; border-bottom: 1px solid #eee; padding-bottom: 25px; }
    a.title { font-size: 1.4em; font-weight: 600; color: #2980b9; text-decoration: none; display: block; margin-bottom: 5px; }
    a.title:hover { text-decoration: underline; color: #3498db; }
    .date { color: #95a5a6; font-size: 0.9em; }
    .nav { margin-bottom: 40px; }
    .nav a { margin-right: 15px; color: #555; text-decoration: none; font-weight: 500; }
    .nav a:hover { color: #000; }
</style>
"""

def publish():
    # 1. 讀取草稿
    if not os.path.exists(DRAFT_FILE):
        print(f"❌ 找不到草稿檔案：{DRAFT_FILE}")
        return

    content = ""
    try:
        with open(DRAFT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print("⚠️ 切換至 Big5 編碼讀取...")
        try:
            with open(DRAFT_FILE, 'r', encoding='big5') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ 無法讀取檔案：{e}")
            return

    # 2. 輸入標題
    title = input("請輸入文章標題 (Title): ").strip()
    if not title:
        print("標題不能為空！")
        return

    # 3. 處理內容與檔名
    paragraphs = "".join([f"<p>{line.strip()}</p>" for line in content.split('\n') if line.strip()])
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 建立乾淨的檔名 (移除 draft 字樣，改用標題)
    clean_title = "".join([c for c in title if c.isalnum() or c in [' ', '-']]).replace(' ', '-').lower()
    filename = f"{today}-{clean_title}.html"
    filepath = os.path.join(BLOG_DIR, filename)

    if not os.path.exists(BLOG_DIR):
        os.makedirs(BLOG_DIR)

    # 4. 生成單篇文章 HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - Sinclair Huang</title>
        {ARTICLE_STYLE}
    </head>
    <body>
        <div style="margin-bottom: 30px;">
            <a href="index.html" class="back">← Back to Blog</a>
            <a href="../index.html" class="back" style="margin-left:10px;">Home</a>
        </div>
        <article>
            <h1>{title}</h1>
            <div class="meta">Po-Sung (Sinclair) Huang · {today}</div>
            <hr>
            {paragraphs}
        </article>
        <hr>
        <footer style="text-align: center; font-size: 0.8em; color: #999; margin-top: 50px;">
            © {datetime.datetime.now().year} Sinclair Huang
        </footer>
    </body>
    </html>
    """

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 文章頁面已建立：{filepath}")

    # 5. 更新 Blog 首頁 (列表)
    update_blog_index(title, filename, today)
    
    # 6. 清理首頁 (移除之前的 Latest Insights)
    clean_home_page()

def update_blog_index(title, filename, date):
    # 如果 Blog 首頁不存在，建立一個新的
    if not os.path.exists(BLOG_INDEX_FILE):
        print("🆕 建立全新的 Blog 首頁...")
        base_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Insights & Analysis - Sinclair Huang</title>
            {BLOG_INDEX_STYLE}
        </head>
        <body>
            <div class="nav">
                <a href="../index.html">← Home</a>
                <a href="../news/index.html">News</a>
            </div>
            <h1>Insights & Analysis</h1>
            <div class="subtitle">Research notes, industry analysis, and thoughts on AI & Biotech.</div>
            <hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;">
            <ul id="article-list">
                </ul>
        </body>
        </html>
        """
        with open(BLOG_INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(base_html)

    # 讀取 Blog 首頁並插入新連結
    with open(BLOG_INDEX_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    list_container = soup.find('ul', id='article-list')
    if not list_container:
        # 如果找不到列表 (可能是舊檔案)，就插在 hr 後面
        list_container = soup.new_tag('ul', id='article-list')
        hr = soup.find('hr')
        if hr: hr.insert_after(list_container)
        else: soup.body.append(list_container)

    # 檢查連結是否已存在
    if not list_container.find('a', href=filename):
        new_li = soup.new_tag('li')
        
        link = soup.new_tag('a', href=filename, class_='title')
        link.string = title
        
        date_div = soup.new_tag('div', class_='date')
        date_div.string = date
        
        new_li.append(link)
        new_li.append(date_div)
        
        # 插在最前面
        list_container.insert(0, new_li)
        
        with open(BLOG_INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        print("🎉 Blog 列表已更新！")
    else:
        print("ℹ️ 文章連結已存在於 Blog 列表。")

def clean_home_page():
    if not os.path.exists(HOME_INDEX_FILE): return
    
    with open(HOME_INDEX_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    changed = False
    
    # 1. 刪除亂入的 H2 標題
    for h2 in soup.find_all('h2'):
        if "Latest Insights" in h2.get_text():
            print("🧹 正在移除首頁上的 'Latest Insights' 區塊 (將移動至 Blog)...")
            # 刪除跟在後面的列表 (ul)
            next_ul = h2.find_next_sibling('ul')
            if next_ul: next_ul.decompose()
            h2.decompose()
            changed = True
    
    # 2. 刪除亂入的 Body 開頭列表 (針對之前的錯誤)
    if soup.body:
        first_elem = soup.body.find('ul', recursive=False)
        # 如果 body 第一個元素是 ul 且裡面有 blog 連結，大概就是錯的
        if first_elem and first_elem.find('a', href=lambda x: x and 'blog/' in x):
            print("🧹 正在移除首頁頂端錯誤的列表...")
            first_elem.decompose()
            changed = True

    if changed:
        with open(HOME_INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        print("✅ 首頁已修復還原。")

if __name__ == "__main__":
    publish()
