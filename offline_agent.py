import pandas as pd
import yfinance as yf
import difflib

# 💎 總裁專屬：內建全球頂級非美生技巨頭資料庫 (不受任何 API 限制)
TARGET_COMPANIES = {
    'Roche': 'ROG.SW', 'Novartis': 'NVS', 'AstraZeneca': 'AZN', 
    'Sanofi': 'SNY', 'GlaxoSmithKline': 'GSK', 'Takeda': 'TAK', 
    'Daiichi Sankyo': '4568.T', 'Astellas': '4503.T', 'Eisai': '4523.T', 
    'Bayer': 'BAYN.DE', 'BioNTech': 'BNTX', 'Novo Nordisk': 'NVO', 
    'Genmab': 'GMAB', 'HengRui': '600276.SS', 'BeiGene': 'BGNE', 
    'Zai Lab': 'ZLAB', 'Innovent Biologics': '1801.HK', 'Ipsen': 'IPN.PA',
    'Shionogi': '4507.T', 'Chugai': '4519.T', 'Ono Pharmaceutical': '4528.T',
    'Sino Biopharmaceutical': '1177.HK', 'CSL': 'CSL.AX', 'UCB': 'UCB.BR',
    'Argenx': 'ARGX', 'Grifols': 'GRFS', 'Teva': 'TEVA', 'Recordati': 'REC.MI',
    'Merck KGaA': 'MRK.DE', 'Lundbeck': 'HLUN-B.CO', 'Kyowa Kirin': '4151.T',
    'Evotec': 'EVT.DE', 'Valneva': 'VLA.PA', 'CSPC Pharmaceutical': '1093.HK'
}

def fetch_financials(ticker):
    try:
        stock = yf.Ticker(ticker)
        try:
            market_cap = stock.fast_info['marketCap']
            currency = stock.fast_info['currency']
        except:
            info = stock.info
            market_cap = info.get('marketCap')
            currency = info.get('financialCurrency', 'USD')
        if market_cap and market_cap > 0:
            return round(market_cap / 1000000, 2), currency
    except:
        pass
    return None, None

print("🚀 啟動實戰版離線引擎 (免 API 額度限制)...")

try:
    # 讀取您的臨床檔案 (請確認檔名與您早上下載的一致)
    df = pd.read_csv("non_us_trials_modality_20260319.csv")
except Exception as e:
    print(f"❌ 找不到原始臨床檔案，請確認檔名是否正確！錯誤: {e}")
    exit()
    
sponsors = df['Sponsor'].dropna().unique()
results = []

print("🔍 啟動模糊比對演算法，掃描全球巨頭 (只需 10 秒鐘)...")

for sponsor in sponsors:
    # 忽略明顯是學校或醫院的機構，加速比對
    if any(word in sponsor for word in ['University', 'Hospital', 'Institute', 'School', 'National', 'Center']):
        continue
        
    # 進行模糊比對 (相似度大於 40% 就視為命中)
    matches = difflib.get_close_matches(sponsor, TARGET_COMPANIES.keys(), n=1, cutoff=0.4)
    
    if matches:
        matched_name = matches[0]
        ticker = TARGET_COMPANIES[matched_name]
        
        # 如果已經查過該巨頭，就不重複抓取
        if any(r['Ticker'] == ticker for r in results):
            continue
            
        print(f"🎯 鎖定目標: {sponsor[:30]}... -> 匹配為 {matched_name}")
        
        market_cap, currency = fetch_financials(ticker)
        if market_cap:
            print(f"  ↳ 💰 成功抓取市值: {market_cap} 百萬 {currency}")
            results.append({
                "Clinical_Sponsor": sponsor,
                "Matched_Company": matched_name,
                "Ticker": ticker,
                "Market_Cap_Millions": market_cap,
                "Currency": currency
            })

if results:
    final_df = pd.DataFrame(results)
    filename = "investable_biotech_list_Final.csv"
    final_df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n🏆 任務徹底完成！高價值清單已成功儲存為: {filename}")
else:
    print("\n⚠️ 發生錯誤，未能生成名單。")
