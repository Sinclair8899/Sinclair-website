import os

# 定義檔案路徑
HOME_FILE = 'docs/index.html'
ABOUT_DIR = 'docs/about'
ABOUT_FILE = os.path.join(ABOUT_DIR, 'index.html')

# 確保目錄存在
if not os.path.exists(ABOUT_DIR):
    os.makedirs(ABOUT_DIR)

# ==========================================
# 1. 設定共用 CSS (讓網站風格一致)
# ==========================================
COMMON_STYLE = """
<style>
    :root {
        --primary: #2c3e50;
        --accent: #2980b9;
        --bg-light: #f8f9fa;
        --text: #333;
        --text-light: #666;
    }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.7; color: var(--text); margin: 0; padding: 0; }
    
    /* 導航欄 */
    nav { padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; background: #fff; position: sticky; top: 0; z-index: 100; }
    nav .logo { font-weight: 800; font-size: 1.3em; letter-spacing: -0.5px; }
    nav .logo a { text-decoration: none; color: #000; }
    nav .links a { margin-left: 25px; font-size: 0.95em; color: var(--text-light); text-decoration: none; font-weight: 500; }
    nav .links a:hover { color: var(--accent); }
    
    /* 通用區塊 */
    section { padding: 80px 20px; max-width: 800px; margin: 0 auto; }
    h1 { font-size: 3em; line-height: 1.2; margin-bottom: 20px; letter-spacing: -1px; }
    h2 { font-size: 2em; margin-bottom: 30px; color: var(--primary); }
    h3 { font-size: 1.4em; margin-top: 40px; margin-bottom: 10px; color: var(--accent); }
    p { font-size: 1.15em; color: #555; margin-bottom: 1.5em; }
    
    /* 首頁特定樣式 */
    .hero { text-align: center; padding: 120px 20px; background: linear-gradient(to bottom, #fff, #f8f9fa); }
    .theme { background: #fff; border-left: 5px solid var(--primary); padding: 60px 40px; margin-top: 40px; margin-bottom: 40px; background: #fcfcfc; }
    .domains { border-top: 1px solid #eee; }
    
    /* Research Profile 特定樣式 */
    .profile-header { background: var(--primary); color: #fff; padding: 80px 20px; text-align: center; }
    .profile-header h1 { color: #fff; margin: 0; }
    .profile-section { margin-bottom: 50px; }
    .profile-list dt { font-weight: bold; font-size: 1.1em; margin-top: 20px; color: var(--primary); }
    .profile-list dd { margin-left: 0; margin-bottom: 10px; color: #555; }

    footer { text-align: center; padding: 60px 20px; color: #999; font-size: 0.9em; border-top: 1px solid #eee; margin-top: 60px; }
    
    @media (max-width: 768px) {
        h1 { font-size: 2.2em; }
        nav { flex-direction: column; padding: 15px; }
        nav .links { margin-top: 15px; }
        nav .links a { margin: 0 10px; }
    }
</style>
"""

# 導航欄 HTML (共用)
NAV_HTML = """
<nav>
    <div class="logo"><a href="/docs/index.html">Sinclair Huang</a></div>
    <div class="links">
        <a href="../index.html">Home</a>
        <a href="../about/index.html">Research Profile</a>
        <a href="../publications/index.html">Publications</a>
        <a href="../blog/index.html">Blog</a>
        <a href="../news/index.html">News</a>
    </div>
</nav>
""".replace('/docs/index.html', '../index.html') # 修正相對路徑

# ==========================================
# 2. 生成首頁 (HOME)
# ==========================================
home_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sinclair Huang - AI & Industrial Strategy</title>
    {COMMON_STYLE}
