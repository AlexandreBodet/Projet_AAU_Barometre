"""
Fonctions pour analyser les métadonnées associés aux publications
Pour l'instant, seulement pour les données sortant de hal
"""

import pandas as pd
import json as j


def deduce_oa(row):
    '''déduit si la publication est en open access'''
    if (row["hal_location"] == "file" and row["hal_openAccess_bool"]) or (row["hal_location"] == "arxiv") or (row["hal_location"] == "pubmedcentral") or (row["upw_coverage"] == "oa"):
        return True
    else:
        return False


def deduce_oa_type(row):
    loc = []
    if pd.notna(row["upw_location"]):
        loc.extend(row["upw_location"].split(";"))

    # si unpaywall n'a pas trouvé de "repository" mais que c'est dans HAL : s'assurer que c'est sans embargo puis ajouter repository
    if "repository" not in loc and\
        ((row["hal_location"] == "file" and row["hal_openAccess_bool"] == "True") or
         row["hal_location"] == "arxiv" or
         row["hal_location"] == "pubmedcentral"):
        loc.append("repository")

    if loc:
        loc.sort()
        return ";".join(loc)
    else:
        return "closed"

#alignement avec les données de hal
match_ref = j.load(open("../data/match_referentials.json"))


def align_doctype(row):
    if pd.notna(row["genre"]):
        return row["genre"]
    # si pas de genre chez unpaywall mais présence chez HAL
    if pd.isna(row["genre"]) and pd.notna(row["hal_docType"]):
        if row["hal_docType"] in match_ref["docType"]:
            return match_ref["docType"][row["hal_docType"]]
        else:
            print("cannot align doctype", row["halId"])


def align_domain(row):
    if pd.notna(row["hal_domain"]):
        if row["hal_domain"] in match_ref["domain"]:
            return match_ref["domain"][row["hal_domain"]]
        else:
            print("cannot align domain", row["halId"])
            return "Autres"
    else:
        print("cannot align domain", row["halId"])
        return "Autres"


def aligner(df=None):
    if df is None:
        df = pd.read_csv(
            "../resultats/fichiers_csv/ajout_apc.csv", encoding='utf8')
            
    df["is_oa"] = df.apply(lambda row: deduce_oa(row), axis=1)
    df["oa_type"] = df.apply(lambda row: deduce_oa_type(row), axis=1)
    df["genre"] = df.apply(lambda row: align_doctype(row), axis=1)
    df["scientific_field"] = df.apply(lambda row: align_domain(row), axis=1)

    df['hal_coverage'].fillna('missing', inplace=True)
    df['upw_coverage'].fillna('missing', inplace=True)
    df.to_csv("../resultats/fichiers_csv/data_complete.csv", index=False)
    return None
