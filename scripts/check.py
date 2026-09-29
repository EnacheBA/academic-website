"""Check generated navigation, bibliography reconciliation and privacy boundaries."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist'
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__();self.links=[];self.ids=set();self.h1=0;self.noindex=False;self.feed(path.read_text())
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   assert a['id'] not in self.ids,'Duplicate id: '+a['id']
   self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='meta' and a.get('name')=='robots':self.noindex='noindex' in a.get('content','')
  if tag=='img':assert a.get('alt'),'Missing image alt'
  for key in ['href','src']:
   if a.get(key):self.links.append(a[key])
pages={p.name:Page(p) for p in OUT.glob('*.html')}
for name,page in pages.items():
 assert page.h1==1 and page.noindex,name
 for link in page.links:
  url=urlsplit(link)
  if url.scheme or url.netloc:continue
  target=unquote(url.path) or name
  assert (OUT/target).is_file(),f'{name}: missing {link}'
  if url.fragment and target.endswith('.html'):assert url.fragment in pages[target].ids,f'{name}: missing anchor {link}'
pubs=json.loads((ROOT/'data/publications.json').read_text());projects=json.loads((ROOT/'data/projects.json').read_text())
assert len(pubs)==len({p['id'] for p in pubs})
dois=[p['doi'].lower() for p in pubs if p['doi']];assert len(dois)==len(set(dois))
assert len(projects)==12 and len(pages)==20
scholar=json.loads((ROOT/'research/scholar.json').read_text())
urls={s['url'] for p in pubs for s in p['sources']}
assert all(r['scholar_url'] in urls for r in scholar),'Scholar source entry omitted'
assert not list(OUT.rglob('*.pdf')),'Original unredacted CV must not be deployed'
assert not list(OUT.rglob('.env*'))
assert (OUT/'publications.bib').read_text().count('\n@')+1==len(pubs)
print(f'PASS: {len(pages)} pages, all internal links/anchors, 100 Scholar records accounted for, {len(pubs)} unique works, {len(dois)} unique DOIs, no raw CV or secrets.')
