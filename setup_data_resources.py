import os

def create_data_page():
    data_content = """---
title: "Data & Resources"
description: "Quantitative datasets and analytical frameworks for AI-driven industrial and market analysis."
---

## 📊 AI Semiconductor Valuation Dataset

This dataset encompasses a longitudinal study of **95 global semiconductor firms**, focusing on the transition from traditional logic/memory chips to AI-centric architectures.

* **Methodology**: Utilizing **Generalized Estimating Equations (GEE) regression** and **Random Forest models** to analyze the impact of R&D intensity on firm valuation.
* **Key Indicators**: Patent quality metrics, AI-related patent density, and capital expenditure (CapEx) trends.
* **Access**: The processed dataset is available for academic collaboration upon request.

---

## 🧪 Computational Biology Frameworks

Derived from my research at the intersection of AI and life sciences:

* **Multi-Target Gene Therapy Framework**: A computational approach to identify synergistic effects in regenerative medicine for Osteoarthritis.
* **Molecular Docking Protocols**: High-throughput screening parameters optimized for AlphaFold 3 predictions.

---

## 🛠️ Open Research Tools

* **Patent Quality vs. Quantity Scraper**: A tool for extracting intangible asset value from public patent filings.
* **Infrastructure Transformation Index**: A strategic benchmark for evaluating "Old Economy" firms adopting AI.

---

## 📧 Collaboration
Interested in utilizing these datasets for joint research? Please reach out via **sinclair@sinclairhuang.org**.
"""

    path = 'content/data.md'
    if not os.path.exists('content'):
        os.makedirs('content')
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data_content)
    print(f"✅ 數據資源頁面已成功建立於: {path}")

if __name__ == "__main__":
    create_data_page()
