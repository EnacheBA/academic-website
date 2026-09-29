import json,re,time,unicodedata,concurrent.futures,urllib.parse,urllib.request
from pathlib import Path
from difflib import SequenceMatcher
ROOT=Path(__file__).resolve().parents[1]
norm=lambda x:re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',x).encode('ascii','ignore').decode().lower())
sch=json.loads((ROOT/'research/scholar.json').read_text())
matched=json.loads((ROOT/'research/matched-crossref.json').read_text())
seen={x[0]['scholar_url'] for x in matched}
todo=[x for x in sch if x['scholar_url'] not in seen]
todo += [{'title':'A TinyML-Driven Edge Computing Framework for State of Health Estimation of Second-Life Li-Ion Battery','scholar_url':''},{'title':'Improvement of teaching activities in higher education: a case study','scholar_url':''}]
def fetch(p):
 url='https://api.crossref.org/works?'+urllib.parse.urlencode({'query.bibliographic':p['title'],'rows':3})
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'AcademicPortfolioMetadata/1.0'})
  data=json.load(urllib.request.urlopen(req,timeout=25))['message']['items']
  out=[]
  for x in data:
   score=SequenceMatcher(None,norm(p['title']),norm(' '.join(x.get('title',[])))).ratio()
   if score>.9 and any('enache' in a.get('family','').lower() for a in x.get('author',[])):
    out.append((p,x,score))
  return max(out,key=lambda z:z[2]) if out else None
 except Exception as e:return {'title':p['title'],'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(fetch,todo))
(ROOT/'research/enriched-crossref.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('Additional matches',sum(isinstance(x,list) or isinstance(x,tuple) for x in results),'of',len(todo),flush=True)
