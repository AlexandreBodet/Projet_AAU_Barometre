import json
from fonctions_analyse.chargement_sources import chargement_tout
from importation_data.retrieve_hal import api_to_csv
from fonctions_analyse.recuperer_data import enrich_to_csv
# Lecture des paramètres du projet
# import sys
# print(sys.path)

with open("../settings.json") as json_file:
    data = json.load(json_file)

api_to_csv(data["hal_fichier_api"])

stats, df_charge = chargement_tout(donnees=data, api_hal=True, recherche_erreur=True)
print(df_charge)
df_charge = enrich_to_csv(df_charge)
#print(df_charge)
