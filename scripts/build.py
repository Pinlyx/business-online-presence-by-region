import json,csv,match
A={'Catalunya':'Cataluña','Euskadi':'País Vasco'}
def r1(x): return round(x,1)
def areas_from(regf,popf=None,code_key=None,alias=None,merge=None):
    d=match.load(regf); ar=d['areas']
    if merge:
        for src,dst in merge.items():
            s=[a for a in ar if a['name']==src]; t=[a for a in ar if a['name']==dst]
            if s and t:
                for k in ('places','web','ig'): t[0][k]+=s[0][k]
                ar=[a for a in ar if a['name']!=src]
    pop={}
    if popf:
        P=list(csv.DictReader(open(popf,encoding='utf-8')))
        if code_key=='ch':
            byc={p['code']:p for p in P}; pop={a['name']:byc.get(a['code'].split('-')[-1]) for a in ar}
        else:
            for a in ar:
                if alias and a['name'] in alias: a2=dict(a,name=alias[a['name']])
                else: a2=a
                m,_=match.match([a2],P); pop[a['name']]=m.get(a2['name'])
    out=[]
    for a in ar:
        p=pop.get(a['name'])
        row=dict(name=a['name'],places=a['places'],website_pct=r1(100*a['web']/a['places']),instagram_pct=round(100*a['ig']/a['places'],2))
        if p:
            n=int(p['population']); row.update(official_name=p['name'],official_code=p['code'],population=n,population_year=int(p['year']),
              places_per_1000=r1(1000*a['places']/n),websites_per_1000=r1(1000*a['web']/n))
        out.append(row)
    out.sort(key=lambda r:-r['places'])
    return dict(total=d['total'],matched=sum(r['places'] for r in out),areas=out)
def at_pop():
    rows=[l.split(';') for l in open('off/at_pop.csv',encoding='utf-8').read().splitlines()[1:]]
    with open('off/at_pop_std.csv','w',encoding='utf-8',newline='') as f:
        w=csv.writer(f); w.writerow(['code','name','population','year'])
        for r in rows:
            if r[5]=='2023': w.writerow([r[2],r[7],int(float(r[8].replace(',','.'))),2023])
at_pop()
S=json.load(open('stats_all.json'))
countries=[dict(country=cc,places=v['n'],website_pct=r1(100*v['web']),any_social_pct=r1(100*v['social']),facebook_pct=r1(100*v['fb']),
  instagram_pct=round(100*v['ig'],2),x_pct=round(100*v['x'],2),phone_pct=r1(100*v['phone']),email_pct=r1(100*v['email']),
  whatsapp_pct=round(100*v['wa'],2)) for cc,v in S.items()]
countries.sort(key=lambda r:-r['places'])
regions={
 'AT':dict(level='Bundesland',**areas_from('reg_AT_region.json','off/at_pop_std.csv')),
 'CH':dict(level='Kanton',**areas_from('reg_CH_region.json','off/ch_pop.csv',code_key='ch')),
 'ES':dict(level='provincia',**areas_from('reg_ES_county.json','off/es_pop.csv')),
 'ES_CCAA':dict(level='comunidad autónoma',**areas_from('reg_ES_region.json','off/es_ccaa_pop.csv',alias=A)),
 'FR':dict(level='département',**areas_from('reg_FR_county.json','off/fr_pop.csv',merge={'Métropole de Lyon':'Rhône'})),
 'FR_REG':dict(level='région',**areas_from('reg_FR_region.json','off/fr_region_pop.csv')),
}
for cc,lvl in [('DE','Land'),('MX','estado'),('BR','estado'),('ID','provinsi')]:
    try: regions[cc]=dict(level=lvl,**areas_from(f'reg_{cc}_region.json'))
    except FileNotFoundError: print('missing',cc)
cities={}
for c in ['nyc','toronto','madrid','istanbul','izmir']:
    d=match.load(f'city_{c}.json'); ar=[]
    for a in d['areas']:
        row=dict(name=a['name'],places=a['places'],website_pct=r1(100*a['web']/a['places']),instagram_pct=round(100*a['ig']/a['places'],2))
        if a['population']: row.update(population=a['population'],population_year=int(a['pop_year']),places_per_1000=r1(1000*a['places']/a['population']),websites_per_1000=r1(1000*a['web']/a['population']))
        ar.append(row)
    cities[c]=dict(places=sum(r['places'] for r in ar),areas=ar)
for k,v in regions.items():
    miss=[a['name'] for a in v['areas'] if 'population' not in a]
    print(k,len(v['areas']),'areas',v['matched'],'/',v['total'],'no pop:',miss if k in ('AT','CH','ES','ES_CCAA','FR','FR_REG') else '-')
json.dump(dict(release='2026-11-18.0',countries=countries,regions=regions,cities=cities),open('final.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
