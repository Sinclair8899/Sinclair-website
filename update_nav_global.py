import os
from bs4 import BeautifulSoup

# 設定網站根目錄
DOCS_DIR = 'docs'

# 定義標準選單結構 (顯示名稱 : 連結路徑標記)
# {root} 會被自動替換為相對路徑 (例如 "." 或 "..")
MENU_ITEMS = [
    ("Home", "{root}/index.html"),
    ("Research Profile", "{root}/about/index.html"),
    ("Publications", "{root}/publications/index.html"),
    ("Projects", "{root}/projects/index.html"),
    ("Blog", "{root}/blog/index.html"),
    ("News", "{root}/news/index.html")
]

def get_nav_html(depth):
    """根據檔案深度生成正確的導航 HTML"""
    # 計算相對路徑前綴 (例如 root 是 "." 或 "..")
    root_prefix = ".." if depth > 0 else "."
    if depth > 1: root_prefix = "../.." # 針對更深層的頁面
    
    # 針對 blog 文章 (depth=1, 但有些結構可能更深，這裡假設標準結構)
    # 我們統一使用相對路徑計算
    
    links_html = ""
    for name, path_template in MENU_ITEMS:
        # 替換路徑變數
        href = path_template.format(root=root_prefix)
        # 修正可能出現的 "./../" 冗餘 (雖然瀏覽器看得懂，但乾淨點好)
        if href.startswith("./.."): href = href[2:]
        if href.startswith(".//"): href = href[2:]
        
        links_html += f'<a href="{href}">{name}</a>\n'
    
    return f"""
    <nav>
        <div class="logo"><a href="{root_prefix}/index.html">Sinclair Huang</a></div>
        <div class="links">
            {links_html}
        </div>
    </nav>
    """

def update_file(filepath):
    """更新單一檔案的 Nav"""
    # 計算檔案深度 (相對於 docs 資料夾)
    # docs/index.html -> depth 0
    # docs/about/index.html -> depth 1
    rel_path = os.path.relpath(filepath, DOCS_DIR)
    depth = rel_path.count(os.sep)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
        # 找到舊的 nav
        old_nav = soup.find('nav')
        if not old_nav:
            print(f"⚠️ 跳過 (沒找到 nav): {filepath}")
            return
            
        # 生成新的 nav (解析為 BeautifulSoup 物件)
        new_nav_html = get_nav_html(depth)
        new_nav_soup = BeautifulSoup(new_nav_html, 'html.parser')
        
        # 替換
        old_nav.replace_with(new_nav_soup.nav)
        
        # 寫回檔案
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
            
        print(f"✅ 已更新選單: {filepath}")
        
    except Exception as e:
        print(f"❌ 更新失敗 {filepath}: {e}")

def main():
    print("🚀 開始全站導航更新...")
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                update_file(filepath)
    print("🎉 所有頁面更新完成！")

if __name__ == "__main__":
    main()
