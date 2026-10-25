"""Builds staged border drafts (NOT live). Nile-corridor and area estimates as buffered geometry.
All geometry is EDITORIAL/APPROXIMATE: hand-placed anchor points (from existing cited extent points
where possible) buffered in degrees. Re-run: python3 build_drafts.py"""
import json
from shapely.geometry import LineString, Point, Polygon, mapping
# Nile anchors (lon,lat), approximate
N=dict(aswan=(32.90,24.09),halfa=(31.32,21.80),semna=(30.97,21.50),kerma=(30.40,19.60),dongola=(30.74,18.22),
 napata=(31.82,18.53),abuhamed=(33.32,19.53),kurgus=(33.48,19.23),berber=(33.98,18.02),shendi=(33.43,16.69),
 khartoum=(32.53,15.60),sennar=(33.60,13.55),kosti=(32.66,13.17),cairo=(31.24,30.04),delta_w=(29.9,31.2),delta_e=(32.3,31.2),
 hiera=(32.70,23.06),fifth=(34.00,18.40),roseires=(34.38,11.80))
nile_lower=[N['delta_w'],N['cairo'],(30.8,28.1),(31.2,27.2),(32.7,25.7),N['aswan']]
S={
'GHA2':{"citation":"G. Mokhtar (ed.) (1981) General History of Africa II: Ancient Civilizations of Africa (UNESCO)","url":"https://unesdoc.unesco.org/ark:/48223/pf0000184265"},
'DAVIES2003':{"citation":"W.V. Davies (2003) La frontière méridionale de l'Empire: les Égyptiens à Kurgus, BSFE 157, 23-37","url":"https://doi.org/10.3406/bsfe.2003.2624"},
'SARS_KURGUS':{"citation":"Sudan Archaeological Research Society, Kurgus fieldwork page","url":"https://www.sudarchrs.org.uk/fieldwork/kurgus/"},
'WELSBY2002':{"citation":"D.A. Welsby (2002) The Medieval Kingdoms of Nubia, British Museum Press","url":"https://books.google.com/books?id=mXIPAQAAMAAJ"},
'OCHALA_ALWA':{"citation":"V. Ochała, Miscellanea Epigraphica Nubica II: Languages and scripts in the Kingdom of Alwa (Collectanea Christiana Orientalia)","url":"https://journals.uco.es/cco/article/download/14673/13083/28959"},
'DRZEWIECKI_SOBA':{"citation":"M. Drzewiecki et al. (2019) Developing a New Approach to Research at Soba, Archaeologies","url":"https://link.springer.com/article/10.1007/s11759-019-09370-x"},
'OFS1974':{"citation":"R.S. O'Fahey & J.L. Spaulding (1974) Kingdoms of the Sudan, Methuen (Routledge reissue 2016)","url":"https://doi.org/10.4324/9781315451138"},
'HD2011':{"citation":"P.M. Holt & M.W. Daly (2011) A History of the Sudan, 6th ed.","url":"https://doi.org/10.4324/9781315834030"},
'GHA5':{"citation":"B.A. Ogot (ed.) (1992) General History of Africa V, ch.7 'The Sudan, 1500-1800' (Y.F. Hasan & B.A. Ogot)","url":"https://unesdoc.unesco.org/ark:/48223/pf0000184290"},
'OFAHEY2008':{"citation":"R.S. O'Fahey (2008) The Darfur Sultanate: A History","url":"https://books.google.com/books?id=HQxYJWkO7EEC"},
}
def corr(pts,w): return LineString(pts).buffer(w,cap_style=1,join_style=1).simplify(0.02)
def area(c,r): return Point(c).buffer(r).simplify(0.02)
D=[]  # (era, zone, geom, confidence, badges, sources, basis)
D+= [('a-group-lower-nubia','influence',corr([N['aswan'],N['hiera'],N['halfa']],0.3),0.35,['APPROXIMATE','EDITORIAL'],['GHA2'],'GHA II ch.9 pp.245,249 place A-Group sites in Lower Nubia between the 1st and 2nd cataracts; corridor = Nile ±0.3°. Cultural zone, not a state border.'),
 ('c-group-lower-nubia','influence',corr([N['aswan'],N['hiera'],N['halfa']],0.3),0.35,['APPROXIMATE','EDITORIAL'],['GHA2'],'GHA II ch.9 p.252: C-Group in Lower Nubia; cultural zone, not a state border.'),
 ('middle-kingdom-egypt','core',corr(nile_lower,0.25),0.7,['APPROXIMATE','DERIVED'],['GHA2'],'Egyptian Nile valley south of Cairo to Aswan (Delta not drawn in this draft).'),
 ('middle-kingdom-egypt','claimed',corr([N['aswan'],N['hiera'],N['halfa'],N['semna']],0.25),0.6,['APPROXIMATE'],['GHA2'],'Fortress frontier to Semna (2nd cataract), GHA II ch.9 pp.255,258.'),
 ('egyptian-new-kingdom-rule-in-nubia','core',corr([N['aswan'],N['halfa'],N['semna'],N['kerma'],N['dongola'],N['napata']],0.25),0.6,['APPROXIMATE'],['GHA2'],'Viceroyalty of Kush to Napata/Gebel Barkal, GHA II ch.10 pp.265,270.'),
 ('egyptian-new-kingdom-rule-in-nubia','claimed',corr([N['napata'],N['abuhamed'],N['kurgus']],0.25),0.5,['APPROXIMATE','SINGLE-SOURCE'],['DAVIES2003','SARS_KURGUS'],'Boundary stelae of Thutmose I and III at Hagar el-Merwa, Kurgus, ~40 km upstream of Abu Hamed (claimed limit, not administered land).'),
 ('ptolemaic-egypt','core',corr(nile_lower,0.25).union(Polygon([N['delta_w'],N['delta_e'],(31.6,30.1),(30.9,30.1)])),0.75,['APPROXIMATE','DERIVED'],['GHA2'],'Nile valley + Delta; southern edge at the Dodekaschoinos per GHA II ch.6-7 pp.189-190, 208.'),
 ('ptolemaic-egypt','contested',corr([N['aswan'],N['hiera']],0.25),0.4,['APPROXIMATE','CONTESTED'],['GHA2'],'Dodekaschoinos frontier zone shared/contested with Meroe.'),
 ('roman-byzantine-egypt','core',corr(nile_lower,0.25).union(Polygon([N['delta_w'],N['delta_e'],(31.6,30.1),(30.9,30.1)])),0.75,['APPROXIMATE','DERIVED'],['GHA2'],'Province of Aegyptus, GHA II ch.7 p.210.'),
 ('roman-byzantine-egypt','claimed',corr([N['aswan'],N['hiera']],0.25),0.5,['APPROXIMATE'],['GHA2'],'Frontier to Hiera Sykaminos after the treaty with Meroe, GHA II ch.7 pp.208, 290; withdrawn to Aswan under Diocletian (verify date).'),
 ('alodia-alwa','core',corr([N['khartoum'],(32.68,15.52),N['sennar']],0.45),0.4,['APPROXIMATE','VERIFY'],['WELSBY2002','DRZEWIECKI_SOBA'],'Core around Soba on the Blue Nile and the northern Gezira.'),
 ('alodia-alwa','claimed',corr([N['fifth'],N['shendi'],N['khartoum']],0.35).union(corr([N['khartoum'],N['kosti']],0.35)).union(corr([N['sennar'],N['roseires']],0.35)),0.25,['APPROXIMATE','VERIFY','EDITORIAL'],['OCHALA_ALWA','WELSBY2002'],'Between the 5th cataract and lands south of Khartoum "about which very little is known" (Ochała, citing Welsby 2002); southern limit editorial.'),
 ('funj-sultanate-of-sennar','core',corr([N['khartoum'],N['sennar'],N['roseires']],0.6),0.6,['APPROXIMATE'],['OFS1974','HD2011'],'Gezira and Blue Nile heartland around Sennar.'),
 ('funj-sultanate-of-sennar','claimed',corr([N['dongola'],N['napata'],N['abuhamed'],N['berber'],N['shendi'],N['khartoum']],0.3).union(area((29.5,13.0),1.0)),0.35,['APPROXIMATE','EDITORIAL'],['OFS1974','HD2011','GHA5'],'Tributary north (Abdallab/Ja\'aliyyin to Dongola) and episodic Kordofan claims; vassals drawn separately.'),
 ('ja-aliyyin-kingdom-sa-dab-funj-vassal','core',corr([(33.97,17.68),N['shendi'],(33.2,16.4)],0.25),0.45,['APPROXIMATE','EDITORIAL'],['HD2011'],'Shendi reach of the Nile (Holt & Daly p.4); width editorial.'),
 ('abdallab-chiefdom-funj-vassal','core',corr([(32.63,16.24),N['khartoum']],0.3),0.4,['APPROXIMATE','EDITORIAL'],['GHA5','OFS1974'],'Around Qarri north of the confluence (GHA V ch.7 p.172).'),
 ('abdallab-chiefdom-funj-vassal','influence',corr([N['khartoum'],N['shendi'],N['berber'],N['abuhamed']],0.35),0.25,['APPROXIMATE','EDITORIAL'],['OFS1974'],'Northern overlordship under the Funj (O\'Fahey & Spaulding ch.5).'),
 ('tunjur-kingdom','core',area((24.32,14.27),0.9),0.3,['APPROXIMATE','SINGLE-SOURCE','EDITORIAL'],['OFAHEY2008'],'Northern Jebel Marra / Ain Farah area; radius editorial.'),
 ('daju-kingdom','core',area((24.27,12.95),0.9),0.25,['APPROXIMATE','SINGLE-SOURCE','EDITORIAL'],['OFAHEY2008'],'South-east of Jebel Marra; radius editorial.'),
 ('restored-darfur-sultanate-ali-dinar','core',Polygon([(22.4,15.2),(25.8,16.2),(27.4,14.4),(27.0,11.0),(24.2,10.4),(22.6,12.0)]),0.5,['APPROXIMATE','VERIFY'],['HD2011','OFS1974'],'Darfur roughly in its Condominium-era provincial outline; west edge with Wadai contested until 1919-23 boundary work (verify).'),
 ('kingdom-of-taqali','core',area((30.75,12.0),0.45),0.4,['APPROXIMATE','EDITORIAL'],['HD2011'],'Jebel Taqali, NE Nuba Mountains.'),
 ('musabba-at-sultanate-kordofan','influence',area((29.5,13.0),1.2),0.25,['APPROXIMATE','SINGLE-SOURCE','EDITORIAL'],[],'Kordofan; source OFS1972 BSOAS doi:10.1017/s0041977x00109383 (from extents file).'),
]
EXTRA={'OFS1972':{"citation":"R.S. O'Fahey & J. Spaulding (1972) Hāshim and the Musabba'āt, BSOAS","url":"https://doi.org/10.1017/s0041977x00109383"}}
S.update(EXTRA); D[-1]=D[-1][:5]+(['OFS1972'],)+D[-1][6:]
out={}
for era,zone,g,conf,b,src,basis in D:
  out.setdefault(era,[]).append({"type":"Feature","geometry":mapping(g),"properties":{"era_id":era,"zone":zone,"confidence":conf,
   "badges":sorted(set(b+['EDITORIAL'] if conf<0.4 else b)),"method":"anchor points + Nile/area buffer (degrees), hand-placed; see README","basis":basis,
   "sources":[dict(id=s,**S[s]) for s in src],"status":"DRAFT – not live, needs Historian sign-off","version":"bd-0.1 2026-10-24"}})
for era,fs in out.items():
  json.dump({"type":"FeatureCollection","features":fs},open(f"{era}.geojson","w"),ensure_ascii=False,indent=1)
json.dump({"type":"FeatureCollection","features":[f for fs in out.values() for f in fs]},open("_all_drafts.geojson","w"),ensure_ascii=False)
print(len(out),"eras",sum(len(v) for v in out.values()),"features")
