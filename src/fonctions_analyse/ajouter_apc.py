import json
import pandas as pd
from datetime import date


def track_apc(doi, ligne, open_apc_dois, openapc_journals, doaj_apc_journals):
    """
    Heuristique sur les APC.

    :param str doi: doi dont on veut récupérer les APC
    :param ligne: ligne du dataframe à utiliser
    :param dataframe openapc_journals: dataframe des apc des journaux depuis openapc
    :param dataframe open_apc_dois: dataframe des apc de openapc
    :param dataframe doaj_apc_journals: dataframe des apc des différents journaux avec les doaj
    :return dict: dictionnaire des apc payés
    """

    # Vérifier si le DOI est dans openapc
    if doi and open_apc_dois["doi"].str.contains(doi, regex=False).any():
        try:
            apc_amount = open_apc_dois.loc[open_apc_dois["doi"] == doi, "apc_amount_euros"].item()
        except:  # Changer ça
            apc_amount = "unknown"
        return {
            "apc_tracking": "doi_in_openapc",
            "apc_amount": apc_amount,
            "apc_currency": "EUR"
        }

    # Si le document n'a pas d'ISSN, ne rien remplir
    if not ligne.journal_issns:
        return {}

    # Récupérer les différents ISSN
    issns = ligne.journal_issns.split(",")
    if ligne.journal_issn_l:
        issns.append(ligne.journal_issn_l)

    # Si un ISSN est dans openapc et que des APC ont été payés la même année
    cols = ["issn", "issn_print", "issn_electronic", "issn_l"]
    openapc_mean = False
    if ligne.published_year and 2014 < int(ligne.published_year) < date.today().year:
        for item in issns:
            for col in cols:
                if item and openapc_journals[col].str.contains(item).any():
                    openapc_mean = openapc_journals.loc[
                        openapc_journals[col] == item, str(int(ligne.published_year))].item()
                    break

    if openapc_mean:
        return {
            "apc_tracking": "journal_in_openapc",
            "apc_amount": openapc_mean,
            "apc_currency": "EUR"
        }

    # Si le type d'accès ouvert du document dans unpaywall est hybride
    if ligne.oa_status == "hybrid":
        return {"apc_tracking": "journal_is_hybrid"}

    # Si le journal est dans le DOAJ extraire les données d' APC du DOAJ
    cols = ["Journal ISSN (print version)", "Journal EISSN (online version)"]
    for item in issns:
        for col in cols:
            if doaj_apc_journals[col].str.contains(item).any():
                return {
                    "apc_tracking": "apc_journals_in_doaj",
                    "apc_amount": doaj_apc_journals.loc[doaj_apc_journals[col] == item, "APC amount"].item(),
                    "apc_currency": doaj_apc_journals.loc[doaj_apc_journals[col] == item, "APC currency"].item()
                }
    # Si aucun cas ne s'est présenté ne rien remplir
    return {}


def check_suspicious_j(ligne, suspiciousIssns):
    """
    Vérifier si le journal est dans la liste de ceux suspects.

    :param ligne: ligne du dataframe à vérifier
    :param json suspiciousIssns: fichier json des journaux suspicieux
    :return dict: dictionnaire qui dit si le journal est suspicieux
    """
    if not ligne.journal_issns:
        return {}

    is_suspicious = False
    issns = ligne.journal_issns.split(";")
    for item in issns:
        if item in suspiciousIssns["print"] or item in suspiciousIssns["electronic"]:
            is_suspicious = True

    return {"suspicious_journal": is_suspicious}


def clean_pub_year(x):
    """
    Donne l'année mais en entier.

    :param str x: année en entrée
    :return int: année en sortie
    """
    if x:
        return int(float(x))


def separation_montant_devise(apc_journal, column):
    """
    Supprime les valeurs en double et sépare monnaie et devise.

    :param dataframe apc_journal: dataframe des apc des journaux
    :param column: colonnes des APC à séparer
    """

    apc_journal["APC amount"] = apc_journal[column].str.split(";", expand=True)
    apc_journal[["APC amount", "APC currency"]] = apc_journal["APC amount"].str.split(" ", expand=True)
    return None


def transformation_df(df):
    """
    Transforme le dataframe pour éviter certaines erreurs.

    :param dataframe df: dataframe à transformer
    """
    # Transformation de l'année en entier
    df["published_year"] = df["published_year"].apply(lambda x: clean_pub_year(x))
    df["published_year"].fillna("", inplace=True)
    # Transformations en str des colonnes qui pourraient causer des erreurs (à cause de nan par exemple)
    df["doi"] = df["doi"].astype(str)
    df["journal_issns"] = df["journal_issns"].astype(str)
    df["journal_issn_l"] = df["journal_issn_l"].astype(str)
    return None


def ajout_apc(df, data_apc):
    """
    Ajoute les APC au dataframe.

    :param dataframe df: dataframe où ajouter les apc
    :param dict data_apc: dictionnaire des noms de fichiers à utiliser
    """
    openapc_dois = pd.read_csv("../data/apc_tracking/" + data_apc["openapc_dois"], na_filter=False)
    openapc_journals = pd.read_csv("../data/apc_tracking/" + data_apc["openapc_journals"], na_filter=False)
    doaj_apc_journals = pd.read_csv("../data/apc_tracking/" + data_apc["doaj_apc_journals"], na_filter=False)
    fh_json = open("../data/apc_tracking/" + data_apc["suspiciousIssns"])
    suspiciousIssns = json.load(fh_json)

    # Supprime les valeurs en double et sépare monnaie et devise
    separation_montant_devise(doaj_apc_journals, "APC amount")

    transformation_df(df=df)

    # Ajout des APC et des données sur les journaux suspicieux
    for row in df.itertuples():

        # Trouver les APC
        md = track_apc(doi=row.doi, ligne=row, open_apc_dois=openapc_dois, openapc_journals=openapc_journals,
                       doaj_apc_journals=doaj_apc_journals)

        # Déduire les journaux suspects
        md.update(check_suspicious_j(ligne=row, suspiciousIssns=suspiciousIssns))

        # Ajouter les métadonnées au dataframe
        for field in md:
            df.loc[row.Index, field] = md[field]

    df.to_csv("../resultats/fichiers_csv/ajout_apc.csv", index=False)
    return None
