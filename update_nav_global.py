import os
from bs4 import BeautifulSoup

DOCS_DIR = 'docs'

# 更新後的選單列表 (加入 Contact)
MENU_ITEMS = [
    ("Home", "{root}/index.html"),
    ("Research Profile", "{root}/about/index.html"),
    ("Publications", "{root}/publications/index.html"),
    ("Research Portfolio", "{root}/projects/index.html"),
    ("Blog", "{root}/blog/index.html"),
    ("News", "{root}/news/index.html"),
    ("Contact", "{root}/contact/index.html")  # 新增這一行
]

def get_nav_html(depth):
    root_prefix = ".." if depth > 0 else "."
    if depth > 1: root_prefix = "../.."
    
    links_html = ""
    for name, path_template in MENU_ITEMS:
        href = path_template.format(root=root_prefix)
        # 簡單清理路徑
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
    rel_path = os.path.relpath(filepath, DOCS_DIR)
    depth = rel_path.count(os.sep)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
        old_nav = soup.find('nav')
        if not old_nav: return
            
        new_nav_html = get_nav_html(depth)
        new_nav_soup = BeautifulSoup(new_nav_html, 'html.parser')
        old_nav.replace_with(new_nav_soup.nav)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
            
        print(f"✅ 選單更新: {filepath}")
    except Exception as e:
        print(f"❌ 失敗: {filepath}")

def main():
    print("🚀 開始更新全站導航 (含 Contact)...")
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".html"):
                update_file(os.path.join(root, file))
    print("🎉 全站更新完成！")

if __name__ == "__main__":
    main()
