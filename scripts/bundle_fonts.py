"""把可爱字体（站酷快乐体 + Baloo 2）内置进 App，断网也能正常显示。
字体来自 npm 上的 @fontsource 包（npm install 时已下载）。
任何一步失败，就去掉外部字体链接，改用手机自带字体，保证 App 完全不联网。"""
import os, re, shutil

HTML = "www/index.html"
OUT = "www/fonts"
NM = "node_modules/@fontsource"
SOURCES = [("zcool-kuaile", "index.css"), ("baloo-2", "latin-700.css"), ("baloo-2", "latin-800.css")]
LINK = r'<link href="https://fonts\.googleapis\.com/css2[^"]+" rel="stylesheet">'

html = open(HTML, encoding="utf-8").read()
try:
    os.makedirs(OUT, exist_ok=True)
    parts, n = [], 0
    for pkg, css_name in SOURCES:
        css = open(os.path.join(NM, pkg, css_name), encoding="utf-8").read()
        css = re.sub(r",\s*url\(\./files/[^)]+\.woff\)\s*format\('woff'\)", "", css)
        for f in sorted(set(re.findall(r"url\(\./files/([^)]+\.woff2)\)", css))):
            shutil.copy(os.path.join(NM, pkg, "files", f), os.path.join(OUT, f))
            n += 1
        parts.append(css.replace("url(./files/", "url("))
    open(os.path.join(OUT, "fonts.css"), "w", encoding="utf-8").write("\n".join(parts))
    html, k = re.subn(LINK, '<link href="fonts/fonts.css" rel="stylesheet">', html)
    if not k:
        html = html.replace("</head>", '<link href="fonts/fonts.css" rel="stylesheet">\n</head>', 1)
    print(f"字体已内置，共 {n} 个文件")
except Exception as e:
    print("字体内置失败，改用手机自带字体：", e)
    html = re.sub(LINK + r"\s*", "", html)
html = re.sub(r'<link rel="preconnect"[^>]*>\s*', "", html)
open(HTML, "w", encoding="utf-8").write(html)
