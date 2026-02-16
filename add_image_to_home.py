import os

HOME_FILE = 'docs/index.html'

# 這是之前的完整首頁代碼，但這次加入了圖片區塊
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sinclair Huang - AI & Industrial Strategy</title>
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

        /* 圖片樣式 */
        .stack-image-container {
            text-align: center;
            margin-top: 50px;
            margin-bottom: 30px;
        }
        .stack-image {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15); /* 增加陰影讓它浮起來 */
            border: 1px solid #eee;
        }
        .image-caption {
            font-size: 0.9em;
            color: #888;
            margin-top: 15px;
            font-style: italic;
        }

        footer { text-align: center; padding: 60px 20px; color: #999; font-size: 0.9em; border-top: 1px solid #eee; margin-top: 60px; }
        
        @media (max-width: 768px) {
            h1 { font-size: 2.2em; }
            nav { flex-direction: column; padding: 15px; }
            nav .links { margin-top: 15px; }
            nav .links a { margin: 0 10px; }
            .theme { padding: 40px 20px; }
        }
    </style>
</head>
<body>

    <nav>
        <div class="logo"><a href="index.html">Sinclair Huang</a></div>
        <div class="links">
            <a href="index.html">Home</a>
            <a href="about/index.html">Research Profile</a>
            <a href="publications/index.html">Publications</a>
            <a href="blog/index.html">Blog</a>
            <a href="news/index.html">News</a>
        </div>
    </nav>

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
        
        <div class="stack-image-container">
            <img src="ai-stack.jpg" alt="The Physical AI Stack Diagram" class="stack-image">
            <div class="image-caption">The Physical AI Stack: Where Intelligence Meets Industrial Reality</div>
        </div>
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

with open(HOME_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"🎉 首頁已更新！圖片連結已加入: {HOME_FILE}")
print("⚠️ 請記得確認 docs 資料夾內有 'ai-stack.jpg' 這張圖片！")
