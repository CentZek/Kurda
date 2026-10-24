"""Build all three static menu languages from the price-free catalog."""
import json
import re
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist/menu'
data = json.loads((OUT / 'menu-data.json').read_text('utf-8'))
translations = json.loads((ROOT / 'menu-source/translations.json').read_text('utf-8'))
template = (ROOT / 'menu-source/template.html').read_text('utf-8')
icons = (ROOT / 'menu-source/icons.html').read_text('utf-8')
groups = ['food', 'drinks', 'bar', 'gifts']
group_icons = dict(zip(groups, ['sandwich', 'coffee', 'cocktail', 'gift']))
group_art = dict(zip(groups, ['sandwich-illustration', 'coffee-illustration', 'cocktail-illustration', None]))
art = {'sandwiches': 'sandwich-illustration', 'pastries': 'pastry-illustration', 'hot-coffee': 'coffee-illustration', 'iced-coffee': 'iced-coffees', 'tea': 'tea', 'chai': 'coffee-illustration', 'hot-chocolate': 'chocolate', 'iced-chocolate': 'chocolate', 'frappe': 'iced-coffees', 'draft-beer': 'beer-illustration', 'beer': 'beer-illustration', 'cocktails': 'cocktail-illustration', 'gin': 'gin-illustration', 'wine': 'wine-illustration', 'cognac': 'cognac-illustration', 'tequila': 'tequila-illustration'}
icon = lambda name: f'<svg class="icon" aria-hidden="true"><use href="#i-{name}"/></svg>'
def image(name, cls='', eager=False, fallback='gift'):
    if not name:
        return f'<span class="gift-art {cls}">{icon(fallback)}</span>'
    assert (OUT / f'assets/{name}.webp').exists()
    return f'<img class="{cls}" src="/menu/assets/{name}.webp" alt="" width="240" height="240" loading="{"eager" if eager else "lazy"}" decoding="async">'
