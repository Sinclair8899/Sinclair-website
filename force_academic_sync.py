import os

def force_sync():
    # 1. 更新 Publications (加入最新 2026.02.18 研究)
    pub_content = """---
title: "Publications"
layout: "archives"
---

## 🔬 Featured Research (2026)

### **Burnout as Biological Irreversibility: A Multi-Scale Framework**
*SSRN (Feb 18, 2026) | Version v2*
> **Key Finding:** This research integrates AlphaFold 3 GPCR predictions and dopamine neuroscience to model burnout as a state of biological irreversibility.

### **Patent Quality vs. Quantity in the Intangible Economy**
*Zenodo (2026) | DOI: 10.5281/zenodo.18678709*
> **Update:** Revised on Feb 18, 2026. Quantitative analysis of the semiconductor industry's competitive landscape.

---
## 📑 Other Academic Works
* **AI Semiconductor Valuation Dataset** (95 Global Firms)
* **Policy-Conditioned Dynamic Capabilities** (SSRN No. 5843722)
* **Multi-Target Gene Therapy for Osteoarthritis** (Research Square)
"""
    with open('content/publications.md', 'w', encoding='utf-8') as f:
        f.write(pub_content)

    # 2. 強制更新 About (解決中文殘留問題)
    # 如果您的主題在 content/_index.md 也有內容，我們會一併清理
    about_eng = """---
title: "About Sinclair Huang"
---
**Sinclair Huang, PhD (EDBA)**, is a researcher working at the intersection of **Artificial Intelligence**, **Physical Infrastructure**, and **Capital Markets**. He holds an Executive Doctorate in Business Administration (EDBA) from **HEC Liège** (2025). 

With over 30 years of executive experience, he serves as Special Advisor to the Chairman at **Continental Carbon Co., Ltd.** His work bridges high-level academic theory with practical industrial strategies in semiconductors and biotechnology.
"""
    with open('content/about.md', 'w', encoding='utf-8') as f:
        f.write(about_eng)
    
    # 額外檢查：如果首頁檔案存在中文，將其內容簡化
    if os.path.exists('content/_index.md'):
        with open('content/_index.md', 'r+', encoding='utf-8') as f:
            f.seek(0)
            f.truncate()
            f.write('---\ntitle: "Sinclair Huang | Research & Consulting"\n---\nWelcome to my research platform.')

    print("✅ 檔案內容已強制同步為英文學術版本！")

if __name__ == "__main__":
    force_sync()
