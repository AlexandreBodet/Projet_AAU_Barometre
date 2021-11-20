import json
import pandas as pd
import numpy as np
from datetime import date
from fonctions_analyse.chargement_sources import chargement_tout
from importation_data.retrieve_hal import api_to_csv
from fonctions_analyse.recuperer_data import enrich_to_csv
from fonctions_analyse.ajouter_apc import ajout_apc
from fonctions_analyse.aligner_data import aligner
from visualisation.graphique import graphique

# Lecture des paramètres du projet
# import sys
# print(sys.path)

with open("../settings.json") as json_file:
    donnees = json.load(json_file)
'''
api_to_csv(fichier_hal=donnees["data"]["dois"]["hal_fichier_api"], query=donnees["query"])

stats, df_charge = chargement_tout(
    donnees=donnees["data"]["dois"], api_hal=True, recherche_erreur=True)

df_charge = enrich_to_csv(df=df_charge, email=donnees["mail"], progression_denominateur=100)

ajout_apc(df=df_charge, data_apc=donnees["data"]["apc_tracking"])

aligner()
'''
df_raw = pd.read_csv("../resultats/fichiers_csv/data_complete.csv", na_filter=False, low_memory=False)
annees = [i for i in range(2016, date.today().year + 1)]
graphique(df_raw=df_raw, annee=2020, disciplinaire=False, circulaire=True, discipline_oa=False, evolution_oa=False,
          oa_editeur=True, comparaison_bases=False, apc_evolution=False, apc_discipline=False, bibliodiversite=False,
          evolution_type_oa=True, annees=annees)
