<<<<<<< HEAD
"""
Programme principal qui appelle les autres fonctions.
"""
if __name__ == "__main__":
    import json
    import pandas as pd
    import numpy as np
    from datetime import date
    from src.configuration import dossiers_data
    from src.fonctions_analyse.chargement_sources import chargement_tout
    from src.importation_data.retrieve_hal import api_to_csv
    from src.fonctions_analyse.recuperer_data import enrich_to_csv
    from src.fonctions_analyse.ajouter_apc import ajout_apc
    from src.fonctions_analyse.aligner_data import aligner
    from src.visualisation.graphique import graphique

    # Lecture des paramètres du projet
    # import sys
    # print(sys.path)

    dossiers_data()  # crée les différents dossiers s'ils n'existent pas

    with open("./settings.json") as json_file:
        donnees = json.load(json_file)

    if donnees["parametres"]["utilise_api_hal"]:
        api_to_csv(fichier_hal=donnees["data"]["dois"]["hal_fichier_api"], donnees_api=donnees["api_hal"])
        print('\n[FINI] Récupération des données hal par api\n')

    stats, df_charge = chargement_tout(donnees=donnees["data"]["dois"], recherche_erreur=donnees["parametres"]["recherche_erreurs"],
                                       utilise_api_hal=donnees["parametres"]["utilise_api_hal"])
    print('\n[FINI] Chargement fini\n')

    df_charge = enrich_to_csv(df=df_charge, email=donnees["mail"], match_ref=donnees["data"]["match_ref"], progression_denominateur=100)
    print('\n[FINI] Enrichissement fini\n')

    df_charge = pd.read_csv("./resultats/fichiers_csv/df_metadonnees.csv")
    df_charge = ajout_apc(df=df_charge, data_apc=donnees["data"]["apc_tracking"])
    print('\n[FINI] Ajout apc fini\n')

    df_charge = aligner(df=df_charge, referentials=donnees["data"]["match_ref"], choixDomaines=donnees["choixDomaines"])

    annees = [i for i in range(2010, date.today().year + 1)]
    graphique(df_raw=df_charge, annee=2020, annees=annees, rec_base=False, rec_disciplines=False, rec_genre=False,
              oa_circulaire=False, oa_discipline=False, oa_evolution=False, oa_editeur=False,
              apc_evolution=False, apc_discipline=False, bibliodiversite=True,
              oa_type_evolution=False, domain=True, domain_shs=True, domain_info=True)

    # graphique(df_raw=df_charge, annee=2020, annees=annees)
=======
import json
import pandas as pd
import numpy as np
from datetime import date
from src.configuration import dossiers_data
from src.fonctions_analyse.chargement_sources import chargement_tout
from src.importation_data.retrieve_hal import api_to_csv
from src.fonctions_analyse.recuperer_data import enrich_to_csv
from src.fonctions_analyse.ajouter_apc import ajout_apc
from src.fonctions_analyse.aligner_data import aligner
from src.visualisation.graphique import graphique

# Lecture des paramètres du projet
# import sys
# print(sys.path)

dossiers_data()  # crée les différents dossiers s'ils n'existent pas

with open("./settings.json") as json_file:
    donnees = json.load(json_file)

'''if donnees["parametres"]["utilise_api_hal"]:
    api_to_csv(fichier_hal=donnees["data"]["dois"]["hal_fichier_api"], query=donnees["query"])
    print('\n[FINI] Récupération des données hal par api\n')

stats, df_charge = chargement_tout(donnees=donnees["data"]["dois"], recherche_erreur=donnees["parametres"]["recherche_erreurs"],
                                   utilise_api_hal=donnees["parametres"]["utilise_api_hal"])
print('\n[FINI] Chargement fini\n')

df_charge = enrich_to_csv(df=df_charge, email=donnees["mail"], progression_denominateur=100)
print('\n[FINI] Enrichissement fini\n')

df_charge = pd.read_csv("./resultats/fichiers_csv/df_metadonnees.csv")
df_charge = ajout_apc(df=df_charge, data_apc=donnees["data"]["apc_tracking"])  # une fois que je l'ai chargé, je le commente pour pas que ça le refasse
print('\n[FINI] Ajout apc fini\n')'''

df_charge = aligner(
    df=None, referentials=donnees["data"]["match_ref"], choixDomaines=donnees["choixDomaines"])

annees = [i for i in range(2010, date.today().year + 1)]

graphique(df_raw=df_charge, annee=2020, annees=annees, rec_base=True, rec_disciplines=True, rec_genre=False,
          oa_circulaire=False, oa_discipline=False, oa_evolution=False, oa_editeur=False,
          apc_evolution=False, apc_discipline=False, bibliodiversite=False,
          oa_type_evolution=False, domain=True, domain_shs=True, domain_info=True)
>>>>>>> devV2_laurence
