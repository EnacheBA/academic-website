#!/usr/bin/env python3
"""Build a dependency-free static website from the reviewed JSON catalogue."""
from pathlib import Path
from html import escape as e
from collections import Counter
import json,shutil,re
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'dist'; OUT.mkdir(exist_ok=True)
P=json.loads((ROOT/'data/publications.json').read_text()); PROJECTS=json.loads((ROOT/'data/projects.json').read_text()); C=json.loads((ROOT/'data/career.json').read_text())
SCHOLAR='https://scholar.google.com/citations?user=MZdHJ7MAAAAJ&hl=en'; RG='https://www.researchgate.net/profile/Bogdan-Adrian-Enache'; ORCID='https://orcid.org/0000-0001-9979-3837'; EMAIL='bogdan.enache2207@upb.ro'
DATE='29 September 2026'
for file in ['styles.css','app.js']:shutil.copy2(ROOT/file,OUT/file)
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
(OUT/'data').mkdir(exist_ok=True)
for name in ['publications.json','projects.json','career.json','supplementary.json']:shutil.copy2(ROOT/'data'/name,OUT/'data'/name)
(OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(OUT/'.nojekyll').touch()

def link(url,text,cls='',external=False):
 return f'<a href="{e(url,quote=True)}"'+(f' class="{cls}"' if cls else '')+(' target="_blank" rel="noopener noreferrer"' if external else '')+f'>{text}</a>'
def profiles():return f'<div class="profile-links">{link(SCHOLAR,"Google Scholar",external=True)}{link(RG,"ResearchGate",external=True)}{link(ORCID,"ORCID",external=True)}</div>'
def head(title,active,body,description='',bodyclass=''):
 nav=''.join(f'<a href="{name}.html"'+(' aria-current="page"' if active==name else '')+f'>{label}</a>' for name,label in [('index','Overview'),('research','Research'),('publications','Publications'),('teaching','Teaching'),('about','About'),('contact','Contact')])
 return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Bogdan-Adrian Enache</title><meta name="description" content="{e(description or 'Academic profile, research projects, publications and teaching of Bogdan-Adrian Enache, Associate Professor at POLITEHNICA Bucharest.',quote=True)}"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#142f40"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><script src="app.js" defer></script></head><body class="{bodyclass}"><a class="skip" href="#main">Skip to content</a><div class="review-strip"><span>PRIVATE REVIEW · SEPTEMBER 2026</span><a href="review.html">Review notes</a></div><header class="header"><div class="wrap header-inner"><a class="brand" href="index.html"><span class="monogram">BE</span><span class="brand-name">Bogdan-Adrian Enache<small>Research &amp; academic profile</small></span></a><button class="menu-toggle" aria-controls="main-nav" aria-expanded="false">Menu</button><nav class="nav" id="main-nav" aria-label="Main navigation">{nav}</nav></div></header><main id="main">{body}</main><footer class="footer"><div class="wrap"><div class="footer-top"><div><strong>Bogdan-Adrian Enache</strong><br>Electrical engineering · POLITEHNICA Bucharest</div><nav aria-label="Academic profiles">{link(SCHOLAR,'Google Scholar',external=True)}{link(RG,'ResearchGate',external=True)}{link(ORCID,'ORCID',external=True)}{link('cv.html','Academic CV')}</nav></div><div class="footer-bottom"><span>© 2026 Bogdan-Adrian Enache · Bucharest, Romania</span><span>{link('review.html','Sources & review notes')} · Compiled {DATE}</span></div></div></footer></body></html>'''
def write(name,title,active,body,**kw):(OUT/name).write_text(head(title,active,body,**kw))
def intro(label,title,lead,extra=''):
 return f'<div class="wrap page-intro"><p class="eyebrow">{label}</p><h1>{title}</h1><p class="lead">{lead}</p>{extra}</div>'
def section_heading(label,title,right=''):
 return f'<div class="section-head"><div><p class="eyebrow">{label}</p><h2>{title}</h2></div>{right}</div>'
def citation(p):
 venue=p['venue']; parts=[]
 if p.get('volume'):parts.append('Volume '+str(p['volume']))
 if p.get('issue'):parts.append('Issue '+str(p['issue']))
 if p.get('pages'):parts.append('pp. / article '+str(p['pages']))
 return venue+(' · '+' · '.join(parts) if parts else '')
def pubrow(p,details=True):
 url='https://doi.org/'+p['doi'] if p['doi'] else p['sources'][0]['url']
 attrs=f'data-search="{e(p["title"]+" "+p["authors"]+" "+p["venue"]+" "+p["doi"],quote=True)}" data-year="{p["year"] or ""}" data-type="{e(p["type"],quote=True)}" data-topic="{e("|".join(p["topics"]),quote=True)}"'
 actions=link(url,'DOI / publisher' if p['doi'] else 'Source record',external=True)
 actions+=' '+link('publications.bib','Full BibTeX catalogue') if not details else ''
 inner=''
 if details:
  fields=[('Authors',p['authors']),('Publication',p['venue']),('Date',p['date'] or str(p['year'] or 'Not listed')),('Publisher',p.get('publisher')),('Volume',p.get('volume')),('Issue',p.get('issue')),('Pages / article',p.get('pages')),('DOI',p.get('doi'))]
  dl=''.join(f'<dt>{e(k)}:</dt><dd>{e(str(v))}</dd>' for k,v in fields if v)
  summary=f'<p>{e(p["summary"])}</p>' if p.get('summary') else ''
  source_links=' · '.join(link(s['url'],e(s['name']),external=True) for s in p['sources'])
  notes=''.join(f'<p><small>{e(n)}</small></p>' for n in dict.fromkeys(p['notes']))
  tags=''.join(f'<span class="tag">{e(t)}</span>' for t in p['topics'])
  inner=f'<details class="pub-detail"><summary>Bibliographic details &amp; sources</summary><div class="pub-detail-body">{summary}<dl>{dl}</dl><p>{tags}</p><p>{source_links}</p>{notes}</div></details>'
 return f'<article class="pub-row" id="{p["id"]}" {attrs}><div class="pub-year">{p["year"] or "—"}</div><div><div class="pub-meta">{e(p["type"])}</div><h3>{link(url,e(p["title"]),external=True)}</h3><p class="pub-authors">{e(p["authors"])}</p><p class="pub-venue">{e(citation(p))}</p><div class="pub-actions">{actions}</div>{inner}</div></article>'
def projectfeature(p):
 return f'<article class="project-feature"><a class="name" href="project-{p["id"]}.html">{e(p["name"])}</a><div><h3>{e(p["summary"])}</h3><p>{e(p["funding"])}</p></div><div class="role"><strong>{e(p["role"])}</strong><small>{e(p["period"])}</small></div></article>'
hero=f'''<div class="wrap"><section class="hero"><div><p class="eyebrow">Electrical engineering · Research · Education</p><h1>Bogdan-Adrian<br>Enache</h1><p class="position">Associate Professor, PhD · IEEE Senior Member</p><p class="lead">Connecting electrical measurements, intelligent systems and sustainable energy.</p><p>National University of Science and Technology<br><strong>POLITEHNICA Bucharest</strong></p><div class="buttons">{link('research.html','Explore research','button')}{link('publications.html','View publications','button secondary')}</div>{profiles()}</div><div class="hero-portrait"><figure><img src="assets/portrait.jpg" alt="Portrait of Bogdan-Adrian Enache" width="1297" height="1491" fetchpriority="high"><figcaption class="portrait-caption"><span>BOGDAN-ADRIAN ENACHE</span><span>BUCHAREST, RO</span></figcaption></figure></div></section><div class="metrics"><div class="metric"><strong>{len(P)}</strong><span>Research outputs catalogued</span></div><div class="metric"><strong>12</strong><span>Research project appointments</span></div><div class="metric"><strong>4</strong><span>Project-director appointments</span></div><div class="metric"><strong>14</strong><span>Google Scholar h-index</span></div></div><p class="metric-note">Catalogue combines profile records and merges duplicate entries. Google Scholar metrics observed {DATE}.</p></div>'''
themes='''<div class="themes"><article class="theme"><span class="num">01 / ENERGY</span><h3>Batteries &amp;<br>sustainable energy</h3><p>Battery modelling, state-of-charge and state-of-health estimation, second-life screening, power conversion and renewable integration.</p><a href="research.html#projects">Energy research projects</a></article><article class="theme"><span class="num">02 / INTELLIGENCE</span><h3>Measurements &amp;<br>intelligent systems</h3><p>Signal processing, virtual instrumentation, connected sensors and data-driven methods for electrical and biomedical applications.</p><a href="publications.html">Explore the publications</a></article><article class="theme"><span class="num">03 / MATHEMATICS &amp; STATISTICS</span><h3>Mathematical modelling &amp;<br>statistical analysis</h3><p>Mathematical modelling, statistical analysis and predictive methods for electrical measurements, battery behaviour and social-service impact assessment.</p><a href="project-evosst.html">Current work in EVOSST</a></article></div>'''
selected=[]
for term in ['Enhanced OCV','High-Speed SMVs','Flexibility Market']:
 found=next((p for p in P if term.lower() in p['title'].lower()),None)
 if found:selected.append(found)
body=hero+f'<section class="section"><div class="wrap">{section_heading("Research interests","From measurement to meaningful decisions.")}{themes}</div></section>'
body+=f'<section class="section dark-section"><div class="wrap">{section_heading("Research in practice","Leadership & collaboration",link("research.html","All 12 project appointments","text-link"))}{"".join(projectfeature(next(p for p in PROJECTS if p["id"]==i)) for i in ["evosst","smartelter","electron"])}</div></section>'
body+=f'<section class="section"><div class="wrap">{section_heading("Selected publications","A closer look at the research",link("publications.html","Complete publication catalogue","text-link"))}<div class="pub-list">{"".join(pubrow(p,False) for p in selected)}</div></div></section>'
body+='<section class="wrap section"><div class="callout"><div><p class="eyebrow">Teaching & academic practice</p><h2>Bringing research into the laboratory.</h2><p>Signal processing, electrical measurements and virtual instrumentation.</p></div><div class="buttons">'+link('teaching.html','Teaching profile','button secondary')+'</div></div></section>'
write('index.html','Academic & Research','index',body)

# Research index and all detailed project records.
body=intro('Research portfolio','Research that connects<br>systems, data and people.','Project leadership and research collaboration across battery storage, resilient power networks, renewable energy and applied data science.')
body+='<section class="wrap section"><div class="research-flow" aria-label="Research approach"><div><p class="eyebrow">01 / Observe</p><strong>Measure & characterise</strong><span>Electrical signals, battery behaviour and operating conditions.</span></div><div><p class="eyebrow">02 / Understand</p><strong>Model & interpret</strong><span>Physical models, statistical analysis and machine learning.</span></div><div><p class="eyebrow">03 / Apply</p><strong>Control & evaluate</strong><span>Energy systems, smart infrastructure and decision support.</span></div></div></section>'
body+='<section class="wrap section" id="projects">'+section_heading('Project appointments','The complete project portfolio')+'<p class="figure-note">Dates below describe personal participation. Detailed records identify consortium dates and budgets separately.</p><div class="project-grid">'
for p in PROJECTS:
 body+=f'<article class="project-card {"director" if p["role"]=="Project Director" else ""}"><p class="eyebrow">{e(p["category"])}</p><h2>{link("project-"+p["id"]+".html",e(p["name"]))}</h2><h3>{e(p["summary"])}</h3><p>{e(p["institution"])}</p><div class="project-meta"><strong>{e(p["role"])}</strong><span>{e(p["period"])}</span></div>{link("project-"+p["id"]+".html","Project details","text-link")}</article>'
body+='</div></section>';write('research.html','Research projects','research',body)
for p in PROJECTS:
 body='<div class="wrap breadcrumb">'+link('research.html','Research projects')+' / '+e(p['name'])+'</div>'
 body+=intro(e(p['category']),e(p['name']),e(p['title']))
 details=''.join('<li>'+e(x)+'</li>' for x in p['details'])
 contributions=''.join('<li>'+e(x)+'</li>' for x in p['contributions'])
 facts=[('Appointment',p['role']),('Participation',p['period']),('Institution',p['institution']),('Funding',p['funding']),('Grant / project ID',p['grant']),('Consortium duration',p.get('programmeDates','')),('Budget',p.get('budget',''))]
 dl=''.join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k,v in facts if v)
 sources=link('cv.html','Professional CV record')+((' · '+link(p['url'],'Official project / institutional source',external=True)) if p['url'] else '')
 body+=f'<section class="wrap section project-detail"><div class="prose"><h2>Project overview</h2><p>{e(p["description"])}</p><h2>My role &amp; contribution</h2><ul>{contributions}</ul><h2>Project context</h2><ul>{details}</ul><h2>Sources</h2><p>{sources}</p><p class="figure-note">Role and participation dates: supplied Europass CV. Additional consortium information: linked official source, where available.</p></div><aside class="fact-panel" aria-label="Project facts"><dl>{dl}</dl></aside></section>'
 body+='<div class="wrap section">'+link('research.html','Back to all projects','button secondary')+'</div>'
 write('project-'+p['id']+'.html',p['name'],'research',body)

