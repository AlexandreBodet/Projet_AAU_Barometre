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
dataframe donné en entrée.
"""


def graphique(df_raw=None, annee=date.today().year, annees=None,
              rec_base=True, rec_disciplines=True, rec_genre=True,
              oa_circulaire=True, oa_discipline=True, oa_evolution=True, oa_editeur=True,
              apc_evolution=True, apc_discipline=True, bibliodiversite=True,
              oa_type_evolution=True, domain=False, domain_shs=False, domain_info=False):
    """
    Fonction principale pour générer les graphiques.
    :param dataframe df_raw: le dataframe à utiliser
    :param int annee: année utilisée pour certains graphiques
    :param list annees: liste des années pour les graphiques d'évolution
    :param bool domain: dit s'il doit y avoir un recapitulatif de discipline qui inclue tous les domaines
    :param bool domain_shs: même chose avec les sous-domaines des shs
    :param bool domain_info: même chose avec les sous-domaines informatiques
    :param bool rec_base: récapitulatif des bases
    :param bool rec_disciplines: récapitulatif des disciplines
    :param bool rec_genre: récapitulatif des genres
    :param bool oa_circulaire: graphique open access circulaire
    :param bool oa_discipline: open access par discipline
    :param bool oa_evolution: évolution de l'open access
    :param bool oa_editeur: open access par éditeur
    :param bool apc_evolution: évolution des apc
    :param bool apc_discipline: apc par discipline
    :param bool bibliodiversite:
    :param bool oa_type_evolution: evolution de chaque type d'open access
    :return:
    """
    if annees is None:
        annees = [i for i in range(2016, date.today().year + 1)]
    if df_raw is None:
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
    if rec_disciplines:
        if domain:
            graphique_rec_discipline.graphique_discipline(df, domain=True, dossier=nom_dossier)
            graphique_rec_discipline.graphique_discipline(df, annee=annee, domain=True,
                                                          dossier=nom_dossier)  # Sur une seule année
            graphique_rec_discipline.graphique_discipline(df, annee=annees, domain=True,
                                                          dossier=nom_dossier)  # Liste d'années
        if domain_shs:
            graphique_rec_discipline.graphique_discipline(df, domain_shs=True, dossier=nom_dossier)
            graphique_rec_discipline.graphique_discipline(df, annee=annee, domain_shs=True, dossier=nom_dossier)
            graphique_rec_discipline.graphique_discipline(df, annee=annees, domain_shs=True, dossier=nom_dossier)
        if domain_info:
            graphique_rec_discipline.graphique_discipline(df, domain_info=True, dossier=nom_dossier)
            graphique_rec_discipline.graphique_discipline(df, annee=annee, domain_info=True, dossier=nom_dossier)
            graphique_rec_discipline.graphique_discipline(df, annee=annees, domain_info=True, dossier=nom_dossier)

    if rec_base:  # proportion doi/no-doi par base
        graphique_rec_base.graphique_comparaison_bases(dossier=nom_dossier)

    if rec_genre:  # NEW -- à voir si tu trouves ça pertinent
        graphique_rec_genre.graphique_genre(df, dossier=nom_dossier)
        graphique_rec_genre.graphique_genre(df, annee=annee, dossier=nom_dossier)
        graphique_rec_genre.graphique_genre(df, annee=annees, dossier=nom_dossier)

    # Taux d'Open Access
    if oa_circulaire:
        graphique_oa_circulaire.graphique_circulaire_oa(df=df, dossier=nom_dossier)
        graphique_oa_circulaire.graphique_circulaire_oa(df=df, annee=annee, dossier=nom_dossier)
        graphique_oa_circulaire.graphique_circulaire_oa(df=df, annee=annees, dossier=nom_dossier)

    if oa_discipline:
        graphique_oa_discipline.graphique_discipline_oa(df=df, dossier=nom_dossier)
        graphique_oa_discipline.graphique_discipline_oa(df=df, annee=annee, dossier=nom_dossier)
        graphique_oa_discipline.graphique_discipline_oa(df=df, annee=annees, dossier=nom_dossier)

    if oa_evolution:
        graphique_oa_evolution.graphique_oa_evolution(df=df, annees=annees, dossier=nom_dossier, doi_only=False)
    if oa_editeur:  # problème d'éditeur/publisher -> il manque la moitié
        graphique_oa_editeur.graphique_oa_editeur(df=df, annee=annee, dossier=nom_dossier)
    if oa_type_evolution:
        graphique_oa_type_evolution.graphique_evolution_type_oa(df=df, annees=annees, dossier=nom_dossier)

    # APCs
    if apc_evolution:  # peut-être pas utile, à modifier # je n'ai encore pu regarder ça 
        graphique_apc_evolution.graphique_apc_evolution(df=df, annees=annees, dossier=nom_dossier)
    if apc_discipline:  # donner la possibilité de faire sur plusieurs années
        graphique_apc_discipline.graphique_apc_discipline(df=df, annee=annee, dossier=nom_dossier)

    if bibliodiversite:
        graphique_bibliodiversite.graphique_bibliodiversite(df=df, dossier=nom_dossier)
        graphique_bibliodiversite.graphique_bibliodiversite(df=df, annee=annee, dossier=nom_dossier)
        graphique_bibliodiversite.graphique_bibliodiversite(df=df, annee=annees,
                                                            dossier=nom_dossier)  # Même chose sur plusieurs années
