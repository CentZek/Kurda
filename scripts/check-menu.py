"""Regression checks for the price-free menu requested on 24 October 2026.

Checks catalog preservation and absence of monetary data in public outputs.
Run after build-menu.py. No browser or third-party dependencies required.
"""
import json
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT/'dist/menu/menu-data.json').read_text('utf-8'))
tr = json.loads((ROOT/'menu-source/translations.json').read_text('utf-8'))
cats = {c['id']: c for c in data['categories']}
items = {i['id']: i for c in cats.values() for i in c['items']}
assert len(cats) == 35 and len(items) == 255
assert sum(len(c['items']) for c in cats.values()) == len(items)
assert {g: sum(len(c['items']) for c in cats.values() if c['group'] == g) for g in ['food','drinks','bar','gifts']} == {'food':54,'drinks':63,'bar':104,'gifts':34}
for id in ['white-mocha','creme-frappe','white-frappe','iced-spanish-latte','milk']:
 assert items[id]['sizes'] == ['Small','Medium','Large']
assert items['macchiato-single']['sizes'] == ['Small','Medium']
assert items['flower']['sizes'] == ['Medium','Large']
assert items['tang']['sizes'] == ['Small','Large']
assert items['heineken-draught-35']['sizes'] == ['35 cl']
assert items['draft-beer-1']['sizes'] == ['50 cl']
assert items['krombacher-pils']['sizes'] == ['500 ml']
for i in cats['pizza']['items']: assert i['sizes'] == ['Small','Medium','Large']
assert items['creme-frappe']['flavours'] == ['Vanilla','Hazelnut','Chocolate']
assert items['iced-latte']['flavours'] == ['Caramel','Hazelnut']
assert items['iced-mocha']['flavours'] == ['Mocha','White Mocha']
assert len(items['magnum']['flavours']) == 9 and len(items['cornetto']['flavours']) == 7
assert len(items['freez']['flavours']) == 4 and len(items['rani']['flavours']) == 3
for i in cats['central-meals']['items']: assert i['noteKey'] == 'k5Only'
for i in cats['mobile-services']['items']: assert i['noteKey'] == 'variableAmount'
for removed in ['iraqi-tea','dark-frappe','bear-xl','liqueur-6','cocktails-4','iced-latte-flavour','macchiato-double','iced-white-mocha']:
 assert removed not in items
for lang in ['ar','ckb']:
 assert set(tr[lang]['items']) == set(items)
 assert set(tr[lang]['categories']) == set(cats)
for i in items.values():
 for key in i: assert key in {'id','name','sizes','flavours','noteKey'}, key
 for lang in tr:
  for f in i.get('flavours',[]): assert tr[lang]['ui'][f]
  for size in i['sizes']: assert not size or tr[lang]['ui'][size]

class CardParser(HTMLParser):
 def __init__(self): super().__init__(); self.ids=[]; self.references=[]; self.symbols=[]
 def handle_starttag(self, tag, attrs):
  a=dict(attrs)
  if 'data-item' in a: self.ids.append(a['data-item'])
  if tag == 'use': self.references.append(a['href'][1:])
  if tag == 'symbol': self.symbols.append(a['id'])

for lang in tr:
 path=ROOT/'dist/menu'/('index.html' if lang=='en' else lang+'/index.html')
 html=path.read_text('utf-8'); parser=CardParser(); parser.feed(html)
 assert set(parser.ids)==set(items) and len(parser.ids)==255
 assert set(parser.references)<=set(parser.symbols)
 embedded=json.loads(re.search(r'<script type="application/json" id="menu-data">(.*?)</script>',html,re.S)[1])
 embedded_items={i['id']:i for c in embedded['categories'] for i in c['items']}
 assert {id:i['sizes'] for id,i in embedded_items.items()} == {id:i['sizes'] for id,i in items.items()}
 schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)[1])
 schema_items=[i for c in schema['hasMenuSection'] for i in c['hasMenuItem']]
 assert len(schema_items)==255
 for item, structured in zip([i for c in data['categories'] for i in c['items']], schema_items):
  name=item['name'] if lang=='en' else tr[lang]['items'][item['id']]
  assert structured['name']==name
  assert 'offers' not in structured
 assert not re.search(r'\{\{[^}]+\}\}',html)
 assert not re.search(r'"(?:price|prices|currency|priceCurrency|priceType|offers)"\s*:',html)
 assert 'class="prices' not in html and 'value="low"' not in html and 'value="high"' not in html
 assert tr[lang]['ui']['cashierNote'] in html
print('PASS: 255 items, 35 categories, no prices, retained sizes, translations and all three generated pages.')
