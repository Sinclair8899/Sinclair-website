import requests
import pandas as pd
from datetime import datetime

def fetch_non_us_trials(keywords, max_studies=500):
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    all_studies = []
    page_token = None
    total_fetched = 0
    
    while total_fetched < max_studies:
        params = {
            "query.cond": keywords,
            "filter.advanced": "AREA[LocationCountry] NOT USA",
            # 💡 升級：多抓了 ArmsInterventionsModule，用來分析藥物類型！
            "fields": "NCTId,BriefTitle,Condition,Phase,LeadSponsorName,OverallStatus,StartDate,CompletionDate,LocationCountry,ArmsInterventionsModule",
            "pageSize": 1000,
            "format": "json"
        }
        if page_token:
            params["pageToken"] = page_token
            
        try:
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "studies" not in data:
                print("No more studies found.")
                break
                
            for study in data["studies"]:
                protocol = study.get("protocolSection", {})
                sponsor = protocol.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name", "Unknown")
                
                # 再次確認非美國
                locations = study.get("locations", [])
                if any("United States" in loc.get("country", "") for loc in locations):
                    continue
                
                # 💡 升級：萃取治療方式 (Interventions) 並自動判定是否為前沿技術 (Modality)
                interventions = []
                is_emerging_modality = False
                arms_module = protocol.get("armsInterventionsModule", {})
                for intervention in arms_module.get("interventions", []):
                    int_name = intervention.get("name", "")
                    interventions.append(int_name)
                    # 關鍵字掃描：mRNA, CAR-T, Gene Therapy 等
                    if any(keyword in int_name.upper() for keyword in ["MRNA", "CAR-T", "GENE THERAPY", "CELL THERAPY", "CRISPR", "RNAI"]):
                        is_emerging_modality = True

                all_studies.append({
                    "NCTId": protocol.get("identificationModule", {}).get("nctId", ""),
                    "Sponsor": sponsor,
                    "Phase": ", ".join(protocol.get("designModule", {}).get("phases", [])),
                    "Status": protocol.get("statusModule", {}).get("overallStatus", ""),
                    "Countries": ", ".join(set(loc.get("country", "Unknown") for loc in locations)),
                    "Interventions": " | ".join(interventions),
                    "Emerging_Modality": "Yes" if is_emerging_modality else "No" # 直接為您的模型準備好標籤！
                })
                
                total_fetched += 1
                if total_fetched >= max_studies:
                    break
                    
            page_token = data.get("nextPageToken")
            if not page_token:
                break
            print(f"目前已抓取 {total_fetched} 筆...")
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            break

    if all_studies:
        df = pd.DataFrame(all_studies)
        today = datetime.now().strftime("%Y%m%d")
        filename = f"non_us_trials_modality_{today}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ 成功！已儲存 {len(df)} 筆非美臨床資料至 {filename}")
        return df
    return pd.DataFrame()

# 🚀 執行：自動標記全球非美的癌症前沿療法
df = fetch_non_us_trials("cancer OR oncology OR immunotherapy", max_studies=500)
