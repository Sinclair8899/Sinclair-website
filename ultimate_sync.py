import os

def update():
    # 1. 強制更新 Publications (加入最新的 Burnout 與 Zenodo 研究)
    pub_content = """---
title: "Publications"
layout: "archives"
---

## 🔬 Recent Research

### **Burnout as Biological Irreversibility: A Multi-Scale Framework**
*SSRN (Feb 18, 2026) | Version v2*
> **Summary:** A mechanistic framework integrating structural biology (AlphaFold 3 GPCR predictions) and dopamine neuroscience to explain progressive treatment resistance.

### **Patent Quality vs. Quantity in the Intangible Economy**
*Zenodo (2026) | DOI: 10.5281/zenodo.18678709*
> **Summary:** Version v2 updated on Feb 18, 2026. Analysis of competitive moats in the semiconductor industry through patent metrics.

---
## 📑 Working Papers
* **Policy-Conditioned Dynamic Capabilities and AI-Driven Valuation** (SSRN No. 5843722)
* **Multi-Target Gene Therapy for Osteoarthritis: A Computational Framework** (Research Square)
"""
    with open('content/publications.md', 'w', encoding='utf-8') as f:
        f.write(pub_content)

    # 2. 強制更新 About 為專業英文
    about_content = """---
title: "About Sinclair Huang"
---
**Sinclair Huang, PhD (EDBA)**, is an independent researcher and strategic advisor at the intersection of **Artificial Intelligence**, **Capital Markets**, and **Physical Infrastructure**. He holds an Executive DBA from **HEC Liège**.

With 30+ years of executive experience, he serves as Special Advisor to the Chairman at **Continental Carbon Co., Ltd.**, bridging academic theory with industrial practices in semiconductors and biotech.
"""
    with open('content/about.md', 'w', encoding='utf-8') as f:
        f.write(about_content)

    # 3. 強制刷新選單配置 (hugo.toml)
    config_file = 'hugo.toml' if os.path.exists('hugo.toml') else 'config.yaml'
    menu_logic = """
[menu]
  [[menu.main]]
    name = "Home"
    url = "/"
    weight = 10
  [[menu.main]]
    name = "Publications"
    url = "/publications"
    weight = 20
  [[menu.main]]
    name = "Data"
    url = "/data"
    weight = 30
  [[menu.main]]
    name = "About"
    url = "/about"
    weight = 40
"""
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        new_lines = [l for l in lines if not l.strip().startswith('[[menu.main]]') and 'name =' not in l and 'url =' not in l and 'weight =' not in l]
        if '[menu]' in "".join(new_lines):
            final_content = "".join(new_lines).split('[menu]')[0] + menu_logic
        else:
            final_content = "".join(new_lines) + menu_logic
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(final_content)

    print("✅ 所有頁面與選單已強制更新！")

if __name__ == "__main__":
    update()