# Full bibliography with progressive enhancement: records remain readable without JavaScript.
counts=Counter(p['year'] for p in P if p['year']);maxcount=max(counts.values());chart=''
for yr in sorted(counts):chart+=f'<div class="bar-wrap"><span class="bar-count">{counts[yr]}</span><div class="bar" style="height:{counts[yr]/maxcount*105:.1f}px" aria-hidden="true"></div><span class="bar-label">{yr}</span></div>'
body=intro('Publication catalogue','Publications & research outputs',f'{len(P)} catalogue records spanning journal articles, conference papers, book chapters and a preprint. Reconciled from Google Scholar and ResearchGate, with publisher metadata where available.',profiles()+'<div class="buttons">'+link('publications.bib','Download BibTeX','button secondary')+link('data/publications.json','Download catalogue data','button secondary')+'</div>')
body+=f'<section class="wrap"><figure style="margin:0"><div class="bar-chart" role="img" aria-label="Catalogue records by year: {e(", ".join(str(y)+": "+str(counts[y]) for y in sorted(counts)))}">{chart}</div><figcaption class="figure-note">Outputs by publication year in this catalogue · Google Scholar: 642 citations, h-index 14, i10-index 23, observed {DATE}.</figcaption></figure>'
options=lambda vals:'<option value="">All</option>'+''.join(f'<option value="{e(str(v),quote=True)}">{e(str(v))}</option>' for v in vals)
body+=f'<form class="filters" data-filter-form><label class="search-field">Search publications<input type="search" placeholder="Title, author, journal or DOI" aria-label="Search publications"></label><label>Year<select name="year" aria-label="Filter by year">{options(sorted(counts,reverse=True))}</select></label><label>Type<select name="type" aria-label="Filter by publication type">{options(sorted(set(p["type"] for p in P)))}</select></label><label>Research area<select name="topic" aria-label="Filter by research area">{options(sorted(set(t for p in P for t in p["topics"])))}</select></label></form><div class="filter-count"><span data-result-count role="status" aria-live="polite">{len(P)} of {len(P)} publications</span><a href="review.html#bibliography">About this catalogue</a></div><div class="pub-list">{"".join(pubrow(p) for p in P)}</div><div class="empty" data-empty hidden><h2>No matching publications</h2><p>Try another title, author or filter.</p><button class="button secondary" data-reset>Clear filters</button></div></section>'
body+='<section class="wrap section"><h2>Supplementary profile material</h2><p>ResearchGate also lists a January 2015 upload titled “Chapter”, associated with <em>Batteries for Electrical Vehicles: A Review</em>. It is retained as supplementary material and is not counted as a separate paper.</p>'+link('https://www.researchgate.net/publication/271521697_Chapter','View supplementary ResearchGate record','text-link',True)+'</section>'
write('publications.html','Publications','publications',body)

