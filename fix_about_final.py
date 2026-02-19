import os
from bs4 import BeautifulSoup

# 直接鎖定你提供的正確路徑
target_path = 'docs/index.html'

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

if not os.path.exists(target_path):
    print(f"❌ 錯誤：在路徑 '{target_path}' 找不到檔案。")
else:
    with open(target_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # 尋找既存的 about 區塊
    existing = soup.find('section', id='about')
    new_block = BeautifulSoup(about_content, 'html.parser')
    
    if existing:
        existing.replace_with(new_block)
        print(f"✅ 已成功更新 '{target_path}' 中的 About 區塊。")
    else:
        # 如果沒找到區塊，嘗試插入在 footer 之前，或 body 尾端
        footer = soup.find('footer')
        if footer:
            footer.insert_before(new_block)
            print(f"✅ 已將 About 區塊插入至 '{target_path}' 的 footer 之前。")
        elif soup.body:
            soup.body.append(new_block)
            print(f"✅ 已將 About 區塊添加至 '{target_path}' 的 body 尾端。")
        else:
            soup.append(new_block)
            print(f"✅ 已將 About 內容附加至檔案末尾。")

    # 寫回檔案並保持格式整齊
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
