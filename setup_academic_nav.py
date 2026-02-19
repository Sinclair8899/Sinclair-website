import os

def update_config():
    config_file = 'hugo.toml' if os.path.exists('hugo.toml') else 'config.yaml'
    
    # 定義國際學術標準選單
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
    name = "Research Projects"
    url = "/projects"
    weight = 30
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
            content = f.read()
        
        # 移除舊選單並注入新選單
        if '[menu]' in content:
            content = content.split('[menu]')[0]
        
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(content + academic_menu)
        print(f"✅ {config_file} 已更新為國際學術選單佈局！")

if __name__ == "__main__":
    update_config()