# Career and education.
def timeline(items):
 return ''.join(f'<article class="timeline-row"><div class="date">{e(date)}</div><div><h3>{e(title)}</h3><p class="org">{e(org)}</p><p>{e(text)}</p></div></article>' for date,title,org,text in items)
def affiliations():
 items=[]
 for name,description in C['affiliations']:
  societies=''
  if name=='IEEE':
   societies='<p class="society-label">Society memberships</p><ul class="society-list">'+''.join('<li>'+e(society)+'</li>' for society in C['ieeeSocieties'])+'</ul>'
  items.append(f'<div><strong>{e(name)}</strong><span>{e(description)}</span>{societies}</div>')
 return '<div class="affiliations">'+''.join(items)+'</div>'

body=intro('Biography & experience','An engineering career,<br>grounded in measurement.','Associate Professor in the Department of Measurements, Electrical Apparatus and Static Converters at POLITEHNICA Bucharest.', '<div class="buttons">'+link('cv.html','View academic CV','button secondary')+'</div>')
body+='<section class="wrap section two-col"><div><h2>Research, teaching<br>and applied engineering.</h2></div><div class="prose"><p>My work connects electrical engineering with experimental measurement, signal processing and data analysis. Research interests include battery modelling, energy-storage diagnostics, power conversion, electrical-grid resilience and intelligent monitoring.</p><p>Alongside university research and teaching, my professional experience includes utility-network design, engineering-team leadership and the management of industrial R&D projects. Since February 2025, my work in EVOSST also applies predictive analytics to the long-term impact of social services.</p></div></section>'
for label,title,key in [('Academic career','University appointments','appointments'),('Professional practice','Industry experience','industry'),('Education & training','A foundation in electrical engineering','education')]:body+='<section class="wrap section">'+section_heading(label,title)+timeline(C[key])+'</section>'
body+='<section class="wrap section">'+section_heading('Professional community','Memberships & qualifications')+affiliations()+'<p style="margin-top:30px">'+e(C['languages'])+'</p></section>'
write('about.html','About & experience','about',body)

