import json
from fonctions_analyse.chargement_sources import chargement_tout
from importation_data.retrieve_hal import hal_to_csv

# Lecture des paramètres du projet
import sys
print(sys.path)

hal_to_csv()

with open("../settings.json") as json_file:
    data = json.load(json_file)

stats, df_charge = chargement_tout(data)