import json
W="https://en.wikipedia.org/wiki/"
B="https://www.britannica.com/"
def P(name,stream,s,e,prom,events,caps,src,note=""):
    return dict(name=name,stream=stream,start=s,end=e,prominence=prom,key_events=events,
      capitals=[dict(name=c[0],lat=c[1],lon=c[2]) for c in caps],sources=src,dating_note=note)
D=[
# Sudan Nile core
P("Khartoum Mesolithic (Early Khartoum)","Sudan – Middle Nile",-8000,-4900,0.35,["Wavy-line pottery among the earliest ceramics in Africa","Fishing/hunting settlements along the Nile near Khartoum"],[("Early Khartoum site",15.6,32.53)],[W+"Early_Khartoum"],"Approximate; radiocarbon ranges vary"),
P("Khartoum Neolithic (Shaheinab)","Sudan – Middle Nile",-4900,-3800,0.3,["Domesticated cattle, sheep and goat at Esh-Shaheinab"],[("Esh-Shaheinab",16.13,32.53)],[W+"Khartoum_Neolithic"],"Approximate"),
P("A-Group (Lower Nubia)","Sudan – Middle Nile",-3800,-2900,0.35,["Trade with Predynastic/Early Dynastic Egypt","Qustul elite cemetery"],[("Qustul",22.1,31.5)],[W+"A-Group_culture"]),
P("C-Group (Lower Nubia)","Sudan – Middle Nile",-2400,-1550,0.3,["Pastoralist culture contemporary with Kerma"],[("Aniba",22.67,32.03)],[W+"C-Group_culture"]),
P("Kingdom of Kerma","Sudan – Middle Nile",-2500,-1500,0.7,["Western Deffufa mud-brick temple","Largest African state outside Egypt in the 2nd millennium BCE","Sacked by Thutmose I c.1500 BCE"],[("Kerma",19.6,30.41)],[W+"Kerma_culture"],"Kerma culture c.2500–1500 BCE"),
P("Egyptian New Kingdom rule in Nubia","Sudan – Middle Nile",-1500,-1070,0.45,["Viceroy of Kush administers Nubia","Temples at Jebel Barkal, Soleb, Abu Simbel"],[("Jebel Barkal / Napata",18.54,31.83)],[W+"Viceroy_of_Kush"]),
P("Kingdom of Kush – Napatan period","Sudan – Middle Nile",-800,-270,0.85,["Piye conquers Egypt c.727 BCE","25th Dynasty rules Egypt to 656 BCE","Taharqa; pyramids at El-Kurru and Nuri"],[("Napata",18.54,31.83)],[W+"Kingdom_of_Kush",W+"Twenty-fifth_Dynasty_of_Egypt"],"Burial shift to Meroe c.270 BCE"),
P("Kingdom of Kush – Meroitic period","Sudan – Middle Nile",-270,350,0.8,["Meroitic script","Iron working at Meroe","Kandakes (queens) e.g. Amanirenas resists Rome 25–21 BCE","Decline; Aksumite incursion c.350 CE"],[("Meroë",16.94,33.75),("Naqa",16.27,33.27),("Musawwarat es-Sufra",16.42,33.32)],[W+"Meroë",W+"Kingdom_of_Kush",W+"Amanirenas"]),
P("Noba / X-Group (Ballana culture)","Sudan – Middle Nile",350,550,0.4,["Post-Meroitic royal tumuli at Ballana and Qustul"],[("Ballana",22.27,31.58)],[W+"Ballana_culture"]),
P("Nobadia","Sudan – Middle Nile",400,700,0.4,["Christianised c.543 CE","Merged into Makuria in the 7th century"],[("Faras (Pachoras)",22.2,31.48)],[W+"Nobadia"]),
P("Makuria","Sudan – Middle Nile",500,1500,0.7,["Repulsed Arab armies at Dongola 651/652","Baqt treaty with Egypt","Faras cathedral frescoes","Decline under Mamluk pressure, 14th c."],[("Old Dongola",18.22,30.75)],[W+"Makuria",W+"Baqt"],"End date approximate"),
P("Alodia (Alwa)","Sudan – Middle Nile",500,1504,0.55,["Christian kingdom on the Blue/White Nile","Capital Soba","Fell to Funj/Abdallab c.1504"],[("Soba",15.52,32.68)],[W+"Alodia"]),
P("Funj Sultanate of Sennar","Sudan – Middle Nile",1504,1821,0.75,["Founded by Amara Dunqas 1504","Islamisation and Sufi orders","Conquered by Ottoman-Egyptian army 1821"],[("Sennar",13.55,33.62)],[W+"Funj_Sultanate"]),
P("Turkiyya (Ottoman-Egyptian rule)","Sudan – Middle Nile",1821,1885,0.7,["Invasion by Muhammad Ali's forces 1820–21","Khartoum founded as capital c.1824","Slave and ivory trade expansion"],[("Khartoum",15.5,32.56)],[W+"Turco-Egyptian_Sudan",W+"Ottoman_Egyptian_invasion_of_Sudan"]),
P("Mahdist State (Mahdiyya)","Sudan – Middle Nile",1885,1899,0.75,["Muhammad Ahmad declares himself Mahdi 1881","Fall of Khartoum, death of Gordon 1885","Khalifa Abdallahi rules","Battle of Omdurman 1898; Umm Diwaykarat 1899"],[("Omdurman",15.64,32.48)],[W+"Mahdist_State",W+"Battle_of_Omdurman"]),
P("Anglo-Egyptian Sudan (Condominium)","Sudan – Middle Nile",1899,1956,0.75,["Condominium Agreement 19 Jan 1899","Gezira Scheme 1925","Southern Policy","Self-government 1953"],[("Khartoum",15.5,32.56)],[W+"Anglo-Egyptian_Sudan"]),
P("Independent Sudan – First parliamentary period","Sudan – Republic",1956,1958,0.5,["Independence 1 January 1956","PM Ismail al-Azhari, then Abdallah Khalil"],[("Khartoum",15.5,32.56)],[W+"History_of_Sudan_(1956–1969)"]),
P("Abboud military regime","Sudan – Republic",1958,1964,0.5,["Coup Nov 1958","October Revolution 1964 ends rule"],[("Khartoum",15.5,32.56)],[W+"Ibrahim_Abboud",W+"October_1964_Revolution"]),
P("Second parliamentary period","Sudan – Republic",1964,1969,0.45,["Civilian governments; First Sudanese Civil War continues"],[("Khartoum",15.5,32.56)],[W+"History_of_Sudan_(1956–1969)"]),
P("Nimeiry era (Democratic Republic of Sudan)","Sudan – Republic",1969,1985,0.6,["May 1969 coup","Addis Ababa Agreement 1972 ends first civil war","September Laws 1983; Second Civil War begins","April 1985 uprising"],[("Khartoum",15.5,32.56)],[W+"Gaafar_Nimeiry",W+"Addis_Ababa_Agreement_(1972)"]),
P("Transitional & third parliamentary period","Sudan – Republic",1985,1989,0.45,["Swar al-Dahab transitional council","PM Sadiq al-Mahdi 1986–89"],[("Khartoum",15.5,32.56)],[W+"Sadiq_al-Mahdi"]),
P("Al-Bashir / NCP (Ingaz) regime","Sudan – Republic",1989,2019,0.7,["30 June 1989 coup","Darfur war from 2003; ICC warrants 2009","Comprehensive Peace Agreement 2005","South Sudan secedes 9 July 2011"],[("Khartoum",15.5,32.56)],[W+"Omar_al-Bashir",W+"War_in_Darfur",W+"Comprehensive_Peace_Agreement"]),
P("December Revolution & transition","Sudan – Republic",2019,2023,0.55,["Protests from Dec 2018; Bashir ousted 11 Apr 2019","Sovereignty Council; PM Abdalla Hamdok","Military coup 25 Oct 2021"],[("Khartoum",15.5,32.56)],[W+"Sudanese_revolution",W+"2021_Sudanese_coup_d'état"]),
P("War in Sudan (SAF vs RSF)","Sudan – Republic",2023,2026,0.6,["Fighting erupts 15 April 2023","Mass displacement; famine declared in parts of Darfur 2024","Government relocates to Port Sudan"],[("Port Sudan",19.62,37.22),("Khartoum",15.5,32.56)],[W+"Sudanese_civil_war_(2023–present)"],"Ongoing; end=present"),
# Darfur/West
P("Daju kingdom","Sudan – Darfur & Kordofan",1100,1400,0.3,["Early recorded dynasty of Darfur (dates uncertain)"],[("Jebel Marra region",13.0,24.3)],[W+"Daju_people",W+"History_of_Darfur"],"Very approximate"),
P("Tunjur kingdom","Sudan – Darfur & Kordofan",1400,1650,0.3,["Ruled Darfur and Wadai before the Keira"],[("Ain Farah",15.0,24.9)],[W+"Tunjur_people"],"Approximate"),
P("Sultanate of Darfur (Keira)","Sudan – Darfur & Kordofan",1603,1874,0.55,["Founded by Sulayman Solongdungu c.1603","Capital El Fasher from 1791","Conquered by Zubayr Pasha 1874"],[("El Fasher",13.63,25.35)],[W+"Sultanate_of_Darfur"]),
P("Restored Darfur Sultanate (Ali Dinar)","Sudan – Darfur & Kordofan",1898,1916,0.35,["Ali Dinar rules autonomously","Annexed by Anglo-Egyptian Sudan 1916"],[("El Fasher",13.63,25.35)],[W+"Ali_Dinar",W+"Sultanate_of_Darfur"]),
P("Kingdom of Taqali","Sudan – Darfur & Kordofan",1750,1969,0.25,["Nuba Mountains kingdom; tributary to Funj/Darfur at times","Incorporated into Condominium administration"],[("Tegali / Tasi",11.95,31.05)],[W+"Kingdom_of_Taqali"],"Founding c.1750 approximate"),
# South Sudan
P("Shilluk Kingdom","South Sudan – Upper Nile",1490,1861,0.35,["Founded by Nyikang (tradition)","Royal seat at Fashoda"],[("Fashoda (Kodok)",9.88,32.12)],[W+"Shilluk_Kingdom"],"Founding traditional"),
P("Southern Sudan under Condominium / Sudan","South Sudan – Upper Nile",1899,2011,0.35,["First Civil War 1955–72","Second Civil War 1983–2005","Referendum Jan 2011"],[("Juba",4.85,31.58)],[W+"First_Sudanese_Civil_War",W+"Second_Sudanese_Civil_War"]),
P("Republic of South Sudan","South Sudan – Upper Nile",2011,2026,0.4,["Independence 9 July 2011","Civil war 2013–2020","Revitalised peace agreement 2018"],[("Juba",4.85,31.58)],[W+"South_Sudan",W+"South_Sudanese_Civil_War"]),
# Egypt
P("Early Dynastic & Old Kingdom Egypt","Egypt",-3100,-2181,0.8,["Unification c.3100 BCE","Giza pyramids"],[("Memphis",29.84,31.25)],[W+"Old_Kingdom_of_Egypt"]),
P("Middle Kingdom Egypt","Egypt",-2055,-1650,0.7,["Fortresses at the Second Cataract (Buhen, Semna)"],[("Itjtawy",29.4,31.2)],[W+"Middle_Kingdom_of_Egypt"]),
P("New Kingdom Egypt","Egypt",-1550,-1070,0.9,["Conquest of Kush","Ramesses II"],[("Thebes",25.7,32.64)],[W+"New_Kingdom_of_Egypt"]),
P("Late Period / Persian Egypt","Egypt",-664,-332,0.5,["26th Dynasty; Psamtik II raids Napata 593 BCE"],[("Sais",30.96,30.77)],[W+"Late_Period_of_ancient_Egypt"]),
P("Ptolemaic Egypt","Egypt",-305,-30,0.65,["Greek dynasty; contacts with Meroe"],[("Alexandria",31.2,29.92)],[W+"Ptolemaic_Kingdom"]),
P("Roman & Byzantine Egypt","Egypt",-30,641,0.65,["Petronius campaign vs Kush 24 BCE","Treaty of Samos 21/20 BCE"],[("Alexandria",31.2,29.92)],[W+"Egypt_(Roman_province)"]),
P("Islamic Egypt (Rashidun–Fatimid–Ayyubid)","Egypt",641,1250,0.7,["Arab conquest 641","Fatimid Cairo 969"],[("Fustat / Cairo",30.0,31.23)],[W+"Muslim_conquest_of_Egypt",W+"Fatimid_Caliphate"]),
P("Mamluk Sultanate","Egypt",1250,1517,0.7,["Campaigns against Makuria"],[("Cairo",30.04,31.24)],[W+"Mamluk_Sultanate"]),
P("Ottoman Egypt & Muhammad Ali dynasty","Egypt",1517,1882,0.65,["Muhammad Ali invades Sudan 1820"],[("Cairo",30.04,31.24)],[W+"Muhammad_Ali_dynasty"]),
P("British-occupied / Kingdom of Egypt","Egypt",1882,1953,0.55,["Co-domini of Sudan 1899"],[("Cairo",30.04,31.24)],[W+"Kingdom_of_Egypt"]),
P("Republic of Egypt","Egypt",1953,2026,0.65,["Aswan High Dam; Nubian displacement & Wadi Halfa flooding 1964"],[("Cairo",30.04,31.24)],[W+"Aswan_Dam"]),
# Horn
P("Land of Punt / D'mt","Ethiopia & Eritrea (Horn)",-980,-400,0.3,["D'mt kingdom in Eritrea/Tigray"],[("Yeha",14.29,39.02)],[W+"Dʿmt"],"Approximate"),
P("Kingdom of Aksum","Ethiopia & Eritrea (Horn)",100,940,0.7,["Christianity under Ezana c.330s","Campaign against Meroe/Noba c.350"],[("Aksum",14.13,38.72),("Adulis",15.26,39.66)],[W+"Kingdom_of_Aksum",W+"Ezana_of_Axum"]),
P("Zagwe dynasty","Ethiopia & Eritrea (Horn)",900,1270,0.45,["Lalibela rock-hewn churches"],[("Lalibela",12.03,39.04)],[W+"Zagwe_dynasty"],"Start date debated"),
P("Ethiopian Empire (Solomonic)","Ethiopia & Eritrea (Horn)",1270,1974,0.75,["Gondar period 1636–1769","Battle of Gallabat vs Mahdists 1889","Adwa 1896"],[("Gondar",12.6,37.47),("Addis Ababa",9.03,38.74)],[W+"Ethiopian_Empire",W+"Battle_of_Gallabat"]),
P("Derg & Federal Ethiopia","Ethiopia & Eritrea (Horn)",1974,2026,0.6,["GERD on Blue Nile (construction from 2011)"],[("Addis Ababa",9.03,38.74)],[W+"Derg",W+"Grand_Ethiopian_Renaissance_Dam"]),
P("Eritrea (Italian colony → independent)","Ethiopia & Eritrea (Horn)",1890,2026,0.3,["Italian colony 1890","Independence 1993"],[("Asmara",15.32,38.93)],[W+"Eritrea"]),
# Chad/Sahara/Libya
P("Kanem Empire","Chad & Central Sahara",700,1380,0.45,["Islam adopted 11th c."],[("Njimi",14.3,15.6)],[W+"Kanem_Empire"],"Approximate"),
P("Bornu Empire","Chad & Central Sahara",1380,1893,0.5,["Idris Alooma 16th c."],[("Ngazargamu",13.0,11.8)],[W+"Bornu_Empire"]),
P("Wadai Sultanate","Chad & Central Sahara",1635,1912,0.4,["Rival and neighbour of Darfur","French conquest 1909–12"],[("Abéché",13.83,20.83)],[W+"Wadai_Sultanate"]),
P("French Chad → Republic of Chad","Chad & Central Sahara",1900,2026,0.4,["Independence 1960","Hosts Sudanese refugees from 2003 and 2023"],[("N'Djamena",12.13,15.06)],[W+"Chad"]),
P("Garamantes (Fezzan)","Chad & Central Sahara",-500,700,0.3,["Trans-Saharan trade in Libya"],[("Garama (Germa)",26.55,13.08)],[W+"Garamantes"]),
P("Libya (Ottoman, Italian, independent)","Chad & Central Sahara",1551,2026,0.35,["Independence 1951"],[("Tripoli",32.89,13.19)],[W+"History_of_Libya"]),
# Central Africa
P("Zande kingdoms","Central Africa (CAR/Congo border)",1700,1905,0.3,["Avungara-ruled states straddling Sudan/Congo/CAR"],[("Zandeland",4.6,27.0)],[W+"Zande_people"],"Approximate"),
P("Central African Republic (Ubangi-Shari)","Central Africa (CAR/Congo border)",1903,2026,0.3,["Independence 1960"],[("Bangui",4.39,18.56)],[W+"Central_African_Republic"]),
# Red Sea/Arabia
P("Sabaean & South Arabian kingdoms","Red Sea & Arabia",-1000,275,0.45,["Incense trade","Influence on D'mt/Aksum"],[("Ma'rib",15.43,45.33)],[W+"Sabaeans"],"Approximate"),
P("Rise of Islam & Caliphates","Red Sea & Arabia",610,1258,0.75,["First Hijra to Aksum c.615","Abbasid trade via Red Sea"],[("Medina",24.47,39.61),("Baghdad",33.31,44.36)],[W+"Rashidun_Caliphate",W+"Abbasid_Caliphate"]),
P("Suakin – Red Sea port (Beja, Ottoman)","Red Sea & Arabia",1100,1922,0.35,["Ottoman Habesh province port from 16th c.","Superseded by Port Sudan (opened 1909)"],[("Suakin",19.1,37.33)],[W+"Suakin"]),
P("Ottoman Hejaz & Saudi state","Red Sea & Arabia",1517,2026,0.5,["Kingdom of Saudi Arabia 1932","Jeddah talks on Sudan war 2023"],[("Mecca/Riyadh",24.71,46.68)],[W+"Saudi_Arabia",W+"Treaty_of_Jeddah_(2023)"]),
]
json.dump(dict(meta=dict(title="Sudan & Region Histomap dataset",years="negative=BCE; 2026=present",streams=list(dict.fromkeys(p["stream"] for p in D))),periods=D),open("data/periods.json","w"),ensure_ascii=False,indent=1)
open("data/periods.js","w").write("window.HISTO="+json.dumps(dict(periods=D),ensure_ascii=False)+";")
print(len(D))
