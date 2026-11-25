# Business online presence by region 2026

How many local businesses list a website, region by region? 50,928,232 open places in 15 countries
from [Overture Maps](https://overturemaps.org) (release `2026-11-18.0`), assigned to 294 regions and
120 city districts and normalised with **official population tables and district boundaries from
government open-data portals** (data.gv.at, opendata.swiss, datos.gob.es, data.gouv.fr,
datos.madrid.es, NYC Open Data, City of Toronto Open Data, İzmir and İstanbul open data).

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24519450.svg)](https://doi.org/10.5281/zenodo.24519450)

Full write-up, tables and charts: **https://pinlyx.com/research/business-online-presence-by-region-2026**

## Headline numbers
- Inside one city the gap is wider than between most countries: Madrid's Centro district has
  110.4 business websites per 1,000 residents, Vicálvaro 11.1. Manhattan 102.9 vs the Bronx 16.2.
  İstanbul's Şişli 64.8 vs Sultangazi 3.4.
- Share of places with a website: US 76.4%, CA 75.7%, GB 73.8%, DE 73.6%, AT 71.2%, CH 67.7%,
  FR 58.3%, ES 53.5%, BR 36.9%, TR 33.6%, MX 27.4%, ID 24.5%.
- Austria: Tirol 62.7 websites per 1,000 residents, Wien 40.3. Switzerland: Zug 80.9, Fribourg 42.6.
  France: Paris 72.6, Seine-Saint-Denis 17.1. Spain: Illes Balears 36.6, Huelva 20.1.

Cross-country comparisons need care: where most Overture records come from Facebook business pages
(TR, MX, BR, ID, PT), the social share is near 100% by construction and the website share is lower
partly for the same reason. Compare regions within a country.

## Luxembourg by canton

26,595 open places from Overture Maps assigned to the 12 cantons (point-in-polygon, Overture division areas) and related to the official resident population on 1 January 2026 from STATEC ([Population by canton and municipality](https://data.public.lu/fr/datasets/statistiques-par-niveau-geographique-cantons-population/), data.public.lu, CC0). File: `data/luxembourg-cantons-2026.csv`.

| Canton | Places | With a website | Residents (2026) | Business websites per 1,000 residents |
|---|---:|---:|---:|---:|
| Clervaux | 1,137 | 77.9% | 22,179 | 39.9 |
| Luxembourg | 10,167 | 77.6% | 213,766 | 36.9 |
| Wiltz | 783 | 74.3% | 20,391 | 28.5 |
| Remich | 957 | 73.4% | 24,827 | 28.3 |
| Capellen | 2,022 | 78.2% | 56,562 | 28.0 |
| Echternach | 779 | 71.2% | 20,683 | 26.8 |
| Grevenmacher | 1,090 | 77.0% | 34,007 | 24.7 |
| Esch-sur-Alzette | 6,539 | 71.4% | 197,314 | 23.7 |
| Diekirch | 1,239 | 69.2% | 36,530 | 23.5 |
| Redange | 657 | 73.7% | 21,701 | 22.3 |
| Mersch | 1,048 | 71.0% | 37,191 | 20.0 |
| Vianden | 177 | 65.5% | 5,808 | 20.0 |

Clervaux (tourism-heavy, 39.9) and the canton of Luxembourg (36.9) lead; Mersch and Vianden (20.0) trail. The share of places with a website is high everywhere (65.5% to 78.2%).

## Files
| File | Content |
|---|---|
| `data/business-online-presence-by-region-2026.csv` | One row per country, region and city district: places, website %, Instagram %, population, places and websites per 1,000 residents |
| `data/business-online-presence-by-region-2026.json` | Same tables plus country-level phone, e-mail, X and WhatsApp shares, and the source list |
| `data/official-sources.json` | Every official dataset used, with portal page, publisher and licence |
| `scripts/` | The pipeline (Python + DuckDB 1.5) |

## Method
1. `extract.py`: read Overture places for each country straight from the public S3 parquet with DuckDB
   (bounding box + `addresses[1].country`), keep open places only.
2. `div.py` + `regjoin.py`: point-in-polygon against Overture division areas (`class = 'land'`,
   simplified 0.003°) for first-level regions (and Spanish provinces, French départements).
3. `cityjoin.py`: point-in-polygon against the **official** district boundaries of New York City,
   Toronto, Madrid and İzmir. İstanbul uses Overture district polygons because İBB publishes no
   district boundary file; its population comes from İBB.
4. `match.py` + `build.py`: join each area to the official population table by name
   (accent-insensitive, bilingual names handled), compute shares and per-1,000-resident rates.
5. `emit.py`: write the CSV/JSON.

Definitions: *website* = at least one URL in the record's `websites`; *Instagram* = an
`instagram.com` link in `socials`. Population years differ by source (AT 2023, CH 2025, ES 1 Jan 2026,
FR populations légales 2023, NYC 2010 census by borough because the portal's 2020 column is a
projection, Toronto 2021 census, Madrid 1 Jan 2026, İstanbul 2025, İzmir 2023).

## Official sources
| Used for | Kind | Dataset | Publisher | Licence |
|---|---|---|---|---|
| AT | population | [Bevölkerungsentwicklung Bundesländer Österreich](https://www.data.gv.at/katalog/datasets/8f6ed11c-c785-4cf0-b7ee-49598f655330) | Stadt Wien (MA 23), data.gv.at | CC BY 4.0 |
| nyc | boundaries | [Borough Boundaries](https://data.cityofnewyork.us/City-Government/Borough-Boundaries/gthc-hcne) | NYC Department of City Planning (DCP) | NYC Open Data Terms of Use (no license field on dataset page) |
| nyc | population | [New York City Population by Borough, 1950 - 2040](https://data.cityofnewyork.us/City-Government/New-York-City-Population-by-Borough-1950-2040/xywu-7bv9) | NYC Department of City Planning (DCP) | NYC Open Data Terms of Use (no license field on dataset page) |
| toronto | boundaries | [City Wards](https://open.toronto.ca/dataset/city-wards/) | City Clerk's Office | Open Government Licence - Toronto |
| toronto | population | [Ward Profiles (25-Ward Model)](https://open.toronto.ca/dataset/ward-profiles-25-ward-model/) | City Planning (source: Statistics Canada 2021 Census, custom tabulation) | Open Government Licence - Toronto |
| madrid | boundaries | [Distritos municipales de Madrid](https://datos.madrid.es/dataset/300497-0-distritos-municipales-madrid) | Ayuntamiento de Madrid | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| madrid | population | [Población por distrito y barrio a 1 de enero](https://datos.madrid.es/dataset/300557-0-poblacion-distrito-barrio) | Ayuntamiento de Madrid | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| izmir | boundaries | [İzmir Şehir Haritası (ilceler.geojson)](https://acikveri.bizizmir.com/dataset/izmir-sehir-haritasi) | Akıllı Şehir ve Kent Bilgi Sistemleri Dairesi Başkanlığı (İzmir Büyükşehir Belediyesi) | Izmir Metropolitan Municipality Open Data License |
| izmir | population | [İzmir İlçelerinin Cinsiyete Göre Nüfus Bilgileri](https://acikveri.bizizmir.com/dataset/izmir-ilcelerinin-cinsiyete-gore-nufus-bilgileri) | TÜİK (published by İzmir Büyükşehir Belediyesi) | License not specified on portal |
| istanbul | population | [Population Information (Nüfus Bilgileri)](https://data.ibb.gov.tr/dataset/nufus-bilgileri) | Istanbul Metropolitan Municipality, built from TÜİK MEDAS | Istanbul Metropolitan Municipality Open Data License |
| CH | population | [Bilanz der ständigen Wohnbevölkerung, nach Kanton und Stadt, 1999-2025](https://opendata.swiss/de/dataset/bilanz-der-standigen-wohnbevolkerung-nach-kanton-und-stadt-1999-2025) | Bundesamt für Statistik (BFS) | opendata.swiss terms of use: free use, attribution required (terms_by) https://opendata.swiss/terms-of-use#terms_by |
| ES | population | [Población residente por fecha, sexo y edad (desde 1971). ECP (Identificador API: 69792)](https://datos.gob.es/es/catalogo/ea0042823-poblacion-residente-por-fecha-sexo-y-edad-desde-1971-ecp-identificador-api-69792) | Instituto Nacional de Estadística (INE) | INE reuse conditions (free reuse citing INE as source); datos.gob.es lists no explicit license |
| ES_CCAA | population | [Población residente por fecha, sexo y edad. ECP (Identificador API: 59238)](https://datos.gob.es/es/catalogo/ea0042823-poblacion-residente-por-fecha-sexo-y-edad-ecp-identificador-api-59238) | Instituto Nacional de Estadística (INE) | INE reuse conditions (free reuse citing INE as source); datos.gob.es lists no explicit license |
| FR | population | [Populations de référence (populations légales 2023)](https://www.data.gouv.fr/datasets/populations-de-reference) | Institut national de la statistique et des études économiques (Insee) | Licence Ouverte v2.0 (lov2) |
| FR_REG | population | [Populations de référence (populations légales 2023)](https://www.data.gouv.fr/datasets/populations-de-reference) | Institut national de la statistique et des études économiques (Insee) | Licence Ouverte v2.0 (lov2) |

Overture Maps data: CDLA-Permissive-2.0. Official datasets keep their own licences (above); the
official files are not redistributed here, download them from the portal pages.

## Licence and citation
Derived tables and scripts: **CC BY 4.0** (data) and MIT (scripts).

> Güven, E. (2026). *Business online presence by region 2026* [Data set]. Pinlyx. https://doi.org/10.5281/zenodo.24519450

---

**DE:** Wie viele Betriebe nennen eine Website? 50,9 Mio. Orte in 15 Ländern, je Bundesland, Kanton und
Stadtbezirk, normiert mit amtlichen Bevölkerungsdaten (data.gv.at, opendata.swiss). Tirol 62,7 Websites
je 1.000 Einwohner, Wien 40,3; Zug 80,9, Fribourg 42,6.

**FR :** Quelle part des commerces affiche un site web ? 50,9 millions de lieux dans 15 pays, par
département et par région, rapportés aux populations légales de l’INSEE (data.gouv.fr). Paris 72,6 sites
pour 1 000 habitants, Seine-Saint-Denis 17,1.

**ES:** ¿Cuántos negocios tienen web? 50,9 millones de lugares en 15 países, por provincia, comunidad
autónoma y distrito de Madrid, con población oficial del INE (datos.gob.es) y del Ayuntamiento de Madrid.
Centro 110,4 webs por cada 1.000 habitantes, Vicálvaro 11,1.

**TR:** İşletmelerin kaçının web sitesi var? 15 ülkede 50,9 milyon kayıt; İstanbul ve İzmir ilçe ilçe,
İBB ve İzmir Büyükşehir açık verisindeki resmî nüfusla. 1.000 kişi başına web sitesi: Şişli 64,8,
Sultangazi 3,4; Çeşme 41,2, Kiraz 1,6.
