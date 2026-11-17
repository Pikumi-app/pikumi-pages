#!/usr/bin/env python3
"""Build self-contained, script-free public pages using the Python standard library."""
import argparse
import html
import json
import posixpath
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANGUAGES = {'en': 'English', 'ru': 'Русский', 'fr': 'Français', 'es': 'Español', 'zh-Hans': '简体中文'}
PAGES = ('index', 'privacy', 'support')


def page_path(language, page):
    return f'{page}.html' if language == 'en' else f'{language}/{page}.html'


def relative(current, target):
    return posixpath.relpath(target, posixpath.dirname(current) or '.')


def escape(value):
    return html.escape(value, quote=True)


def render(language, page, content, site):
    c = content[language]
    current = page_path(language, page)
    link = lambda target: escape(relative(current, target))
    labels = {'index': c['home'], 'privacy': c['privacy'], 'support': c['support']}
    title = c['homeTitle'] if page == 'index' else c[f'{page}Title']
    lead = c['homeLead'] if page == 'index' else c[f'{page}Lead']
    alternate = '\n'.join(f'<link rel="alternate" hreflang="{lang}" href="{link(page_path(lang, page))}">' for lang in LANGUAGES)
    nav = ''.join(f'<a href="{link(page_path(lang, page))}" lang="{lang}" hreflang="{lang}"'
                  f'{" aria-current=\"page\"" if lang == language else ""}>{name}</a>' for lang, name in LANGUAGES.items())
    if page == 'index':
        body = ''.join(f'<h2><a href="{link(page_path(language, item))}">{escape(c[item])} →</a></h2><p>{escape(c[f"{item}Summary"])}</p>' for item in ('privacy', 'support'))
    elif page == 'privacy':
        body = ''.join(f'<section><h2>{index}. {escape(heading)}</h2>'+''.join(f'<p>{escape(p.format_map(site))}</p>' for p in paragraphs)+'</section>'
                       for index, (heading, *paragraphs) in enumerate(c['sections'], 1))
    else:
        body = f'<h2>{escape(c["contact"])}</h2><p>{escape(c["supportIntro"])}</p>'
        body += f'<p><a href="mailto:{escape(site["email"])}?subject=Pikumi%20Support">{escape(site["email"])}</a></p><p class="small">{escape(c["supportSafety"])}</p>'
        body += f'<h2>{escape(c["faqTitle"])}</h2>'+''.join(f'<section class="faq"><h3>{escape(question)}</h3><p>{escape(answer)}</p></section>' for question, answer in c['faq'])
        body += f'<p><a href="{link(page_path(language,"privacy"))}">{escape(c["privacy"])}</a></p>'
    if page != 'index':
        body += f'<section class="contact" id="contact"><h2>{escape(c["contact"])}</h2><p>{escape(site["brand"])} · {escape(c["developer"])}: {escape(site["developer"])}</p><p><a href="mailto:{escape(site["email"])}">{escape(site["email"])}</a></p></section>'
    if page == 'privacy':
        body += f'<aside><h2>{escape(c["related"])}</h2><ul class="resources"><li><a href="https://www.apple.com/legal/privacy/">{escape(c["applePrivacy"])}</a></li><li><a href="https://support.apple.com/104967">{escape(c["appleDeletion"])}</a></li><li><a href="https://policies.google.com/privacy">{escape(c["googlePrivacy"])}</a></li><li><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">{escape(c["githubPrivacy"])}</a></li></ul></aside>'
    footer = ''.join(f'<a href="{link(page_path(language, item))}">{escape(c[item])}</a>' for item in ('home', 'privacy', 'support') if item != 'home')
    return f'''<!doctype html>
<html lang="{language}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{escape(lead)}">
<title>{escape(labels[page])} | Pikumi</title>
<link rel="stylesheet" href="{link('styles.css')}">
{alternate}
<link rel="alternate" hreflang="x-default" href="{link(page_path('en',page))}">
</head>
<body>
<a class="skip" href="#content">{escape(c['skip'])}</a>
<main>
<header>
<a class="brand" href="{link(page_path(language,'index'))}"><span class="logo" aria-hidden="true">P✦</span>Pikumi</a>
<nav class="lang" aria-label="{escape(c['language'])}">{nav}</nav>
</header>
<article id="content">
<span class="pill">{escape(c['tagline'] if page == 'index' else labels[page])}</span>
<h1>{escape(title)}</h1>
<p class="sub">{escape(lead)}</p>
{f'<p class="small"><time datetime="{site["updated"]}">{escape(c["updated"])}</time></p>' if page == 'privacy' else ''}
<div class="card">{body}</div>
</article>
<footer><nav class="links" aria-label="Pikumi">{footer}</nav><p>© 2026 Pikumi · {escape(site["developer"])}</p></footer>
</main>
</body>
</html>
'''


def build(output):
    content = json.loads((ROOT/'src/content.json').read_text())
    site = json.loads((ROOT/'src/site.json').read_text())
    if set(content) != set(LANGUAGES) or site['edition'] != 'noads' or site['supportRetention'] != 'delete-after-resolution':
        raise ValueError('Content must match the confirmed ad-free edition and retention policy')
    if not site['developer'].strip() or '@' not in site['email']:
        raise ValueError('A confirmed developer name and contact email are required')
    output.mkdir(parents=True, exist_ok=True)
    files=[]
    for language in LANGUAGES:
        for page in PAGES:
            target = output/page_path(language,page)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(language,page,content,site),encoding='utf-8')
            files.append(target)
    if output.resolve() != ROOT.resolve():
        shutil.copy2(ROOT/'styles.css',output/'styles.css')
    files.append(output/'styles.css')
    return files


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT)
    parser.add_argument('--zip',type=Path,help='Optional archive of public HTML/CSS only')
    args=parser.parse_args()
    files=build(args.output)
    if args.zip:
        args.zip.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(args.zip,'w',zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                archive.write(path,path.relative_to(args.output))
        print(f'Publication archive: {args.zip}')
    print(f'Built 15 HTML pages in 5 languages and one stylesheet: {args.output}')


if __name__=='__main__':
    main()
