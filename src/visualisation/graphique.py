import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import date, datetime
from src.visualisation import graphique_oa_editeur, graphique_oa_discipline, graphique_oa_circulaire, \
    graphique_oa_evolution, graphique_rec_base, graphique_rec_discipline, graphique_rec_genre, graphique_apc_evolution, \
    graphique_apc_discipline, graphique_bibliodiversite, graphique_oa_type_evolution
from ast import literal_eval

"""
Fichier pour la fonction graphique qui a pour but de lancer les fonctions du package visualisation en se servant du 
dataframe donné en entrée et des parametres de settings.json
"""


def graphique(df_raw=None, parametres=None):
    """
    Fonction principale pour générer les graphiques.
    :param dataframe df_raw: le dataframe à utiliser
    :param dict parametres: dict de tous les paramètres donnés par settings.json. Contient :
        calcul_APC: dit si les apc ont été calculés
        graphique: dict des paramètres des graphiques
            int annee: année utilisée pour certains graphiques
            int annees_debut: début de la liste des années pour les graphiques d'évolution
            int annees_fin: fin de la liste des années pour les graphiques d'évolution
            rec_base: récapitulatif des bases
            rec_disciplines: récapitulatif des disciplines
            domain_rec_disciplines: dit s'il doit y avoir un recapitulatif de discipline qui inclue tous les domaines
            domain_shs_rec_disciplines: même chose avec les sous-domaines des shs
            domain_info_rec_disciplines: même chose avec les sous-domaines informatiques
            rec_genre: récapitulatif des genres
            oa_circulaire: graphique open access circulaire
            oa_discipline: open access par discipline
            oa_evolution: évolution de l'open access
            oa_editeur: open access par éditeur
            apc_evolution: évolution des apc
            apc_discipline: apc par discipline
            bibliodiversite:
            oa_type_evolution: evolution de chaque type d'open access
    :return nom_dossier: nom du dossier où les images sont enregistrées pour l'affichage
    """
    graphiques = parametres["graphiques"]

    if parametres["annees_debut"] is None and parametres["annees_fin"] is None:
        annees = [i for i in range(2016, date.today().year + 1)]
    elif parametres["annees_debut"] is None:
        annees = [i for i in range(2016, parametres["annees_fin"] + 1)]
    elif parametres["annees_fin"] is None:
        annees = [i for i in range(parametres["annees_debut"], date.today().year + 1)]
    else:
        annees = [i for i in range(parametres["annees_debut"], parametres["annees_fin"] + 1)]

    if parametres["annee"] is None:
        annee = date.today().year
    else:
        annee = parametres["annee"]

    if df_raw is None:
        if os.path.exists("./resultats/fichiers_csv/data_complete.csv"):
            print("\n[Dataframe data_complete.csv chargé à partir de résultats précédents !!!]\n")
            df_raw = pd.read_csv("./resultats/fichiers_csv/data_complete.csv")
        else:
            print("Pas de dataframe chargé. Impossible de générer les graphiques.")
            return None

    # Création du dossier et des sous-dossiers
    nom_dossier = datetime.now().isoformat(
        timespec="seconds")  # Nom du dossier unique dans lequel les images seront enregistrées
    nom_dossier = nom_dossier.replace(":", "-")  # Supprime les ":"
    os.mkdir("./resultats/img/" + nom_dossier)
    os.mkdir("./resultats/img/" + nom_dossier + "/" + str(annee))
    os.mkdir("./resultats/img/" + nom_dossier + "/" + str(annees[0]) + "-" + str(annees[-1]))

    # filtre : retrait des documents de paratexte
    df = df_raw[
        (df_raw["is_paratext"] == "") | df_raw["is_paratext"].isna()]  # pour nous : inutile, car ils sont tous comme ça

    if type(df.scientific_field[0]) == str:
        df.scientific_field = df.scientific_field.apply(literal_eval)  # passe les listes de domaines du str à list
    if type(df.shs_field[0]) == str:
        df.shs_field = df.shs_field.apply(literal_eval)  # passe les listes de domaines du str à list
    if type(df.info_field[0]) == str:
        df.info_field = df.info_field.apply(literal_eval)

    # Récapitulatifs
    if graphiques["rec_discipline"]:
        if graphiques["domain_rec_discipline"]:
            graphique_rec_discipline.graphique_discipline(df=df, domain=True, dossier=nom_dossier)
            graphique_rec_discipline.graphique_discipline(df=df, annee=annee, domain=True,
                                                          dossier=nom_dossier)  # Sur une seule année
            graphique_rec_discipline.graphique_discipline(df=df, annee=annees, domain=True,
                                                          dossier=nom_dossier)  # Liste d'années
        if graphiques["domain_shs_rec_discipline"]:
            graphique_rec_discipline.graphique_discipline(df=df, domain_shs=True, dossier=nom_dossier)
            graphique_rec_discipline.graphique_discipline(df=df, annee=annee, domain_shs=True, dossier=nom_dossier)
            graphique_rec_discipline.graphique_discipline(df=df, annee=annees, domain_shs=True, dossier=nom_dossier)
        if graphiques["domain_info_rec_discipline"]:
            graphique_rec_discipline.graphique_discipline(df=df, domain_info=True, dossier=nom_dossier)
            graphique_rec_discipline.graphique_discipline(df=df, annee=annee, domain_info=True, dossier=nom_dossier)
            graphique_rec_discipline.graphique_discipline(df=df, annee=annees, domain_info=True, dossier=nom_dossier)

    if graphiques["rec_base"]:  # proportion doi/no-doi par base
        graphique_rec_base.graphique_comparaison_bases(dossier=nom_dossier)

    if graphiques["rec_genre"]:
        fonctions_multiples(func=graphique_rec_genre.graphique_genre, df=df, dossier=nom_dossier,
                            annee=annee, annees=annees)

    # Taux d'Open Access
    if graphiques["oa_circulaire"]:
        fonctions_multiples(func=graphique_oa_circulaire.graphique_circulaire_oa, df=df, dossier=nom_dossier,
                            annee=annee, annees=annees)

    if graphiques["oa_discipline"]:
        fonctions_multiples(func=graphique_oa_discipline.graphique_discipline_oa, df=df, dossier=nom_dossier,
                            annee=annee, annees=annees)

    if graphiques["oa_evolution"]:
        graphique_oa_evolution.graphique_oa_evolution(df=df, annees=annees, dossier=nom_dossier, doi_only=False)

    if graphiques["oa_editeur"]:
        fonctions_multiples(func=graphique_oa_editeur.graphique_oa_editeur, df=df, dossier=nom_dossier,
                            annee=annee, annees=annees)

    if graphiques["bibliodiversite"]:
        fonctions_multiples(func=graphique_bibliodiversite.graphique_bibliodiversite, df=df, dossier=nom_dossier,
                            annee=annee, annees=annees)

    if graphiques["oa_type_evolution"] and parametres["calcul_APC"]:  # a besoin des APC
        graphique_oa_type_evolution.graphique_evolution_type_oa(df=df, annees=annees, dossier=nom_dossier)

    # APCs
    if graphiques["apc_evolution"] and parametres["calcul_APC"]:
        graphique_apc_evolution.graphique_apc_evolution(df=df, annees=annees, dossier=nom_dossier)

    if graphiques["apc_discipline"] and parametres["calcul_APC"]:
        fonctions_multiples(func=graphique_apc_discipline.graphique_apc_discipline, df=df, dossier=nom_dossier,
                            annee=annee, annees=annees)
    return nom_dossier


def fonctions_multiples(func, df, dossier, annee, annees):
    func(df=df, dossier=dossier)
    func(df=df, annee=annee, dossier=dossier)
    func(df=df, annee=annees, dossier=dossier)
