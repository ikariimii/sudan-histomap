"""Research corrections & additions (Sudan Historian, 2026-10-19). Applied by build_data.py.
Only sources actually consulted online are cited. See CHANGELOG-research.md."""
WEL96="https://search.worldcat.org/title/34888835"  # Welsby, The Kingdom of Kush (BMP 1996)
WEL02="https://doi.org/10.1017/s002185370323855x"   # review record of Welsby, Medieval Kingdoms of Nubia (BMP 2002)
HD="https://doi.org/10.4324/9781315834030"          # Holt & Daly, A History of the Sudan, 6th ed. 2011
OF08="https://books.google.com/books?id=HQxYJWkO7EEC"  # O'Fahey, The Darfur Sultanate (2008)
OFS72="https://doi.org/10.1017/s0041977x00109383"   # O'Fahey & Spaulding, 'Hashim and the Musabba'at', BSOAS 1972
SP85="https://catdir.loc.gov/catdir/toc/ecip0615/2006019294.html"  # Spaulding, The Heroic Age in Sinnar
GHA2="https://unesdoc.unesco.org/ark:/48223/pf0000184265"  # UNESCO GHA vol. II (1981)
WHC1073="https://whc.unesco.org/en/list/1073"; WHC1336="https://whc.unesco.org/en/list/1336"
KERMA="https://kerma.ch/en/history/"
EP_NUER="https://monoskop.org/images/4/4d/Evans_Pritchard_E_E_The_Nuer_a_description_of_the_modes_1940.pdf"
EP_ANUAK="https://doi.org/10.4324/9781003135395"
WD=lambda q:"https://www.wikidata.org/wiki/"+q
PL=lambda n:"https://pleiades.stoa.org/places/"+str(n)
C=lambda n,lat,lon:dict(name=n,lat=lat,lon=lon)

def P(name,stream,s,e,prom,events,caps,src,note=""):
    return dict(name=name,stream=stream,start=s,end=e,prominence=prom,key_events=events,capitals=caps,sources=src,dating_note=note)

def apply(D):
    by={d["name"]:d for d in D}
    def upd(n,**kw):
        d=by[n]
        for k,v in kw.items():
            if k=="add_src": d["sources"]=[*v,*[s for s in d["sources"] if s not in v]]
            elif k=="add_ev": d["key_events"]+=v
            elif k=="add_caps": d["capitals"]+=v
            else: d[k]=v
    # --- Prehistory / Nubia before Napata
    upd("Khartoum Neolithic (Shaheinab)",capitals=[C("Esh-Shaheinab",16.0624,32.5394),C("Kadero",15.75,32.55)],
        add_src=[WD("Q109284524"),WD("Q109284535")],dating_note="Approximate; site coordinates from Wikidata (Esh-Shaheinab corrected from 16.13N). Kadero added as second Khartoum Neolithic site (coordinates approximate, Wikidata).")
    upd("Khartoum Mesolithic (Early Khartoum)",dating_note="Approximate; radiocarbon ranges vary. Site point is a city-level approximation (not a surveyed site location). No stronger source verified yet.")
    upd("A-Group (Lower Nubia)",add_src=[GHA2],capitals=[C("Qustul",22.2333,31.6167),C("Faras",22.2,31.46)],
        dating_note="UNESCO GHA II ch.9 (Sherif) places the A-Group's flowering c.3100 BCE, contemporary with Egypt's 1st Dynasty; -3800 start is a broad conventional bracket. Qustul coordinates corrected (Wikidata).")
    upd("C-Group (Lower Nubia)",add_src=[GHA2],dating_note="GHA II ch.9: C-Group appears late Old Kingdom/First Intermediate Period and lasts until Egyptianisation of Nubia in the 16th c. BCE; -2400 start is at the early edge of that bracket. Aniba coordinates not independently verified.")
    upd("Kingdom of Kerma",start=-2450,end=-1480,add_src=[KERMA,GHA2],capitals=[C("Kerma",19.6008,30.4097)],
        add_ev=["Swiss mission phases: Early Kerma c.2450–2050, Middle c.2050–1750, Classic c.1750–1480 BCE (Final Kerma to c.1450)"],
        dating_note="Corrected to Swiss Archaeological Mission chronology (kerma.ch). Note GHA II (1981) still dates 'Kerma' to -1730/-1580, i.e. only the Classic phase; superseded by Bonnet/Honegger excavations.")
    upd("Egyptian New Kingdom rule in Nubia",add_src=[WHC1073,GHA2],add_caps=[C("Soleb",20.4333,30.3333),C("Kurgus",19.2308,33.4772)],
        dating_note="WHC: Gebel Barkal sacred to Amun since c.1500 BCE. Soleb/Kurgus coordinates from Wikidata (approximate).")
    # --- Kush
    upd("Kingdom of Kush – Napatan period",add_src=[GHA2,WEL96,WHC1073],
        key_events=["Alara, then Kashta (c.760–750 BCE); Kushites in Upper Egypt c.750",
          "Peye (Piye/'Piankhi') reign from c.751 BCE; Victory Stela; conquest of Egypt c.728/727",
          "Shabaka from c.713 BCE founds 25th Dynasty rule over all Egypt",
          "Shabataka (Shebitku) c.700–690; Taharqa 690–664 BCE (cenotaph/pyramid at Nuri)",
          "Tanwetamani (Tanoutamon) 664–c.656; Assyrian sack of Thebes 663; Kushite withdrawal",
          "Atlanarsa 653–643, Senkamanisken 643–623, Anlamani 623–593, Aspelta 593–568 BCE",
          "Psamtik II's expedition captures Napata (GHA: 591 BCE; widely dated 593 BCE)",
          "Royal burials at El-Kurru then Nuri; burial shift to Meroe c.270 BCE"],
        capitals=[C("Jebel Barkal / Napata",18.5368,31.8276),C("El-Kurru",18.4089,31.7705),C("Nuri",18.5643,31.9161),C("Kawa (Gematon)",19.1231,30.4966)],
        dating_note="Reign dates follow UNESCO GHA II ch.10 (Leclant, 1981); later scholarship revises several (incl. the Shabaka/Shebitku order) – treat as approximate. WHC gives Napatan 900–270 BCE; -800 start kept as display convention. Coordinates: Pleiades/Wikidata.")
    upd("Kingdom of Kush – Meroitic period",add_src=[GHA2,WHC1336,WEL96],
        key_events=["Ergamenes/Arkamani (3rd c. BCE), friendly relations with Ptolemaic Egypt",
          "Queen Shanakdakhete (c.170–160 BCE): among earliest Meroitic hieroglyphic inscriptions (Naqa)",
          "Taniydamani (late 2nd c. BCE): first long Meroitic texts",
          "Iron working at Meroe; Meroitic script transliterated by Griffith 1909, language still not understood",
          "Kandakes Amanirenas and Amanishakheto; Prince/King Akinidad; war with Rome: Napata taken by Petronius 23 BCE (GHA), Treaty of Samos 21/20 BCE",
          "Natakamani & Amanitore (GHA: c.12 BCE–12 CE; dating debated): Naqa Lion Temple, Amara, restoration of Napata",
          "Collapse by time of Ezana of Aksum's campaign 'against the Nubas' (c.mid-4th c. CE)"],
        capitals=[C("Meroë",16.9351,33.7507),C("Naqa",16.2694,33.275),C("Musawwarat es-Sufra",16.4158,33.3236),C("Wad ban Naqa",16.5111,33.1122),C("Hamadab",16.9117,33.6919)],
        dating_note="Meroitic chronology uncertain (GHA II: 'particularly serious' for 2nd–1st c. BCE). Which kandake negotiated with Rome (Amanirenas vs Amanishakheto) is unresolved in GHA. End c.350 CE approximate.")
    upd("Noba / X-Group (Ballana culture)",add_src=[WEL02,GHA2],dating_note="Approximate. Ballana coordinates not independently verified.")
    upd("Nobadia",add_src=[WEL02,GHA2],capitals=[C("Faras (Pachoras)",22.2,31.46),C("Qasr Ibrim",22.6502,31.9915)],dating_note="Christianisation c.543 and merger with Makuria (7th c.) per standard accounts; specific dates not re-verified in a primary source in this pass.")
    upd("Makuria",add_src=[WEL02],add_caps=[C("Banganarti",18.1667,30.7849)],dating_note="End date approximate (kingdom fragmented in 14th–15th c.).")
    upd("Alodia (Alwa)",add_src=[WEL02,HD],dating_note="Fall c.1504 traditional (Funj/'Abdallab); Soba coordinates not independently verified.")
    # --- Funj and after
    upd("Funj Sultanate of Sennar",add_src=[HD,SP85],add_ev=["Holt & Daly: Funj suzerainty over Upper Nubia (above 3rd Cataract) incl. vassal-kingdom of Dongola; 'Abdallab recognised as paramount chiefs of the Arabs"],
        dating_note="1504–1821 per Holt & Daly. Foundation by a Shilluk band is a tradition, not established fact.")
    for n in ["Turkiyya (Ottoman-Egyptian rule)","Mahdist State (Mahdiyya)","Anglo-Egyptian Sudan (Condominium)","Independent Sudan – First parliamentary period","Abboud military regime","Second parliamentary period","Nimeiry era (Democratic Republic of Sudan)","Transitional & third parliamentary period"]:
        upd(n,add_src=[HD])
    upd("Al-Bashir / NCP (Ingaz) regime",add_src=[HD],dating_note="Holt & Daly 6th ed. (2011) covers to c.2010; 2011+ events still Wikipedia-sourced.")
    # --- Darfur / Kordofan
    upd("Sultanate of Darfur (Keira)",start=1650,add_src=[OF08,HD],key_events=["Keira dynasty from Jabal Marra; founder Sulayman (Solongdungu) – O'Fahey dates the sultanate c.1650–1916","Expansion into Kordofan under Muhammad Tayrab c.1785","Capital fixed at al-Fashir c.1790/91 under 'Abd al-Rahman","Conquered by al-Zubayr Rahma 1874"],
        dating_note="Start corrected 1603→c.1650 (O'Fahey 2008). Older chronologies place Sulayman earlier; founding date genuinely uncertain. El Fasher date c.1790–91.")
    upd("Restored Darfur Sultanate (Ali Dinar)",add_src=[OF08,HD])
    upd("Daju kingdom",add_src=[OF08],dating_note="Very approximate; known mainly from oral tradition (O'Fahey 2008, 'Daju and Tunjur'). Jebel Marra point is a regional marker.")
    upd("Tunjur kingdom",add_src=[OF08],dating_note="Approximate. Ain Farah coordinates UNVERIFIED: Wikidata gives 16.76N 29.19E, which conflicts with its stated North Darfur location; original 15.0N 24.9E retained pending check.")
    upd("Kingdom of Taqali",add_src=[HD],dating_note="Founding c.1750 and end 1969 NOT verified. Holt & Daly: semi-autonomous after 1821 and integrated into Condominium local government; royal line claims Ja'ali holy-man ancestry.")
    # --- South Sudan
    upd("Shilluk Kingdom",add_src=[HD],add_ev=["Holt & Daly: range formerly reached Aba Island (mid-19th c.); raided Arab settlements down the White Nile until early Turco-Egyptian period","Tradition ascribes the Funj foundation to a Shilluk war-band"],
        dating_note="Founding c.1490 traditional (Nyikang); 1861 end-point not re-verified.")
    # --- Egypt / Horn / Rome corrections
    upd("Late Period / Persian Egypt",key_events=["26th Dynasty; Psamtik II's expedition takes Napata (GHA II: 591 BCE; often 593 BCE)"],add_src=[GHA2])
    upd("Roman & Byzantine Egypt",key_events=["Petronius' punitive campaign captures Napata 23 BCE after Meroitic sack of Aswan (GHA II)","Treaty of Samos 21/20 BCE; frontier at Hiera Sycaminos (Maharraqa)"],add_src=[GHA2])
    upd("Kingdom of Aksum",add_src=[GHA2])
    upd("Land of Punt / D'mt",add_src=[GHA2])
    upd("Suakin – Red Sea port (Beja, Ottoman)",add_src=[HD],capitals=[C("Suakin",19.1025,37.33)])
    upd("Southern Sudan under Condominium / Sudan",add_src=[HD])
    for n in ["Early Dynastic & Old Kingdom Egypt","Middle Kingdom Egypt","New Kingdom Egypt","Ptolemaic Egypt","Garamantes (Fezzan)","Sabaean & South Arabian kingdoms"]:
        upd(n,add_src=[GHA2])
    # --- Additions
    D+= [
     P("Beja (Red Sea Hills peoples)","Red Sea & Arabia",700,2026,0.3,
       ["Recognised by medieval Muslim writers as distinct from Nubians, Arabs and 'Sudan'","Camel-nomads of the Red Sea Hills; gradual Islamisation and varying arabisation","'Ababda (north) Arabic-speaking; 18th c. southward expansion; Hadendowa in Taka (Gash) by early 19th c.","Nabtab ruling clan of the Banu 'Amir claims Ja'ali descent"],
       [C("Suakin",19.1025,37.33)],[HD],"Start 700 is a display convention for medieval attestation only; links to ancient Medjay/Blemmyes not asserted here. Ongoing people, not a single polity."),
     P("'Abdallab chiefdom (Funj vassal)","Sudan – Middle Nile",1480,1821,0.35,
       ["Founded by 'Abdallah Jamma' (Rufa'a) at the Blue/White Nile confluence, late 15th c.","Prospered from tolls on desert nomads","Recognised by Funj sultans as paramount chiefs of the Arabs","Capital Qarri, later Halfayat al-Muluk; an 'Abdallabi chief ruled Quz Rajab on the Atbara"],
       [C("Qarri",16.2356,32.6316)],[HD,SP85],"Start 'late 15th c.' per Holt & Daly; 1480 is approximate. Qarri coordinates from Wikidata (settlement, approximate). End 1821 = Turco-Egyptian conquest."),
     P("Ja'aliyyin kingdom (Sa'dab, Funj vassal)","Sudan – Middle Nile",1500,1821,0.3,
       ["Tribal kingdom between the Atbara confluence and the Sabaluqa Gorge from the 16th c.","Royal clan the Sa'dab; Mirafab kingdom at Berber to the north","Shendi became the chief commercial centre of the eastern Bilad al-Sudan by early 19th c., under Makk Nimr"],
       [C("Shendi",16.6914,33.4339)],[HD],"'From the sixteenth century' (Holt & Daly); 1500 approximate."),
     P("Musabba'at sultanate (Kordofan)","Sudan – Darfur & Kordofan",1680,1785,0.25,
       ["Exiled Keira faction contesting Kordofan with Funj and Darfur, late 17th–18th c.","Isawi dislodges Funj (Ghudiyat) administration c.1734","Hashim b. 'Isawi retakes Kordofan c.1772; ousted by Funj 1782","Darfur's Muhammad Tayrab conquers Kordofan c.1785"],
       [],[OFS72,OF08,"https://en.wikipedia.org/wiki/Muhammad_Tayrab"],"Bracket from O'Fahey & Spaulding (BSOAS 1972 abstract: 'late seventeenth and eighteenth centuries'); 1734/1772/1782/1785 events taken from a Wikipedia summary citing O'Fahey 2008 pp.49–59 – book pages not directly checked. No capital location verified."),
     P("Dinka (Jieng) communities","South Sudan – Upper Nile",1500,2026,0.3,
       ["Group of tribes without central kingship, mostly in Bahr al-Ghazal floodplains, some east of the White Nile (Holt & Daly)","Cattle pastoralism; culturally close to the Nuer, together a Nilotic subdivision (Evans-Pritchard 1940)"],
       [],[HD,EP_NUER],"Start 1500 is a display convention ONLY; Dinka presence long predates it and no founding date exists. Not a state."),
     P("Nuer (Naath) communities","South Sudan – Upper Nile",1500,2026,0.25,
       ["Self-name Nath; c.200,000 people in the 1930s (Evans-Pritchard)","Swamps and savannah on both sides of the Nile south of the Sobat/Bahr al-Ghazal junction and along both tributaries","Seasonal movement between villages and dry-season cattle camps"],
       [],[EP_NUER],"Start 1500 is a display convention; 19th-c. eastward expansion not yet sourced. Not a state."),
     P("Anuak (Anywaa) communities","South Sudan – Upper Nile",1500,2026,0.2,
       ["Shilluk-speaking (Luo) Nilotic people (Evans-Pritchard 1940)","Studied in Evans-Pritchard, The Political System of the Anuak (1940)"],
       [],[EP_ANUAK,EP_NUER],"Start 1500 is a display convention. Location (Sobat/Pibor–Gambela borderland) and political details not verified in this pass."),
    ]
    apply2(D,by,upd)
    apply3(D)
    return D

