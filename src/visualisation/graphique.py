import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from src.visualisation import graphique_oa_editeur, graphique_oa_discipline, graphique_oa_circulaire, graphique_oa_evolution, graphique_rec_base, graphique_rec_discipline, graphique_rec_genre, graphique_apc_evolution, graphique_apc_discipline, graphique_bibliodiversite, graphique_oa_type_evolution
from ast import literal_eval

"""
  circulaire : bilan open access sur une année
  oa_evol : evolution taux open access par an et type oa
  oa_discipline : type d'accès ouvert par discipline
  oa_editeur : type d'accès ouvert par éditeurs

  evol types d'accès ouvert green to diamond
"""


# circulaire // oa_evol // oa_discipline // oa_editeur //
# comparaison_bases // apc_evol // apc_discipline // bibliodiversity
# disciplines


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
    :param bool rec_base: dit si le graphique doit être fait
    :param bool rec_disciplines: dit si le graphique doit être fait
    :param bool rec_genre: dit si le graphique doit être fait
    :param bool oa_circulaire: dit si le graphique doit être fait
    :param bool oa_discipline: dit si le graphique doit être fait
    :param bool oa_evolution: dit si le graphique doit être fait
    :param bool oa_editeur: dit si le graphique doit être fait
    :param bool apc_evolution: dit si le graphique doit être fait
    :param bool apc_discipline: dit si le graphique doit être fait
    :param bool bibliodiversite: dit si le graphique doit être fait
    :param bool oa_type_evolution: dit si le graphique doit être fait
    :return:
    """
    if annees is None:
        annees = [i for i in range(2016, date.today().year + 1)]
    if df_raw is None:
        print("Pas de dataframe chargé.")
        return None

    # filtre : retrait des documents de paratexte
    df = df_raw[(df_raw["is_paratext"] == "") | df_raw["is_paratext"].isna()]  # pour nous : inutile car ils sont tous comme ça
    # remarque:  des publications ne sont pas dans la fourchette souhaitée [2016-XX]
    if type(df.scientific_field[0]) == str:
        df.scientific_field = df.scientific_field.apply(literal_eval) # passe les listes de domaines du str à list
    if type(df.shs_field[0]) == str:
        df.shs_field = df.shs_field.apply(literal_eval)  # passe les listes de domaines du str à list
    if type(df.info_field[0]) == str:
        df.info_field = df.info_field.apply(literal_eval)

    if rec_disciplines: 
        graphique_rec_discipline.graphique_discipline(
            df, domain, domain_shs, domain_info)
    if rec_base:  # je pense c'est pertinent pour montrer la proportion de doi - nodoi
        #néanmoins, on voit quasi-pas la diff (il y en a une car on enlève qlq doublons), donc à retravailler jpense
        graphique_rec_base.graphique_comparaison_bases()
    if rec_genre: #NEW -- à voir si tu trouves ça pertinent
        graphique_rec_genre.graphique_genre(df)

    if oa_circulaire: 
        graphique_oa_circulaire.graphique_circulaire_oa(df, annee)
    if oa_discipline:
        graphique_oa_discipline.graphique_discipline_oa(df, annee)
    if oa_evolution:
        graphique_oa_evolution.graphique_oa_evolution(df, annees=annees, doi_only=False, )
    if oa_editeur:  # prbl d'éditeur/publisher -> il manque la moitié
        graphique_oa_editeur.graphique_oa_editeur(df, annee)
    if oa_type_evolution:  # à creuser, je comprends pas trop, 
        # -> j'ai du commenter la ligne 56 et remplacer tout les suscpicious par suscpicious_journal mais pas sûr qu'il fallait faire ça
        graphique_oa_type_evolution.graphique_evolution_type_oa(df, annees)

    # apc
    if apc_evolution:  # peut-être pas utile, à modifier # je n'ai encore pu regarder ça 
        graphique_apc_evolution.graphique_apc_evolution(df, annees=annees)
    if apc_discipline:  # donner la possibilité de faire sur plusieurs années
        graphique_apc_discipline.graphique_apc_discipline(df, annee)
    if bibliodiversite:  # pas sûr de ce que c'est sensé rendre, peut-être pas utile
        # le problème c'est que même pas la moitié ont un publisher ...
        graphique_bibliodiversite.graphique_bibliodiversite(df, annee)
    
