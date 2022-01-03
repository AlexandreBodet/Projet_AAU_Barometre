"""
Programme principal qui appelle les autres fonctions.
"""
if __name__ == "__main__":
    import json
    import os
    import pandas as pd
    import numpy as np
    from datetime import date
    from src.configuration import configurations
    from src.fonctions_analyse.chargement_sources import chargement_tout
    from src.importation_data.retrieve_hal import api_to_csv
    from src.fonctions_analyse.recuperer_data import enrich_to_csv
    from src.fonctions_analyse.ajouter_apc import ajout_apc
    from src.fonctions_analyse.aligner_data import aligner
    from src.visualisation.graphique import graphique

    step = configurations()  # crée les différents dossiers s'ils n'existent pas et change les settings si besoin

    with open("./settings.json", "r", encoding="utf-8") as json_file:
        donnees = json.load(json_file)

    if donnees["parametres"]["utilise_api_hal"] and step == 0:
        api_to_csv(fichier_hal=donnees["data"]["dois"]["hal_fichier_api"], donnees_api=donnees["api_hal"])
        print("\n[FINI] Récupération des données hal par api\n")

    if step < 1:
        df_charge = chargement_tout(donnees=donnees["data"]["dois"],
                                    recherche_erreur=donnees["parametres"]["recherche_erreurs"],
                                    utilise_api_hal=donnees["parametres"]["utilise_api_hal"])
        print("\n[FINI] Chargement fini\n")
    elif step == 1:
        df_charge = pd.read_csv("./resultats/fichiers_csv/consolider_doi_hal_id.csv", encoding="utf8")

    if step < 2:
        enrich_to_csv(df=df_charge, email=donnees["mail"], match_ref=donnees["data"]["match_ref"],
                      progression_denominateur=100)
        print("\n[FINI] Enrichissement fini\n")
    elif step == 2:
        pd.read_csv("./resultats/fichiers_csv/df_metadonnees.csv", encoding="utf8")

    if donnees["parametres"]["calcul_APC"]:
        if step < 3:
            df_charge = ajout_apc(df=df_charge, data_apc=donnees["data"]["apc_tracking"])
            print("\n[FINI] Ajout apc fini\n")
        elif step == 3:
            df_charge = pd.read_csv("./resultats/fichiers_csv/ajout_apc.csv", encoding="utf8")

    if step < 4:
        df_charge = aligner(referentials=donnees["data"]["match_ref"],
                            choixDomaines=donnees["choixDomaines"])
        print("\n[FINI] Alignement du dataframe fini")
    elif step == 4:
        df_charge = pd.read_csv("./resultats/fichiers_csv/data_complete.csv", encoding="utf8")

    nom_dossier = graphique(df_raw=df_charge, parametres=donnees["parametres"])  # génération des graphiques
    print("\n[FINI] Génération des graphiques fini")

    print("Dossier des images générées : ./resultats/img/" + nom_dossier)
