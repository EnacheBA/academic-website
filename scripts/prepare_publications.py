import json,re,unicodedata,html
from pathlib import Path
from difflib import SequenceMatcher
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/'research'/name).read_text())
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
rows=read('scholar.json');rg=read('researchgate.json')
matched=read('matched-crossref.json')+[x for x in read('enriched-crossref.json') if isinstance(x,list)]
metadata={x[0]['scholar_url']:x[1] for x in matched if x[0].get('scholar_url')}
# Publisher metadata takes precedence; source variants remain attached for review.
works=[]
for i,r in enumerate(rows):
 p={'id':f'pub-{i+1:03}','title':r['title'],'authors':r['authors'],'venue':r['venue'],'year':int(r['year']) if r['year'] else None,'sources':[{'name':'Google Scholar','url':r['scholar_url']}],'notes':[],'type':'Conference paper' if re.search('Conference|Symposium|Workshop|CAR 2026',r['venue'],re.I) else 'Journal article','citations':r['citations'],'doi':'','date':'','publisher':'','volume':'','issue':'','pages':''}
 m=metadata.get(r['scholar_url'])
 if m:
  p.update({'title':html.unescape(re.sub('<[^>]+>','',' '.join(m.get('title',[])))),'authors':'; '.join(' '.join([a.get('given',''),a.get('family','')]).strip() for a in m.get('author',[])),'venue':'; '.join(m.get('container-title',[])),'doi':m.get('DOI',''),'publisher':m.get('publisher',''),'volume':m.get('volume',''),'issue':m.get('issue',''),'pages':m.get('page',m.get('article-number','')),'type':{'journal-article':'Journal article','proceedings-article':'Conference paper','book-chapter':'Book chapter','posted-content':'Preprint'}.get(m.get('type'),p['type'])})
  date=m.get('published',{}).get('date-parts',[[p['year']]])[0]
  p['date']='-'.join(str(x).zfill(2) for x in date if x is not None)
  if date and date[0]:
   if p['year'] and p['year']!=date[0]:p['notes'].append(f"Google Scholar lists {p['year']}; publisher metadata lists {date[0]}.")
   p['year']=date[0]
  p['sources'].append({'name':'Publisher / DOI','url':'https://doi.org/'+p['doi']})
 # Link ResearchGate profile provenance, matching actual titles without inventing record URLs.
 rs=[q for q in rg if SequenceMatcher(None,norm(q['title']).replace('soc','stateofcharge'),norm(r['title']).replace('soc','stateofcharge')).ratio()>.95]
 if rs:
  p['sources'].append({'name':'ResearchGate profile','url':'https://www.researchgate.net/profile/Bogdan-Adrian-Enache'})
  if not p['year']:p['year']=int(rs[0]['date'][-4:])
  if not m:p['type']={'Article':'Journal article','Chapter':'Book chapter','Conference Paper':'Conference paper','Preprint':'Preprint'}.get(rs[0]['type'],p['type'])
 if not m:p['notes'].append('Bibliographic record from Google Scholar; fields not independently resolved with publisher metadata are retained as listed.')
 if '...' in p['authors']:p['notes'].append('The source abbreviates the author list. Follow the source link for the complete list.')
 works.append(p)
# Source-specific corrections backed by ResearchGate/CV and supplied publisher records.
for p in works:
 t=norm(p['title'])
 if t.startswith('modelingaspectsofanelectricstartersystemforaninternalcombustionengine'):
  p['title']='Modeling aspects of an electric starter system for an internal combustion engine'
  p['authors']='Bogdan-Adrian Enache; Luminita-Mirela Constantinescu; Emilian Lefter'
 if t=='comparativestudyofscreeningmethodsforsecondlifelifepo4batteries':
  p['venue']='Revue Roumaine des Sciences Techniques – Série Électrotechnique et Énergétique';p['volume']='65';p['issue']='1–2';p['pages']='71–74'
 if t.startswith('hybridizationoftrolleybuses'):
  p['authors']='Emilian Lefter; Bogdan-Adrian Enache; Ionuț Bogdan Maria; Cătălin Goia'
 if t.startswith('stateofchargeestimationofalifepo4batteryusinganadaptiveobserver'):
  p['notes'].append('Date discrepancy: Google Scholar lists 2015; ResearchGate lists January 2016. Retained as 2015 pending confirmation.')
 if t.startswith('lowtemperaturecapacityloss'):
  p['notes'].append('Listed on Google Scholar as CAR 2026. Publication status and final proceedings details need confirmation.')
 if t.startswith('smartsystemforstandby'):
  p['notes'].append('English-language title variant of the French-titled household standby-power paper. Combined in this catalogue.')
