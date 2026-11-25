import duckdb,sys,json,csv,time
c=duckdb.connect(); c.sql("LOAD spatial; SET threads=4")
city,src=sys.argv[1],sys.argv[2]
t=time.time()
if city=='istanbul':
    c.sql("CREATE TABLE a AS SELECT nm AS name, nm AS code, ST_GeomFromWKB(wkb) g FROM 'divisions.parquet' WHERE country='TR' AND subtype='county' AND region='TR-34'")
else:
    c.sql(f"CREATE TABLE a AS SELECT CAST(code AS VARCHAR) code, name, geom g FROM ST_Read('off/{city}_areas.geojson')")
x0,y0,x1,y1=c.sql("SELECT ST_XMin(ST_Extent_Agg(g)),ST_YMin(ST_Extent_Agg(g)),ST_XMax(ST_Extent_Agg(g)),ST_YMax(ST_Extent_Agg(g)) FROM a").fetchone()
c.sql(f"""CREATE TABLE p AS SELECT ST_Point(lon,lat) g, len(coalesce(websites,[]))>0 web,
  list_has_any(list_transform(list_transform(coalesce(socials,[]),s->lower(s)), s->s LIKE '%instagram.com%'),[true]) ig
  FROM '{src}.parquet' WHERE coalesce(operating_status,'open')='open' AND lon BETWEEN {x0} AND {x1} AND lat BETWEEN {y0} AND {y1}""")
r=c.sql("SELECT a.code,a.name,count(*) n,sum(web::int) w,sum(ig::int) ig FROM p JOIN a ON ST_Contains(a.g,p.g) GROUP BY ALL").fetchall()
pop={}
for row in csv.DictReader(open(f'off/{city}_pop.csv',encoding='utf-8')): pop[row['name'] if city=='istanbul' else row['code']]=row
out=[]
for code,name,n,w,ig in r:
    pr=pop.get(code); 
    out.append(dict(code=code,name=name,places=n,web=w,ig=ig,population=int(pr['population']) if pr else None,pop_year=pr['year'] if pr else None))
miss=[o['name'] for o in out if o['population'] is None]
json.dump(dict(city=city,areas=sorted(out,key=lambda o:-o['places'])),open(f'city_{city}.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(city,len(out),'areas',sum(o['places'] for o in out),'places, missing pop:',miss, round(time.time()-t),'s')
