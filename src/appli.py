import json
from src.fonctions_analyse.chargement_sources import chargement_tout


# Lecture des paramètres du projet
with open("../settings.json") as json_file:
    data = json.load(json_file)

stats, df_charge = chargement_tout(data)
