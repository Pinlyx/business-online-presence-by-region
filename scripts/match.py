import json,csv,unicodedata,re,sys
def load(p):
    b=open(p,'rb').read()
    try: return json.loads(b.decode('utf-8'))
    except UnicodeDecodeError: return json.loads(b.decode('cp1252'))
def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z ]',' ',s)
def keys(s):
    out={norm(s).strip()}
    for part in re.split(r'[/,]',s): out.add(norm(part).strip())
    out|={' '.join(sorted(norm(s).split()))}
    return {k for k in out if k}
def match(areas,pop):
    res={};un=[]
    for a in areas:
        ka=keys(a['name']); hit=None
        for p in pop:
            if ka & keys(p['name']): hit=p;break
        if not hit:
            for p in pop:
                if any(x in y or y in x for x in ka for y in keys(p['name']) if len(x)>4 and len(y)>4): hit=p;break
        if hit: res[a['name']]=hit
        else: un.append(a['name'])
    return res,un
if __name__=='__main__':
    reg,popf=sys.argv[1],sys.argv[2]
    d=load(reg); pop=list(csv.DictReader(open(popf,encoding='utf-8')))
    res,un=match(d['areas'],pop)
    print('unmatched areas:',un)
    used={v['code'] for v in res.values()}; print('unused pop:',[p['name'] for p in pop if p['code'] not in used])
    from collections import Counter; print('dupe pop:',[k for k,v in Counter(v['code'] for v in res.values()).items() if v>1])
