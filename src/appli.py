import json
import src.fonctions_analyse.chargement_sources


# Lecture des paramètres du projet
with open("../settings.json") as json_file:
    data = json.load(json_file)

stats, df_charge = src.fonctions_analyse.chargement_sources.chargement_tout(data)
