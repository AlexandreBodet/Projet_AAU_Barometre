import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from visualisation import graphique_oa_editeur, graphique_discipline, graphique_circulaire_oa, graphique_discipline_oa, graphique_oa_evolution, graphique_comparaison_bases, graphique_apc_evolution, graphique_apc_discipline, graphique_bibliodiversite, graphique_evolution_type_oa
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
              disciplinaire=True, circulaire=True, discipline_oa=True, evolution_oa=True, oa_editeur=True,
              comparaison_bases=True, apc_evolution=True, apc_discipline=True, bibliodiversite=True, evolution_type_oa=True):
    """
    Fonction principale pour générer les graphiques.
    :param dataframe df_raw: le dataframe à utiliser
    :param int annee: année utilisée pour certains graphiques
    :param list annees: liste des années pour les graphiques d'évolution
    :param bool disciplinaire: dit si le graphique doit être fait
    :param bool circulaire: dit si le graphique doit être fait
    :param bool discipline_oa: dit si le graphique doit être fait
    :param bool evolution_oa: dit si le graphique doit être fait
    :param bool oa_editeur: dit si le graphique doit être fait
    :param bool comparaison_bases: dit si le graphique doit être fait
    :param bool apc_evolution: dit si le graphique doit être fait
    :param bool apc_discipline: dit si le graphique doit être fait
    :param bool bibliodiversite: dit si le graphique doit être fait
    :param bool evolution_type_oa: dit si le graphique doit être fait
    :return:
    """
    if annees is None:
        annees = [i for i in range(2016, date.today().year + 1)]
    if df_raw is None:
        print("Pas de dataframe chargé.")
        return None

    # filtre : retrait des documents de paratexte
    df = df_raw[df_raw["is_paratext"] == ""]  # pour nous : inutile car ils sont tous comme ça
    # remarque:  des publications ne sont pas dans la fourchette souhaitée [2016-XX]
    df.scientific_field = df.scientific_field.apply(literal_eval)

    if disciplinaire:
        graphique_discipline.graphique_discipline(df)
    if circulaire:
        graphique_circulaire_oa.graphique_circulaire_oa(df, annee)
    if discipline_oa:
        graphique_discipline_oa.graphique_discipline_oa(df, annee)
    if evolution_oa:  # à corriger
        graphique_oa_evolution.graphique_oa_evolution(df, annees=annees, doi_only=False, )
    if comparaison_bases:  # à corriger pour afficher qu'une fois dans le cas où on a une seule source
        #je pense c'est pertinent pour montrer la proportion de doi/nodoi
        graphique_comparaison_bases.graphique_comparaison_bases()
    if apc_evolution:  # peut-être pas utile, à modifier # je n'ai encore pu regarder ça 
        graphique_apc_evolution.graphique_apc_evolution(df, annees=annees)
    if apc_discipline:  # donner la possibilité de faire sur plusieurs années
        graphique_apc_discipline.graphique_apc_discipline(df, annee)
    if bibliodiversite:  # pas sûr de ce que c'est sensé rendre, peut-être pas utile
        # le problème c'est que même pas la moitié ont un publisher ...
        graphique_bibliodiversite.graphique_bibliodiversite(df, annee)
    if oa_editeur:  # prbl d'éditeur/publisher
        graphique_oa_editeur.graphique_oa_editeur(df, annee)
    if evolution_type_oa:  # à vérifier -> j'ai du commenter la ligne 56 et remplacer tout les suscpicious par suscpicious_journal mais pas sûr qu'il fallait faire ça 
        graphique_evolution_type_oa.graphique_evolution_type_oa(df, annees)
