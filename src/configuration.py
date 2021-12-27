import os
import shutil
import json


def configurations():
    """
    Crée les dossiers s'ils n'existent pas, demande à l'utilisateur s'il veut réutiliser des données existantes et s'il veut changer les settings
    """
    garder_donnees = None
    while garder_donnees != "y" and garder_donnees != "n":
        garder_donnees = input(
            "Voulez-vous repartir des données intermédiaires calculées auparavant pour générer les graphiques? [y/n]")
    step = 0

    if garder_donnees == "y":
        with open("./settings.json", "r", encoding="utf-8") as json_file:
            donnees = json.load(json_file)  # ouvre les settings initiaux

        if os.path.isfile("./resultats/fichiers_csv/consolider_doi_hal_id.csv"):
            step = 1
        if os.path.isfile("./resultats/fichiers_csv/df_metadonnees.csv"):
            step = 2
        if donnees["parametres"]["calcul_APC"]:
            if os.path.isfile("./resultats/fichiers_csv/ajout_apc.csv"):
                step = 3
        if os.path.isfile("./resultats/fichiers_csv/data_complete.csv"):
            step = 4

    elif garder_donnees == "n":
        shutil.rmtree("./resultats/fichiers_csv/")  # supprime récursivement le dossier des résultats en csv
        changer_settings = None
        while changer_settings != "y" and changer_settings != "n":
            changer_settings = input("Souhaitez-vous changer les settings/paramètres? [y/n]")
        if changer_settings == "y":
            modification_settings()

    dossiers_data()
    return step


def dossiers_data():
    """
    Crée les dossiers nécessaires s'ils n'existaient pas déjà
    """
    if not os.path.isdir("./data"):
        os.mkdir("./data")
    if not os.path.isdir("./data/dois"):
        os.mkdir("./data/dois")
    if not os.path.isdir("./data/apc_tracking"):
        os.mkdir("./data/apc_tracking")
    if not os.path.isdir("./resultats"):
        os.mkdir("./resultats")
    if not os.path.isdir("./resultats/fichiers_csv"):
        os.mkdir("./resultats/fichiers_csv")
    if not os.path.isdir("./resultats/fichiers_csv/erreurs"):
        os.mkdir("./resultats/fichiers_csv/erreurs")
    if not os.path.isdir("./resultats/img"):
        os.mkdir("./resultats/img")


def modification_settings():
    with open("./settings.json", "r", encoding="utf-8") as json_file:
        donnees = json.load(json_file)  # ouvre les settings initiaux
    print("yes je veux modifier les settings")
    with open("./settings.json", "w", encoding="utf-8") as json_file:
        json.dump(donnees, json_file, ensure_ascii=False, indent=2)  # écrit les settings modifiés
    return None