# ---------------- Pass 2 (2026-10-19, follow-up) ----------------
GHA=lambda v:{"III":"https://unesdoc.unesco.org/ark:/48223/pf0000184282","IV":"https://unesdoc.unesco.org/ark:/48223/pf0000184287",
  "V":"https://unesdoc.unesco.org/ark:/48223/pf0000121577","VI":"https://unesdoc.unesco.org/ark:/48223/pf0000184295",
  "VII":"https://unesdoc.unesco.org/ark:/48223/pf0000184296","VIII":"https://unesdoc.unesco.org/ark:/48223/pf0000184297"}[v]
AAR21="https://link.springer.com/article/10.1007/s10437-021-09432-y"
RILLY="https://www.sudarchrs.org.uk/wp-content/uploads/2020/11/SARS_SN22_Rilly.pdf"
ICG19="https://www.crisisgroup.org/africa/horn-africa/sudan/281-safeguarding-sudans-revolution"
ICG21="https://www.crisisgroup.org/africa/horn-africa/sudan/reversing-sudans-dangerous-coup"
UNSC2524="https://docs.un.org/en/S/RES/2524(2020)"
UN23="https://news.un.org/en/story/2023/04/1135702"
UNSC23="https://press.un.org/en/2023/sc15257.doc.htm"
IPC24="https://www.ipcinfo.org/fileadmin/user_upload/ipcinfo/docs/IPC_Famine_Review_Committee_Report_Sudan_July2024.pdf"
JEDDAH="https://www.state.gov/jeddah-declaration-of-commitment-to-protect-the-civilians-of-sudan"
UNSC1996="https://peacekeeping.un.org/sites/default/files/past/unmis/documents/sres1996_2011.pdf"
ICG14="https://www.crisisgroup.org/sites/default/files/south-sudan-a-civil-war-by-any-other-name.pdf"
RARCSS="https://peaceaccords.nd.edu/wp-content/uploads/2020/01/9-12-2018-R-ARCSS.pdf"
ACCORD20="https://www.accord.org.za/conflict-trends/the-formation-of-the-revitalized-transitional-government-of-national-unity-in-south-sudan/"

def apply2(D,by,upd):
    by.update({d["name"]:d for d in D})
    # 1) coordinates
    upd("Tunjur kingdom",capitals=[C("Ain Farah",14.2657,24.3161)],add_src=[WD("Q405860")],
        dating_note="Approximate. Ain Farah corrected 15.0N 24.9E -> 14.2657N 24.3161E (2nd Wikidata statement; matches de/ar Wikipedia). Wikidata's other value 16.76N 29.19E (repeated on rainerebert.com) lies outside Darfur and is rejected. MEDIUM confidence: the descriptive '15 km NW of Kutum' does not fit (point is c.35 km W of Kutum); no excavation-report coordinate found.")
    upd("Alodia (Alwa)",capitals=[C("Soba",15.524,32.6809)],add_src=[WD("Q1247214")],
        dating_note="Fall c.1504 traditional (Funj/'Abdallab). Soba point confirmed by Wikidata Q1247214 (15.524N 32.681E), consistent with the original; there is no Pleiades entry; no excavation-report coordinate checked.")
    upd("Noba / X-Group (Ballana culture)",capitals=[C("Ballana",22.2667,31.5667)],add_src=[PL(795783)],
        dating_note="Approximate. Ballana coordinates verified: Pleiades 795783 (Barrington Atlas 81 B3). Site now under Lake Nasser.")
    upd("C-Group (Lower Nubia)",capitals=[C("Aniba",22.6683,32.017)],add_src=[PL(795777)],
        dating_note="GHA II ch.9: C-Group appears late Old Kingdom/First Intermediate Period and lasts until Egyptianisation of Nubia in the 16th c. BCE; -2400 start sits at the early edge. Aniba verified: Pleiades 795777 (BAtlas 81 C3).")
    upd("Kingdom of Kush – Meroitic period",add_caps=[C("Sedeinga",20.5435,30.2871)],add_src=[PL(795855),RILLY])
    # 2) placeholder starts
    b=by["Beja (Red Sea Hills peoples)"]; b["start"]=275
    b["sources"]=[HD,GHA2]; b["key_events"].insert(0,"Blemmyes (GHA II: 'customarily identified with the Bedja tribes') raid Upper Egypt; suppressed under Probus (276–282 CE)")
    b["key_events"].insert(1,"After Meroe's fall the Nobades push the Blemmyes ('Bega or Buga') into the eastern desert")
    b["dating_note"]="Start c.275 CE = earliest dated Blemmyes activity in GHA II ch.7 (Probus 276–282). The Blemmyes=Beja equation is customary, NOT proven (GHA II ch.10); GHA II ch.11 says earlier Meroitic-era Majai/Reheres 'could have been' Beja ancestors, so earlier origins are possible. Ongoing people, not a polity."
    for n in ["Dinka (Jieng) communities","Nuer (Naath) communities","Anuak (Anywaa) communities"]:
        by[n]["dating_note"]="UNSOURCED START (1500 = display placeholder). No source found giving a datable emergence; Nilotic presence long predates it. Not a state. "+("Nuer 19th-c. expansion still unsourced." if "Nuer" in n else "")
    # 3) Wikipedia-only upgrades
    upd("Khartoum Mesolithic (Early Khartoum)",start=-8500,end=-5000,add_src=[AAR21],
        dating_note="Corrected -8000/-4900 -> c.8500–5000 cal BC for Early Khartoum ceramics of central Sudan (Garcea/Jesse et al., African Archaeological Review 2021 review). Northern 'Khartoum Variant' is c.8000–4900 cal BC. Site point = city-level approximation.")
    upd("December Revolution & transition",add_src=[ICG19,ICG21,UNSC2524],add_ev=["Constitutional Document signed 17 Aug 2019; Hamdok PM; cabinet 8 Sep 2019 (ICG)","UNITAMS created by UNSC res. 2524, 3 Jun 2020"])
    upd("War in Sudan (SAF vs RSF)",add_src=[UN23,UNSC23,IPC24,JEDDAH],add_ev=["Jeddah Declaration on protection of civilians, 11 May 2023","IPC Famine Review Committee: famine plausibly ongoing in Zamzam camp, July 2024 (published 1 Aug 2024)"],
        dating_note="Ongoing; end=present. 'Government relocates to Port Sudan' not yet tied to a non-Wikipedia source (UN sources confirm the UN hub moved there).")
    upd("Republic of South Sudan",add_src=[UNSC1996,ICG14,RARCSS,ACCORD20],key_events=["Independence 9 July 2011; UNMISS created by UNSC res. 1996 (8 Jul 2011)","Civil war from 15 Dec 2013 (ICG 2014)","R-ARCSS signed 12 Sep 2018","Revitalised Transitional Government of National Unity formed 22 Feb 2020 (ACCORD)"])
    upd("Southern Sudan under Condominium / Sudan",add_src=[UNSC1996])
    for n,v in [("Islamic Egypt (Rashidun–Fatimid–Ayyubid)",["III","IV"]),("Rise of Islam & Caliphates",["III"]),("Mamluk Sultanate",["IV"]),("Zagwe dynasty",["IV"]),
                ("Ethiopian Empire (Solomonic)",["IV","V","VI","VII"]),("Kanem Empire",["III","IV"]),("Bornu Empire",["IV","V","VI"]),("Wadai Sultanate",["V","VI"]),
                ("Zande kingdoms",["V","VI"]),("Ottoman Egypt & Muhammad Ali dynasty",["V","VI"]),("British-occupied / Kingdom of Egypt",["VII"]),
                ("Eritrea (Italian colony → independent)",["VII","VIII"]),("French Chad → Republic of Chad",["VII","VIII"]),("Libya (Ottoman, Italian, independent)",["V","VII","VIII"]),
                ("Central African Republic (Ubangi-Shari)",["VII","VIII"]),("Republic of Egypt",["VIII"]),("Derg & Federal Ethiopia",["VIII"])]:
        upd(n,add_src=[GHA(x) for x in v])
    upd("Ottoman Hejaz & Saudi state",add_src=[JEDDAH])

