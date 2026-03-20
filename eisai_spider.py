import requests
import pandas as pd
import time
from collections import Counter

def get_eisai_citation_network():
    headers = {'User-Agent': 'mailto:research@sinclairhuang.org'}
    print("🚀 啟動「專利引用者溯源引擎 (Citation Network Spider)」...")
    print("🔍 步驟 1：鎖定 Eisai (衛采) 影響力最高的 Top 5 核心研發資產...")

    # 1. 取得 Eisai 影響力最高的 5 篇核心文獻
    url_works = "https://api.openalex.org/works"
    params_works = {
        "search": "Eisai",
        "filter": "publication_year:2015-2024",
        "per-page": 5,
        "sort": "cited_by_count:desc"
    }

    try:
        res = requests.get(url_works, params=params_works, headers=headers)
        top_works = res.json().get('results', [])
    except Exception as e:
        print(f"❌ 連線錯誤: {e}")
        return

    print(f"🎯 成功鎖定！準備對這 {len(top_works)} 項核心資產進行「逆向引用追蹤」...")

    citing_institutions = []

    # 2. 針對每一篇核心文獻，抓取是「誰」引用了它
    for i, work in enumerate(top_works):
        work_id = work['id'].split('/')[-1]
        work_title = work.get('title', '未命名文獻')
        if not work_title:
            work_title = "未命名文獻"
        citation_count = work.get('cited_by_count', 0)
        
        print(f"\n   ➤ 鑽探核心資產 {i+1}: {work_title[:50]}... (總被引用 {citation_count} 次)")

        # 抓取最具代表性的 50 篇前向引用文獻來分析其機構
        params_cites = {
            "filter": f"cites:{work_id}",
            "per-page": 50, 
            "sort": "cited_by_count:desc"
        }

        try:
            res_cites = requests.get(url_works, params=params_cites, headers=headers)
            citing_works = res_cites.json().get('results', [])

            for c_work in citing_works:
                # 剝離出引用者的所屬機構
                authorships = c_work.get('authorships', [])
                for author in authorships:
                    institutions = author.get('institutions', [])
                    for inst in institutions:
                        inst_name = inst.get('display_name')
                        if inst_name:
                            citing_institutions.append(inst_name)
        except Exception as e:
            print(f"      ⚠️ 抓取引用文獻時發生錯誤: {e}")

        # 禮貌延遲，保護您的專屬 API 通道
        time.sleep(1.5) 

    print("\n🧠 步驟 2：清洗數據，剔除自我引用，提煉純淨的「技術依賴名單」...")

    # 3. 統計與清洗 (排除 Eisai 自己的機構)
    inst_counts = Counter(citing_institutions)
    filtered_counts = {k: v for k, v in inst_counts.items() if 'Eisai' not in k}

    # 轉換成 DataFrame 並抓取前 30 大依賴機構
    df_top_citers = pd.DataFrame(filtered_counts.items(), columns=['Institution', 'Citation_Count_Sample'])
    df_top_citers = df_top_citers.sort_values(by='Citation_Count_Sample', ascending=False).head(30)

    # 儲存結果
    filename = "Eisai_Citation_Network.csv"
    df_top_citers.to_csv(filename, index=False, encoding='utf-8-sig')

    print(f"\n🏆 溯源徹底完成！")
    print(f"📄 「Eisai 核心技術依賴者清單」已儲存為：{filename}")
    
    # 預覽 Top 10 名單
    print("\n🌟 【總裁專屬洞察】高度依賴 Eisai 核心技術的 Top 10 機構：")
    print(df_top_citers.head(10).to_string(index=False))

# 點火！
get_eisai_citation_network()