# Teaching content only from documented appointments; no invented course downloads.
body=intro('Teaching & mentoring','Learning through signals,<br>instruments and experiments.','Teaching experience across electrical measurements, signal processing, virtual instrumentation and automotive electrical systems.')
body+='<section class="wrap section">'+section_heading('POLITEHNICA Bucharest','Current teaching')+'<div class="course-list">'
for title,kind,desc in [('Signal Processing','Course · Associate Professor appointment','Delivery of the Signal Processing course, connecting mathematical methods with the analysis of measured signals.'),('Electrical Measurement','Laboratory teaching','Laboratory instruction in electrical measurement and practical measurement methods.'),('Electrical & Electronic Measurements','Laboratory teaching','Practical instruction in electrical and electronic measurement techniques.'),('Virtual Instrumentation','Laboratory teaching','Laboratory instruction in computer-based instrumentation and measurement systems.')]:
 body+=f'<article class="course"><small>{kind}</small><h3>{title}</h3><p>{desc}</p></article>'
body+='</div></section><section class="wrap section">'+section_heading('Teaching experience','Earlier courses & laboratories')+timeline(C['appointments'][1:])+'</section>'
body+='<section class="wrap section">'+section_heading('Education research','Teaching as a research practice')+'<div class="pub-list">'+''.join(pubrow(p,False) for p in P if any(s in p['title'].lower() for s in ['teaching activities','didactic implementation']))+'</div></section>'
body+='<section class="wrap section"><div class="callout"><div><h2>Academic enquiries</h2><p>For course information and research discussions, use the university email.</p></div>'+link('mailto:'+EMAIL,'Contact by email','button secondary')+'</div></section>'
write('teaching.html','Teaching','teaching',body)

