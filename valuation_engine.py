import pandas as pd
import numpy as np

def run_valuation_engine(csv_filename):
    print("🚀 啟動「全球生技估值與重定價引擎 (Valuation Engine)」...")
    
    try:
        df = pd.read_csv(csv_filename)
        print(f"📂 成功載入 {len(df)} 家巨頭的財務與 R&D 數據！")
    except Exception as e:
        print(f"❌ 讀取失敗，請確認檔名！錯誤: {e}")
        return

    # 💡 建立穩定版匯率轉換表 (將各國貨幣轉換為 1 單位 USD)
    # 這裡使用 2026 年近期的基準匯率，確保計算不受 API 網路波動影響
    exchange_rates_to_usd = {
        'USD': 1.0,
        'CHF': 1.13,      # 1 瑞士法郎 約 1.13 美金
        'EUR': 1.09,      # 1 歐元 約 1.09 美金
        'JPY': 0.0067,    # 1 日圓 約 0.0067 美金 (150 JPY/USD)
        'CNY': 0.14,      # 1 人民幣 約 0.14 美金
        'HKD': 0.13,      # 1 港幣 約 0.13 美金
        'GBP': 1.28,      # 1 英鎊 約 1.28 美金
        'DKK': 0.15,      # 1 丹麥克朗 約 0.15 美金
        'AUD': 0.66       # 1 澳幣 約 0.66 美金
    }

    print("\n💱 正在進行全球跨幣別市值換算 (統一為百萬美金 USD)...")
    
    # 計算轉換後的市值 (Market Cap in USD Millions)
    df['Market_Cap_USD_Millions'] = df.apply(
        lambda row: round(row['Market_Cap_Millions'] * exchange_rates_to_usd.get(row['Currency'], 1.0), 2) 
        if pd.notna(row['Market_Cap_Millions']) else np.nan, 
        axis=1
    )

    print("🧠 正在計算核心財務指標：創新溢價乘數 (Innovation Premium Multiplier)...")
    
    # 計算創新溢價乘數：市值(百萬美金) / 前向引用數
    # 如果引用數為 0，則給予空值避免除以零的錯誤
    df['Innovation_Premium_Multiplier'] = df.apply(
        lambda row: round(row['Market_Cap_USD_Millions'] / row['Forward_Citations'], 4)
        if pd.notna(row['Forward_Citations']) and row['Forward_Citations'] > 0 else np.nan,
        axis=1
    )

    # 依照「創新溢價乘數」由低到高排序 (越低代表 CP 值越高、越被低估)
    df_sorted = df.sort_values(by='Innovation_Premium_Multiplier', ascending=True)

    # 儲存最終的估值大表
    output_filename = "final_valuation_repricing_board.csv"
    
    # 整理欄位顯示順序，讓您閱讀更直覺
    columns_order = [
        'Matched_Company', 'Ticker', 'Market_Cap_USD_Millions', 
        'Total_RnD_Works_15_24', 'Forward_Citations', 'Innovation_Premium_Multiplier',
        'Market_Cap_Millions', 'Currency', 'Clinical_Sponsor'
    ]
    df_sorted = df_sorted[[col for col in columns_order if col in df_sorted.columns]]
    
    df_sorted.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"\n🏆 估值重定價完成！")
    print(f"📄 您的終極投資分析總表已儲存為：{output_filename}")
    
    # 在終端機印出前 5 名最被低估的公司讓總裁先睹為快
    print("\n🌟 【總裁專屬洞察】創新溢價乘數最低 (最被低估) 的 Top 5 巨頭：")
    top_5 = df_sorted.head(5)
    for index, row in top_5.iterrows():
        print(f"   ➤ {row['Matched_Company']} | 乘數: {row['Innovation_Premium_Multiplier']} | 市值: {row['Market_Cap_USD_Millions']}M USD | 引用數: {row['Forward_Citations']}")

# 啟動引擎！讀取上一階段產生的 master 檔案
run_valuation_engine("biotech_valuation_master.csv")