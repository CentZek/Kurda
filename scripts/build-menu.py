"""Build the static, no-JavaScript-friendly menu from the verified menu data.

Run from any directory: python scripts/build-menu.py
Source prices: MENU BOARDS.pdf supplied by Kurda, reviewed 2026-10-22.
No third-party dependencies. Commit generated dist/menu/index.html too.
"""
import json
import math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist/menu'
data = json.loads((OUT / 'menu-data.json').read_text(encoding='utf-8'))
icon = lambda name: f'<svg class="icon" aria-hidden="true"><use href="#i-{name}"/></svg>'
sections, tabs, schema_sections = [], ['<button type="button" class="category active" data-category="all" aria-pressed="true">The whole menu <span>53</span></button>'], []
ids = set()
for n, cat in enumerate(data['categories'], 1):
    cards, schema_items = [], []
    tabs.append(f'<button type="button" class="category" data-category="{cat["id"]}" aria-pressed="false">{icon(cat["icon"])}{escape(cat["name"])}</button>')
    for item in cat['items']:
        assert item['id'] not in ids
        ids.add(item['id'])
        assert all(isinstance(p, int) and p > 0 for p in item['prices'].values())
        price_rows = ''.join(f'<div><dt>{escape(size) if size else "Price"}</dt><dd>{price:,}<small> IQD</small></dd></div>' for size, price in item['prices'].items())
        flavours = f'<p class="flavours">{" · ".join(item["flavours"])}</p>' if item.get('flavours') else ''
        cards.append(f'''<article class="menu-card" data-item="{item['id']}"><div class="card-top"><span class="card-category">{escape(cat['name'])}</span><button class="save-item" data-save="{item['id']}" type="button" aria-label="Save {escape(item['name'])}" aria-pressed="false">{icon('heart')}</button></div><h4>{escape(item['name'])}</h4>{flavours}<dl class="prices {'single-price' if '' in item['prices'] else ''}">{price_rows}</dl></article>''')
        schema_items.append({'@type': 'MenuItem', 'name': item['name'], 'description': ', '.join(item.get('flavours', [])), 'offers': [{'@type': 'Offer', 'name': size or item['name'], 'price': price, 'priceCurrency': 'IQD'} for size, price in item['prices'].items()]})
    artwork = {'iced-coffee': 'iced-coffees', 'tea': 'tea', 'hot-chocolate': 'chocolate', 'iced-chocolate': 'chocolate', 'frappe': 'iced-coffees'}.get(cat['id'])
    decoration = f'<img class="section-art" src="/menu/assets/{artwork}.webp" width="100" height="100" alt="" loading="lazy">' if artwork else f'<span class="section-icon">{icon(cat["icon"])}</span>'
    sections.append(f'''<section class="menu-section" data-section="{cat['id']}" aria-labelledby="heading-{cat['id']}"><div class="section-heading"><span class="section-number">{n:02}</span><div><p class="eyebrow">{escape(cat['eyebrow'])}</p><h3 id="heading-{cat['id']}">{escape(cat['name'])}</h3><p>{escape(cat['description'])}</p></div>{decoration}</div><div class="card-grid">{''.join(cards)}</div></section>''')
    schema_sections.append({'@type': 'MenuSection', 'name': cat['name'], 'hasMenuItem': schema_items})
assert len(ids) == 53
schema = {'@context': 'https://schema.org', '@type': 'Menu', 'name': 'Kurda Menu', 'url': 'https://menu.kurda.com/', 'inLanguage': 'en', 'hasMenuSection': schema_sections}
text = (ROOT / 'menu-source/template.html').read_text(encoding='utf-8')
for key, value in {'MENU': ''.join(sections), 'CATEGORIES': ''.join(tabs), 'DATA': json.dumps(data, ensure_ascii=False).replace('<', '\\u003c'), 'SCHEMA': json.dumps(schema, ensure_ascii=False), 'TICKER': '<span>COFFEE &amp; CONVERSATION <b>✦</b> A BITE TO SAVOUR <b>✦</b> SOMETHING SWEET <b>✦</b> A LITTLE KURDA MOMENT <b>✦</b></span>'}.items():
    text = text.replace('{{' + key + '}}', value)
(OUT / 'index.html').write_text(text, encoding='utf-8')
points = ' '.join(f'{300 + (290 if i % 2 == 0 else 132) * math.cos(i * math.pi / 21 - math.pi/2):.2f},{300 + (290 if i % 2 == 0 else 132) * math.sin(i * math.pi / 21 - math.pi/2):.2f}' for i in range(42))
sun = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600"><polygon fill="#f9bf20" points="{points}"/></svg>'
(OUT / 'assets/sun.svg').write_text(sun, encoding='utf-8')
(OUT / 'assets/favicon.svg').write_text(sun, encoding='utf-8')
print(f'Built {len(ids)} items across {len(data["categories"])} categories.')
