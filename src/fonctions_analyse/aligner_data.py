"""
Fonctions pour analyser les métadonnées associées aux publications.
Pour l'instant, seulement pour les données sortant de hal.
"""

import pandas as pd
import json as j
from ast import literal_eval
import os


def deduce_oa(row):
    """
    Déduit si la publication est en open access
    :param row: ligne du dataframe à traiter
    :return bool: publication en open access
    """
    if (row["hal_location"] == "file" and row["hal_openAccess_bool"]) or (row["hal_location"] == "arxiv") or (
            row["hal_location"] == "pubmedcentral") or (row["upw_coverage"] == "oa"):
        return True
    else:
        return False


def deduce_oa_type(row):
    """
    Déduit le type d'open access
    :param row: ligne du dataframe à traiter
    :return str: type d'open access (closed, repository, publisher ou bien publisher;repository)
    """
    loc = []
    if pd.notna(row["upw_location"]):
        loc.extend(row["upw_location"].split(";"))

    # si unpaywall n'a pas trouvé de "repository" mais que c'est dans HAL : s'assurer que c'est sans embargo puis ajouter repository
    if "repository" not in loc and \
            ((row["hal_location"] == "file" and row["hal_openAccess_bool"]) or
             row["hal_location"] == "arxiv" or
             row["hal_location"] == "pubmedcentral"):
        loc.append("repository")
    if loc:
        loc.sort()
        return ";".join(loc)
    else:
        return "closed"


def align_doctype(row, match_ref):
    """
    Donne le type de document (chapitres d'ouvrage, articles dans une revue, ...)
    :param row: ligne à traiter
    :param dict match_ref: noms des domaines et de type de documents
    :return:
    """
    """
    if pd.notna(row["genre"]):
        return row["genre"]
    """
    # je n'utilise que les données de HAL, car elles sont pour tous
    # si pas de genre chez unpaywall, mais présence chez HAL
    if pd.notna(row["hal_docType"]):
        if row["hal_docType"] in match_ref["docType"]:
            return match_ref["docType"][row["hal_docType"]]
        else:
            print("cannot align doctype", row["halId"])


def align_domain(row, match_ref, choixDomain):
    """
    Donne la liste des domaines correspondants

    :param row: ligne à traiter
    :param dict match_ref: noms des domaines et de type de documents
    :param dict choixDomain: dictionnaire des settings choisis dans les settings
    :return list: la liste des domaines
    """
    res = []
    for e in row["hal_domain"]:
        if choixDomain[match_ref["domain"][e]]:
            res.append(match_ref["domain"][e])
        else:
            res.append("Autres")
    return res


def align_shsdomain(row, match_ref, choixShsDomain):
    """
    Donne la liste des domaines correspondants
    :param row: ligne à traiter
    :param dict match_ref: noms des domaines et de type de documents
    :param dict choixShsDomain: dictionnaire des sous-domaines shs choisis dans les settings
    :return list: la liste des domaines
    """
    res = []
    for e in row["hal_shsdomain"]:
        if choixShsDomain[match_ref["shsdomain"][e]]:
            res.append(match_ref["shsdomain"][e])
        else:
            res.append("Autres")
    return res


def align_infodomain(row, match_ref, choixInfoDomain):
    """
    Donne la liste des domaines correspondants

    :param row: ligne à traiter
    :param dict match_ref: noms des domaines et de type de documents
    :param dict choixInfoDomain: dictionnaire des sous-domaines infos choisis dans les settings
    :return list: la liste des domaines
    """
    res = []
    for e in row["hal_infodomain"]:
        if choixInfoDomain[match_ref["infodomain"][e]]:
            res.append(match_ref["infodomain"][e])
        else:
            res.append("Autres")
    return res


def aligner(referentials, choixDomaines, df=None):
    """
    Aligne les données dans les bonnes colonnes. Open_access ou non, le type d'oa

    :param str referentials: str du nom de fichier json pour les noms des domaines et de type de documents
    :param dict choixDomaines: dictionnaire des choix de domaines effectués dans les settings
    :param df: dataframe en sortie de ajout_apc() ou enrich_to_csv()
    :return pd.Dataframe: dataframe modifié
    """
    if df is None:
        if os.path.isfile("./resultats/fichiers_csv/ajout_apc.csv"):
            df = pd.read_csv("./resultats/fichiers_csv/ajout_apc.csv", encoding="utf8")
        else:
            df = pd.read_csv("./resultats/fichiers_csv/df_metadonnees.csv", encoding="utf8")

    # alignement avec les données de hal
    with open("./data/"+referentials, "r", encoding="utf-8") as json_file:
        match_ref = j.load(json_file)

    if type(df.hal_domain[0]) == str:
        df.hal_domain = df.hal_domain.apply(literal_eval)
    if type(df.hal_shsdomain[0]) == str:
        df.hal_shsdomain = df.hal_shsdomain.apply(literal_eval)
    if type(df.hal_infodomain[0]) == str:
        df.hal_infodomain = df.hal_infodomain.apply(literal_eval)

    df["is_oa"] = df.apply(lambda row: deduce_oa(row), axis=1)
    df["oa_type"] = df.apply(lambda row: deduce_oa_type(row), axis=1)
    df["genre"] = df.apply(lambda row: align_doctype(row, match_ref), axis=1)
    df["scientific_field"] = df.apply(
        lambda row: align_domain(row, match_ref, choixDomaines["domain"]), axis=1)
    df["shs_field"] = df.apply(lambda row: align_shsdomain(
        row, match_ref, choixDomaines["shsdomain"]), axis=1)
    df["info_field"] = df.apply(lambda row: align_infodomain(
        row, match_ref, choixDomaines["infodomain"]), axis=1)

    df["hal_coverage"].fillna("missing", inplace=True)
    df["upw_coverage"].fillna("missing", inplace=True)
    df.to_csv("./resultats/fichiers_csv/data_complete.csv", index=False, encoding="utf8")
    return df
