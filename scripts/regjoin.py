import duckdb,sys,time,json
c=duckdb.connect(); c.sql("LOAD spatial;"); c.sql("SET threads=4")
cc,sub=sys.argv[1],sys.argv[2]
t=time.time()
c.sql(f"CREATE TABLE a AS SELECT id did, nm, region rcode, ST_SimplifyPreserveTopology(ST_GeomFromWKB(wkb),0.003) g FROM 'divisions.parquet' WHERE country='{cc}' AND subtype='{sub}'")
c.sql(f"""CREATE TABLE p AS SELECT ST_Point(lon,lat) g,
  len(coalesce(websites,[]))>0 web,
  list_has_any(list_transform(list_transform(coalesce(socials,[]),s->lower(s)), s->s LIKE '%instagram.com%'),[true]) ig
  FROM '{cc}.parquet' WHERE coalesce(operating_status,'open')='open'""")
r=c.sql("""SELECT a.nm, a.rcode, count(*) n, sum(web::int) w, sum(ig::int) ig
  FROM p JOIN a ON ST_Contains(a.g, p.g) GROUP BY ALL ORDER BY n DESC""").fetchall()
tot=c.sql("select count(*) from p").fetchone()[0]
out=[dict(name=x[0],code=x[1],places=x[2],web=x[3],ig=x[4]) for x in r]
json.dump(dict(country=cc,level=sub,total=tot,matched=sum(o['places'] for o in out),areas=out),open(f'reg_{cc}_{sub}.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(cc,sub,len(out),'areas matched',sum(o['places'] for o in out),'/',tot, round(time.time()-t),'s')
for o in out[:5]: print('  ',o['name'],o['code'],o['places'],round(100*o['web']/o['places'],1))
