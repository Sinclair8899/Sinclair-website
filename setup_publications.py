import os

# 目標目錄與檔案
PUB_DIR = 'docs/publications'
PUB_FILE = os.path.join(PUB_DIR, 'index.html')

# 確保目錄存在
if not os.path.exists(PUB_DIR):
    os.makedirs(PUB_DIR)

# 您的論文資料 (包含最新的三篇 SSRN)
papers = [
    {
        "category": "Latest Research (2026)",
        "items": [
            {
                "title": "AI, Information Depth, and the Collapse of Shallow Signal Predictability: Evidence from a 40-Year Structural Break in Equity Markets",
                "date": "February 08, 2026",
                "link": "https://ssrn.com/abstract=6195878",
                "desc": "SSRN Working Paper"
            },
            {
                "title": "Architectural Trade-Offs in Vision-Only FSD and Sensor-Fusion Chip Design",
                "date": "February 05, 2026",
                "link": "https://ssrn.com/abstract=6184459",
                "desc": "SSRN Working Paper - Analysis of Memory Bandwidth and Cache Capacity"
            },
            {
                "title": "Patent Quality Versus Quantity in the Intangible Economy",
                "date": "January 31, 2026",
                "link": "https://ssrn.com/abstract=6157046",
                "desc": "SSRN Working Paper - A Cross-Industry Empirical Analysis"
            }
        ]
    },
    {
        "category": "Biotech & AI",
        "items": [
            {
                "title": "Multi-Target Gene Therapy for Osteoarthritis: A Computational Framework",
                "date": "2026",
                "link": "https://doi.org/10.21203/rs.3.rs-8774255/v1",
                "desc": "Research Square - DOI: 10.21203/rs.3.rs-8774255/v1"
            },
            {
                "title": "AlphaFold 3 and the Future of Molecular Discovery",
                "date": "Dec 2025",
                "link": "../blog/index.html", # 連結到您的 blog 文章
                "desc": "Research Note"
            }
        ]
    },
    {
        "category": "Industrial Strategy & Economics",
        "items": [
            {
                "title": "Patent Quality vs Quantity in Intangible Economy",
                "date": "2026",
                "link": "https://doi.org/10.5281/zenodo.18437953",
                "desc": "Zenodo - DOI: 10.5281/zenodo.18437953"
            },
            {
                "title": "Policy-Conditioned Dynamic Capabilities and AI-Driven Valuation",
                "date": "2025",
                "link": "#",
                "desc": "SSRN Working Paper No. 5843722"
            }
        ]
    }
]

# HTML 樣式
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Publications - Sinclair Huang</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #fcfcfc; }
        
        /* 導航欄 (保持一致) */
        nav { padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; background: #fff; }
        nav .logo { font-weight: 700; font-size: 1.2em; }
        nav .links a { margin-left: 20px; font-size: 0.95em; color: #666; text-decoration: none; }
        nav .links a:hover { color: #000; }

        .container { max-width: 800px; margin: 60px auto; padding: 0 20px; }
        h1 { font-size: 2.5em; margin-bottom: 40px; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; display: inline-block; }
        
        .section-title { font-size: 1.5em; color: #2c3e50; margin-top: 50px; margin-bottom: 20px; font-weight: 600; }
        
        .paper-item { background: #fff; padding: 25px; margin-bottom: 20px; border: 1px solid #e0e0e0; border-radius: 8px; transition: 0.2s; }
        .paper-item:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.05); border-color: #bdc3c7; }
        
        .paper-title { font-size: 1.2em; font-weight: 600; color: #2980b9; text-decoration: none; display: block; margin-bottom: 8px; }
        .paper-title:hover { text-decoration: underline; }
        
        .paper-meta { font-size: 0.9em; color: #7f8c8d; }
        .paper-desc { margin-top: 8px; font-size: 0.95em; color: #555; }
        
        footer { text-align: center; padding: 50px; color: #aaa; font-size: 0.9em; }
    </style>
</head>
<body>

    <nav>
        <div class="logo"><a href="../index.html">Sinclair Huang</a></div>
        <div class="links">
            <a href="../index.html">Home</a>
            <a href="../blog/index.html">Blog</a>
            <a href="../news/index.html">News</a>
            <a href="#" style="color: #000; font-weight: bold;">Publications</a>
        </div>
    </nav>

    <div class="container">
        <h1>Selected Publications</h1>
"""

# 動態生成列表
for category in papers:
    html_content += f'<div class="section-title">{category["category"]}</div>'
    for paper in category["items"]:
        html_content += f"""
        <div class="paper-item">
            <a href="{paper['link']}" class="paper-title" target="_blank">{paper['title']}</a>
            <div class="paper-meta">{paper['date']}</div>
            <div class="paper-desc">{paper['desc']}</div>
        </div>
        """

html_content += """
    </div>
    <footer>© 2026 Sinclair Huang</footer>
</body>
</html>
"""

with open(PUB_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"🎉 Publications 頁面已建立：{PUB_FILE}")
