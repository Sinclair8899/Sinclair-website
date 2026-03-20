import pandas as pd
import yfinance as yf
import time
import os
from google import genai

# ==========================================
# 🔑 設定您的 Gemini API Key
# ==========================================
API_KEY = "AIzaSyD_SrCYxfijyZUL8NiV8GwelAMgEerKgBA" 
client = genai.Client(api_key=API_KEY)

def clean_academic_institutions(df):
    print("🧹 助理正在清洗資料，剔除學術與醫療機構...")
    exclude_words = ['University', 'Hospital', 'Institute', 'School', 'Center', 'Clinic', 'National', 'Hôpitaux', 'Association', 'Foundation', 'Council', 'Universite', 'Research']
    pattern = '|'.join(exclude_words)
    commercial_df = df[~df['Sponsor'].str.contains(pattern, case=False, na=False)].copy()
    unique_sponsors = commercial_df['Sponsor'].unique()
    print(f"✅ 清洗完成！梳理出 {len(unique_sponsors)} 家潛在商業公司。")
    return unique_sponsors

def get_ticker_from_ai(company_name):
    prompt = f"""
    判斷 '{company_name}' (或其母公司) 是否為上市企業。
    如果是，只准輸出股票代號 (如: LLY, 4568.T, GILD)。
    如果未上市，只准輸出 NONE。不准有任何解釋與標點符號。
    """
    # 💡 耐心模組：加入自動重試機制
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            ticker = response.text.replace('`', '').replace('*', '').strip().upper()
            if "NONE" in ticker or len(ticker) > 15:
                return None
            return ticker
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print(f"   ⏳ [API 頻率限制] 助理喝口咖啡，休息 60 秒後繼續 (第 {attempt+1} 次重試)...")
                time.sleep(60) # 被擋了就休息一分鐘
            else:
                return None
    return None

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
            market_cap_m = round(market_cap / 1000000, 2)
            return market_cap_m, currency
        return None, None
    except Exception as e:
        return None, None

def run_financial_agent(csv_filename):
    print("🚀 啟動全自動財務與估值虛擬助理 (耐心狙擊版)...")
    df = pd.read_csv(csv_filename)
    sponsors = clean_academic_institutions(df)
    
    results = []
    print("🔍 助理開始進行跨庫比對 (預計需要 20-30 分鐘，請將視窗縮小即可)...")
    
    for sponsor in sponsors:
        print(f"\n正在分析: {sponsor}...")
        
        ticker = get_ticker_from_ai(sponsor)
        
        if ticker:
            print(f"   ↳ 找到代號: {ticker}，正在抓取財務數據...")
            market_cap, currency = fetch_financials(ticker)
            if market_cap:
                print(f"   ↳ 🎯 成功！市值: {market_cap} 百萬 {currency}")
                results.append({
                    "Sponsor": sponsor,
                    "Ticker": ticker,
                    "Market_Cap_Millions": market_cap,
                    "Currency": currency
                })
                # 💡 即時存檔模組：每抓到一筆就存檔，避免中途斷線白跑
                pd.DataFrame(results).to_csv("investable_biotech_list.csv", index=False, encoding='utf-8-sig')
            else:
                print("   ↳ 無法取得市值資料 (可能已下市或 Yahoo 阻擋)。")
        else:
            print("   ↳ 未上市或查無代號。")
            
        # 💡 節流閥：每問完一家，強制等 5 秒，確保絕對不超速
        time.sleep(5)

    print(f"\n🏆 任務徹底完成！已將高價值清單儲存為 investable_biotech_list.csv")

# 啟動助理！
run_financial_agent("non_us_trials_modality_20260319.csv")