</head>
<body>

    {NAV_HTML}

    <section class="hero">
        <h1>Sinclair Huang, PhD (EDBA)</h1>
        <p style="font-size: 1.3em; color: #2c3e50;"><strong>AI • Semiconductors • Industrial Strategy</strong></p>
        <p style="max-width: 700px; margin: 0 auto; color: #666;">
            Researching the global transition from intangible artificial intelligence to physical intelligence — 
            where value shifts toward energy systems, advanced manufacturing, and industrial deployment.
        </p>
    </section>

    <section class="theme">
        <h2>From Intangible AI to Physical Intelligence</h2>
        <p>The next decade of artificial intelligence will not be defined by larger models alone, but by the physical systems that sustain real-time intelligence — energy infrastructure, advanced semiconductors, manufacturing capacity, and industrial deployment.</p>
        <p style="font-weight: 500; color: #333;">My research examines this transformation: the shift from software-centric digital value toward physical AI capability.</p>
    </section>

    <section class="domains">
        <h2 style="text-align: center; margin-bottom: 60px;">Research Domains</h2>
        
        <h3>AI Industrial Economics</h3>
        <p>Understanding how compute constraints, energy systems, and industrial deployment shape the long-term economics of artificial intelligence.</p>

        <h3>Semiconductor Strategy</h3>
        <p>Analyzing capability amplification, equipment-first dynamics, and global supply chain restructuring.</p>

        <h3>AI in Biotech & Science</h3>
        <p>Investigating how AI transforms molecular discovery and biological innovation.</p>
        
        <div style="text-align: center; margin-top: 50px;">
            <a href="about/index.html" style="display: inline-block; padding: 12px 25px; border: 1px solid #333; border-radius: 30px; text-decoration: none; color: #333; font-weight: bold; transition: 0.2s;">View Full Research Profile &rarr;</a>
        </div>
    </section>

    <footer>
        <p>&copy; 2026 Sinclair Huang. All Rights Reserved.</p>
    </footer>

</body>
</html>
"""

# ==========================================
# 3. 生成 RESEARCH PROFILE 頁 (ABOUT)
# ==========================================
about_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Profile - Sinclair Huang</title>
    {COMMON_STYLE}
</head>
<body>

    {NAV_HTML}

    <div class="profile-header">
        <h1>Research Profile</h1>
        <p style="color: #ccc; max-width: 600px; margin: 20px auto 0;">Independent Researcher & Industrial Strategist</p>
    </div>

    <section>
        <div class="profile-section">
            <h2>Research Statement</h2>
            <p style="font-size: 1.25em; line-height: 1.8; color: #333;">
                I study the industrial transformation driven by artificial intelligence, focusing on how value is shifting from software-centric digital models toward physical infrastructure, manufacturing capabilities, and real-world deployment systems.
            </p>
            <p>My work integrates academic research with decades of industrial leadership experience.</p>
        </div>

        <hr style="border: 0; border-top: 1px solid #eee; margin: 50px 0;">

        <div class="profile-section">
            <h2>Research Areas</h2>
            <dl class="profile-list">
                <dt>Physical AI Economics</dt>
                <dd>The structural transition from intangible AI value to physical capability-driven value.</dd>

                <dt>Semiconductor Capability Amplification</dt>
                <dd>How equipment, process innovation, and supply chains determine strategic advantage.</dd>

                <dt>AI in Scientific Discovery</dt>
                <dd>Applications of AI in molecular biology, drug discovery, and industrial science.</dd>
            </dl>
        </div>

        <div class="profile-section">
            <h2>Professional Background</h2>
            <ul style="list-style: none; padding: 0; font-size: 1.1em; line-height: 2;">
                <li>🎓 <strong>PhD (Executive DBA)</strong>, HEC Liège</li>
                <li>🏭 <strong>Former President</strong>, Global carbon materials industry</li>
                <li>💼 <strong>Advisor</strong>, Board-level industrial strategy consultant</li>
            </ul>
        </div>

        <div class="profile-section" style="background: #f8f9fa; padding: 40px; border-radius: 8px;">
            <h2>Collaboration</h2>
            <p>Open to collaboration in research, policy dialogue, and industrial strategy.</p>
            <p><a href="mailto:contact@sinclairhuang.org" style="color: var(--accent); font-weight: bold;">Get in touch &rarr;</a></p>
        </div>
    </section>

    <footer>
        <p>&copy; 2026 Sinclair Huang. All Rights Reserved.</p>
    </footer>

</body>
</html>
"""

# 寫入檔案
with open(HOME_FILE, 'w', encoding='utf-8') as f:
    f.write(home_html)
print(f"✅ 首頁已更新: {HOME_FILE}")

with open(ABOUT_FILE, 'w', encoding='utf-8') as f:
    f.write(about_html)
print(f"✅ Research Profile 頁面已建立: {ABOUT_FILE}")

# 順便修正其他頁面的導航連結 (Publications, Blog, News 也要能連回來)
# 這是一個小腳本，用來確保所有頁面的 Menu 連結都是一致的
def update_nav_links(file_path):
    if not os.path.exists(file_path): return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 簡單的替換邏輯：如果有舊的導航，試著統一更新 (這裡僅做簡單檢查，避免覆蓋太複雜的邏輯)
    # 更好的方式是我們下次統一用 Python 生成所有頁面，目前先不更動其他頁面以免出錯
    pass

