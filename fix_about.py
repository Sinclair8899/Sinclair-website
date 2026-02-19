import os
from bs4 import BeautifulSoup

# 可能的路徑清單
possible_paths = [
    'themes/sinclair-theme/layouts/index.html',
    'layouts/index.html',
    'index.html'
]

about_content = """
<section id="about" class="py-5">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 mx-auto">
                <h2 class="mb-4">About Me</h2>
                <p class="lead">
                    Sinclair Huang 是一位專注於人工智慧（AI）、實體基礎設施與資本市場交叉領域的研究員。他擁有 HEC Liège（列日大學管理學院）的企業管理高階博士學位 (EDBA)。
                </p>
                <p>
                    其研究重點在於新興市場跨國企業如何透過 AI 驅動的決策模型與全球佈局維持競爭優勢。
                </p>
            </div>
        </div>
    </div>
</section>
"""

target_path = None
for p in possible_paths:
    if os.path.exists(p):
        target_path = p
        break

if not target_path:
    print("❌ 找不到 index.html，請確認你是否在網站根目錄執行。")
else:
    with open(target_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    existing = soup.find('section', id='about')
    new_block = BeautifulSoup(about_content, 'html.parser')
    
    if existing:
        existing.replace_with(new_block)
        print(f"✅ 已更新既存的 About 區塊: {target_path}")
    else:
        # 如果沒找到，嘗試插入到 main 或 body
        main = soup.find('main') or soup.body
        if main:
            main.append(new_block)
            print(f"✅ 已插入新的 About 區塊至 {target_path}")
        else:
            soup.append(new_block)
            print(f"✅ 已將 About 內容附加至檔案末尾: {target_path}")

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
