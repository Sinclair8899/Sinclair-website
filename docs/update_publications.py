import os
from bs4 import BeautifulSoup

TARGET_FILE = 'index.html'

new_papers = [
    {
        "title": "AI, Information Depth, and the Collapse of Shallow Signal Predictability: Evidence from a 40-Year Structural Break in Equity Markets",
        "date": "February 08, 2026",
        "link": "https://ssrn.com/abstract=6195878",
        "author": "Huang, Po-Sung (Sinclair)"
    },
    {
        "title": "Architectural Trade-Offs in Vision-Only FSD and Sensor-Fusion Chip Design: Memory Bandwidth, Cache Capacity, and Competitive Dynamics in Autonomous Driving Semiconductors",
        "date": "February 05, 2026",
        "link": "https://ssrn.com/abstract=6184459",
        "author": "Huang, Po-Sung (Sinclair)"
    },
    {
        "title": "Patent Quality Versus Quantity in the Intangible Economy: A Cross-Industry Empirical Analysis of Innovation-Driven Market Valuation",
        "date": "January 31, 2026",
        "link": "https://ssrn.com/abstract=6157046",
        "author": "Huang, Po-Sung (Sinclair)"
    }
]

def update_website():
    if not os.path.exists(TARGET_FILE):
        print(f"❌ 這裡也沒有 '{TARGET_FILE}'。")
        print("看來這個資料夾也不是正確的網站位置。請再試試看別的資料夾。")
        return

    with open(TARGET_FILE, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # 嘗試 1: 找 id="publications-list"
    pub_list = soup.find('ul', {'id': 'publications-list'}) 
    
    # 嘗試 2: 找標題包含 "Publication" 下面的第一個列表
    if not pub_list:
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        for header in headers:
            if 'Publication' in header.get_text() or 'Research' in header.get_text():
                pub_list = header.find_next('ul')
                if pub_list: break
    
    # 嘗試 3 (暴力法): 真的找不到，就直接插在 body 的最前面，讓您手動搬
    inserted_location = "列表"
    if not pub_list:
        print("⚠️  找不到標準列表，將暫時插入到頁面最上方 (Body Start)...")
        pub_list = soup.body
        inserted_location = "頁面最上方"
        if not pub_list:
             print("❌ 錯誤：這個 HTML 檔案結構太奇怪了，找不到 body。")
             return

    print(f"✅ 準備將 {len(new_papers)} 篇論文插入到 {inserted_location}...")

    # 準備一個容器來裝新論文
    container = soup.new_tag("ul") if inserted_location == "頁面最上方" else None

    for paper in reversed(new_papers):
        new_li = soup.new_tag("li")
        link_tag = soup.new_tag("a", href=paper["link"], target="_blank")
        link_tag.string = paper["title"]
        date_span = soup.new_tag("span", style="color: #666; margin-left: 10px;")
        date_span.string = f"({paper['date']})"
        
        new_li.append(link_tag)
        new_li.append(date_span)
        
        if container:
            container.append(new_li)
        else:
            pub_list.insert(0, new_li)

    if container:
        pub_list.insert(0, container)

    with open(TARGET_FILE, 'w', encoding='utf-8') as file:
        file.write(str(soup.prettify()))

    print(f"🎉 更新成功！請打開 {TARGET_FILE} 確認結果。")

if __name__ == "__main__":
    update_website()
