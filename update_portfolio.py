import os

# 定義檔案路徑
PROJECTS_DIR = 'docs/projects'
PROJECTS_FILE = os.path.join(PROJECTS_DIR, 'index.html')

# 確保目錄存在
if not os.path.exists(PROJECTS_DIR):
    os.makedirs(PROJECTS_DIR)

# ==========================================
# CSS 樣式 (針對 Portfolio 優化)
# ==========================================
STYLE = """
<style>
    :root {
        --primary: #2c3e50;
        --accent: #2980b9;
        --bg-light: #f8f9fa;
        --text: #333;
        --text-light: #555;
        --border: #e0e0e0;
    }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.7; color: var(--text); margin: 0; padding: 0; background-color: #fdfdfd; }
    
    /* 導航欄 */
    nav { padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; background: #fff; position: sticky; top: 0; z-index: 100; }
    nav .logo { font-weight: 800; font-size: 1.3em; letter-spacing: -0.5px; }
    nav .logo a { text-decoration: none; color: #000; }
    nav .links a { margin-left: 25px; font-size: 0.95em; color: #666; text-decoration: none; font-weight: 500; }
    nav .links a:hover { color: var(--accent); }
    
    /* 頁面標題區 */
    .header-section { text-align: center; padding: 80px 20px 50px; background: linear-gradient(to bottom, #fff, #f8f9fa); border-bottom: 1px solid #eee; }
    h1 { font-size: 3em; margin-bottom: 15px; color: var(--primary); letter-spacing: -1px; }
    .subtitle { font-size: 1.2em; color: #7f8c8d; max-width: 700px; margin: 0 auto; line-height: 1.6; }
    
    /* 內容容器 */
    .container { max-width: 900px; margin: 60px auto; padding: 0 20px; }
    
    /* 區塊標題 */
    .section-header { 
        font-size: 1.8em; 
        font-weight: 700; 
        color: var(--primary); 
        margin-top: 60px; 
        margin-bottom: 30px; 
        padding-bottom: 10px; 
        border-bottom: 2px solid var(--accent); 
        display: inline-block;
    }

    /* 項目卡片 */
    .item-card { 
        background: #fff; 
        border: 1px solid var(--border); 
        border-radius: 8px; 
        padding: 30px; 
        margin-bottom: 30px; 
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .item-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.06); }
    
    .item-title { font-size: 1.4em; font-weight: 700; color: #2c3e50; margin-bottom: 15px; }
    .item-desc { color: var(--text-light); font-size: 1.05em; margin-bottom: 15px; }
    
    .link-box { 
        margin-top: 15px; 
        background: #f1f8ff; 
        padding: 15px; 
        border-radius: 6px; 
        font-size: 0.95em; 
        border-left: 4px solid var(--accent);
    }
    .link-box a { color: var(--accent); text-decoration: none; font-weight: 600; word-break: break-all; }
    .link-box a:hover { text-decoration: underline; }

    /* Collaboration 區塊 */
    .collab-section { background: var(--primary); color: #fff; padding: 50px 40px; border-radius: 8px; margin-top: 80px; text-align: center; }
    .collab-section h2 { color: #fff; border: none; margin-bottom: 20px; font-size: 1.8em; }
    .collab-section p { color: #ccc; font-size: 1.1em; max-width: 700px; margin: 0 auto 30px; }
    .btn-contact { display: inline-block; padding: 10px 25px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.3); color: #fff; text-decoration: none; border-radius: 30px; transition: 0.3s; }
    .btn-contact:hover { background: #fff; color: var(--primary); }

    footer { text-align: center; padding: 60px 20px; color: #999; font-size: 0.9em; margin-top: 60px; }
    
    @media (max-width: 768px) {
        nav { flex-direction: column; padding: 15px; }
        nav .links { margin-top: 15px; display: flex; flex-wrap: wrap; justify-content: center; }
        nav .links a { margin: 5px 10px; }
        .item-card { padding: 20px; }
    }
</style>
"""

# ==========================================
# 頁面內容
# ==========================================
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Portfolio - Sinclair Huang</title>
    {STYLE}
