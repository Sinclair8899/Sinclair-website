import os
import re

def run(cmd):
    print(f"🏃 執行: {cmd}")
    os.system(cmd)

def upgrade():
    # 1. 優化所有 Markdown 檔案
    content_dir = './content'
    if os.path.exists(content_dir):
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.md'):
                    p = os.path.join(root, file)
                    with open(p, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    # 刪除測試文章
                    if "Your Title" in text or "Your content here" in text:
                        os.remove(p)
                        print(f"🗑️ 已刪除測試檔: {file}")
                        continue

                    # 補全 SEO Description (優化 Google 搜尋結果)
                    if 'description:' not in text and '---' in text:
                        parts = text.split('---', 2)
                        if len(parts) >= 3:
                            snippet = re.sub(r'[#*`>]', '', parts[2]).strip()[:100].replace('\n', ' ')
                            new_text = f"{parts[0]}---\ndescription: \"{snippet}...\"{parts[1]}---\n{parts[2]}"
                            with open(p, 'w', encoding='utf-8') as f:
                                f.write(new_text)
                            print(f"📝 已優化 SEO 摘要: {file}")

    # 2. 自動提交 Git 並推送至 GitHub
    run("git add .")
    run('git commit -m "🚀 One-click optimization: SEO and content cleanup"')
    run("git push origin main")
    print("\n✨ 全部完成！您的網站 sinclairhuang.org 已優化並同步。")

if __name__ == "__main__":
    upgrade()
