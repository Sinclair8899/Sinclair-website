import os
import datetime
from bs4 import BeautifulSoup

# 設定
DRAFT_FILE = 'draft.txt'
DOCS_DIR = 'docs'
BLOG_DIR = os.path.join(DOCS_DIR, 'blog')
BLOG_INDEX_FILE = os.path.join(BLOG_DIR, 'index.html')
HOME_INDEX_FILE = os.path.join(DOCS_DIR, 'index.html')

# 文章內頁樣式 (維持不變)
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

    # 3. 處理內容
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    paragraphs = "".join([f"<p>{line}</p>" for line in lines])
    
    # 抓取第一段作為「摘要」 (Summary)
    summary = lines[0] if lines else "Click to read more..."
    if len(summary) > 150: summary = summary[:150] + "..."

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 建立檔名
    clean_title = "".join([c for c in title if c.isalnum() or c in [' ', '-']]).replace(' ', '-').lower()
    filename = f"{today}-{clean_title}.html"
    filepath = os.path.join(BLOG_DIR, filename)

    if not os.path.exists(BLOG_DIR):
        os.makedirs(BLOG_DIR)

    # 4. 生成文章頁面
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

    # 5. 更新 Blog 列表 (PaperMod 風格)
    update_blog_index(title, filename, today, summary)

def update_blog_index(title, filename, date, summary):
    if not os.path.exists(BLOG_INDEX_FILE):
        print("❌ 找不到 Blog 首頁 index.html，無法插入。")
        return

    with open(BLOG_INDEX_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # === 1. 清理舊的「亂入」文字 (如果有) ===
    # 刪除 body 直接包含的文字節點 (那些擠在左下角的字)
    for element in soup.body.contents:
        if element.name is None and "馬年展望" in str(element):
            element.extract()
    # 刪除可能存在的錯誤列表
    wrong_ul = soup.find('ul', id='article-list')
    if wrong_ul: wrong_ul.decompose()

    # === 2. 尋找主要容器 (Main Container) ===
    # PaperMod 主題通常把文章放在 <main class="main"> 裡面
    main_container = soup.find('main', class_='main')
    
    if not main_container:
        print("⚠️ 找不到 main 容器，嘗試搜尋第一個 article 的父層...")
        first_article = soup.find('article')
        if first_article:
            main_container = first_article.parent
        else:
            main_container = soup.body

    # === 3. 建立 PaperMod 風格的卡片 ===
    # <article class="post-entry"> 
    #   <header><h2>Title</h2></header>
    #   <div content>Summary</div>
    #   <footer>Meta</footer>
    #   <a class="entry-link"></a>
    # </article>
    
    new_article = soup.new_tag('article', attrs={'class': 'post-entry'})
    
    # Header
    header = soup.new_tag('header', attrs={'class': 'entry-header'})
    h2 = soup.new_tag('h2')
    h2.string = title
    header.append(h2)
    
    # Content (Summary)
    content_div = soup.new_tag('div', attrs={'class': 'entry-content'})
    p = soup.new_tag('p')
    p.string = summary
    content_div.append(p)
    
    # Footer
    footer = soup.new_tag('footer', attrs={'class': 'entry-footer'})
    span = soup.new_tag('span')
    span.string = f"{date} · Po-Sung (Sinclair) Huang"
    footer.append(span)
    
    # Link (覆蓋整個卡片的連結)
    link = soup.new_tag('a', attrs={
        'class': 'entry-link',
        'aria-label': f"post link to {title}",
        'href': filename
    })
    
    # 組裝
    new_article.append(header)
    new_article.append(content_div)
    new_article.append(footer)
    new_article.append(link)

    # === 4. 插入到列表最上方 ===
    # 找到第一個現有的 article，插在它前面
    first_existing_article = main_container.find('article', class_='post-entry')
    if first_existing_article:
        first_existing_article.insert_before(new_article)
    else:
        # 如果沒有文章，就插在 main 的最後面
        main_container.append(new_article)

    with open(BLOG_INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
        
    print(f"🎉 Blog 列表已更新！文章已以「卡片風格」插入。")

if __name__ == "__main__":
    publish()