</head>
<body>

    <nav>
        <div class="logo"><a href="../index.html">Sinclair Huang</a></div>
        <div class="links">
            <a href="../index.html">Home</a>
            <a href="../about/index.html">Research Profile</a>
            <a href="../publications/index.html">Publications</a>
            <a href="#" style="color: #000; font-weight: bold;">Projects</a>
            <a href="../blog/index.html">Blog</a>
            <a href="../news/index.html">News</a>
        </div>
    </nav>

    <div class="header-section">
        <h1>Research Portfolio</h1>
        <div class="subtitle">
            Active research and long-term research programs at the intersection of artificial intelligence, 
            semiconductor strategy, and industrial transformation.
        </div>
    </div>

    <div class="container">

        <div class="section-header">Featured Research</div>

        <div class="item-card">
            <div class="item-title">Multi-Target Gene Therapy for Osteoarthritis: Dual-Axis Modeling and In Silico Validation</div>
            <div class="item-desc">
                An interdisciplinary study integrating computational biology, structural modeling, and regenerative medicine to evaluate multi-target therapeutic strategies for osteoarthritis.
            </div>
            <div class="link-box">
                📄 Preprint available on Research Square<br>
                <a href="https://doi.org/10.21203/rs.3.rs-8774255/v2" target="_blank">https://doi.org/10.21203/rs.3.rs-8774255/v2</a>
            </div>
        </div>

        <div class="item-card">
            <div class="item-title">AI Valuation and Semiconductor Industry Transformation (2020–2025)</div>
            <div class="item-desc">
                A large-scale empirical analysis of 95 global semiconductor firms examining the relationship between AI-driven technological shifts and corporate valuation dynamics.
            </div>
        </div>

        <div class="item-card">
            <div class="item-title">Industrial Competitiveness and Innovation of Taiwan-Listed Firms</div>
            <div class="item-desc">
                A comprehensive analysis of global engagement strategies and innovation performance among Taiwanese publicly listed companies.
            </div>
        </div>


        <div class="section-header">Research Programs</div>

        <div class="item-card">
            <div class="item-title">The Physical AI Economics Project</div>
            <div class="item-desc">
                Examining how AI value is shifting from software-centric innovation toward physical infrastructure, manufacturing capability, and energy-constrained intelligence systems.
            </div>
        </div>

        <div class="item-card">
            <div class="item-title">Semiconductor Capability Amplification Research</div>
            <div class="item-desc">
                Exploring how advanced manufacturing capabilities and supply chain architecture determine long-term competitive advantage.
            </div>
        </div>

        <div class="item-card">
            <div class="item-title">AI-Driven Scientific Discovery Initiative</div>
            <div class="item-desc">
                Investigating how AI transforms molecular biology, drug discovery, and scientific innovation processes.
            </div>
        </div>


        <div class="section-header">Data & Analytical Projects</div>

        <div class="item-card">
            <div class="item-title">Global Semiconductor Panel Dataset (2020–2025)</div>
            <div class="item-desc">
                Construction and analysis of a multi-source dataset covering financial performance, technological capabilities, and market positioning of global semiconductor firms.
            </div>
        </div>

        <div class="item-card">
            <div class="item-title">AI–Industry Value Mapping Framework</div>
            <div class="item-desc">
                Development of quantitative and conceptual tools for analyzing how AI reshapes industrial value chains and strategic asset allocation.
            </div>
        </div>


        <div class="collab-section">
            <h2>Collaboration</h2>
            <p>
                I welcome collaboration in research, data analysis, and strategic dialogue related to AI, 
                semiconductor ecosystems, and industrial transformation.
            </p>
            <a href="../about/index.html" class="btn-contact">Get in Touch via Research Profile &rarr;</a>
        </div>

    </div>

    <footer>
        <p>&copy; 2026 Sinclair Huang. All Rights Reserved.</p>
    </footer>

</body>
</html>
"""

# 寫入檔案
with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"🎉 Research Portfolio 頁面已更新：{PROJECTS_FILE}")