body=intro('Contact & academic profiles','Let’s connect.','For research collaboration, academic discussions and teaching enquiries.')
body+='<section class="wrap section contact-grid"><div><div class="contact-card"><h2>University contact</h2><p>'+link('mailto:'+EMAIL,EMAIL)+'</p><p>Department of Measurements, Electrical Apparatus and Static Converters<br>National University of Science and Technology POLITEHNICA Bucharest<br>Bucharest, Romania</p></div><div class="contact-card"><h2>Professional profile</h2><p>Associate Professor, PhD<br>IEEE Senior Member · Region 8, Romania</p>'+link('cv.html','View academic CV','text-link')+'</div></div><div><div class="contact-card"><h2>Research profiles</h2><p>'+link(SCHOLAR,'Google Scholar',external=True)+'<br>'+link(RG,'ResearchGate',external=True)+'<br>'+link(ORCID,'ORCID · 0000-0001-9979-3837',external=True)+'</p></div><div class="contact-card"><h2>Areas of interest</h2><p>Battery diagnostics and second-life storage; electrical measurement and signal processing; grid resilience and renewable integration; applied data science and connected monitoring.</p></div></div></section>'
write('contact.html','Contact','contact',body)

body=intro('Academic curriculum vitae','Bogdan-Adrian Enache','Associate Professor, PhD · IEEE Senior Member',f'<p class="cv-contact">POLITEHNICA Bucharest · {EMAIL}<br>ORCID: 0000-0001-9979-3837 · Compiled {DATE}</p><div class="buttons"><button class="button" data-print>Print / save as PDF</button>{link("about.html","Return to website","button secondary")}</div>')
for label,title,key in [('','Academic appointments','appointments'),('','Professional experience','industry'),('','Education & training','education')]:body+='<section class="wrap section">'+section_heading(label,title)+timeline(C[key])+'</section>'
body+='<section class="wrap section"><h2>Research projects</h2>'+timeline([(p['period'],p['role']+' · '+p['name'],p['institution'],p['title']+('. Grant: '+p['grant'] if p['grant'] else '')) for p in PROJECTS])+'</section>'
body+='<section class="wrap section"><h2>Memberships & qualifications</h2>'+affiliations()+'<p style="margin-top:24px">'+e(C['languages'])+'</p><h2>Publications</h2><p>'+str(len(P))+' distinct catalogue records. Full bibliography available in the website’s Publications section.</p>'+link('publications.html','Full publication catalogue')+'</section>'
write('cv.html','Academic CV','about',body,bodyclass='cv-page')

