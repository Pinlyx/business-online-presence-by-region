import duckdb,time
c=duckdb.connect(); c.sql("INSTALL httpfs; LOAD httpfs; INSTALL spatial; LOAD spatial; SET s3_region='us-west-2';")
t=time.time()
c.sql("""COPY (SELECT id, country, region, subtype, class, names."primary" AS nm, ST_AsWKB(geometry) wkb
 FROM read_parquet('s3://overturemaps-us-west-2/release/2026-11-18.0/theme=divisions/type=division_area/*', hive_partitioning=1)
 WHERE subtype IN ('region','county') AND class='land'
   AND country IN ('AT','CH','ES','FR','DE','TR','MX','BR','ID','GB','PT','LU','US','CA','RU'))
 TO 'divisions.parquet' (FORMAT parquet)""")
print(c.sql("select country, subtype, count(*) from 'divisions.parquet' group by all order by 1,2").fetchall(), time.time()-t)
