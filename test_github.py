import requests
from bs4 import BeautifulSoup
from github import Github
from datetime import datetime
import os

# 讀取 GitHub Secret 
ACCESS_TOKEN = os.getenv("MY_GITHUB_TOKEN")
g = Github(ACCESS_TOKEN)
repo = g.get_repo("Sinclair8899/Sinclair-website")

# 依照您的需求設定關鍵字
topics = [
    "AI Semiconductor", 
    "Unmanned Aerial Vehicle", 
    "Autonomous Driving", 
    "Biotechnology", 
    "Regenerative Medicine", 
    "AlphaFold 3"
]

# 建立 Markdown 內容
final_md_content = f"# 每日研究簡報 (Daily Research Brief)\n"
final_md_content += f"更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

for topic in topics:
    print(f"正在搜集：{topic}...")
    # 使用 Google News 搜尋
    search_url = f"https://news.google.com/search?q={topic}&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article h3")[:3] # 每個主題抓前 3 則最熱門的
        
        final_md_content += f"## 🔍 {topic}\n"
        if not articles:
            final_md_content += "- 暫無今日更新\n"
        for a in articles:
            final_md_content += f"- {a.text}\n"
        final_md_content += "\n---\n"
    except Exception as e:
        print(f"{topic} 抓取失敗: {e}")

# 設定存放在 GitHub 的路徑 (這會自動建立 data 資料夾)
file_path = "data/research_news.md"

try:
    try:
        contents = repo.get_contents(file_path)
        repo.update_file(contents.path, "📊 自動更新多領域研究報告", final_md_content, contents.sha)
        print("✅ 雲端資料已更新成功！")
    except:
        repo.create_file(file_path, "📂 建立研究報告資料夾與檔案", final_md_content)
        print("✅ 成功建立雲端資料夾與檔案！")
except Exception as e:
    print(f"❌ 發生錯誤：{e}")
