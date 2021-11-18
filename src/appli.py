import json
import pandas as pd

from fonctions_analyse.chargement_sources import chargement_tout
from importation_data.retrieve_hal import api_to_csv
from fonctions_analyse.recuperer_data import enrich_to_csv
from fonctions_analyse.ajouter_apc import ajout_apc
from fonctions_analyse.aligner_data import aligner
# Lecture des paramètres du projet
# import sys
# print(sys.path)

with open("../settings.json") as json_file:
    donnees = json.load(json_file)

api_to_csv(fichier_hal=donnees["data"]["dois"]["hal_fichier_api"], query=donnees["query"])

stats, df_charge = chargement_tout(
    donnees=donnees["data"]["dois"], api_hal=True, recherche_erreur=True)

df_charge = enrich_to_csv(df=df_charge, email=donnees["mail"], progression_denominateur=100)

ajout_apc(df=df_charge, data_apc=donnees["data"]["apc_tracking"])

aligner()
