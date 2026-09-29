"""Explicit bibliographic corrections, with field-level provenance links."""
JOURNAL='Revue Roumaine des Sciences Techniques – Série Électrotechnique et Énergétique'
CV='https://upb.ro/wp-content/uploads/2020/01/Enache-B-Lista-lucr%C4%83ri.pdf'
COAUTHOR='https://www.sdie.upb.ro/wp-content/uploads/2025/08/SERITAN-George_LL.pdf'
CONSTANTINESCU='https://www.upit.ro/_document/236175/lista_de_lucrari_constantinescu_luminita_mirela_2022.pdf'
OVERRIDES={
'pub-025':dict(authors='Teodor-Iulian Voicila; George-Calin Seritan; Bogdan-Adrian Enache',venue=JOURNAL,volume='69',issue='3',pages='311–316',doi='10.59277/RRST-EE.2024.69.3.10',date='2024-09-29',url='https://journal.iem.pub.ro/rrst-ee/en/article/view/813',summary='Compares bidirectional DC–DC converter topologies for retired-battery screening using multicriteria analysis and LTspice simulations.'),
'pub-095':dict(title='Power LED Efficiency for Automotive Headlights',authors='Costel-Ciprian Raicu; George-Călin Serițan; Bogdan-Adrian Enache',volume='9',issue='2',pages='107–119',venue='EMERG: Energy. Environment. Efficiency. Resources. Globalization',doi='10.37410/EMERG.2023.2.07',url='https://emerg.ro/files/power-led-efficiency-for-automotive-headlights/',summary='Examines buck–boost driver topologies for automotive LED headlights, comparing electrical efficiency and system flexibility.'),
'pub-015':dict(title='Comparison Study of Top Development Boards in the Context of IoT',authors='George-Călin Serițan; Bogdan-Adrian Enache; Irina Vîlciu; Sorin-Dan Grigorescu; Valeri Mladenov',venue=JOURNAL,volume='67',issue='4',pages='483–486',date='2022-12-22',url='https://journal.iem.pub.ro/rrst-ee/en/article/view/181',summary='Uses multicriteria analysis to compare development boards for Internet of Things applications.'),
'pub-030':dict(title='A LiFePO4 Battery Discharge Simulator for EV Applications — Part 1: Determining the Optimal Circuit Based Battery Model',authors='Bogdan-Adrian Enache; Magdalena Emilia Alexandru; Luminita-Mirela Constantinescu',doi='10.1109/ATEE.2015.7133925',venue='2015 9th International Symposium on Advanced Topics in Electrical Engineering (ATEE)',pages='877–882',publisher='IEEE',url=CONSTANTINESCU),
'pub-076':dict(authors='Bogdan-Adrian Enache; Magdalena Emilia Alexandru; Luminita-Mirela Constantinescu',doi='10.1109/ATEE.2015.7133926',venue='2015 9th International Symposium on Advanced Topics in Electrical Engineering (ATEE)',pages='883–888',publisher='IEEE',url=CONSTANTINESCU),
'pub-rg-2':dict(authors='George-Călin Serițan; Bogdan-Adrian Enache; Sorin-Dan Grigorescu; Sanda Victorinne Pațurcă; Costin Cepișcă; Vasiliki Vita; Radu Porumb; Daniel Ghiculescu',volume='64',issue='2',pages='169–172',url=CV),
'pub-028':dict(authors='Bogdan-Adrian Enache; George-Calin Seritan; Costin Cepisca; Sorin-Dan Grigorescu; Florin-Ciprian Argatu; Felix-Constantin Adochiei; Teodor-Iulian Voicila',volume='65',issue='1–2',pages='71–74',url=COAUTHOR),
'pub-090':dict(authors='Bogdan-Adrian Enache; Cosmin Karl Banica; Geroge Bogdan Ana',volume='9',issue='4',venue='Journal of Electrical Engineering, Electronics, Control and Computer Science',url='https://mail.jeeeccs.net/index.php/journal/article/view/352/0'),
'pub-068':dict(authors='Bogdan-Adrian Enache; Emilian Lefter; Costin Cepisca',venue='Autonomous Vehicles: Intelligent Transport Systems and Smart Technologies',publisher='Nova Science Publishers',url=CV,note='Pagination differs across sources: Google Scholar lists 409–429; the author’s institutional publication list identifies Chapter 15, pp. 323–345. Pagination is left unresolved pending confirmation.'),
}
def apply(works):
 for p in works:
  if p['id'] not in OVERRIDES: continue
  x=OVERRIDES[p['id']]
  p.update({k:v for k,v in x.items() if k not in ('url','note')})
  p['sources'].append({'name':'Publisher / institutional bibliography','url':x['url']})
  p['notes']=[n for n in p['notes'] if not n.startswith(('Bibliographic record from Google Scholar','The source abbreviates'))]
  if x.get('note'):p['notes'].append(x['note'])
  if p['doi'] and not any(s['url']=='https://doi.org/'+p['doi'] for s in p['sources']):p['sources'].append({'name':'DOI','url':'https://doi.org/'+p['doi']})
 works.append(dict(id='pub-institutional-1',title='48 V Network Adoption for Automotive Lighting Systems',authors='Costel-Ciprian Raicu; George-Călin Serițan; Bogdan-Adrian Enache',venue=JOURNAL,year=2021,date='2021',type='Journal article',doi='',volume='66',issue='4',pages='231–236',publisher='',citations='',sources=[{'name':'Institutional bibliography','url':COAUTHOR}],notes=['Additional article identified in an institutional coauthor publication list. The source prints “lightning systems”; the title is rendered as “lighting systems”, consistent with the automotive-lighting context. WOS:000754884700004.']))
