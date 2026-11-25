import duckdb,time,sys,os
B={'FR':(-5.3,41.3,9.7,51.2),'DE':(5.8,47.2,15.1,55.1),'ES':(-18.2,27.6,4.4,43.9),'MX':(-118.5,14.5,-86.7,32.8),
'BR':(-74.1,-33.8,-34.7,5.3),'ID':(95.0,-11.1,141.1,6.1),'GB':(-8.7,49.8,1.8,60.9),'AT':(9.5,46.3,17.2,49.1),
'PT':(-9.6,36.9,-6.1,42.2),'CA':(-141.0,41.6,-52.6,70.0),'RU':(19.6,41.1,180.0,78.0),'US':(-125.0,24.4,-66.9,49.4),
'TR':(25.6,35.8,44.9,42.2),'CH':(5.9,45.8,10.5,47.9),'LU':(5.7,49.4,6.55,50.2)}
c=duckdb.connect(); c.sql("INSTALL httpfs; LOAD httpfs; SET s3_region='us-west-2';")
for cc in sys.argv[1:]:
    out=f"{cc}.parquet"
    if os.path.exists(out): print(cc,'exists'); continue
    x0,y0,x1,y1=B[cc]; t=time.time()
    c.sql(f"""COPY (SELECT id, (bbox.xmin+bbox.xmax)/2 lon, (bbox.ymin+bbox.ymax)/2 lat, websites, socials,
      len(phones)>0 has_phone, len(emails)>0 has_email, basic_category, taxonomy.primary cat, confidence, operating_status,
      addresses[1].region region
     FROM read_parquet('s3://overturemaps-us-west-2/release/2026-11-18.0/theme=places/type=place/*', hive_partitioning=1)
     WHERE bbox.xmin BETWEEN {x0} AND {x1} AND bbox.ymin BETWEEN {y0} AND {y1} AND addresses[1].country='{cc}')
     TO '{out}.tmp' (FORMAT parquet)""")
    os.replace(out+'.tmp',out)
    n=c.sql(f"select count(*) from '{out}'").fetchone()[0]
    print(cc,n,round(time.time()-t),'s',flush=True)