# Extra works on ResearchGate not represented as separate works on Scholar.
extras=[
 {'title':'A TinyML-Driven Edge Computing Framework for State of Health Estimation of Second-Life Li-Ion Battery','authors':'Efstathios Fiorentis; Bogdan-Adrian Enache; Mihaela-Marilena Albu','year':2026,'date':'2026-01','type':'Preprint','venue':'SSRN','doi':'10.2139/ssrn.6169928','url':'https://www.researchgate.net/publication/400391780_A_TinyML-Driven_Edge_Computing_Framework_for_State_of_Health_Estimation_of_Second-Life_Li-Ion_Battery','summary':'A compact neural-network approach estimates the health of second-life lithium-ion cells from partial-discharge voltages, with an architecture intended for resource-constrained edge devices.'},
 {'title':'Improvement of Teaching Activities in Higher Education: A Case Study','authors':'George-Călin Serițan; Bogdan-Adrian Enache; Sorin-Dan Grigorescu; et al.','year':2019,'date':'2019-06','type':'Journal article','venue':'Revue Roumaine des Sciences Techniques – Série Électrotechnique et Énergétique','doi':'','url':'https://www.researchgate.net/publication/336686566_IMPROVEMENT_OF_TEACHING_ACTIVITIES_IN_HIGHER_EDUCATION_A_CASE_STUDY','summary':'A case study of objective-oriented, web-based engineering laboratory teaching.'}
]
for j,x in enumerate(extras):
 p={**x,'id':f'pub-rg-{j+1}','sources':[{'name':'ResearchGate','url':x['url']}],'notes':[],'publisher':'','volume':'','issue':'','pages':'','citations':''}
 if p['doi']:p['sources'].append({'name':'Publisher / DOI','url':'https://doi.org/'+p['doi']})
 works.append(p)
# Merge exact DOI/title duplicates and two established source variants; never add citation counts.
unique=[]
for p in works:
 t=norm(p['title']);existing=None
 for u in unique:
  same=(p['doi'] and p['doi'].lower()==u['doi'].lower()) or t==norm(u['title'])
  translation=(t.startswith('smartsystemforstandby') and norm(u['title']).startswith('systemeintelligentpourlareduction'))
  if same or translation:existing=u;break
 if existing:
  existing['sources'] += [s for s in p['sources'] if s not in existing['sources']]
  existing['notes'].append('Duplicate or alternate profile entry combined; source links retained. Citation counts are not summed.')
  if '...' in existing['venue'] or '…' in existing['venue']:
   if '…' not in p['venue']:existing['venue']=p['venue']
  if t.startswith('smartsystemforstandby'):existing['alternate_title']=p['title']
 else:unique.append(p)
from curated_metadata import apply
apply(unique)
# Attach topic tags based on titles, solely for navigation.
for p in unique:
 t=p['title'].lower()
 p['topics']=[]
 for label,pattern in [('Batteries & energy storage',r'batter|lifepo|lfp|lco|state.of.charge|state.of.health'),('Power systems & resilience',r'grid|power|transformer|voltage|photovoltaic|pv |solar|trolley|generator|alternator|electric|energy|rectifier|converter'),('Sensors, IoT & signal processing',r'iot|sensor|monitor|signal|eeg|ecg|electrocardio|stethoscope|wireless|mqtt|websocket|scada|weather|stress|alzheimer|brain'),('Robotics & mobility',r'robot|vehicle|automotive|headlight|path planning|scooter'),('Education & computing',r'teach|didactic|compiler|language|learning|devops|logistics')]:
  if re.search(pattern,t):p['topics'].append(label)
 if not p['topics']:p['topics']=['Applied engineering']
unique.sort(key=lambda p:(-(p['year'] or 0),p['title'].lower()))
(ROOT/'data/publications.json').write_text(json.dumps(unique,ensure_ascii=False,indent=2))
# Supplementary upload retained explicitly, without calling it an extra paper.
(ROOT/'data/supplementary.json').write_text(json.dumps([{'title':'Chapter — supplementary ResearchGate upload','date':'January 2015','authors':'Bogdan-Adrian Enache; Emilian Lefter; Costin Cepisca','type':'Data / supplementary upload','url':'https://www.researchgate.net/publication/271521697_Chapter','note':'ResearchGate labels this upload “Data”. Its description corresponds to Batteries for Electrical Vehicles: A Review. It is preserved here separately and is not counted as an additional paper.'}],ensure_ascii=False,indent=2))
print(len(unique),'distinct works; DOI records',sum(bool(p['doi']) for p in unique),'full authors',sum('...' not in p['authors'] and 'et al.' not in p['authors'] for p in unique))
print('Missing DOI:',json.dumps([p['title'] for p in unique if not p['doi']],ensure_ascii=False))
