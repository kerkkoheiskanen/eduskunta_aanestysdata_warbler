import json
import requests
import pandas as pd
import pickle
from datetime import datetime, timezone

data = pd.read_json("data.json")
data_supp = pd.read_json("data_supp.json")
data_distr = pd.read_json("data_distr.json")
data_main = pd.read_json("data_main.json")


data_cols = ["AanestysId","TekninenAvain","IstuntoTyyppi","IstuntoTila","IstuntoTilaSeliteFI","IstuntoTilaSeliteSV","IstuntoVPVuosi","IstuntoNumero","IstuntoPvm","IstuntoIlmoitettuAlkuaika","IstuntoAlkuaika","IstuntoLoppuaika","IstuntoNimenhuutoaika","KasiteltavaKohtaTekninenAvain","PJTekninenAvain","PJOtsikkoFI","PJOtsikkoSV","PJTila","XmlData","Created","Modified","PuhujaHenkilonumero","ManuaalinenEsto","AttachmentGroupId","Imported"]
data_supp_cols = ["AanestysId","KieliId","IstuntoVPVuosi","IstuntoNumero","IstuntoPvm","IstuntoIlmoitettuAlkuaika","IstuntoAlkuaika","PJOtsikko","AanestysNumero","AanestysAlkuaika","AanestysLoppuaika","AanestysMitatoity","AanestysOtsikko","AanestysLisaOtsikko","PaaKohtaTunniste","PaaKohtaOtsikko","PaaKohtaHuomautus","KohtaKasittelyOtsikko","KohtaKasittelyVaihe","KohtaJarjestys","KohtaTunniste","KohtaOtsikko","KohtaHuomautus","AanestysTulosJaa","AanestysTulosEi","AanestysTulosTyhjia","AanestysTulosPoissa","AanestysTulosYhteensa","Url","AanestysPoytakirja","AanestysPoytakirjaUrl","AanestysValtiopaivaasia","AanestysValtiopaivaasiaUrl","AliKohtaTunniste","Imported"]
data_distr_cols = ["JakaumaId","AanestysId","Ryhma","Jaa","Ei","Tyhjia","Poissa","Yhteensa","Tyyppi","Imported"]
data_main_cols = ["AanestysId","KieliId","IstuntoVPVuosi","IstuntoNumero","IstuntoPvm","IstuntoIlmoitettuAlkuaika","IstuntoAlkuaika","PJOtsikko","AanestysNumero","AanestysAlkuaika","AanestysLoppuaika","AanestysMitatoity","AanestysOtsikko","AanestysLisaOtsikko","PaaKohtaTunniste","PaaKohtaOtsikko","PaaKohtaHuomautus","KohtaKasittelyOtsikko","KohtaKasittelyVaihe","KohtaJarjestys","KohtaTunniste","KohtaOtsikko","KohtaHuomautus","AanestysTulosJaa","AanestysTulosEi","AanestysTulosTyhjia","AanestysTulosPoissa","AanestysTulosYhteensa","Url","AanestysPoytakirja","AanestysPoytakirjaUrl","AanestysValtiopaivaasia","AanestysValtiopaivaasiaUrl","AliKohtaTunniste","Imported"]

data.columns = data_cols
data_supp.columns = data_supp_cols
data_distr.columns = data_distr_cols
data_main.columns = data_main_cols

print("convert some values to numerical type")

# data["AanestysId"] = data["AanestysId"].apply(pd.to_numeric, errors="coerce")
# data_supp["AanestysId"] = data_supp["AanestysId"].apply(pd.to_numeric, errors="coerce")
# data_distr["AanestysId"] = data_distr["AanestysId"].apply(pd.to_numeric, errors="coerce")
# data_distr["Jaa"] = data_distr["Jaa"].apply(pd.to_numeric, errors="coerce")
# data_distr["Ei"] = data_distr["Ei"].apply(pd.to_numeric, errors="coerce")
data_main["AanestysId"] = data_main["AanestysId"].apply(pd.to_numeric, errors="coerce")
data_main["AanestysTulosJaa"] = data_main["AanestysTulosJaa"].apply(pd.to_numeric, errors="coerce")
data_main["AanestysTulosEi"] = data_main["AanestysTulosEi"].apply(pd.to_numeric, errors="coerce")
data_main["IstuntoVPVuosi"] = data_main["IstuntoVPVuosi"].apply(pd.to_numeric, errors="coerce")

print("fix data with empty columns")

# data.dropna()
# data_supp.dropna()
# data_distr.dropna()
data_main.dropna()

#merged = pd.merge(data_supp, data_distr, on="AanestysId")

print("data main:")
print(data_main.info()) 

most_voted = data_main.loc[
    (data_main["IstuntoVPVuosi"] > 2014) &
    (data_main['KohtaOtsikko'].str.contains('Välikysymys', case=False) == False) &
    (data_main['KohtaOtsikko'].str.contains('työtaistel', case=False) == True) |
    (data_main['KohtaOtsikko'].str.contains('saimaan', case=False) == True) |
    (data_main['KohtaOtsikko'].str.contains('raskau', case=False) == True) |
    (data_main['KohtaOtsikko'].str.contains('tartuntatauti', case=False) == True) &
    (data_main['KohtaOtsikko'].str.contains('talousarvio', case=False) == False)]

for row in most_voted.iterrows():
    print(row.AanestysId, row.KohtaOtsikko)

# for id in most_voted["AanestysId"]:
#     print(id)

print(len(most_voted["KohtaOtsikko"]))

# turvallisuuslaki = data_supp.loc[data_supp['KohtaOtsikko'].str.contains("potilasturvallisuu", case=False, na=False)]

# for item in turvallisuuslaki["KohtaOtsikko"]:
#     print(item)