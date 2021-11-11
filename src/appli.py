import json
from fonctions_analyse.chargement_sources import chargement_tout
from src.importation_data.retrieve_hal import req_to_csv

# Lecture des paramètres du projet
# import sys
# print(sys.path)

with open("../settings.json") as json_file:
    data = json.load(json_file)

req_to_csv(data["hal_fichier_api"])

stats, df_charge = chargement_tout(data, api_hal=True)
