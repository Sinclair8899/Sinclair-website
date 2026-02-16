import os
import datetime
from bs4 import BeautifulSoup

# 設定
DRAFT_FILE = 'draft.txt'
DOCS_DIR = 'docs'
BLOG_DIR = os.path.join(DOCS_DIR, 'blog')
INDEX_FILE = os.path.join(DOCS_DIR, 'index.html')

# Medium 風格的 CSS 樣式
STYLE = """
<style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 700px; margin: 0 auto; padding: 20px; }
    h1 { font-size: 2.5em; margin-bottom: 0.2em; font-weight: 700; color: #111; }
    .meta { color: #757575; font-size: 0.9em; margin-bottom: 30px; }
    p { font-size: 1.1em; margin-bottom: 1.5em; letter-spacing: -0.003em; }
    a.back { text-decoration: none; color: #555; border: 1px solid #ddd; padding: 5px 10px; border-radius: 4px; font-size: 0.8em; }
    a.back:hover { background: #f5f5f5; }
    hr { border: 0; height: 1px; background: #eee; margin: 40px 0; }
</style>
"""

def publish():
    # 1. 檢查草稿
    if not os.path.exists(DRAFT_FILE):
        print(f"❌ 找不到草稿檔案：{DRAFT_FILE}")
        print("請先建立一個 draft.txt 並貼上您的文章內容。")
        return

    # 2. 詢問標題
    title = input("請輸入文章標題 (Title): ").strip()
    if not title:
        print("標題不能為空！")
        return

    # 3. 讀取內容並轉為 HTML 段落
    with open(DRAFT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 簡單的換行轉段落處理
    paragraphs = "".join([f"<p>{line.strip()}</p>" for line in content.split('\n') if line.strip()])
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-{title.replace(' ', '-').lower()}.html"
    # 移除檔名中的特殊符號
    filename = "".join([c for c in filename if c.isalnum() or c in ['-', '.']])
    
    filepath = os.path.join(BLOG_DIR, filename)

    # 確保 blog 資料夾存在
    if not os.path.exists(BLOG_DIR):
        os.makedirs(BLOG_DIR)

    # 4. 生成文章頁面 HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - Sinclair Huang</title>
        {STYLE}
    </head>
    <body>
        <div style="margin-bottom: 20px;"><a href="../index.html" class="back">← Back to Home</a></div>
        <article>
            <h1>{title}</h1>
            <div class="meta">Po-Sung (Sinclair) Huang · {today}</div>
            <hr>
            {paragraphs}
        </article>
        <hr>
        <footer style="text-align: center; font-size: 0.8em; color: #999;">
            © {datetime.datetime.now().year} Sinclair Huang
        </footer>
    </body>
    </html>
    """

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 文章頁面已建立：{filepath}")

    # 5. 更新首頁列表
    update_index(title, filename, today)

def update_index(title, filename, date):
    if not os.path.exists(INDEX_FILE):
        print("❌ 找不到首頁 index.html，無法自動加入連結。")
        return

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # 尋找 "Insights" 或 "Blog" 區塊，如果沒有就建立一個
    section_title = None
    for h in soup.find_all(['h2', 'h3']):
        if 'Insight' in h.get_text() or 'Blog' in h.get_text() or 'Analysis' in h.get_text():
            section_title = h
            break
    
    # 如果還沒有 Insights 區塊，我們把它插在 Publications 之後
    if not section_title:
        print("⚠️  正在建立新的 'Latest Insights' 區塊...")
        # 找 Publications
        pub_list = soup.find('ul', {'id': 'publications-list'})
        if not pub_list:
            # 隨便找個地方插
            target = soup.find('body')
        else:
            target = pub_list.find_next_sibling() or pub_list.parent
        
        # 建立標題與列表
        new_h2 = soup.new_tag('h2')
        new_h2.string = "Latest Insights & Analysis"
        new_ul = soup.new_tag('ul', id='insights-list')
        
        if pub_list:
            pub_list.insert_after(new_ul)
            pub_list.insert_after(new_h2)
            section_title = new_h2
        else:
            # 插在 body 最前面（緊急用）
            soup.body.insert(0, new_ul)
            soup.body.insert(0, new_h2)

    # 找到列表容器
    container = section_title.find_next('ul')
    if not container:
        container = soup.new_tag('ul')
        section_title.insert_after(container)

    # 插入新文章連結
    new_li = soup.new_tag('li')
    link = soup.new_tag('a', href=f"blog/{filename}")
    link.string = title
    link['style'] = "font-weight: bold; color: #d35400;" # 用不同顏色區分
    
    date_span = soup.new_tag('span')
    date_span.string = f" ({date})"
    date_span['style'] = "color: #7f8c8d; font-size: 0.9em;"

    new_li.append(link)
    new_li.append(date_span)
    
    # 插在最前面
    container.insert(0, new_li)

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

    print("🎉 首頁已更新！文章連結已加入。")

if __name__ == "__main__":
    publish()