# Review notes are intentionally part of the owner-only review, and explain unresolved provenance.
body=intro('Owner review','Sources, scope & review notes','A transparent record of what was included, how records were reconciled, and the small number of details that still need your confirmation.')
body+='<section class="wrap section prose"><h2>Source material</h2><ul><li>Your supplied four-page Europass CV and portrait, with subsequent owner-confirmed updates to the ANRE authorisation, IEEE membership and society affiliations, and language profile.</li><li>'+link('https://chatgpt.com/share/6abb9bd1-84b0-83ed-b1d3-cd7fbd09fa83','Shared conversation',external=True)+'.</li><li>'+link(SCHOLAR,'Google Scholar profile',external=True)+' — 100 records collected.</li><li>'+link(RG,'ResearchGate profile',external=True)+' — 91 entries in the accessible indexed profile snapshot.</li><li>'+link(ORCID,'ORCID public record',external=True)+' and publisher-deposited Crossref metadata for bibliographic cross-checking.</li><li>CORDIS official factsheets for EVOSST, ELECTRON, FARCROSS and FLEXITRANSTORE.</li></ul><h2 id="bibliography">Bibliography coverage</h2><p>All 100 collected Scholar entries and all 91 ResearchGate entries were considered. Duplicates and confirmed alternate titles were combined, while a ResearchGate-only preprint and the separate teaching case study were included. One additional automotive-lighting article was located in an institutional coauthor bibliography. A generic “Chapter” upload is preserved as supplementary material. The catalogue contains '+str(len(P))+' distinct records, including a preprint and a CAR 2026 record whose publication status needs confirmation.</p><p>Records contain author lists, venues, years, and volume, issue, pagination, publisher and DOI information when available. Unresolved information is identified in each record’s details. The archive is a dated snapshot, not a live synchronisation; newly added or privately listed papers may not be represented.</p>'
notes=[('EVOSST funding programme','The supplied CV says H2020; the official European Commission record identifies Horizon Europe. This website uses Horizon Europe.'),('Three 2013 research assignments','The CV gives March–June 2013 for all three PN-II-PT-PCCA-2013-4 assignments. These dates are preserved, with a note asking for confirmation.'),('Adaptive-observer battery paper','Google Scholar lists 2015; ResearchGate lists January 2016. The catalogue preserves 2015 pending confirmation.'),('CAR 2026 battery-capacity record','The low-temperature LCO/LFP capacity-loss paper is included as listed on Scholar. Final proceedings information and publication status remain to be confirmed.'),('Source duplicates and date differences','The 2018 teaching paper, electric-starter paper, digital-stethoscope chapter and English/French standby-power title variants are combined. Publisher dates are preferred when available, with conflicting source dates retained in the notes.'),('Battery review chapter pagination','Google Scholar and the institutional publication list give different page ranges for Batteries for Electrical Vehicles: A Review. Both are recorded in the catalogue for confirmation.'),('Privacy and review','The website uses your academic email and professional experience. Your home address, personal telephone number, birth date and family details are not included. The original unredacted CV is not distributed with the site.'),('GitHub and private review','The source repository is intended to remain private. The review site uses owner-only access. A noindex tag or a private repository alone does not make a deployed website private.'),('Updates','The publication data are editable JSON files, with a reproducible static build. No recurring synchronisation or automatic public deployment has been enabled.')]
for title,text in notes:body+=f'<div class="review-note"><h3>{e(title)}</h3><p>{e(text)}</p></div>'
body+='<h2>Scope of project descriptions</h2><p>Personal roles and participation dates come from the supplied CV. Official consortium objectives, durations and budgets are shown separately. No unpublished results, unverified deliverables, individual leadership claims or project photographs were invented.</p></section>'
write('review.html','Review notes','',body)

