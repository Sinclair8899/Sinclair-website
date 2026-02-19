import os

def force_update():
    config_file = 'hugo.toml' if os.path.exists('hugo.toml') else 'config.yaml'
    
    # 1. 強制覆蓋為國際學術選單
    academic_menu = """
[menu]
  [[menu.main]]
    name = "Home"
    url = "/"
    weight = 10
  [[menu.main]]
    name = "Publications"
    url = "/publications"
    weight = 20
  [[menu.main]]
    name = "Data & Resources"
    url = "/data"
    weight = 40
  [[menu.main]]
    name = "Insights"
    url = "/posts"
    weight = 50
  [[menu.main]]
    name = "About"
    url = "/about"
    weight = 60
"""
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 尋找並刪除所有舊的 [menu] 及其下方的設定
        new_lines = []
        skip = False
        for line in lines:
            if line.strip().startswith('[menu]'):
                skip = True
                continue
            if skip and line.strip().startswith('['): # 遇到下一個大標籤就停止刪除
                skip = False
            if not skip:
                new_lines.append(line)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            f.write(academic_menu)
        print(f"✅ 選單已強制更新。")

    # 2. 強制更新 About 為專業英文版
    about_path = 'content/about.md'
    english_about = """---
title: "About Sinclair Huang"
---
Sinclair Huang, PhD (EDBA), is an independent researcher and strategic advisor specializing in the strategic implications of **Artificial Intelligence** on industrial competitiveness and capital markets. He holds an **Executive DBA from HEC Liège**.

With over 30 years of cross-border executive experience, Sinclair serves as a **Special Advisor to the Chairman at Continental Carbon Co., Ltd.** His work bridges high-level academic theory with large-scale industrial practice in semiconductors, biotech, and physical infrastructure.
"""
    with open(about_path, 'w', encoding='utf-8') as f:
        f.write(english_about)
    print(f"✅ About 頁面已強制更新為英文版。")

if __name__ == "__main__":
    force_update()
