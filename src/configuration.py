import os
import shutil
import json


def configurations():
    """
    Crée les dossiers s'ils n'existent pas, demande à l'utilisateur s'il veut réutiliser des données existantes et s'il veut changer les settings
    :return int: étape du dernier fichier récupéré, celui depuis lequel on repart
    """
    garder_donnees = None
    while garder_donnees != "y" and garder_donnees != "n":
        garder_donnees = input(
            "Voulez-vous repartir des données intermédiaires calculées auparavant pour générer les graphiques? [y/n]\n")
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
        if os.path.isdir("./resultats/fichiers_csv"):
            shutil.rmtree("./resultats/fichiers_csv/")  # supprime récursivement le dossier des résultats en csv
        changer_settings = None
        while changer_settings != "y" and changer_settings != "n":
            changer_settings = input("Souhaitez-vous changer les settings/paramètres? [y/n]\n")
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
    """
    Si l'utilisateur le veut, la fonction permet de modifier le fichier settings.json qui a tous les paramètres du projet.
    """
    with open("./settings.json", "r", encoding="utf-8") as json_file:
        donnees = json.load(json_file)  # ouvre les settings initiaux
    print(
        "A chaque modification proposée, entrer quelque chose pour modifier et ne rien entrer pour ne rien modifier.\n")

    print("Adresse mail actuelle pour les requêtes à l'API d'Unpaywall : " + donnees["mail"])
    entree = input("Modification de l'adresse mail?\n")
    if entree != "":
        donnees["mail"] = entree
        print("Adresse mail modifiée en : " + entree + "\n")

    print("Utilisation actuelle de l'API de hal : " + str(donnees["parametres"]["utilise_api_hal"]))
    entree = input("Utilisation de l'API hal? [y/n]\n")
    if entree == "y":
        donnees["parametres"]["utilise_api_hal"] = True
        print("API hal utilisée!\n")
        print("Nom du labo pour la requête à HAL : " + donnees["api_hal"]["nom_labo"])
        entree = input("Nouveau nom de labo? :\n")
        if entree != "":
            donnees["api_hal"]["nom_labo"] = entree
            print("Nom du labo changé en : " + donnees["api_hal"]["nom_labo"] + " !\n")
    elif entree == "n":
        donnees["parametres"]["utilise_api_hal"] = False
        print("Fichier hal manuel utilisé! Nom : " + donnees["data"]["doi"]["hal_manuel"] + "\n")

    print("Chercher les erreurs (doublons de titres et hal sans doi) : " + str(
        donnees["parametres"]["recherche_erreurs"]))
    entree = input("Chercher les erreurs pour les mettre en csv? [y/n]\n")
    if entree == "y":
        donnees["parametres"]["recherche_erreurs"] = True
        print("Les erreurs seront enregistrées!")
    elif entree == "n":
        donnees["parametres"]["recherche_erreurs"] = False
        print("Les erreurs ne seront pas enregistrées!\n")

    print("Calcul des APC actuel : " + str(donnees["parametres"]["calcul_APC"]))
    entree = input("Calculer les APC ? [y/n]\n")
    if entree == "y":
        donnees["parametres"]["calcul_APC"] = True
        print("APC calculés\n")
    elif entree == "n":
        donnees["parametres"]["calcul_APC"] = False
        print("APC non calculés\n")

    print("Année pour les graphiques sur 1 an : " + str(donnees["parametres"]["annee"]))
    entree = input("Nouvelle année?\n")
    if entree != "":
        try:
            donnees["parametres"]["annee"] = int(entree)
            print("Année changée pour : " + entree + "\n")
        except ValueError:
            print("L'année doit être un entier\n")

    print("Années pour les graphiques sur plusieurs années : " + str(donnees["parametres"]["annees_debut"]) + "-" + str(
        donnees["parametres"]["annees_fin"]))
    entree = input("Année de début?\n")
    entree2 = input("Année de fin?\n")
    if entree != "" and entree2 != "":
        try:
            entree = int(entree)
            entree2 = int(entree2)
            if entree < entree2:
                donnees["parametres"]["annees_debut"] = entree
                donnees["parametres"]["annees_fin"] = entree2
                print("Nouvelles années : " + str(entree) + "-" + str(entree2) + "\n")
            else:
                print("Année de début égale ou supérieure à l'année de fin.\n")
        except ValueError:
            print("Les années doivent être des entiers\n")
    elif entree != "":
        try:
            entree = int(entree)
            if entree < donnees["parametres"]["annees_fin"]:
                donnees["parametres"]["annees_debut"] = entree
                print("Nouvelle année de début : " + str(entree) + "\n")
            else:
                print("Année de début supérieure ou égale à l'année de fin.\n")
        except ValueError:
            print("Les années doivent être des entiers\n")
    elif entree2 != "":
        try:
            entree2 = int(entree2)
            if entree2 > donnees["parametres"]["annees_debut"]:
                donnees["parametres"]["annees_fin"] = entree2
                print("Nouvelle année de fin : " + str(entree2) + "\n")
            else:
                print("Année de fin inférieure ou égale à l'année de début.\n")
        except ValueError:
            print("Les années doivent être des entiers\n")

    entree = input("Changement des graphiques à produire? y?\n")
    if entree == "y":
        for i in donnees["parametres"]["graphiques"]:
            print("\nGraphique " + i + " : " + str(donnees["parametres"]["graphiques"][i]))
            entree = input("Produire ce graphique? [y/n]\n")
            if entree == "y":
                donnees["parametres"]["graphiques"][i] = True
                print("Le graphique " + i + " sera produit!")
            elif entree == "n":
                donnees["parametres"]["graphiques"][i] = False
                print("Le graphique " + i + " ne sera pas produit!")

    with open("./settings.json", "w", encoding="utf-8") as json_file:
        json.dump(donnees, json_file, ensure_ascii=False, indent=2)  # écrit les settings modifiés
    return None
