"""Regression checks for the replacement menu approved on 23 October 2026.

Fixtures below are customer prices outside brackets in the supplied list.
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
single = {'espresso-single':6500, 'espresso-double':8000, 'espresso-creme':8000, 'flat-white':9000, 'turkish-coffee':5000, 'shaken-espresso':8000, 'chicken-steak':10000, 'beef-fajita':10000, 'grilled-chicken':10000, 'tanduri-chicken':10000, 'beef-steak':10000, 'halloumi':9000, 'club-sandwich':9000, 'plain-croissant':5000, 'cupcakes':2500, 'muffins':5500, 'cake':6500, 'red-pasta':15000, 'white-pasta':17500, 'cocktails-6':10000, 'cocktails-8':10000, 'long-island-iced-tea':12000, 'liqueur-4':19000, 'liqueur-5':13500, 'liqueur-2':10000, 'liqueur-7':10000, 'american-whiskey-1':14500, 'irish-whiskey-1':14500, 'rum-2':11000, 'bacardi-black':11000, 'single-malt-1':19000, 'single-malt-5':19000, 'tequila-5':19000, 'patron':10000, 'tequila-3':16500, 'magnum':7000, 'cornetto':5000, 'rice-meal':15000, 'water':2000, 'pepsi':3000, 'redbull':6500, 'ginger-shot':4500}
for id, price in single.items(): assert items[id]['prices'] == {'':price}, id
sized = {
 'white-mocha': {'Small':8500,'Medium':9500,'Large':10500},
 'macchiato-single': {'Small':6500,'Medium':9000},
 'espresso-freddo': {'Small':8000,'Medium':9000},
 'creme-frappe': {'Small':8000,'Medium':9000,'Large':10500},
 'white-frappe': {'Small':8000,'Medium':9000,'Large':10500},
 'iced-spanish-latte': {'Small':10000,'Medium':11000,'Large':12000},
 'iced-americano': {'Small':7000,'Medium':8000,'Large':9000},
 'iced-latte': {'Small':8000,'Medium':9000,'Large':10000},
 'fresh-orange': {'Small':8000,'Medium':9000,'Large':10000},
 'english-breakfast-tea': {'Small':3000,'Medium':3500,'Large':4000},
 'milk': {'Small':3000,'Medium':3500,'Large':4000},
 'tang': {'Small':3000,'Large':5000},
 'flower': {'Medium':5000,'Large':12000},
 'teddy-bear': {'Small':7000,'Medium':15000,'Large':25000},
 'kurda-nuts': {'Small':7000,'Large':14000},
 'man-al-sama': {'Small':35000,'Medium':57500},
 'baklava': {'Small':40000,'Medium':65000},
 'heineken-draught-35': {'35 cl':9500},
 'draft-beer-1': {'50 cl':15000},
 'krombacher-pils': {'500 ml':13500},
 'al-amira-extra': {'Large':8000},
 'lays': {'Small':1500,'Medium':2500},
 'pringles': {'Small':3000}
}
for id, prices in sized.items(): assert items[id]['prices'] == prices, id
for i in cats['pizza']['items']: assert i['prices'] == {'Small':10500,'Medium':15000,'Large':19500}
for i in cats['mocktails']['items']: assert i['prices'] == {'':8000}
assert items['creme-frappe']['flavours'] == ['Vanilla','Hazelnut','Chocolate']
assert items['iced-latte']['flavours'] == ['Caramel','Hazelnut']
assert items['iced-mocha']['flavours'] == ['Mocha','White Mocha']
assert len(items['magnum']['flavours']) == 9 and len(items['cornetto']['flavours']) == 7
assert len(items['freez']['flavours']) == 4 and len(items['rani']['flavours']) == 3
assert {id for id,i in items.items() if any(p is None for p in i['prices'].values())} == {'mobile-card','e-sim'}
for i in cats['central-meals']['items']: assert i['noteKey'] == 'k5Only'
for i in cats['mobile-services']['items']: assert i['priceType'] == 'variable' and i['noteKey'] == 'variableAmount'
for removed in ['iraqi-tea','dark-frappe','bear-xl','liqueur-6','cocktails-4','iced-latte-flavour','macchiato-double','iced-white-mocha']:
 assert removed not in items
for lang in ['ar','ckb']:
 assert set(tr[lang]['items']) == set(items)
 assert set(tr[lang]['categories']) == set(cats)
for i in items.values():
 for key in i: assert key in {'id','name','prices','flavours','noteKey','priceType'}, key
 for lang in tr:
  for f in i.get('flavours',[]): assert tr[lang]['ui'][f]
  for size in i['prices']: assert not size or tr[lang]['ui'][size]

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
 assert {id:i['prices'] for id,i in embedded_items.items()} == {id:i['prices'] for id,i in items.items()}
 schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)[1])
 schema_items=[i for c in schema['hasMenuSection'] for i in c['hasMenuItem']]
 assert len(schema_items)==255
 for item, structured in zip([i for c in data['categories'] for i in c['items']], schema_items):
  name=item['name'] if lang=='en' else tr[lang]['items'][item['id']]
  assert structured['name']==name
  assert [o['price'] for o in structured.get('offers',[])]==[p for p in item['prices'].values() if p is not None]
  assert all(o['priceCurrency']=='IQD' for o in structured.get('offers',[]))
 assert not re.search(r'\{\{[^}]+\}\}',html)
print('PASS: 255 items, 35 categories, approved prices/sizes, translations and all three generated pages.')
