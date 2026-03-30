#!/usr/bin/env python3
"""포트폴리오 케이스 스터디 → HTML 프리뷰 생성"""

import markdown
from pathlib import Path

# Mermaid 다이어그램 읽기
diagrams_dir = Path(__file__).parent / "diagrams"
diagrams = {}
for f in sorted(diagrams_dir.glob("*.mmd")):
    diagrams[f.stem] = f.read_text(encoding="utf-8")

# 케이스 스터디 읽기 (순서 지정)
cases_dir = Path(__file__).parent / "cases"
case_files = [
    ("about", "D1_career_narrative.md"),
    ("battery", "D2_battery_compatibility_case.md"),
    ("statemachine", "D3_state_machine_case.md"),
    ("pump", "D4_pump_power_case.md"),
    ("testdriven", "D12_test_driven_engineer.md"),
    ("thememap", "THEME_MAP.md"),
]

md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "attr_list"])

sections_html = []
nav_items = []

for section_id, filename in case_files:
    filepath = cases_dir / filename
    if not filepath.exists():
        continue
    content = filepath.read_text(encoding="utf-8")
    md.reset()
    html = md.convert(content)
    sections_html.append((section_id, html))

    # 네비게이션용 제목 추출
    first_line = content.split("\n")[0].replace("#", "").strip()
    nav_items.append((section_id, first_line))

# 다이어그램 섹션 추가
diagram_labels = {
    "system_architecture": "시스템 아키텍처",
    "state_machine": "상태 전이도",
    "can_network": "CAN 네트워크 구성도",
}

# HTML 생성
html_output = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>황인혁 — Physical AI 브릿지 엔지니어 포트폴리오</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
    <style>
        :root {{
            --bg: #0d1117;
            --bg-card: #161b22;
            --bg-code: #1c2128;
            --border: #30363d;
            --text: #e6edf3;
            --text-dim: #8b949e;
            --accent: #58a6ff;
            --accent2: #3fb950;
            --accent3: #d2a8ff;
            --accent4: #f97583;
            --accent5: #ffa657;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.7;
        }}

        /* 네비게이션 */
        nav {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(13,17,23,0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border);
            z-index: 100;
            padding: 0 2rem;
        }}
        nav ul {{
            display: flex;
            list-style: none;
            gap: 0;
            max-width: 1200px;
            margin: 0 auto;
            overflow-x: auto;
        }}
        nav li a {{
            display: block;
            padding: 1rem 1.2rem;
            color: var(--text-dim);
            text-decoration: none;
            font-size: 0.85rem;
            white-space: nowrap;
            border-bottom: 2px solid transparent;
            transition: all 0.2s;
        }}
        nav li a:hover, nav li a.active {{
            color: var(--accent);
            border-bottom-color: var(--accent);
        }}

        /* Hero */
        .hero {{
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 6rem 2rem 4rem;
            background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #1c2128 100%);
        }}
        .hero h1 {{
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        .hero .subtitle {{
            font-size: 1.3rem;
            color: var(--accent);
            margin-bottom: 1rem;
        }}
        .hero .tagline {{
            font-size: 1.1rem;
            color: var(--text-dim);
            max-width: 600px;
            margin-bottom: 3rem;
        }}
        .hero-stats {{
            display: flex;
            gap: 3rem;
            flex-wrap: wrap;
            justify-content: center;
        }}
        .stat-card {{
            text-align: center;
        }}
        .stat-card .number {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--accent2);
        }}
        .stat-card .label {{
            font-size: 0.85rem;
            color: var(--text-dim);
            margin-top: 0.3rem;
        }}

        /* 메인 콘텐츠 */
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }}
        section {{
            padding: 4rem 0;
            border-bottom: 1px solid var(--border);
        }}
        section:last-child {{ border-bottom: none; }}

        /* 타이포그래피 */
        h1 {{ font-size: 2rem; margin: 2rem 0 1rem; color: var(--text); }}
        h2 {{ font-size: 1.6rem; margin: 2.5rem 0 1rem; color: var(--accent); border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }}
        h3 {{ font-size: 1.2rem; margin: 2rem 0 0.8rem; color: var(--accent3); }}
        h4 {{ font-size: 1rem; margin: 1.5rem 0 0.5rem; color: var(--accent5); }}
        p {{ margin: 0.8rem 0; }}
        strong {{ color: var(--accent); }}

        /* 테이블 */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.9rem;
        }}
        th {{
            background: var(--bg-code);
            color: var(--accent);
            padding: 0.8rem 1rem;
            text-align: left;
            border: 1px solid var(--border);
            font-weight: 600;
        }}
        td {{
            padding: 0.7rem 1rem;
            border: 1px solid var(--border);
            vertical-align: top;
        }}
        tr:hover td {{
            background: rgba(88,166,255,0.05);
        }}

        /* 코드 블록 */
        code {{
            background: var(--bg-code);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.85em;
            color: var(--accent5);
        }}
        pre {{
            background: var(--bg-code);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            overflow-x: auto;
            margin: 1.5rem 0;
        }}
        pre code {{
            background: none;
            padding: 0;
            color: var(--text);
        }}

        /* 인용 */
        blockquote {{
            border-left: 3px solid var(--accent);
            padding: 1rem 1.5rem;
            margin: 1.5rem 0;
            background: rgba(88,166,255,0.05);
            border-radius: 0 8px 8px 0;
            color: var(--text-dim);
        }}
        blockquote strong {{ color: var(--accent); }}

        /* 리스트 */
        ul, ol {{
            margin: 0.8rem 0;
            padding-left: 2rem;
        }}
        li {{ margin: 0.4rem 0; }}

        /* 다이어그램 */
        .diagram-section {{
            margin: 3rem 0;
            padding: 2rem;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
        }}
        .diagram-section h3 {{
            color: var(--accent);
            margin-top: 0;
        }}
        .mermaid {{
            display: flex;
            justify-content: center;
            margin: 1.5rem 0;
            overflow-x: auto;
        }}

        /* 섹션 구분자 */
        hr {{
            border: none;
            border-top: 1px solid var(--border);
            margin: 2rem 0;
        }}

        /* 반응형 */
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 2rem; }}
            .hero-stats {{ gap: 1.5rem; }}
            nav li a {{ padding: 0.8rem; font-size: 0.75rem; }}
            .container {{ padding: 1rem; }}
            table {{ font-size: 0.8rem; }}
            th, td {{ padding: 0.5rem; }}
        }}
    </style>
