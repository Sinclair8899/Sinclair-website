import os

def create_about():
    about_content = """---
title: "About Sinclair Huang"
description: "Academic Researcher & Strategic Advisor at the intersection of AI, Capital Markets, and Industrial Infrastructure."
---

## 🎓 Academic & Professional Profile

**Sinclair Huang** is an independent researcher and executive advisor specializing in the strategic implications of **Artificial Intelligence** on industrial competitiveness and capital markets. He holds an **Executive DBA from HEC Liège**, where his research focused on the transformation of traditional physical infrastructure through AI-driven innovation.

With over 30 years of cross-border executive experience, Sinclair serves as a **Special Advisor to the Chairman at Continental Carbon Co., Ltd.** His unique position allows him to bridge the gap between high-level academic theory and large-scale industrial practice.

---

## 🔬 Research Focus

My current work explores how AI technologies (such as AlphaFold 3 in biotech and predictive modeling in semiconductors) reshape competitive moats:

* **AI-Driven Industrial Strategy**: Analyzing the shift from labor-intensive to intelligence-driven manufacturing.
* **Capital Market Valuation**: Developing quantitative frameworks (Random Forest, GEE Regression) to evaluate AI chip firms and intangible assets.
* **Biotechnology & Regenerative Medicine**: Computational modeling for multi-target gene therapies (e.g., Osteoarthritis research).

---

## 💼 Expertise & Advisory

Beyond academia, I provide strategic counsel to global firms in the electronics, chemical, and biotechnology sectors. I am particularly passionate about:

1.  **Industrial Infrastructure**: Modernizing "Old Economy" sectors with "New Economy" tools.
2.  **Intellectual Property**: Evaluating patent quality as a key indicator of long-term firm value.
3.  **Cross-Disciplinary Innovation**: Integrating AI systems into specialty materials and life sciences research.

---

## 📬 Academic Presence

* **Preprints**: [SSRN](https://ssrn.com/abstract=5843722), [Research Square](https://doi.org/10.21203/rs.3.rs-8774255/v1)
* **Open Data**: [Zenodo](https://doi.org/10.5281/zenodo.18437953)
* **Contact**: [sinclair@sinclairhuang.org](mailto:sinclair@sinclairhuang.org)
"""

    path = 'content/about.md'
    # 確保 content 目錄存在
    if not os.path.exists('content'):
        os.makedirs('content')
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(about_content)
    print(f"✅ 專業簡介已成功建立於: {path}")

if __name__ == "__main__":
    create_about()