# ---------------- Pass 3: meta.sources + key_events_ar (2026-10-19) ----------------
# Format expected by index.html cite(): HISTO.meta.sources[id] = {author, year, title, publisher, pages, url}
# Extra fields (edition, isbn, note) are carried for the DB/other consumers; ISBNs only where verified online.
REFS={
 "HD2011":dict(author="P.M. Holt & M.W. Daly",title="A History of the Sudan: From the Coming of Islam to the Present Day",edition="6th ed.",publisher="Routledge (Pearson/Longman)",year="2011",url=HD,isbn="978-1-4058-7445-8"),
 "GHA2":dict(author="G. Mokhtar (ed.), UNESCO International Scientific Committee",title="General History of Africa, II: Ancient Civilizations of Africa",publisher="UNESCO / Heinemann / University of California Press",year="1981",url=GHA2,isbn="92-3-101708-X",note="Ch.9 N.M. Sherif (p.245); ch.10 J. Leclant (pp.278–297)"),
 "WELSBY1996":dict(author="Derek A. Welsby",title="The Kingdom of Kush: The Napatan and Meroitic Empires",publisher="British Museum Press",year="1996",url=WEL96,isbn="978-0-7141-0986-2"),
 "WELSBY2002":dict(author="Derek A. Welsby",title="The Medieval Kingdoms of Nubia: Pagans, Christians and Muslims along the Middle Nile",publisher="British Museum Press",year="2002",url=WEL02,isbn="0-7141-1947-4",note="URL is a review record (J. African History)"),
 "OFAHEY2008":dict(author="R.S. O'Fahey",title="The Darfur Sultanate: A History",publisher="Hurst / Columbia University Press",year="2008",url=OF08,isbn="978-0-231-70038-2 (Columbia); 978-1-85065-853-5 (Hurst)"),
 "OFAHEY_SPAULDING1972":dict(author="R.S. O'Fahey & J. Spaulding",title="Hāshim and the Musabba'āt",publisher="Bulletin of the School of Oriental and African Studies",year="1972",url=OFS72),
 "SPAULDING1985":dict(author="Jay Spaulding",title="The Heroic Age in Sinnār",publisher="African Studies Center, Michigan State University (1985); later reissue catalogued by LoC",year="1985",url=SP85),
 "EP1940_NUER":dict(author="E.E. Evans-Pritchard",title="The Nuer: A Description of the Modes of Livelihood and Political Institutions of a Nilotic People",publisher="Clarendon Press",year="1940",url=EP_NUER),
 "EP1940_ANUAK":dict(author="E.E. Evans-Pritchard",title="The Political System of the Anuak of the Anglo-Egyptian Sudan",publisher="Routledge (reissue)",year="1940",url=EP_ANUAK),
 "KERMA_MISSION":dict(author="Swiss-Sudanese Archaeological Mission at Kerma",title="History (Kerma chronology)",publisher="kerma.ch",year="",url=KERMA),
 "WHC1073":dict(author="UNESCO World Heritage Centre",title="Gebel Barkal and the Sites of the Napatan Region",publisher="UNESCO",year="2003",url=WHC1073),
 "WHC1336":dict(author="UNESCO World Heritage Centre",title="Archaeological Sites of the Island of Meroe",publisher="UNESCO",year="2011",url=WHC1336),
 "RILLY_SN22":dict(author="Claude Rilly",title="The QSAP Programme on the Temple of Queen Tiye in Sedeinga",publisher="Sudan & Nubia 22, Sudan Archaeological Research Society",year="2018",url=RILLY),
 "AAR2021":dict(author="African Archaeological Review",title="Seventy Years of Pottery Studies in the Archaeology of Mesolithic and Neolithic Sudan",publisher="Springer",year="2021",url=AAR21),
 "ICG2019":dict(author="International Crisis Group",title="Safeguarding Sudan's Revolution (Africa Report 281)",publisher="ICG",year="2019",url=ICG19),
 "ICG2021":dict(author="International Crisis Group",title="Reversing Sudan's Dangerous Coup",publisher="ICG",year="2021",url=ICG21),
 "UNSC2524":dict(author="UN Security Council",title="Resolution 2524 (2020) [UNITAMS]",publisher="United Nations",year="2020",url=UNSC2524),
 "UNNEWS2023":dict(author="UN News",title="UN chief and officials condemn fighting between Sudanese forces",publisher="United Nations",year="2023",url=UN23),
 "UNSC_SC15257":dict(author="UN Security Council",title="Press Statement on Clashes in Sudan (SC/15257)",publisher="United Nations",year="2023",url=UNSC23),
 "IPC_FRC2024":dict(author="IPC Famine Review Committee",title="Famine Review Committee report: Zamzam camp, North Darfur, Sudan",publisher="IPC",year="2024",url=IPC24),
 "JEDDAH2023":dict(author="US Department of State",title="Jeddah Declaration of Commitment to Protect the Civilians of Sudan",publisher="US Department of State",year="2023",url=JEDDAH),
 "UNSC1996":dict(author="UN Security Council",title="Resolution 1996 (2011) [UNMISS]",publisher="United Nations",year="2011",url=UNSC1996),
 "ICG2014":dict(author="International Crisis Group",title="South Sudan: A Civil War by Any Other Name (Africa Report 217)",publisher="ICG",year="2014",url=ICG14),
 "RARCSS2018":dict(author="IGAD (text via Peace Accords Matrix, Univ. of Notre Dame)",title="Revitalised Agreement on the Resolution of the Conflict in the Republic of South Sudan",publisher="IGAD",year="2018",url=RARCSS),
 "ACCORD2020":dict(author="ACCORD, Conflict Trends",title="The Formation of the Revitalized Transitional Government of National Unity in South Sudan",publisher="ACCORD",year="2020",url=ACCORD20),
}
for v,t,y in [("III","Africa from the Seventh to the Eleventh Century",""),("IV","Africa from the Twelfth to the Sixteenth Century",""),("V","Africa from the Sixteenth to the Eighteenth Century",""),("VI","Africa in the Nineteenth Century until the 1880s",""),("VII","Africa under Colonial Domination 1880–1935",""),("VIII","Africa since 1935","")]:
    REFS["GHA"+v]=dict(author="UNESCO International Scientific Committee",title=f"General History of Africa, {v}: {t}",publisher="UNESCO",year="",url=GHA(v),note="Volume-level citation; chapters not checked")
def _auto_id(u):
    import re,urllib.parse
    if "wikipedia.org/wiki/" in u:
        slug=urllib.parse.unquote(u.split("/wiki/")[1]); return "WP:"+slug, dict(author="Wikipedia contributors",title=slug.replace("_"," "),publisher="Wikipedia",year="",url=u,note="Secondary/starting-point link")
    if "wikidata.org/wiki/" in u:
        q=u.rsplit("/",1)[1]; return "WD:"+q, dict(author="Wikidata",title=q+" (coordinates)",publisher="Wikimedia",year="",url=u)
    if "pleiades.stoa.org/places/" in u:
        n=u.rstrip("/").rsplit("/",1)[1]; return "PL:"+n, dict(author="Pleiades gazetteer",title="Place "+n,publisher="ISAW, NYU",year="",url=u)
    return None,None
for _k in list(REFS): REFS[_k].setdefault("pages","")

def apply3(D):
    url2id={r["url"]:k for k,r in REFS.items()}
    for d in D:
        ids=[]
        for u in d["sources"]:
            k=url2id.get(u)
            if not k:
                k,r=_auto_id(u)
                if not k: raise ValueError("No source ID for "+u)
                if k not in REFS: r.setdefault("pages",""); REFS[k]=r; url2id[u]=k
            if k not in ids: ids.append(k)
        d["sources"]=ids
        miss=[e for e in d["key_events"] if e not in AR_EVENTS]
        if miss: raise ValueError("Missing Arabic for: "+repr(miss))
        d["key_events_ar"]=[AR_EVENTS[e] for e in d["key_events"]]
    return D

