import os

# 定義檔案路徑
CONTACT_DIR = 'docs/contact'
CONTACT_FILE = os.path.join(CONTACT_DIR, 'index.html')

# 確保目錄存在
if not os.path.exists(CONTACT_DIR):
    os.makedirs(CONTACT_DIR)

# CSS 樣式 (維持全站一致，並加入 Contact 專用樣式)
STYLE = """
<style>
    :root {
        --primary: #2c3e50;
        --accent: #2980b9;
        --bg-light: #f8f9fa;
        --text: #333;
        --text-light: #555;
    }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.7; color: var(--text); margin: 0; padding: 0; background-color: #fcfcfc; }
    
    /* 導航欄 */
    nav { padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; background: #fff; position: sticky; top: 0; z-index: 100; }
    nav .logo { font-weight: 800; font-size: 1.3em; letter-spacing: -0.5px; }
    nav .logo a { text-decoration: none; color: #000; }
    nav .links a { margin-left: 25px; font-size: 0.95em; color: #666; text-decoration: none; font-weight: 500; }
    nav .links a:hover { color: var(--accent); }

    /* 標題區 */
    .header-section { text-align: center; padding: 80px 20px 50px; background: linear-gradient(to bottom, #fff, #f8f9fa); border-bottom: 1px solid #eee; }
    h1 { font-size: 3em; margin-bottom: 20px; color: var(--primary); letter-spacing: -1px; }
    .intro { max-width: 700px; margin: 0 auto; font-size: 1.2em; color: #666; }

    /* 內容區 */
    .container { max-width: 900px; margin: 60px auto; padding: 0 20px; }
    
    /* 雙欄佈局 */
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 60px; }
    
    /* 卡片樣式 */
    .contact-card { 
        background: #fff; 
        padding: 40px; 
        border-radius: 8px; 
        border: 1px solid #eee; 
        box-shadow: 0 5px 15px rgba(0,0,0,0.03); 
        transition: transform 0.2s;
    }
    .contact-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.06); }
    
    .card-title { font-size: 1.5em; font-weight: 700; color: var(--primary); margin-bottom: 20px; border-bottom: 2px solid var(--accent); padding-bottom: 10px; display: inline-block; }
    
    ul { padding-left: 20px; margin-bottom: 30px; color: var(--text-light); }
    li { margin-bottom: 8px; }

    .email-box { 
        background: #f0f7fb; 
        padding: 15px; 
        border-radius: 6px; 
        text-align: center; 
        font-weight: 600; 
        color: var(--accent);
        font-size: 1.1em;
    }
    .email-box a { text-decoration: none; color: inherit; }
    .email-box:hover { background: var(--accent); color: #fff; }

    /* General Notes & Philosophy */
    .section-box { margin-bottom: 50px; padding: 30px; background: #fff; border-left: 5px solid #eee; }
    .section-title { font-size: 1.3em; font-weight: 700; color: #333; margin-bottom: 15px; }

    footer { text-align: center; padding: 60px 20px; color: #999; font-size: 0.9em; margin-top: 60px; border-top: 1px solid #eee; }

    @media (max-width: 768px) {
        nav { flex-direction: column; padding: 15px; }
        nav .links { margin-top: 15px; display: flex; flex-wrap: wrap; justify-content: center; }
        nav .links a { margin: 5px 10px; }
        .grid { grid-template-columns: 1fr; }
    }
</style>
"""

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact - Sinclair Huang</title>
    {STYLE}
</head>
<body>

    <nav>
        <div class="logo"><a href="../index.html">Sinclair Huang</a></div>
        <div class="links">
            <a href="../index.html">Home</a>
            <a href="../about/index.html">Research Profile</a>
            <a href="../publications/index.html">Publications</a>
            <a href="../projects/index.html">Research Portfolio</a>
            <a href="../blog/index.html">Blog</a>
            <a href="#" style="color: #000; font-weight: bold;">Contact</a>
        </div>
    </nav>

    <div class="header-section">
        <h1>Contact</h1>
        <div class="intro">
            Get in touch for research, collaboration, and advisory inquiries.<br>
            I welcome thoughtful dialogue across academic, industrial, and strategic domains.
        </div>
    </div>

    <div class="container">
        
        <div class="grid">
            <div class="contact-card">
                <div class="card-title">Research & Academic</div>
                <ul>
                    <li>Research partnerships</li>
                    <li>Academic exchange</li>
                    <li>Working papers and publications</li>
                    <li>Conference invitations</li>
                </ul>
                <div class="email-box">
                    <a href="mailto:research@sinclairhuang.org">📧 research@sinclairhuang.org</a>
                </div>
            </div>

            <div class="contact-card">
                <div class="card-title">Advisory & Industry</div>
                <ul>
                    <li>Board-level strategy consultation</li>
                    <li>Industrial AI deployment</li>
                    <li>Semiconductor ecosystem analysis</li>
                    <li>Technology capability assessment</li>
                </ul>
                <div class="email-box">
                    <a href="mailto:advisory@sinclairhuang.org">📧 advisory@sinclairhuang.org</a>
                </div>
            </div>
        </div>

        <div class="section-box">
            <div class="section-title">General Notes</div>
            <p>Please include a brief introduction and context for your inquiry to facilitate a meaningful response.</p>
            <p style="color: #777; font-size: 0.95em;">Due to professional commitments, response times may vary. Thank you for your understanding.</p>
        </div>

        <div class="section-box" style="border-left-color: var(--primary);">
            <div class="section-title">Collaboration Philosophy</div>
            <p style="font-size: 1.1em; line-height: 1.8; font-style: italic; color: #555;">
                "I believe the most valuable insights emerge at the intersection of <strong>academic rigor</strong>, 
                <strong>industrial experience</strong>, and <strong>strategic perspective</strong>."
            </p>
            <p>This site serves as an open platform for advancing dialogue on the future of intelligence, technology, and global industrial systems.</p>
        </div>

    </div>

    <footer>
        <p>&copy; 2026 Sinclair Huang. All Rights Reserved.</p>
    </footer>

</body>
</html>
"""

with open(CONTACT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"🎉 Contact 頁面已建立：{CONTACT_FILE}")