# BibTeX uses the same records shown on the website.
def bibescape(s):return str(s).replace('\\','\\textbackslash{}').replace('&','\\&').replace('%','\\%').replace('_','\\_').replace('#','\\#').replace('{','\\{').replace('}','\\}')
bib=[]
for p in P:
 typ={'Journal article':'article','Conference paper':'inproceedings','Book chapter':'incollection','Preprint':'misc'}.get(p['type'],'misc')
 fields={'title':p['title'],'author':re.sub(r'(?:; |, )', ' and ', p['authors']).replace('...', 'others').replace('et al.', 'others'),'year':p['year'],'journal' if typ=='article' else 'booktitle':p['venue'],'volume':p['volume'],'number':p['issue'],'pages':p['pages'],'publisher':p['publisher'],'doi':p['doi'],'url':'https://doi.org/'+p['doi'] if p['doi'] else p['sources'][0]['url']}
 bib.append('@'+typ+'{'+p['id']+',\n'+',\n'.join('  '+k+' = {'+bibescape(v)+'}' for k,v in fields.items() if v)+'\n}')
(OUT/'publications.bib').write_text('\n\n'.join(bib)+'\n')
print(f'Built {len(list(OUT.glob("*.html")))} pages with {len(P)} publication records and {len(PROJECTS)} project appointments.')
