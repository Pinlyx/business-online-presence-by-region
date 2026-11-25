import duckdb,sys,json
c=duckdb.connect()
res={}
for cc in sys.argv[1:]:
    f=f"{cc}.parquet"
    q=f"""WITH p AS (SELECT *, list_transform(coalesce(socials,[]), s->lower(s)) so, list_transform(coalesce(websites,[]), s->lower(s)) we
      , coalesce(has_phone,false) hp, coalesce(has_email,false) he FROM '{f}' WHERE coalesce(operating_status,'open')='open')
    SELECT count(*) n,
     avg((len(we)>0)::int) web, avg((len(so)>0)::int) social, avg(hp::int) phone, avg(he::int) email,
     avg((len(we)=0 AND len(so)=0 AND hp)::int) phone_only,
     avg((len(we)=0 AND len(so)=0 AND NOT hp AND NOT he)::int) no_contact,
     avg(list_has_any(list_transform(so, s->s LIKE '%facebook.com%'),[true])::int) fb,
     avg(list_has_any(list_transform(so, s->s LIKE '%instagram.com%'),[true])::int) ig,
     avg(list_has_any(list_transform(so, s->(s LIKE '%twitter.com%' OR s LIKE '%x.com/%')),[true])::int) x,
     avg(list_has_any(list_transform(so, s->s LIKE '%youtube.com%'),[true])::int) yt,
     avg(list_has_any(list_transform(so, s->s LIKE '%linkedin.com%'),[true])::int) li,
     avg(list_has_any(list_transform(so, s->s LIKE '%tiktok.com%'),[true])::int) tt,
     avg(list_has_any(list_transform(list_concat(so,we), s->(s LIKE '%wa.me%' OR s LIKE '%whatsapp%')),[true])::int) wa,
     avg(list_has_any(list_transform(list_concat(so,we), s->(s LIKE '%t.me/%' OR s LIKE '%telegram%')),[true])::int) tg,
     avg(list_has_any(list_transform(so, s->(s LIKE '%vk.com%')),[true])::int) vk
    FROM p"""
    r=c.sql(q).fetchone(); cols=[d[0] for d in c.sql(q).description]
    res[cc]=dict(zip(cols,r))
    print(cc, {k:(round(v*100,1) if isinstance(v,float) else v) for k,v in res[cc].items()}, flush=True)
json.dump(res,open('stats.json','w'),indent=1)