def dump(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')

ids = set()
for cat in data['categories']:
    assert cat['group'] in groups, f'Unknown group: {cat["id"]}'
    cat['names'] = {'en': cat['name'], **{lang: translations[lang]['categories'][cat['id']] for lang in ['ar', 'ckb']}}
    cat['art'] = art.get(cat['id'], 'whiskey-illustration' if cat['group'] == 'bar' else None)
    for item in cat['items']:
        assert item['id'] not in ids
        ids.add(item['id'])
        assert set(item) <= {'id', 'name', 'sizes', 'flavours', 'noteKey'}
        assert isinstance(item['sizes'], list) and all(isinstance(s, str) and s for s in item['sizes'])
        item['names'] = {'en': item['name'], **{lang: translations[lang]['items'][item['id']] for lang in ['ar', 'ckb']}}
        item['flavoursByLanguage'] = {lang: [translations[lang]['ui'][f] for f in item.get('flavours', [])] for lang in translations}
        item['notesByLanguage'] = {lang: translations[lang]['ui'][item['noteKey']] for lang in translations} if item.get('noteKey') else {}
assert len(ids) == sum(len(cat['items']) for cat in data['categories'])
# Show food first in the HTML as well as the interactive view.
data['categories'].sort(key=lambda cat: groups.index(cat['group']))
for lang, tr in translations.items():
    ui = tr['ui']
    url = 'https://www.kurda.com/menu' + (f'/{lang}/' if lang != 'en' else '')
    sections, categories, schema_sections, options = [], [], [], []
    for cat in data['categories']:
        name, cid, group = cat['names'][lang], cat['id'], cat['group']
        options.append(f'<option value="{cid}" data-group="{group}">{e(name)}</option>')
        categories.append(f'<a class="category-tile" data-category="{cid}" data-group="{group}" href="#section-{cid}">{image(cat["art"], fallback=cat["icon"])}<span>{e(name)}</span></a>')
        cards, schema_items = [], []
        for item in cat['items']:
            item_name = item['names'][lang]
            sizes = f'<ul class="sizes" aria-label="{e(ui["sizes"])}">' + ''.join(f'<li>{e(ui[size])}</li>' for size in item['sizes']) + '</ul>' if item['sizes'] else ''
            flavours = f'<p class="flavours">{" · ".join(map(e, item["flavoursByLanguage"][lang]))}</p>' if item.get('flavours') else ''
            note = f'<p class="item-note">{e(item["notesByLanguage"][lang])}</p>' if item['notesByLanguage'] else ''
            cards.append(f'<article class="menu-card" data-item="{item["id"]}"><div class="item-info"><h3>{e(item_name)}</h3>{flavours}{sizes}{note}</div><button class="save-item js-only" data-save="{item["id"]}" type="button" aria-label="{e(ui["save"] + " " + item_name)}" aria-pressed="false">{icon("heart")}</button></article>')
            schema_item = {'@type':'MenuItem','name':item_name}
            descriptions = [ui[s] for s in item['sizes']] + item['flavoursByLanguage'][lang] + ([item['notesByLanguage'][lang]] if item['notesByLanguage'] else [])
            if descriptions: schema_item['description'] = '; '.join(descriptions)
            schema_items.append(schema_item)
        sections.append(f'<section class="menu-section" id="section-{cid}" data-section="{cid}" data-group="{group}" aria-labelledby="heading-{cid}"><div class="section-heading"><div><p class="eyebrow">{e(ui[group])}</p><h2 id="heading-{cid}">{e(name)}</h2></div>{image(cat["art"], fallback=cat["icon"])}</div><div class="card-grid">{"".join(cards)}</div></section>')
        schema_sections.append({'@type':'MenuSection','name':name,'hasMenuItem':schema_items})
    group_cards, tabs = [], []
    for group in groups:
        first = next(cat['id'] for cat in data['categories'] if cat['group'] == group)
        group_cards.append(f'<a class="group-card {group}" data-browse="{group}" href="#section-{first}">{image(group_art[group], eager=True)}<span class="group-copy"><strong>{e(ui[group])}</strong><span>{e(ui[group+"Hint"])}</span></span><span class="card-arrow" aria-hidden="true">↗</span></a>')
        tabs.append(f'<a href="#section-{first}" data-browse="{group}">{icon(group_icons[group])}<span>{e(ui[group])}</span></a>')
    links = ''.join(f'<a href="/menu{("/"+code+"/") if code != "en" else ""}" lang="{code}" hreflang="{code}" data-language="{code}" {"aria-current=page" if code == lang else ""}>{label}</a>' for code, label in [('en','English'),('ckb','کوردی'),('ar','العربية')])
    schema = {'@context':'https://schema.org','@type':'Menu','name':ui['title'],'url':url,'inLanguage':lang,'hasMenuSection':schema_sections}
    values = {**{k:e(v) for k,v in ui.items()}, 'LANG':lang, 'DIR':'ltr' if lang == 'en' else 'rtl', 'URL':url, 'ICONS':icons, 'LANGUAGES':links, 'GROUP_CARDS':''.join(group_cards), 'GROUP_TABS':''.join(tabs), 'CATEGORIES':''.join(categories), 'CATEGORY_OPTIONS':f'<option value="all">{e(ui["all"])}</option>'+''.join(options), 'MENU':''.join(sections), 'TOTAL':str(len(ids)), 'DATA':dump(data), 'UI':dump(ui), 'SCHEMA':dump(schema)}
    html = re.sub(r'\{\{([^}]+)\}\}', lambda m: values[m[1]], template)
    dest = OUT if lang == 'en' else OUT/lang
    dest.mkdir(exist_ok=True)
    (dest/'index.html').write_text(html,encoding='utf-8')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>https://www.kurda.com/menu'+(f'/{lang}/' if lang != 'en' else '')+'</loc></url>' for lang in translations)+'</urlset>',encoding='utf-8')
print(f'Built {len(ids)} items in English, Sorani Kurdish and Arabic.')