</head>
<body>
    <nav>
        <ul>
            <li><a href="#hero">Home</a></li>
"""

for section_id, title in nav_items:
    short_title = title[:20] + "..." if len(title) > 20 else title
    html_output += f'            <li><a href="#{section_id}">{short_title}</a></li>\n'

html_output += """            <li><a href="#diagrams">다이어그램</a></li>
        </ul>
    </nav>

    <!-- Hero -->
    <div class="hero" id="hero">
        <h1>황인혁</h1>
        <div class="subtitle">모터제어 개발자 · Physical AI 브릿지 엔지니어</div>
        <div class="tagline">"소프트웨어가 물리 세계와 만나는 접점에서 제품을 만듭니다"</div>
        <div class="hero-stats">
            <div class="stat-card">
                <div class="number">2</div>
                <div class="label">특허 출원</div>
            </div>
            <div class="stat-card">
                <div class="number">37+</div>
                <div class="label">이슈 해결</div>
            </div>
            <div class="stat-card">
                <div class="number">9</div>
                <div class="label">시험 체계 구축</div>
            </div>
            <div class="stat-card">
                <div class="number">132</div>
                <div class="label">부품 관리</div>
            </div>
        </div>
    </div>

    <div class="container">
"""

# 섹션 추가
for section_id, html in sections_html:
    html_output += f'        <section id="{section_id}">\n{html}\n        </section>\n\n'

# 다이어그램 섹션
html_output += '        <section id="diagrams">\n'
html_output += '            <h1>시스템 다이어그램</h1>\n'
for name, code in diagrams.items():
    label = diagram_labels.get(name, name)
    html_output += f'            <div class="diagram-section">\n'
    html_output += f'                <h3>{label}</h3>\n'
    html_output += f'                <div class="mermaid">\n{code}\n                </div>\n'
    html_output += f'            </div>\n'
html_output += '        </section>\n'

html_output += """
    </div>

    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'dark',
            themeVariables: {
                darkMode: true,
                background: '#161b22',
                primaryColor: '#58a6ff',
                primaryTextColor: '#e6edf3',
                lineColor: '#30363d'
            }
        });

        // 스크롤 시 네비게이션 활성화
        const sections = document.querySelectorAll('section, .hero');
        const navLinks = document.querySelectorAll('nav a');
        window.addEventListener('scroll', () => {
            let current = '';
            sections.forEach(section => {
                const top = section.offsetTop - 80;
                if (scrollY >= top) current = section.id;
            });
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {
                    link.classList.add('active');
                }
            });
        });
    </script>
</body>
</html>
"""

output_path = Path(__file__).parent / "preview.html"
output_path.write_text(html_output, encoding="utf-8")
print(f"생성 완료: {output_path}")
print(f"파일 크기: {output_path.stat().st_size / 1024:.1f} KB")
