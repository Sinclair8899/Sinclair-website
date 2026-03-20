import pandas as pd
import requests
import time

def fetch_rnd_data(company_name):
    # 💡 帶入您的專屬研究信箱，獲取快速通關權限
    headers = {'User-Agent': 'mailto:research@sinclairhuang.org'}
    url = "https://api.openalex.org/works"
    
    # 💡 戰術調整：移除嚴格的 type 限制，擴大打擊範圍為「所有高影響力 R&D 文獻與專利」
    params = {
        "search": company_name,
        "filter": "publication_year:2015-2024",
        "per-page": 50, # 鎖定最具影響力的前 50 篇核心研發成果
        "sort": "cited_by_count:desc"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # 取得總研發產出數量 (含期刊、臨床報告、專利)
            total_works = data.get('meta', {}).get('count', 0)
            
            # 計算前 50 大核心技術的總前向引用次數
            results = data.get('results', [])
            total_citations = sum(work.get('cited_by_count', 0) for work in results)
            
            return total_works, total_citations
        else:
            # 💡 錯誤顯影劑：如果 API 拒絕，直接印出紅色警報
            print(f"   ⚠️ [API 阻擋] 代碼 {response.status_code}: {response.text[:100]}")
            return 0, 0
    except Exception as e:
        print(f"   ⚠️ [系統連線錯誤]: {e}")
        return 0, 0

def run_patent_agent(csv_filename):
    print("🚀 啟動「全域 R&D 研發護城河探勘助理」...")
    
    try:
        df = pd.read_csv(csv_filename)
    except Exception as e:
        print(f"❌ 讀取失敗。請確認檔名是否為 {csv_filename}！錯誤: {e}")
        return
        
    print(f"📂 成功載入 {len(df)} 家巨頭名單，準備連線全球學術開源庫 OpenAlex...\n")
    
    rnd_counts = []
    citation_counts = []
    
    for index, row in df.iterrows():
        company = row.get('Matched_Company') or row.get('Clinical_Sponsor')
        if pd.isna(company):
            rnd_counts.append(0)
            citation_counts.append(0)
            continue
            
        print(f"🔍 正在掃描 {company} 的全域 R&D 護城河...")
        works, citations = fetch_rnd_data(company)
        
        print(f"   ↳ 🛡️ 找到 {works} 項研發產出，核心前向引用達 {citations} 次！")
        rnd_counts.append(works)
        citation_counts.append(citations)
        
        # 禮貌性延遲 1.5 秒，確保連線穩定
        time.sleep(1.5)
        
    # 將 R&D 數據寫入資料表
    df['Total_RnD_Works_15_24'] = rnd_counts
    df['Forward_Citations'] = citation_counts
    
    output_filename = "biotech_valuation_master.csv"
    df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"\n🏆 探勘完成！「生技估值重定價總表」已儲存為 {output_filename}")

# 啟動助理！
run_patent_agent("investable_biotech_list_Final.csv")
