from github import Github
import os
from datetime import datetime

# ... 其他 import ...

# 修改這裡：讓它從 GitHub 的環境變數讀取 Token
ACCESS_TOKEN = os.getenv("MY_GITHUB_TOKEN") 
g = Github(ACCESS_TOKEN)
repo = g.get_repo("Sinclair8899/Sinclair-website")

# 1. 模擬抓到的新資料
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
new_content = f"最後抓取時間：{current_time}\n這是自動上傳的測試資料。"

# 2. 執行上傳 (如果檔案不存在會建立，存在則更新)
file_path = "latest_crawl.txt" # 存放在 GitHub 的檔名

try:
    try:
        # 如果檔案已存在，需要先取得它的 'sha' 才能更新
        contents = repo.get_contents(file_path)
        repo.update_file(contents.path, "自動更新資料", new_content, contents.sha)
        print(f"✅ 成功更新檔案：{file_path}")
    except:
        # 如果檔案不存在，直接建立
        repo.create_file(file_path, "建立初始資料檔", new_content)
        print(f"✅ 成功建立新檔案：{file_path}")

except Exception as e:
    print(f"❌ 發生錯誤：{e}")
