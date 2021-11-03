import json
import fonctions_analyse.consolider_source

# import fonctions_analyse.chargement_data
# import pandas as pd

with open("../settings.json") as json_file:
    data = json.load(json_file)

hal = fonctions_analyse.consolider_source.chargement_hal(data["hal_fichier"])

s

