import os
import datetime
from bs4 import BeautifulSoup

DRAFT_FILE = 'draft.txt'
DOCS_DIR = 'docs'
BLOG_DIR = os.path.join(DOCS_DIR, 'blog')
INDEX_FILE = os.path.join(DOCS_DIR, 'index.html')

STYLE = """
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
    if not os.path.exists(DRAFT_FILE):
        print(f"❌ 找不到草稿檔案：{DRAFT_FILE}")
        return

    # === 修改重點：增加 Big5 相容性 ===
    content = ""
    try:
        # 先嘗試用 UTF-8 讀取
        with open(DRAFT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print("⚠️ 偵測到非 UTF-8 編碼，嘗試切換至 Big5 (繁體中文) 模式讀取...")
        try:
            with open(DRAFT_FILE, 'r', encoding='big5') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ 仍然無法讀取檔案，請確認檔案是否為純文字檔。錯誤：{e}")
            return
    # =================================

    title = input("請輸入文章標題 (Title): ").strip()
    if not title:
        print("標題不能為空！")
        return

    paragraphs = "".join([f"<p>{line.strip()}</p>" for line in content.split('\n') if line.strip()])
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-{title.replace(' ', '-').lower()}.html"
    filename = "".join([c for c in filename if c.isalnum() or c in ['-', '.']])
    
    filepath = os.path.join(BLOG_DIR, filename)

    if not os.path.exists(BLOG_DIR):
        os.makedirs(BLOG_DIR)

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
        <div style="margin-bottom: 30px;"><a href="../index.html" class="back">← Back to Home</a></div>
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
    update_index(title, filename, today)

def update_index(title, filename, date):
    if not os.path.exists(INDEX_FILE):
        print("❌ 找不到首頁 index.html")
        return

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    section_title = None
    for h in soup.find_all(['h2', 'h3']):
        if 'Insight' in h.get_text() or 'Blog' in h.get_text() or 'Analysis' in h.get_text():
            section_title = h
            break
    
    if not section_title:
        print("⚠️  正在建立新的 'Latest Insights' 區塊...")
        pub_list = soup.find('ul', {'id': 'publications-list'})
        if not pub_list:
            target = soup.find('body')
        else:
            target = pub_list.find_next_sibling() or pub_list.parent
        
        new_h2 = soup.new_tag('h2')
        new_h2.string = "Latest Insights & Analysis"
        new_ul = soup.new_tag('ul', id='insights-list')
        
        if pub_list:
            pub_list.insert_after(new_ul)
            pub_list.insert_after(new_h2)
            section_title = new_h2
        else:
            soup.body.insert(0, new_ul)
            soup.body.insert(0, new_h2)

    container = section_title.find_next('ul')
    if not container:
        container = soup.new_tag('ul')
        section_title.insert_after(container)

    new_li = soup.new_tag('li')
    link = soup.new_tag('a', href=f"blog/{filename}")
    link.string = title
    link['style'] = "font-weight: bold; color: #d35400;"
    
    date_span = soup.new_tag('span')
    date_span.string = f" ({date})"
    date_span['style'] = "color: #7f8c8d; font-size: 0.9em;"

    new_li.append(link)
    new_li.append(date_span)
    container.insert(0, new_li)

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

    print("🎉 首頁已更新！文章連結已加入。")

if __name__ == "__main__":
    publish()