def finalize(json_path="data/periods.json",js_path="data/periods.js"):
    import json
    data=json.load(open(json_path,encoding="utf-8"))
    used=sorted({s for p in data["periods"] for s in p["sources"]})
    for _r in REFS.values(): _r.setdefault("lang","en"); _r.setdefault("pages","")
    data["meta"]["sources"]={k:REFS[k] for k in sorted(set(used)|{k for k in REFS if not k.startswith(("WP:","WD:","PL:"))})}
    json.dump(data,open(json_path,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    open(js_path,"w",encoding="utf-8").write("window.HISTO="+json.dumps(dict(meta=data["meta"],periods=data["periods"]),ensure_ascii=False)+";")

AR_EVENTS={
"Wavy-line pottery among the earliest ceramics in Africa":"فخار الخطوط المتموجة من أقدم الفخار في أفريقيا",
"Fishing/hunting settlements along the Nile near Khartoum":"مستوطنات صيد الأسماك والقنص على ضفاف النيل قرب الخرطوم",
"Domesticated cattle, sheep and goat at Esh-Shaheinab":"أبقار وضأن وماعز مستأنسة في الشهيناب",
"Trade with Predynastic/Early Dynastic Egypt":"تجارة مع مصر في عصر ما قبل الأسرات والأسرات المبكرة",
"Qustul elite cemetery":"جبانة النخبة في قسطل",
"Pastoralist culture contemporary with Kerma":"ثقافة رعوية معاصرة لكرمة",
"Western Deffufa mud-brick temple":"معبد الدفوفة الغربية المبني من الطوب اللبن",
"Largest African state outside Egypt in the 2nd millennium BCE":"أكبر دولة أفريقية خارج مصر في الألف الثاني قبل الميلاد",
"Sacked by Thutmose I c.1500 BCE":"نهبها تحتمس الأول نحو 1500 ق.م",
"Swiss mission phases: Early Kerma c.2450–2050, Middle c.2050–1750, Classic c.1750–1480 BCE (Final Kerma to c.1450)":"مراحل البعثة السويسرية: كرمة المبكرة نحو 2450–2050، والوسطى نحو 2050–1750، والكلاسيكية نحو 1750–1480 ق.م (وكرمة المتأخرة حتى نحو 1450)",
"Viceroy of Kush administers Nubia":"نائب الملك في كوش يدير النوبة",
"Temples at Jebel Barkal, Soleb, Abu Simbel":"معابد في جبل البركل وصولب وأبو سمبل",
"Alara, then Kashta (c.760–750 BCE); Kushites in Upper Egypt c.750":"ألارا ثم كاشتا (نحو 760–750 ق.م)؛ الكوشيون في صعيد مصر نحو 750",
"Peye (Piye/'Piankhi') reign from c.751 BCE; Victory Stela; conquest of Egypt c.728/727":"حكم بيي (بيا/«بعنخي») منذ نحو 751 ق.م؛ لوحة النصر؛ فتح مصر نحو 728/727",
"Shabaka from c.713 BCE founds 25th Dynasty rule over all Egypt":"شباكا منذ نحو 713 ق.م يؤسس حكم الأسرة الخامسة والعشرين على مصر كلها",
"Shabataka (Shebitku) c.700–690; Taharqa 690–664 BCE (cenotaph/pyramid at Nuri)":"شبتاكا (شبتكو) نحو 700–690؛ طهارقا 690–664 ق.م (ضريحه الرمزي/هرمه في نوري)",
"Tanwetamani (Tanoutamon) 664–c.656; Assyrian sack of Thebes 663; Kushite withdrawal":"تانوت أماني 664–نحو 656؛ نهب الآشوريين لطيبة 663؛ انسحاب الكوشيين",
"Atlanarsa 653–643, Senkamanisken 643–623, Anlamani 623–593, Aspelta 593–568 BCE":"أتلانرسا 653–643، سنكامانيسكن 643–623، أنلاماني 623–593، أسبلتا 593–568 ق.م",
"Psamtik II's expedition captures Napata (GHA: 591 BCE; widely dated 593 BCE)":"حملة بسماتيك الثاني تستولي على نبتة (تاريخ أفريقيا العام: 591 ق.م؛ ويُؤرَّخ على نطاق واسع بـ593 ق.م)",
"Royal burials at El-Kurru then Nuri; burial shift to Meroe c.270 BCE":"المدافن الملكية في الكرو ثم نوري؛ انتقال الدفن إلى مروي نحو 270 ق.م",
"Ergamenes/Arkamani (3rd c. BCE), friendly relations with Ptolemaic Egypt":"أرجامنيس/أركاماني (القرن الثالث ق.م)، علاقات ودية مع مصر البطلمية",
"Queen Shanakdakhete (c.170–160 BCE): among earliest Meroitic hieroglyphic inscriptions (Naqa)":"الملكة شنكداخيتي (نحو 170–160 ق.م): من أقدم النقوش المروية الهيروغليفية (النقعة)",
"Taniydamani (late 2nd c. BCE): first long Meroitic texts":"تانيدأماني (أواخر القرن الثاني ق.م): أول النصوص المروية الطويلة",
"Iron working at Meroe; Meroitic script transliterated by Griffith 1909, language still not understood":"صناعة الحديد في مروي؛ نقحرة الخط المروي على يد غريفيث 1909، ولا تزال اللغة غير مفهومة",
"Kandakes Amanirenas and Amanishakheto; Prince/King Akinidad; war with Rome: Napata taken by Petronius 23 BCE (GHA), Treaty of Samos 21/20 BCE":"الكنداكتان أماني ريناس وأماني شاخيتو؛ الأمير/الملك أكينيداد؛ الحرب مع روما: بترونيوس يستولي على نبتة 23 ق.م (تاريخ أفريقيا العام)، ومعاهدة ساموس 21/20 ق.م",
"Natakamani & Amanitore (GHA: c.12 BCE–12 CE; dating debated): Naqa Lion Temple, Amara, restoration of Napata":"نتكاماني وأماني تيري (تاريخ أفريقيا العام: نحو 12 ق.م–12 م؛ والتأريخ موضع جدل): معبد الأسد في النقعة، وعمارة، وترميم نبتة",
"Collapse by time of Ezana of Aksum's campaign 'against the Nubas' (c.mid-4th c. CE)":"الانهيار بحلول حملة عيزانا ملك أكسوم «على النوبة» (نحو منتصف القرن الرابع الميلادي)",
"Post-Meroitic royal tumuli at Ballana and Qustul":"تلال المدافن الملكية لما بعد العهد المروي في بلانة وقسطل",
"Christianised c.543 CE":"اعتنقت المسيحية نحو 543 م",
"Merged into Makuria in the 7th century":"اندمجت في المقرة في القرن السابع",
"Repulsed Arab armies at Dongola 651/652":"صد الجيوش العربية عند دنقلا 651/652",
"Baqt treaty with Egypt":"معاهدة البقط مع مصر",
"Faras cathedral frescoes":"جداريات كاتدرائية فرس",
"Decline under Mamluk pressure, 14th c.":"الانحدار تحت ضغط المماليك، القرن الرابع عشر",
"Christian kingdom on the Blue/White Nile":"مملكة مسيحية على النيل الأزرق/الأبيض",
"Capital Soba":"العاصمة سوبا",
"Fell to Funj/Abdallab c.1504":"سقطت في يد الفونج/العبدلاب نحو 1504",
"Founded by Amara Dunqas 1504":"أسسها عمارة دنقس 1504",
"Islamisation and Sufi orders":"انتشار الإسلام والطرق الصوفية",
"Conquered by Ottoman-Egyptian army 1821":"فتحها الجيش التركي المصري 1821",
"Holt & Daly: Funj suzerainty over Upper Nubia (above 3rd Cataract) incl. vassal-kingdom of Dongola; 'Abdallab recognised as paramount chiefs of the Arabs":"هولت وديلي: سيادة الفونج على النوبة العليا (جنوب الشلال الثالث) بما فيها مملكة دنقلا التابعة؛ والاعتراف بالعبدلاب شيوخاً أعلى للعرب",
"Invasion by Muhammad Ali's forces 1820–21":"غزو قوات محمد علي 1820–1821",
"Khartoum founded as capital c.1824":"تأسيس الخرطوم عاصمةً نحو 1824",
"Slave and ivory trade expansion":"توسع تجارة الرقيق والعاج",
"Muhammad Ahmad declares himself Mahdi 1881":"محمد أحمد يعلن نفسه المهدي 1881",
"Fall of Khartoum, death of Gordon 1885":"سقوط الخرطوم ومقتل غوردون 1885",
"Khalifa Abdallahi rules":"حكم الخليفة عبد الله",
"Battle of Omdurman 1898; Umm Diwaykarat 1899":"معركة أم درمان 1898؛ أم دبيكرات 1899",
"Condominium Agreement 19 Jan 1899":"اتفاقية الحكم الثنائي 19 يناير 1899",
"Gezira Scheme 1925":"مشروع الجزيرة 1925",
"Southern Policy":"سياسة الجنوب",
"Self-government 1953":"الحكم الذاتي 1953",
"Independence 1 January 1956":"الاستقلال 1 يناير 1956",
"PM Ismail al-Azhari, then Abdallah Khalil":"رئيس الوزراء إسماعيل الأزهري ثم عبد الله خليل",
"Coup Nov 1958":"انقلاب نوفمبر 1958",
"October Revolution 1964 ends rule":"ثورة أكتوبر 1964 تنهي الحكم",
"Civilian governments; First Sudanese Civil War continues":"حكومات مدنية؛ استمرار الحرب الأهلية السودانية الأولى",
"May 1969 coup":"انقلاب مايو 1969",
"Addis Ababa Agreement 1972 ends first civil war":"اتفاقية أديس أبابا 1972 تنهي الحرب الأهلية الأولى",
"September Laws 1983; Second Civil War begins":"قوانين سبتمبر 1983؛ اندلاع الحرب الأهلية الثانية",
"April 1985 uprising":"انتفاضة أبريل 1985",
"Swar al-Dahab transitional council":"المجلس الانتقالي برئاسة سوار الذهب",
"PM Sadiq al-Mahdi 1986–89":"رئيس الوزراء الصادق المهدي 1986–1989",
"30 June 1989 coup":"انقلاب 30 يونيو 1989",
"Darfur war from 2003; ICC warrants 2009":"حرب دارفور منذ 2003؛ مذكرات المحكمة الجنائية الدولية 2009",
"Comprehensive Peace Agreement 2005":"اتفاقية السلام الشامل 2005",
"South Sudan secedes 9 July 2011":"انفصال جنوب السودان 9 يوليو 2011",
"Protests from Dec 2018; Bashir ousted 11 Apr 2019":"احتجاجات منذ ديسمبر 2018؛ الإطاحة بالبشير 11 أبريل 2019",
"Sovereignty Council; PM Abdalla Hamdok":"مجلس السيادة؛ رئيس الوزراء عبد الله حمدوك",
"Military coup 25 Oct 2021":"الانقلاب العسكري 25 أكتوبر 2021",
"Constitutional Document signed 17 Aug 2019; Hamdok PM; cabinet 8 Sep 2019 (ICG)":"توقيع الوثيقة الدستورية 17 أغسطس 2019؛ حمدوك رئيساً للوزراء؛ تشكيل الحكومة 8 سبتمبر 2019 (مجموعة الأزمات الدولية)",
"UNITAMS created by UNSC res. 2524, 3 Jun 2020":"إنشاء بعثة يونيتامس بقرار مجلس الأمن 2524، 3 يونيو 2020",
"Fighting erupts 15 April 2023":"اندلاع القتال 15 أبريل 2023",
"Mass displacement; famine declared in parts of Darfur 2024":"نزوح جماعي؛ إعلان المجاعة في أجزاء من دارفور 2024",
"Government relocates to Port Sudan":"انتقال الحكومة إلى بورتسودان",
"Jeddah Declaration on protection of civilians, 11 May 2023":"إعلان جدة لحماية المدنيين، 11 مايو 2023",
"IPC Famine Review Committee: famine plausibly ongoing in Zamzam camp, July 2024 (published 1 Aug 2024)":"لجنة مراجعة المجاعة التابعة للتصنيف المرحلي المتكامل: المجاعة مرجحة الاستمرار في معسكر زمزم، يوليو 2024 (نُشر في 1 أغسطس 2024)",
"Early recorded dynasty of Darfur (dates uncertain)":"أسرة حاكمة مبكرة مدونة في دارفور (التواريخ غير مؤكدة)",
"Ruled Darfur and Wadai before the Keira":"حكموا دارفور ووداي قبل الكيرا",
"Keira dynasty from Jabal Marra; founder Sulayman (Solongdungu) – O'Fahey dates the sultanate c.1650–1916":"أسرة الكيرا من جبل مرة؛ المؤسس سليمان (سولونج) – يؤرخ أوفاهي السلطنة بنحو 1650–1916",
"Expansion into Kordofan under Muhammad Tayrab c.1785":"التوسع في كردفان في عهد محمد تيراب نحو 1785",
"Capital fixed at al-Fashir c.1790/91 under 'Abd al-Rahman":"تثبيت العاصمة في الفاشر نحو 1790/1791 في عهد عبد الرحمن",
"Conquered by al-Zubayr Rahma 1874":"فتحها الزبير رحمة 1874",
"Ali Dinar rules autonomously":"علي دينار يحكم حكماً ذاتياً",
"Annexed by Anglo-Egyptian Sudan 1916":"ضمها السودان الإنجليزي المصري 1916",
"Nuba Mountains kingdom; tributary to Funj/Darfur at times":"مملكة في جبال النوبة؛ تابعة بالخراج للفونج/دارفور أحياناً",
"Incorporated into Condominium administration":"أُدمجت في إدارة الحكم الثنائي",
"Founded by Nyikang (tradition)":"أسسها نيكانغ (بحسب الرواية التقليدية)",
"Royal seat at Fashoda":"المقر الملكي في فشودة",
"Holt & Daly: range formerly reached Aba Island (mid-19th c.); raided Arab settlements down the White Nile until early Turco-Egyptian period":"هولت وديلي: امتد نطاقهم سابقاً حتى جزيرة أبا (منتصف القرن التاسع عشر)؛ وأغاروا على مستوطنات العرب على مجرى النيل الأبيض حتى مطلع العهد التركي المصري",
"Tradition ascribes the Funj foundation to a Shilluk war-band":"تنسب الرواية التقليدية تأسيس دولة الفونج إلى عصبة محاربين من الشلك",
"First Civil War 1955–72":"الحرب الأهلية الأولى 1955–1972",
"Second Civil War 1983–2005":"الحرب الأهلية الثانية 1983–2005",
"Referendum Jan 2011":"الاستفتاء يناير 2011",
"Independence 9 July 2011; UNMISS created by UNSC res. 1996 (8 Jul 2011)":"الاستقلال 9 يوليو 2011؛ إنشاء بعثة أونميس بقرار مجلس الأمن 1996 (8 يوليو 2011)",
"Civil war from 15 Dec 2013 (ICG 2014)":"الحرب الأهلية منذ 15 ديسمبر 2013 (مجموعة الأزمات الدولية 2014)",
"R-ARCSS signed 12 Sep 2018":"توقيع الاتفاقية المنشطة لحل النزاع في جنوب السودان 12 سبتمبر 2018",
"Revitalised Transitional Government of National Unity formed 22 Feb 2020 (ACCORD)":"تشكيل حكومة الوحدة الوطنية الانتقالية المنشطة 22 فبراير 2020 (أكورد)",
"Unification c.3100 BCE":"التوحيد نحو 3100 ق.م",
"Giza pyramids":"أهرامات الجيزة",
"Fortresses at the Second Cataract (Buhen, Semna)":"قلاع عند الشلال الثاني (بوهن، سمنة)",
"Conquest of Kush":"فتح كوش",
"Ramesses II":"رمسيس الثاني",
"26th Dynasty; Psamtik II's expedition takes Napata (GHA II: 591 BCE; often 593 BCE)":"الأسرة السادسة والعشرون؛ حملة بسماتيك الثاني تستولي على نبتة (تاريخ أفريقيا العام، المجلد الثاني: 591 ق.م؛ وكثيراً ما تُؤرَّخ بـ593 ق.م)",
"Greek dynasty; contacts with Meroe":"أسرة يونانية؛ صلات مع مروي",
"Petronius' punitive campaign captures Napata 23 BCE after Meroitic sack of Aswan (GHA II)":"حملة بترونيوس التأديبية تستولي على نبتة 23 ق.م بعد نهب المرويين لأسوان (تاريخ أفريقيا العام، المجلد الثاني)",
"Treaty of Samos 21/20 BCE; frontier at Hiera Sycaminos (Maharraqa)":"معاهدة ساموس 21/20 ق.م؛ الحدود عند هيرا سيكامينوس (المحرقة)",
"Arab conquest 641":"الفتح العربي 641",
"Fatimid Cairo 969":"القاهرة الفاطمية 969",
"Campaigns against Makuria":"حملات على المقرة",
"Muhammad Ali invades Sudan 1820":"محمد علي يغزو السودان 1820",
"Co-domini of Sudan 1899":"شريكا الحكم الثنائي في السودان 1899",
"Aswan High Dam; Nubian displacement & Wadi Halfa flooding 1964":"السد العالي في أسوان؛ تهجير النوبيين وإغراق وادي حلفا 1964",
"D'mt kingdom in Eritrea/Tigray":"مملكة دعمت في إريتريا/تيغراي",
"Christianity under Ezana c.330s":"المسيحية في عهد عيزانا نحو ثلاثينيات القرن الرابع",
"Campaign against Meroe/Noba c.350":"حملة على مروي/النوبة نحو 350",
"Lalibela rock-hewn churches":"كنائس لاليبلا المنحوتة في الصخر",
"Gondar period 1636–1769":"عهد غوندار 1636–1769",
"Battle of Gallabat vs Mahdists 1889":"معركة القلابات ضد المهدويين 1889",
"Adwa 1896":"عدوة 1896",
"GERD on Blue Nile (construction from 2011)":"سد النهضة على النيل الأزرق (بدء البناء 2011)",
"Italian colony 1890":"مستعمرة إيطالية 1890",
"Independence 1993":"الاستقلال 1993",
"Islam adopted 11th c.":"اعتناق الإسلام في القرن الحادي عشر",
"Idris Alooma 16th c.":"إدريس ألوما في القرن السادس عشر",
"Rival and neighbour of Darfur":"منافسة دارفور وجارتها",
"French conquest 1909–12":"الغزو الفرنسي 1909–1912",
"Independence 1960":"الاستقلال 1960",
"Hosts Sudanese refugees from 2003 and 2023":"تستضيف لاجئين سودانيين منذ 2003 و2023",
"Trans-Saharan trade in Libya":"التجارة عبر الصحراء في ليبيا",
"Independence 1951":"الاستقلال 1951",
"Avungara-ruled states straddling Sudan/Congo/CAR":"دول يحكمها الأفونغارا تمتد عبر السودان والكونغو وأفريقيا الوسطى",
"Incense trade":"تجارة البخور",
"Influence on D'mt/Aksum":"التأثير في دعمت/أكسوم",
"First Hijra to Aksum c.615":"الهجرة الأولى إلى أكسوم (الحبشة) نحو 615",
"Abbasid trade via Red Sea":"التجارة العباسية عبر البحر الأحمر",
"Ottoman Habesh province port from 16th c.":"ميناء ولاية الحبش العثمانية منذ القرن السادس عشر",
"Superseded by Port Sudan (opened 1909)":"حلّت محلها بورتسودان (افتُتحت 1909)",
"Kingdom of Saudi Arabia 1932":"المملكة العربية السعودية 1932",
"Jeddah talks on Sudan war 2023":"محادثات جدة بشأن حرب السودان 2023",
"Blemmyes (GHA II: 'customarily identified with the Bedja tribes') raid Upper Egypt; suppressed under Probus (276–282 CE)":"البليميون (تاريخ أفريقيا العام، المجلد الثاني: «يُطابَقون عادةً مع قبائل البجة») يغيرون على صعيد مصر؛ قُمعوا في عهد بروبوس (276–282 م)",
"After Meroe's fall the Nobades push the Blemmyes ('Bega or Buga') into the eastern desert":"بعد سقوط مروي دفع النوباديون البليميين («البجة أو البوجة») إلى الصحراء الشرقية",
"Recognised by medieval Muslim writers as distinct from Nubians, Arabs and 'Sudan'":"ميّزهم الكتّاب المسلمون في العصور الوسطى عن النوبة والعرب و«السودان»",
"Camel-nomads of the Red Sea Hills; gradual Islamisation and varying arabisation":"رعاة إبل رحّل في تلال البحر الأحمر؛ أسلمة تدريجية وتعريب متفاوت",
"'Ababda (north) Arabic-speaking; 18th c. southward expansion; Hadendowa in Taka (Gash) by early 19th c.":"العبابدة (في الشمال) يتحدثون العربية؛ توسع نحو الجنوب في القرن الثامن عشر؛ الهدندوة في التاكا (القاش) بحلول مطلع القرن التاسع عشر",
"Nabtab ruling clan of the Banu 'Amir claims Ja'ali descent":"النابتاب، العشيرة الحاكمة لبني عامر، يدّعون النسب الجعلي",
"Founded by 'Abdallah Jamma' (Rufa'a) at the Blue/White Nile confluence, late 15th c.":"أسسها عبد الله جمّاع (من رفاعة) عند ملتقى النيلين الأزرق والأبيض، أواخر القرن الخامس عشر",
"Prospered from tolls on desert nomads":"ازدهرت من المكوس المفروضة على رحّل البادية",
"Recognised by Funj sultans as paramount chiefs of the Arabs":"اعترف بهم سلاطين الفونج شيوخاً أعلى للعرب",
"Capital Qarri, later Halfayat al-Muluk; an 'Abdallabi chief ruled Quz Rajab on the Atbara":"العاصمة قرّي ثم حلفاية الملوك؛ وحكم شيخ عبدلابي قوز رجب على نهر عطبرة",
"Tribal kingdom between the Atbara confluence and the Sabaluqa Gorge from the 16th c.":"مملكة قبلية بين ملتقى عطبرة وخانق السبلوقة منذ القرن السادس عشر",
"Royal clan the Sa'dab; Mirafab kingdom at Berber to the north":"العشيرة الملكية السعداب؛ ومملكة الميرفاب في بربر إلى الشمال",
"Shendi became the chief commercial centre of the eastern Bilad al-Sudan by early 19th c., under Makk Nimr":"أصبحت شندي المركز التجاري الرئيسي لبلاد السودان الشرقية بحلول مطلع القرن التاسع عشر، في عهد المك نمر",
"Exiled Keira faction contesting Kordofan with Funj and Darfur, late 17th–18th c.":"فرع منفي من الكيرا نازع الفونج ودارفور على كردفان، أواخر القرن السابع عشر–القرن الثامن عشر",
"Isawi dislodges Funj (Ghudiyat) administration c.1734":"عيساوي يطرد إدارة الفونج (الغديات) نحو 1734",
"Hashim b. 'Isawi retakes Kordofan c.1772; ousted by Funj 1782":"هاشم بن عيساوي يستعيد كردفان نحو 1772؛ ويطرده الفونج 1782",
"Darfur's Muhammad Tayrab conquers Kordofan c.1785":"محمد تيراب سلطان دارفور يفتح كردفان نحو 1785",
"Group of tribes without central kingship, mostly in Bahr al-Ghazal floodplains, some east of the White Nile (Holt & Daly)":"مجموعة قبائل بلا ملكية مركزية، معظمها في سهول بحر الغزال الفيضية وبعضها شرق النيل الأبيض (هولت وديلي)",
"Cattle pastoralism; culturally close to the Nuer, together a Nilotic subdivision (Evans-Pritchard 1940)":"رعي الأبقار؛ قريبون ثقافياً من النوير، ويشكلون معهم فرعاً نيلياً (إيفانز-بريتشارد 1940)",
"Self-name Nath; c.200,000 people in the 1930s (Evans-Pritchard)":"يسمّون أنفسهم «ناث»؛ نحو 200,000 نسمة في ثلاثينيات القرن العشرين (إيفانز-بريتشارد)",
"Swamps and savannah on both sides of the Nile south of the Sobat/Bahr al-Ghazal junction and along both tributaries":"المستنقعات والسافانا على جانبي النيل جنوب ملتقى السوباط وبحر الغزال وعلى ضفتي الرافدين",
"Seasonal movement between villages and dry-season cattle camps":"تنقل موسمي بين القرى ومعسكرات الماشية في موسم الجفاف",
"Shilluk-speaking (Luo) Nilotic people (Evans-Pritchard 1940)":"شعب نيلي يتحدث لغة من مجموعة الشلك (اللوو) (إيفانز-بريتشارد 1940)",
"Studied in Evans-Pritchard, The Political System of the Anuak (1940)":"دُرسوا في كتاب إيفانز-بريتشارد «النظام السياسي للأنواك» (1940)",
}

# ---------------- Pass 4: era index (data/eras/index.json) ----------------
def era_id(name):
    import re,unicodedata
    s=unicodedata.normalize("NFKD",name).encode("ascii","ignore").decode()
    return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")

def write_eras_index(json_path="data/periods.json",ar_js="data/i18n_ar.js",out="data/eras/index.json"):
    import json,re,os
    P=json.load(open(json_path,encoding="utf-8"))["periods"]
    js=open(ar_js,encoding="utf-8").read()
    m=re.search(r"names:(\{.*?\})\s*,\s*\n?\s*\w+:",js,re.S)
    names=json.loads(m.group(1)) if m else {}
    os.makedirs(os.path.dirname(out),exist_ok=True)
    idx=[dict(id=era_id(p["name"]),name_en=p["name"],name_ar=names.get(p["name"]),stream=p["stream"],start=p["start"],end=p["end"],
              dating_note=p.get("dating_note",""),file=f"data/eras/{era_id(p['name'])}.json") for p in P]
    assert len({i["id"] for i in idx})==len(idx)
    json.dump(dict(meta=dict(generated_by="research_patch.write_eras_index",years="negative=BCE; 2026=present",
        id_rule="ASCII slug of periods.json name; stable unless the English name changes",count=len(idx)),eras=idx),
        open(out,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    return idx

# ---------------- Pass 4b: language-tagged extra sources + era files ----------------
REFS.update({
 "ZH_EMB_HIST2020":dict(author="中华人民共和国驻苏丹大使馆 (PRC Embassy in Sudan)",title="苏丹历史漫谈 (Notes on Sudanese history)",publisher="sd.china-embassy.gov.cn",year="2020",url="https://sd.china-embassy.gov.cn/nwksd/202007/t20200707_6756590.htm",lang="zh",note="Government popular text; not academic"),
 "ZH_EMB_PYR2020":dict(author="中华人民共和国驻苏丹大使馆 (PRC Embassy in Sudan)",title="鲜为人知的苏丹金字塔群 (Sudan's little-known pyramids)",publisher="sd.china-embassy.gov.cn",year="2020",url="https://sd.china-embassy.gov.cn/nwksd/202009/t20200925_6756615.htm",lang="zh",note="Government popular text; internally inconsistent on Meroe capital date"),
 "BRE_AES":dict(author="В. В. Орлов (V.V. Orlov)",title="Англо-египетский Судан (Anglo-Egyptian Sudan)",publisher="Большая российская энциклопедия (Great Russian Encyclopedia)",year="",url="https://old.bigenc.ru/world_history/text/1821574",lang="ru"),
 "RU_HIST1992":dict(author="Ю. М. Кобищанов, Г. И. Смирнова, Д. А. Макаров и др.; отв. ред. В. С. Кошелев",title="История Судана в новое и новейшее время",publisher="Наука, Москва",year="1992",url="https://bigenc.ru/b/istoriia-sudana-v-novoe-i-no-969aa6",isbn="5-02-017341-X",lang="ru",note="Bibliographic record (BRE) only; text not read"),
 "SFDAS_HCS2017":dict(author="C. Rilly, V. Francigny, M. Maillot, B. François, O. Nicoloso",title="Histoire et civilisations du Soudan, de la Préhistoire à nos jours",publisher="Soleb / Bleu autour / SFDAS",year="2017",url="https://sfdas.com/IMG/pdf/histoire_et_civilisations_du_soudan_15_bd.pdf",isbn="978-2-918157-24-3",lang="fr",note="Free PDF; ToC shows 'Groupe C et royaume de Kerma 2450-1450', 'Groupe A, Pré-Kerma 3500-2500'"),
 "FR_MUSEE_MEROE":dict(author="Ministère de la Culture (France) / Musée national du Soudan (virtual)",title="Méroé et les royaumes médiévaux",publisher="archeologie.culture.gouv.fr",year="",url="https://archeologie.culture.gouv.fr/soudan-museum/fr/meroe-et-les-royaumes-medievaux",lang="fr"),
 "DAI_MUSAWWARAT":dict(author="Deutsches Archäologisches Institut (KAAK) / Humboldt-Universität zu Berlin",title="Musawwarat es-Sufra, Sudan (Musawwarat-Projekt)",publisher="DAI",year="",url="https://www.dainst.org/forschung/projekte/musawwarat-es-sufra-sudan/5625",lang="de"),
 "NAGA_PROJ":dict(author="Staatliches Museum Ägyptischer Kunst München",title="Das Grabungsprojekt | Naga",publisher="naga-projekt.de",year="",url="https://naga-projekt.de/das-grabungsprojekt/",lang="de"),
})
for _k,_r in REFS.items(): _r.setdefault("pages",""); _r.setdefault("lang","en")

# Curated era content. Only claims found in the cited sources this session. Arabic = translation of the English.
ERA={
"kingdom-of-kerma":dict(
 geopolitics_en="Rival of Egypt; the Middle Kingdom fixed its southern frontier at Semna; Kerma was sacked by Thutmose I c.1500 BCE.",
 geopolitics_ar="منافسة لمصر؛ ثبّتت الدولة الوسطى حدودها الجنوبية عند سمنة؛ ونهب تحتمس الأول كرمة نحو 1500 ق.م.",
 culture_dominance_en="Indigenous Nubian urban culture: deffufa temples and royal tumuli in the Classic phase (kerma.ch).",
 culture_dominance_ar="ثقافة حضرية نوبية محلية: معابد الدفوفة والمدافن الملكية الركامية في المرحلة الكلاسيكية.",
 economy_en=None,economy_ar=None,sources=["KERMA_MISSION","GHA2","SFDAS_HCS2017"],
 power=[dict(actor="Kerma",score=None,flag="no source gives a comparative power measure"),dict(actor="Middle/New Kingdom Egypt",score=None,flag="unscored")]),
"kingdom-of-kush-napatan-period":dict(
 geopolitics_en="Kushite kings ruled Egypt as the 25th Dynasty; Shabaka 'brought the entire Nile valley as far as the Delta under the empire of Kush' (GHA II). Assyria sacked Thebes 663 BCE and the Kushites withdrew; Psamtik II captured Napata (591/593 BCE).",
 geopolitics_ar="حكم ملوك كوش مصر بوصفهم الأسرة الخامسة والعشرين؛ وأخضع شباكا «وادي النيل كله حتى الدلتا لإمبراطورية كوش» (تاريخ أفريقيا العام II). ونهبت آشور طيبة 663 ق.م فانسحب الكوشيون؛ واستولى بسماتيك الثاني على نبتة (591/593 ق.م).",
 culture_dominance_en="Strong Egyptian religious and funerary influence (Amun cult at Jebel Barkal, pyramids at El-Kurru and Nuri).",
 culture_dominance_ar="تأثير ديني وجنائزي مصري قوي (عبادة آمون في جبل البركل، وأهرامات الكرو ونوري).",
 economy_en="Agriculture and herding developed; gold mining an important activity (PRC Embassy text, popular source).",
 economy_ar="تطور الزراعة والرعي؛ وكان تعدين الذهب نشاطاً مهماً (نص سفارة الصين، مصدر تبسيطي).",
 sources=["GHA2","WHC1073","ZH_EMB_PYR2020"],
 power=[dict(actor="Kush (25th Dynasty, c.713–664 BCE)",score=0.9,basis="GHA II: Shabaka brought the entire Nile valley to the Delta under Kush",method="editorial ordinal: 0.9 = ruler of the whole named region"),
        dict(actor="Assyria",score=None,flag="unscored; defeated Kush in Egypt per GHA II but no comparative measure"),
        dict(actor="Saite Egypt (26th Dyn.)",score=None,flag="unscored")]),
"kingdom-of-kush-meroitic-period":dict(
 geopolitics_en="After Petronius took Napata (23 BCE), the Treaty of Samos (21/20 BCE) renounced Roman tribute and set the frontier at Hiera Sycaminos (GHA II). Naga is described as Meroe's southernmost city and a 'powerful rival' of Ptolemaic and Roman Egypt (Naga project). Collapse by the time of Ezana's campaign, c. mid-4th c. CE.",
 geopolitics_ar="بعد استيلاء بترونيوس على نبتة (23 ق.م) تخلّت معاهدة ساموس (21/20 ق.م) عن الجزية الرومانية وحدّدت الحدود عند هيرا سيكامينوس (تاريخ أفريقيا العام II). ويصف مشروع النقعة النقعةَ بأنها أقصى مدن مروي جنوباً، ومروي بأنها «منافس قوي» لمصر البطلمية والرومانية. وانهارت المملكة بحلول حملة عيزانا نحو منتصف القرن الرابع الميلادي.",
 culture_dominance_en="Local innovations: Meroitic writing, official cult of indigenous gods such as the lion-god Apedemak, ruling queens (Kandakes) (French national-museum text). Naga combines African, Egyptian and Hellenistic elements (Naga project).",
 culture_dominance_ar="ابتكارات محلية: الكتابة المروية، والعبادة الرسمية لآلهة محلية مثل الإله الأسد أباداماك، والملكات الحاكمات (الكنداكات). وتجمع النقعة بين عناصر أفريقية ومصرية وهلنستية.",
 economy_en="Iron working at Meroe (large slag heaps, WHC/GHA); Red Sea trade with Greek merchants (PRC Embassy text); great hafir reservoirs (DAI Musawwarat).",
 economy_ar="صناعة الحديد في مروي (أكوام خبث كبيرة)؛ والتجارة عبر البحر الأحمر مع التجار الإغريق (نص سفارة الصين)؛ وخزانات الحفير الكبرى (مشروع المصورات).",
 sources=["GHA2","WHC1336","NAGA_PROJ","DAI_MUSAWWARAT","FR_MUSEE_MEROE","ZH_EMB_HIST2020"],
 power=[dict(actor="Meroe/Kush",score=None,flag="sources describe Meroe as a 'powerful rival' of Egypt (Naga project) but give no measure"),
        dict(actor="Roman Egypt",score=None,flag="unscored")]),
"funj-sultanate-of-sennar":dict(
 geopolitics_en="Suzerain over Upper Nubia above the Third Cataract, including the vassal kingdom of Dongola; Lower Nubia nominally under Ottoman Egypt. 'Abdallab recognised as paramount chiefs of the Arabs; Kordofan contested with Darfur (Holt & Daly).",
 geopolitics_ar="سيادة على النوبة العليا جنوب الشلال الثالث، بما فيها مملكة دنقلا التابعة؛ والنوبة السفلى تابعة اسمياً لمصر العثمانية. واعتُرف بالعبدلاب شيوخاً أعلى للعرب؛ وتنازعت السلطنة كردفان مع دارفور (هولت وديلي).",
 culture_dominance_en="Islamisation and Sufi orders; Arab genealogical identity (Ja'ali/'Abbasi, Juhayna) spreading among riverain peoples (Holt & Daly).",
 culture_dominance_ar="انتشار الإسلام والطرق الصوفية؛ وانتشار الهوية النسبية العربية (الجعلية/العباسية، جهينة) بين سكان ضفاف النيل (هولت وديلي).",
 economy_en="North–south route Sennar–Egypt and west–east route Darfur–Suakin; Shendi the main market by c.1800; staples millet and dammur cloth used as currency, foreign silver for large deals; slaves of pre-eminent importance in trade (Holt & Daly).",
 economy_ar="طريق شمالي–جنوبي بين سنار ومصر، وطريق غربي–شرقي بين دارفور وسواكن؛ وشندي السوق الرئيسية نحو 1800؛ والذرة وقماش الدمور وسيلتا تبادل، والفضة الأجنبية للصفقات الكبيرة؛ وللرقيق أهمية بارزة في التجارة (هولت وديلي).",
 sources=["HD2011","SPAULDING1985"],
 power=[dict(actor="Funj Sultanate",score=None,flag="suzerainty attested (Holt & Daly) but no comparative measure"),dict(actor="Darfur",score=None,flag="unscored"),dict(actor="Ottoman Egypt",score=None,flag="unscored")]),
"abdallab-chiefdom-funj-vassal":dict(
 geopolitics_en="Vassal paramount chiefs under the Funj, centred at Qarri, later Halfayat al-Muluk; controlled Quz Rajab on the Atbara (Holt & Daly).",
 geopolitics_ar="شيوخ أعلى تابعون للفونج، مركزهم قرّي ثم حلفاية الملوك؛ وسيطروا على قوز رجب على نهر عطبرة (هولت وديلي).",
 culture_dominance_en=None,culture_dominance_ar=None,
 economy_en="Wealth from tolls levied on desert nomads during their annual migration (Holt & Daly).",
 economy_ar="ثروة من المكوس المفروضة على رحّل البادية في دورتهم السنوية (هولت وديلي).",
 sources=["HD2011"],power=[dict(actor="'Abdallab",score=None,flag="unscored")]),
"ja-aliyyin-kingdom-sa-dab-funj-vassal":dict(
 geopolitics_en="Tribal kingdom of the Sa'dab between the Atbara confluence and the Sabaluqa Gorge; Shendi under Makk Nimr was autonomous before 1821 (Holt & Daly).",
 geopolitics_ar="مملكة قبلية للسعداب بين ملتقى عطبرة وخانق السبلوقة؛ وكانت شندي في عهد المك نمر مستقلة ذاتياً قبل 1821 (هولت وديلي).",
 culture_dominance_en=None,culture_dominance_ar=None,
 economy_en="Shendi, where the two trade axes met, was the main commercial centre of the eastern Bilad al-Sudan by the early 19th century (Holt & Daly).",
 economy_ar="كانت شندي، ملتقى محوري التجارة، المركز التجاري الرئيسي لبلاد السودان الشرقية بحلول مطلع القرن التاسع عشر (هولت وديلي).",
 sources=["HD2011"],power=[]),
"sultanate-of-darfur-keira":dict(
 geopolitics_en="Wars with Wadai in the west; eastward expansion into Kordofan c.1785; Kordofan lost after 1821; conquered by al-Zubayr 1874 (O'Fahey 2008 ToC; Holt & Daly).",
 geopolitics_ar="حروب مع وداي غرباً؛ وتوسع شرقاً في كردفان نحو 1785؛ وفقدان كردفان بعد 1821؛ وفتحها الزبير 1874.",
 culture_dominance_en="Muslim Fur dynasty claiming 'Abbasi ancestry (Holt & Daly).",
 culture_dominance_ar="أسرة فوراوية مسلمة تدّعي النسب العباسي (هولت وديلي).",
 economy_en="The Forty Days' Road (Darb al-arba'in) from Kubayh to Asyut in Egypt; slave raiding and trading (Holt & Daly; O'Fahey ToC).",
 economy_ar="درب الأربعين من كوبيه إلى أسيوط في مصر؛ وغزو الرقيق والاتجار بهم (هولت وديلي؛ فهرس أوفاهي).",
 sources=["OFAHEY2008","HD2011"],power=[dict(actor="Darfur",score=None,flag="unscored")]),
"beja-red-sea-hills-peoples":dict(
 geopolitics_en="Separated from the Nile valley by the Red Sea Hills; Suakin looked to the Red Sea and Arabia (Holt & Daly).",
 geopolitics_ar="تفصلهم تلال البحر الأحمر عن وادي النيل؛ وكانت سواكن متجهة نحو البحر الأحمر والجزيرة العربية (هولت وديلي).",
 culture_dominance_en="Islamised, with varying arabisation, often limited to claiming an Arab pedigree (Holt & Daly).",
 culture_dominance_ar="أسلموا مع تعريب متفاوت يقتصر أحياناً على ادعاء نسب عربي (هولت وديلي).",
 economy_en="Camel nomadism; some sedentarisation linked to the modern Gash and Tokar agricultural schemes (Holt & Daly).",
 economy_ar="رعي الإبل؛ مع بعض الاستقرار المرتبط بمشروعات القاش وطوكر الزراعية الحديثة (هولت وديلي).",
 sources=["HD2011","GHA2"],power=[]),
"shilluk-kingdom":dict(
 geopolitics_en="Raided Arab settlements down the White Nile and met northern neighbours 'on equal terms' until firearms and steamers (Holt & Daly).",
 geopolitics_ar="أغاروا على مستوطنات العرب على النيل الأبيض وواجهوا جيرانهم الشماليين «على قدم المساواة» حتى ظهور الأسلحة النارية والبواخر (هولت وديلي).",
 culture_dominance_en=None,culture_dominance_ar=None,economy_en=None,economy_ar=None,sources=["HD2011"],
 power=[dict(actor="Shilluk",score=None,flag="'equal terms' with northern neighbours is qualitative only")]),
"anglo-egyptian-sudan-condominium":dict(
 geopolitics_en="Declared a joint possession (condominium) of Britain and Egypt in January 1899 and in practice turned into a British colony; Egypt's parliament denounced the 1899 agreement on 15 Oct 1951 (BRE, Orlov).",
 geopolitics_ar="أُعلن السودان في يناير 1899 ملكاً مشتركاً (حكماً ثنائياً) لبريطانيا ومصر وتحول فعلياً إلى مستعمرة بريطانية؛ وألغى البرلمان المصري اتفاقية 1899 في 15 أكتوبر 1951 (الموسوعة الروسية الكبرى، أورلوف).",
 culture_dominance_en=None,culture_dominance_ar=None,economy_en=None,economy_ar=None,sources=["BRE_AES","HD2011"],
 power=[dict(actor="Britain",score=None,flag="BRE: de facto colony - qualitative"),dict(actor="Egypt",score=None,flag="unscored")]),
"war-in-sudan-saf-vs-rsf":dict(
 geopolitics_en="SAF–RSF fighting from 15 April 2023; US–Saudi facilitated Jeddah Declaration (11 May 2023); IPC found famine plausible in Zamzam camp (July 2024).",
 geopolitics_ar="قتال بين القوات المسلحة السودانية وقوات الدعم السريع منذ 15 أبريل 2023؛ وإعلان جدة بتيسير أمريكي سعودي (11 مايو 2023)؛ ووجد التصنيف المرحلي المتكامل أن المجاعة مرجحة في معسكر زمزم (يوليو 2024).",
 culture_dominance_en=None,culture_dominance_ar=None,economy_en=None,economy_ar=None,
 sources=["UNNEWS2023","JEDDAH2023","IPC_FRC2024"],power=[dict(actor="SAF",score=None,flag="ongoing war; no defensible score"),dict(actor="RSF",score=None,flag="ongoing war; no defensible score")]),
}

def write_era_files(json_path="data/periods.json"):
    import json
    data=json.load(open(json_path,encoding="utf-8")); idx={e["id"]:e for e in json.load(open("data/eras/index.json",encoding="utf-8"))["eras"]}
    keys=["geopolitics","culture_dominance","economy"]
    for p in data["periods"]:
        i=era_id(p["name"]); c=ERA.get(i,{})
        rec=dict(id=i,name_en=p["name"],name_ar=idx[i]["name_ar"],stream=p["stream"],start=p["start"],end=p["end"],dating_note=p["dating_note"],
                 events=[dict(en=e,ar=a) for e,a in zip(p["key_events"],p["key_events_ar"])],capitals=p["capitals"])
        flags=[]
        for k in keys:
            for l in ("en","ar"):
                rec[f"{k}_{l}"]=c.get(f"{k}_{l}")
            if not c.get(f"{k}_en"): flags.append(f"{k}: no source-backed text yet")
        rec["regional_power"]=c.get("power",[]) or []
        if not rec["regional_power"]: flags.append("regional_power: no actors scored")
        srcs=list(dict.fromkeys(c.get("sources",[])+p["sources"]))
        rec["sources"]=srcs; rec["source_langs"]=sorted({REFS[s]["lang"] for s in srcs})
        rec["flags"]=flags; rec["curated"]=bool(c)
        json.dump(rec,open(f"data/eras/{i}.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
    unknown=set(ERA)-set(idx); assert not unknown,unknown

# ---------------- Pass 4c: lens comparison ----------------
# Divergences observed directly in non-English sources read this session (agree/conflict vs main dataset).
KNOWN_DIVERGENCES=[
 dict(era="kingdom-of-kerma",source="SFDAS_HCS2017",lang="fr",claim="Groupe C et royaume de Kerma 2450–1450",main="-2450/-1480 (+Final Kerma to c.1450 in key_events)",status="agree"),
 dict(era="a-group-lower-nubia",source="SFDAS_HCS2017",lang="fr",claim="Groupe A, Pré-Kerma 3500–2500",main="-3800/-2900",status="conflict",note="French synthesis brackets later start/end"),
 dict(era="kingdom-of-kush-meroitic-period",source="FR_MUSEE_MEROE",lang="fr",claim="Méroïtic dynasty takes power c.270 BCE",main="start -270",status="agree"),
 dict(era="kingdom-of-kush-meroitic-period",source="FR_MUSEE_MEROE",lang="fr",claim="Méroé succombe vers 270 apr. J.-C. sous les assauts des Noubas (from the West)",main="end c.350; collapse by time of Ezana's campaign (GHA II)",status="conflict",note="end date and agent (Noba vs Aksum) differ"),
 dict(era="kingdom-of-kush-meroitic-period",source="FR_MUSEE_MEROE",lang="fr",claim="Amanirénas fought Petronius in a war of 25–21 BCE",main="Napata taken 23 BCE, Samos 21/20 (GHA II); which kandake is unresolved",status="partial",note="French text names Amanirenas outright"),
 dict(era="kingdom-of-kush-meroitic-period",source="NAGA_PROJ",lang="de",claim="Naga Blütezeit 200 v. Chr.–250 n. Chr.",main="no Naga-specific dates",status="no-conflict"),
 dict(era="kingdom-of-kush-napatan-period",source="ZH_EMB_HIST2020",lang="zh",claim="公元前530年左右迁都麦罗埃 (capital moved to Meroe c.530 BCE); Psamtik II sacked Napata 591 BCE",main="burial shift to Meroe c.270 BCE; GHA: Aspelta first attested Meroe sovereign",status="partial",note="capital vs royal burial distinction; 591 matches GHA"),
 dict(era="kingdom-of-kerma",source="ZH_EMB_HIST2020",lang="zh",claim="公元前1700年建立了库施王国(首都在科尔马) (Kush kingdom founded 1700 BCE with capital at Kerma)",main="-2450 start",status="conflict"),
 dict(era="kingdom-of-kush-meroitic-period",source="ZH_EMB_HIST2020",lang="zh",claim="公元350年，库施被阿克苏姆王国所消灭 (destroyed by Aksum 350 CE)",main="end c.350",status="agree"),
 dict(era="kingdom-of-kush-napatan-period",source="ZH_EMB_PYR2020",lang="zh",claim="约前950年摆脱埃及统治独立 (independent of Egypt c.950 BCE); 'Meroe' also given as capital from c.760 in another passage",main="start -800 (display); WHC: Napatan 900–270",status="partial",note="source internally inconsistent"),
 dict(era="anglo-egyptian-sudan-condominium",source="BRE_AES",lang="ru",claim="Англо-египетский Судан — название Судана в 1899–1951",main="1899–1956",status="partial",note="BRE ends the name at Egypt's 1951 denunciation; main runs to independence"),
]

def compare_lenses(out="data/eras/comparison.json"):
    import json,glob,os
    idx={e["id"]:e for e in json.load(open("data/eras/index.json",encoding="utf-8"))["eras"]}
    lens={}
    for f in sorted(glob.glob("db/lens_*.json")):
        lang=os.path.basename(f)[5:-5]
        try: lens[lang]=json.load(open(f,encoding="utf-8"))
        except Exception as e: lens[lang]={"_error":str(e)}
    auto=[]
    for lang,L in lens.items():
        items=L if isinstance(L,list) else L.get("items",L.get("sources",[])) if isinstance(L,dict) else []
        for it in items if isinstance(items,list) else []:
            eras=it.get("era_ids") or it.get("eras") or ([it["era_id"]] if it.get("era_id") else [])
            for e in eras:
                m=idx.get(e); 
                if not m: auto.append(dict(lang=lang,era=e,status="unknown-era-id",source=it.get("id"))); continue
                s,en=it.get("start"),it.get("end")
                st="no-dates" if s is None and en is None else ("agree" if (s in (None,m["start"]) and en in (None,m["end"])) else "conflict")
                auto.append(dict(lang=lang,era=e,source=it.get("id"),lens_start=s,lens_end=en,main_start=m["start"],main_end=m["end"],status=st))
    json.dump(dict(meta=dict(lens_files=sorted(lens),note="auto = date comparison against db/lens_*.json; known = manually read divergences"),
                   known=KNOWN_DIVERGENCES,auto=auto),open(out,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    return len(lens),len(auto)

# ---------------- Pass 5: priority eras (Kush, Christian Nubia, Turkiyya, Mahdiyya, independence, 2019) ----------------
REFS.update({
 "GHA6_CH14":dict(author="H.A. Ibrahim (with B.A. Ogot)",title="The Sudan in the nineteenth century (General History of Africa VI, ch.14)",publisher="UNESCO",year="",pages="pp.356ff",url=GHA("VI"),lang="en",note="Full text read (sahistory.org.za PDF mirror)"),
 "GHA7_CH4":dict(author="H.A. Ibrahim (based on a contribution by Abbas I. Ali)",title="African initiatives and resistance in North-East Africa (General History of Africa VII, ch.4)",publisher="UNESCO",year="",pages="pp.63ff (Mahdiyya pp.73–78)",url=GHA("VII"),lang="en"),
 "GHA8":dict(author="A.A. Mazrui (ed.)",title="General History of Africa VIII: Africa since 1935 – Sudan passages ('North Africa and the Horn', pp.148–150; economy and political-succession passages)",publisher="UNESCO",year="",pages="pp.148–150 and others",url=GHA("VIII"),lang="en",note="Page numbers only for the 'The Sudan' section; other passages located by text search"),
 "GHA2_CH12":dict(author="K. Michałowski",title="The spreading of Christianity in Nubia (General History of Africa II, ch.12)",publisher="UNESCO",year="1981",pages="pp.326–340",url=GHA2,lang="en"),
})
for _r in REFS.values(): _r.setdefault("pages",""); _r.setdefault("lang","en")

ERA.update({
"a-group-lower-nubia":dict(
 geopolitics_en="Flourished c.3100 BCE, contemporary with Egypt's First Dynasty; remains found between the First Cataract and Batn el-Hagar (GHA II ch.9).",
 geopolitics_ar="ازدهرت نحو 3100 ق.م، معاصرة للأسرة المصرية الأولى؛ وعُثر على بقاياها بين الشلال الأول وبطن الحجر (تاريخ أفريقيا العام II، الفصل 9).",
 culture_dominance_en="Non-literate culture known only archaeologically; fine thin pottery; A-Group-type pottery also found farther south (e.g. near Omdurman) (GHA II ch.9).",
 culture_dominance_ar="ثقافة غير كتابية معروفة أثرياً فقط؛ فخار رقيق ناعم؛ ووُجد فخار من نمط المجموعة أ جنوباً أيضاً (مثلاً قرب أم درمان).",
 economy_en="Copper tools (earliest metal tools found in Sudan) and imported Egyptian pottery; a period of prosperity and population growth (GHA II ch.9).",
 economy_ar="أدوات نحاسية (أقدم الأدوات المعدنية المكتشفة في السودان) وفخار مصري مستورد؛ فترة رخاء وزيادة في السكان (تاريخ أفريقيا العام II، الفصل 9).",
 sources=["GHA2","SFDAS_HCS2017"],power=[]),
"c-group-lower-nubia":dict(
 geopolitics_en="Appeared in Lower Nubia late in the Old Kingdom or First Intermediate Period; lasted until the full Egyptianisation of Nubia in the 16th c. BCE; northern limit at Kubanieh North (GHA II ch.9).",
 geopolitics_ar="ظهرت في النوبة السفلى أواخر الدولة القديمة أو في عصر الانتقال الأول؛ واستمرت حتى التمصير الكامل للنوبة في القرن السادس عشر ق.م؛ وحدها الشمالي عند كوبانية الشمالية.",
 culture_dominance_en="Chalcolithic culture with its own burial traditions; brick chapels against tombs; continued despite increasing contact with Egypt (GHA II ch.9).",
 culture_dominance_ar="ثقافة من العصر النحاسي الحجري بتقاليد دفن خاصة؛ مصليات من الطوب ملاصقة للمقابر؛ واستمرت رغم تزايد الاتصال بمصر.",
 economy_en=None,economy_ar=None,sources=["GHA2","SFDAS_HCS2017"],power=[]),
"noba-x-group-ballana-culture":dict(
 geopolitics_en="Post-Meroitic struggle between the Blemmyes and the Nobades; the Nobades won control of the Nile valley and pushed the Blemmyes into the eastern desert; Leclant inclines to see the Nobades as the lords of Ballana and Qustul (GHA II ch.10, 12).",
 geopolitics_ar="صراع ما بعد مروي بين البليميين والنوباديين؛ سيطر النوباديون على وادي النيل ودفعوا البليميين إلى الصحراء الشرقية؛ ويميل لوكلان إلى أن النوباديين هم سادة بلانة وقسطل.",
 culture_dominance_en="Rich royal tumuli at Ballana (excavated by Emery, 1938); some Christian presence before the official conversion is argued from Faras (dating contested) (GHA II ch.12).",
 culture_dominance_ar="مدافن ملكية ركامية غنية في بلانة (نقّب عنها إمري 1938)؛ ويُستدل من فرس على وجود مسيحي قبل التنصير الرسمي (والتأريخ موضع خلاف).",
 economy_en=None,economy_ar=None,sources=["GHA2","GHA2_CH12"],power=[]),
"nobadia":dict(
 geopolitics_en="Kingdom of the Nobadae from Philae to the Second Cataract, capital Faras (Pachoras); Byzantine diplomacy active in the 5th–6th c.; Persian invasion of Egypt (616) stopped at Nubia's northern frontier, with evidence of Sassanid raids; later united with Makuria (GHA II ch.12).",
 geopolitics_ar="مملكة النوباديين من فيلة إلى الشلال الثاني، وعاصمتها فرس (باخوراس)؛ ونشطت الدبلوماسية البيزنطية في القرنين الخامس والسادس؛ وتوقف الغزو الفارسي لمصر (616) عند حدود النوبة الشمالية مع أدلة على غارات ساسانية؛ ثم اتحدت لاحقاً مع المقرة.",
 culture_dominance_en="Official Monophysite conversion by the mission of the priest Julianos sent by Empress Theodora; Christianity had already spread among the people from Egypt; the sovereigns' palace at Faras later became the earliest cathedral (GHA II ch.12).",
 culture_dominance_ar="تنصير رسمي على المذهب المونوفيزي ببعثة القس يوليانوس التي أرسلتها الإمبراطورة ثيودورا؛ وكانت المسيحية قد انتشرت بين الناس من مصر قبل ذلك؛ وتحول قصر الملوك في فرس لاحقاً إلى أقدم كاتدرائية.",
 economy_en="Caravans passing through Aswan carried trade (and beliefs) southward (GHA II ch.12).",
 economy_ar="حملت القوافل المارة بأسوان التجارة (والمعتقدات) نحو الجنوب.",
 sources=["GHA2_CH12","WELSBY2002"],power=[]),
"makuria":dict(
 geopolitics_en="Kingdom centred on Old Dongola from the 6th c.; the baqt agreement with Muslim Egypt, followed by Abdallah ibn Abi Sarh's raid on Dongola in 651–2; Northern and Central Nubia later united into one state (GHA II ch.12).",
 geopolitics_ar="مملكة مركزها دنقلا العجوز منذ القرن السادس؛ واتفاقية البقط مع مصر الإسلامية تلتها غارة عبد الله بن أبي السرح على دنقلا 651–652؛ ثم اتحدت النوبة الشمالية والوسطى في دولة واحدة.",
 culture_dominance_en="Converted to Melkite (Orthodox) Christianity by Justinian's mission (567–70), then adopted Monophysitism between 660 and 700 (King Merkurios, from 697, is credited with introducing it); government nomenclature modelled on Byzantine bureaucracy; Polish excavations at Old Dongola identified churches and the royal palace (GHA II ch.12).",
 culture_dominance_ar="تنصّرت على المذهب الملكاني (الأرثوذكسي) ببعثة جستنيان (567–570) ثم اعتنقت المونوفيزية بين 660 و700 (ويُنسب إدخالها إلى الملك مركوريوس منذ 697)؛ وكانت ألقاب الحكم على نمط البيروقراطية البيزنطية؛ وكشفت الحفريات البولندية في دنقلا العجوز عن كنائس والقصر الملكي.",
 economy_en="Raids did not interrupt the constant trade between Nubia and Muslim Egypt (GHA II ch.12).",
 economy_ar="لم تقطع الغارات التجارة المستمرة بين النوبة ومصر الإسلامية.",
 sources=["GHA2_CH12","WELSBY2002"],power=[]),
"alodia-alwa":dict(
 geopolitics_en="Southernmost of the three Christian Nubian kingdoms by the end of the 6th c. (Nobadia, Makuria, Alodia) (GHA II ch.12).",
 geopolitics_ar="أقصى الممالك النوبية المسيحية الثلاث جنوباً بحلول نهاية القرن السادس (نوباتيا، المقرة، علوة).",
 culture_dominance_en="A Byzantine mission under Bishop Longinos reached Alodia c.580 with Nobadian support and found it already partly converted by the Aksumites (GHA II ch.12).",
 culture_dominance_ar="وصلت بعثة بيزنطية بقيادة الأسقف لونجينوس إلى علوة نحو 580 بدعم من النوباديين، ووجدتها قد تنصرت جزئياً على يد الأكسوميين.",
 economy_en=None,economy_ar=None,sources=["GHA2_CH12","WELSBY2002"],power=[]),
"turkiyya-ottoman-egyptian-rule":dict(
 geopolitics_en="Muhammad 'Ali conquered the disintegrating Funj lands in 1820–1. Ibrahim (GHA VI) calls this the 'first colonial era', ruled by a Turkish-speaking elite in the name of the Ottoman sultan. Egyptian claims of sovereignty by conquest (Shukri's 'theory of the vacuum') are disputed. Resistance included the 1822 revolt (Makk Nimr burned Isma'il at Shendi), the Kassala mutiny of 1865 and Fur risings (Amir Harun 1877–80).",
 geopolitics_ar="فتح محمد علي أراضي الفونج المتفككة في 1820–1821؛ ويسمي إبراهيم (تاريخ أفريقيا العام VI) ذلك «العهد الاستعماري الأول»، إذ حكمته نخبة ناطقة بالتركية باسم السلطان العثماني. وادعاءات السيادة المصرية بحق الفتح («نظرية الفراغ» لشكري) موضع خلاف. ومن صور المقاومة ثورة 1822 (أحرق المك نمر إسماعيلَ في شندي)، وتمرد كسلا 1865، وانتفاضات الفور (الأمير هارون 1877–1880).",
 culture_dominance_en="Rulers known to Sudanese as 'Turks'; government favour to the Shayqiyya and the Khatmiyya order bred rivalries (GHA VI ch.14; GHA VII ch.4).",
 culture_dominance_ar="عرف السودانيون الحكام بـ«الترك»؛ وأثارت محاباة الحكومة للشايقية والطريقة الختمية التنافس.",
 economy_en="Primary aim, per archival studies cited by Ibrahim: Sudanese manpower (slave raids, ghazwas, for the army) and gold, sought around Fazughli without success. Agriculture improved by Egyptian experts. A state monopoly exported indigo, gum, ivory and cattle to Egypt. Heavy cash taxes caused flight and revolt. White Nile slave traffic grew from 1840, with zeribas (forts) in the South (GHA VI ch.14).",
 economy_ar="الهدف الأساسي بحسب الدراسات الأرشيفية التي يستشهد بها إبراهيم: القوى البشرية السودانية (غزوات الرقيق لتجنيدهم في الجيش) والذهب الذي طُلب حول فازوغلي دون جدوى. وطوّر خبراء مصريون الزراعة. وصدّر احتكار حكومي النيلة والصمغ والعاج والماشية إلى مصر. وأدت الضرائب النقدية الباهظة إلى الهجرة والثورات. وتضخمت تجارة الرقيق على النيل الأبيض منذ 1840 مع إقامة الزرائب (الحصون) في الجنوب.",
 sources=["GHA6_CH14","GHA7_CH4","HD2011"],
 power=[dict(actor="Northern Muslim states vs Southern Sudan peoples (on the eve of 1821)",score=None,flag="GHA VI: their powers were 'comparable, if not evenly balanced' – a relative statement, not a numeric score")]),
"mahdist-state-mahdiyya":dict(
 geopolitics_en="A jihad movement that defeated Hicks at Shaykan (5 Nov 1883), took Kordofan, Darfur and Bahr al-Ghazal, and with 'Uthman Digna the east except Suakin; Khartoum fell and Gordon was killed (26 Jan 1885). Under the Khalifa: defeat at Tushki (1889), loss of Tokar (1891) and Kassala (1894), and a long war with Ethiopia that weakened both states. Kitchener's conquest: Atbara (8 Apr 1898), Karari/Omdurman (2 Sep 1898), Umm Diwaykarat (24 Nov 1899) (GHA VII ch.4).",
 geopolitics_ar="حركة جهادية هزمت هكس في شيكان (5 نوفمبر 1883)، واستولت على كردفان ودارفور وبحر الغزال، ثم على الشرق كله عدا سواكن بقيادة عثمان دقنة؛ وسقطت الخرطوم وقُتل غوردون (26 يناير 1885). وفي عهد الخليفة: الهزيمة في توشكي (1889)، وفقدان طوكر (1891) وكسلا (1894)، وحرب طويلة مع إثيوبيا أضعفت الدولتين. ثم فتح كتشنر: عطبرة (8 أبريل 1898)، وكرري/أم درمان (2 سبتمبر 1898)، وأم دبيكرات (24 نوفمبر 1899).",
 culture_dominance_en="Aimed to restore the 'pure and primitive faith of Islam'; followers (Ansar) took the bay'a; the hijra to Jabal Qadir shifted leadership to westerners; institutions based on the Qur'an and Sunna; Mahdist sentiment survived the state (GHA VII ch.4).",
 culture_dominance_ar="سعت إلى إحياء «الإسلام في صفائه الأول»؛ وأدى الأنصار البيعة؛ ونقلت الهجرة إلى جبل قدير القيادة إلى أهل الغرب؛ وقامت المؤسسات على القرآن والسنة؛ وبقيت العاطفة المهدية بعد زوال الدولة.",
 economy_en="Discontent fed by heavy Turkish taxes and by the government's attempts to suppress the slave trade, 'an important source of wealth and the basis of the domestic and agrarian economy' (GHA VII ch.4).",
 economy_ar="غذّى السخطَ ثقلُ الضرائب التركية ومحاولاتُ الحكومة قمع تجارة الرقيق التي كانت «مصدراً مهماً للثروة وأساس الاقتصاد المنزلي والزراعي».",
 sources=["GHA7_CH4","HD2011"],
 power=[dict(actor="Mahdist state (within Sudan, 1885–98)",score=0.9,basis="GHA VII ch.4: 'a powerful and militant state that dominated the Sudan for fourteen years'",method="editorial ordinal: 0.9 = dominant power over the named region"),
        dict(actor="Anglo-Egyptian forces (1896–99)",score=None,flag="GHA VII: victories owed to 'superior armaments' – qualitative")]),
"anglo-egyptian-sudan-condominium":dict(ERA["anglo-egyptian-sudan-condominium"],
 economy_en="Kitchener's railway reached Khartoum, was linked to the Red Sea in 1905 (Port Sudan and Atbara founded), extended to Sennar and reached Kordofan by 1911; a Sennar–Port Sudan line opened in 1924. Egyptian long-staple cotton; the Gezira Scheme irrigated via the Sennar dam; Gash zone; 1929 Nile waters convention (GHA VIII).",
 economy_ar="بلغ خط سكة حديد كتشنر الخرطوم، ورُبط بالبحر الأحمر 1905 (تأسيس بورتسودان وعطبرة)، ومُدّ إلى سنار ثم بلغ كردفان بحلول 1911؛ وافتُتح خط سنار–بورتسودان 1924. والقطن المصري طويل التيلة؛ ومشروع الجزيرة المروي بخزان سنار؛ ومنطقة القاش؛ واتفاقية مياه النيل 1929.",
 culture_dominance_en="Southern Policy developed the South separately: Islamic proselytising banned, Christian missions encouraged, English in mission schools while Arabic became the language of the North (GHA VIII pp.148–150).",
 culture_dominance_ar="طوّرت سياسة الجنوب الإقليمَ الجنوبي بمعزل: حُظر التبشير الإسلامي وشُجعت البعثات المسيحية، واعتمدت مدارس البعثات الإنجليزية بينما صارت العربية لغة الشمال.",
 sources=["BRE_AES","GHA8","HD2011"]),
"independent-sudan-first-parliamentary-period":dict(
 geopolitics_en="The National Unionist Party (successor of the pro-Egyptian Ashikka') won the November 1953 elections but steered toward full independence. Parliament declared independence on 19 Dec 1955, proclaimed on 1 Jan 1956. The Equatoria Corps mutiny of August 1955 began the southern problem (GHA VIII pp.148–150).",
 geopolitics_ar="فاز الحزب الوطني الاتحادي (وريث حزب الأشقاء الموالي لمصر) في انتخابات نوفمبر 1953 لكنه اتجه إلى الاستقلال التام؛ وأعلن البرلمان الاستقلال في 19 ديسمبر 1955 وأُعلن رسمياً في 1 يناير 1956؛ وبدأ تمرد الفرقة الاستوائية في أغسطس 1955 مشكلةَ الجنوب.",
 culture_dominance_en="The two largest religious orders, the Ansar and the Khatmiyya, agreed in Dec 1953 to work for independence (GHA VIII).",
 culture_dominance_ar="اتفقت كبرى الطرق الدينية، الأنصار والختمية، في ديسمبر 1953 على العمل من أجل الاستقلال.",
 economy_en=None,economy_ar=None,sources=["GHA8","HD2011"],power=[]),
"abboud-military-regime":dict(
 geopolitics_en="Ended in 1964 by a civilian-led popular uprising, which GHA VIII calls exceptional in Africa ('political succession after a popular uprising').",
 geopolitics_ar="انتهى في 1964 بانتفاضة شعبية قادها المدنيون، ويصفها تاريخ أفريقيا العام VIII بأنها حالة استثنائية في أفريقيا («تعاقب سياسي إثر انتفاضة شعبية»).",
 culture_dominance_en=None,culture_dominance_ar=None,economy_en=None,economy_ar=None,sources=["GHA8","HD2011"],power=[]),
"nimeiry-era-democratic-republic-of-sudan":dict(
 geopolitics_en="The 1969 coup began in alliance with Sudanese communists; the partners turned on each other and Nimeiri triumphed. Brought down in 1985 by a second popular uprising, after which the military promised and delivered civilian rule within a year (GHA VIII).",
 geopolitics_ar="بدأ انقلاب 1969 بتحالف مع الشيوعيين السودانيين، ثم انقلب الشريكان أحدهما على الآخر وانتصر نميري؛ وأسقطته انتفاضة شعبية ثانية في 1985 وعد الجيش بعدها بعودة الحكم المدني خلال عام ووفى بوعده.",
 culture_dominance_en="The regime executed the thinker Mahmoud Muhammad Taha for apostasy and heresy in 1985 (GHA VIII).",
 culture_dominance_ar="أعدم النظام المفكر محمود محمد طه بتهمة الردة والزندقة في 1985.",
 economy_en=None,economy_ar=None,sources=["GHA8","HD2011"],power=[]),
"transitional-third-parliamentary-period":dict(
 geopolitics_en="After the 1985 uprising the military's promise of restoring democracy within a year was kept, 'though civilian rule did not last' (GHA VIII).",
 geopolitics_ar="بعد انتفاضة 1985 وفى الجيش بوعده بإعادة الديمقراطية خلال عام، «وإن لم يدم الحكم المدني».",
 culture_dominance_en=None,culture_dominance_ar=None,economy_en=None,economy_ar=None,sources=["GHA8","HD2011"],power=[]),
"december-revolution-transition":dict(
 geopolitics_en="Bashir deposed by the military on 11 Apr 2019 after the most sustained civilian protest movement in Sudan's modern history; security forces' attack on protesters on 3 June 2019; 17 Aug 2019 power-sharing deal with an 11-member Sovereign Council; Hamdok PM; UNITAMS created 2020; 25 Oct 2021 coup dissolved the transitional government (ICG; UNSC 2524).",
 geopolitics_ar="أطاح الجيش بالبشير في 11 أبريل 2019 بعد أطول حركة احتجاج مدنية في تاريخ السودان الحديث؛ وهجوم قوات الأمن على المحتجين في 3 يونيو 2019؛ واتفاق تقاسم السلطة في 17 أغسطس 2019 مع مجلس سيادة من 11 عضواً؛ وحمدوك رئيساً للوزراء؛ وإنشاء يونيتامس 2020؛ وانقلاب 25 أكتوبر 2021 الذي حلّ الحكومة الانتقالية.",
 culture_dominance_en=None,culture_dominance_ar=None,
 economy_en="ICG (2019) describes a 'crushing economic crisis' and a 'lopsided, patronage-driven economy' in which the top brass has an interest in clinging to power.",
 economy_ar="تصف مجموعة الأزمات الدولية (2019) «أزمة اقتصادية ساحقة» و«اقتصاداً مختلاً قائماً على المحسوبية» يجعل لكبار الضباط مصلحة في التمسك بالسلطة.",
 sources=["ICG2019","ICG2021","UNSC2524"],power=[]),
})
