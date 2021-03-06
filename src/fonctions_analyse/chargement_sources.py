"""
Fonctions pour consolider les sources
"""

import pandas as pd
import re
import unidecode
from src.fonctions_analyse.dedoublonnage import dedoublonnage_doi, dedoublonnage_titre, doi_ou_hal


def normalize_txt(title):
    """
    Retirer les espaces, les accents, tout en minuscules, retirer les caractères spéciaux.
    :param str title: titre à normaliser
    :return str join_cut: titre normalisé
    """
    cut = re.split(r"\W+", str(title))
    join_cut = "".join(cut).lower()
    join_cut = unidecode.unidecode(join_cut)
    return join_cut


def conforme_df(df, col_name):
    """
    Garde les colonnes de col_name, les renomme et passe en minuscule doi et titre.
    :param pd.Dataframe df: dataframe dont les titres et doi sont normalisés
    :param dict[str, str] col_name: colonnes à garder
    :return pd.Dataframe: dataframe modifié
    """
    # memo : on ne supprime pas la colonne titre, car elle est utilisée pour le dédoublonnage
    print("conformer le df")
    df = df[list(col_name.keys())].copy()
    df.rename(columns=col_name, inplace=True)

    df["doi"] = df["doi"].str.lower()  # doi en minuscule
    df["title_norm"] = df["title"].apply(lambda row: normalize_txt(row))
    return df


def chargement_hal(hal_file="", skip=0):
    """
    Charge un fichier hal.
    :param skip: dit si la première ligne du fichier ne doit pas être lue
    :param str hal_file: du nom de fichier à charger
    :return dataframe: dataframe chargé
    """

    if hal_file:
        # chargement, garde certaines colonnes et transformations des titres du fichier HAL
        fichier_hal = "./data/dois/" + hal_file
        hal = pd.read_csv(fichier_hal, sep=";",
                          skiprows=skip)  
        hal = conforme_df(hal, {"DOI": "doi", "Réf. HAL": "halId", "Titre": "title"})
    else:  # Si le fichier n'est pas spécifié
        hal = None
    return hal


def chargement_scopus(scopus_file=""):
    """
    Charge un fichier scopus.
    :param str scopus_file: nom de fichier à charger
    :return dataframe: dataframe chargé
    """
    if scopus_file:
        # Chargement
        scopus = pd.read_csv("./data/dois/" + scopus_file, encoding="utf8")
        scopus = conforme_df(scopus, {"DOI": "doi", "Title": "title"})
    else:  # Si pas de fichier spécifié
        scopus = None
    return scopus


def chargement_wos(wos_file=None):
    """
    Charge un fichier wos.
    :param list wos_file: nom de fichier à charger
    :return dataframe: dataframe chargé
    """
    if wos_file:
        # fichier_wos = ["wos_2016a.txt", "wos_2016b.txt", "wos_2016c.txt", "wos_2017a.txt", "wos_2017b.txt",
        #               "wos_2017c.txt", "wos_2018a.txt", "wos_2018b.txt", "wos_2018c.txt", "wos_2019a.txt",
        #               "wos_2019b.txt", "wos_2019c.txt", "wos_2020a.txt", "wos_2020b.txt", "wos_2020c.txt"]
        df_buffer = []
        for f in wos_file:
            df = pd.read_csv("./data/dois/" + f, sep="\t", index_col=False)
            df_buffer.append(df)
        wos = pd.concat(df_buffer)
        wos = conforme_df(wos, {"DI": "doi", "TI": "title"})
    else:
        wos = None
    return wos


def chargement_pubmed(pubmed_file=""):
    """
    Charger un fichier pubmed.
    :param str pubmed_file: nom de fichier à charger
    :return dataframe: dataframe chargé
    """
    if pubmed_file:
        pubmed = pd.read_csv("./data/dois/" + pubmed_file)
        pubmed = conforme_df(pubmed, {"DOI": "doi", "Title": "title"})
    else:
        pubmed = None
    return pubmed


def removeJoinDois(x):
    """
    Retirer les listes de doi assemblées par "; ".
    :param str x: liste de dois ou doi
    :return str: premier doi de la liste, ou doi s'il est seul
    """

    doi = str(x).strip()
    if "; " in doi:
        cut = doi.split("; ")
        return cut[0]
    else:
        return x


def chargement_lens(lens_file=""):
    """
    Charger un fichier lens.
    :param str lens_file: du nom de fichier à charger
    :return dataframe: dataframe chargé
    """
    if lens_file:
        lens = pd.read_csv("./data/dois/" + lens_file)
        conforme_df(lens, {"DOI": "doi", "Title": "title"})
        lens["doi"] = lens["doi"].apply(lambda x: removeJoinDois(x))
    else:
        lens = None
    return lens


def extract_stats_from_base(src_name, df, statistiques):
    """
    Extraire du dataframe les données de la base sur le total publications, doi only, no doi.
    :param str src_name: nom de la base de donnée source
    :param dataframe df: dataframe chargé
    :param list statistiques: liste des statistiques
    """
    if statistiques is None:
        statistiques = []
    no_doi = df["doi"].isna().sum()
    w_doi = df["doi"].str.match("10.").sum()
    if no_doi + w_doi == len(df.index):
        print(f"{src_name} : {w_doi} fichiers avec dois importés - {no_doi} fichiers sans doi importés")
        statistiques.append([src_name, len(df.index), w_doi, no_doi])
    else:
        print(f"{src_name} pas importé")


def statistiques_bases(hal_df=None, scopus_df=None, wos_df=None, pubmed_df=None, lens_df=None):
    """
    Extrait les statistiques de toutes les bases données
    :param dataframe hal_df: données de hal
    :param dataframe scopus_df: données de scopus
    :param dataframe wos_df: données de wos
    :param dataframe pubmed_df: données de pubmed
    :param dataframe lens_df: données de lens
    :return list: liste des statistiques extraites
    """
    stats = []

    if hal_df is not None:
        extract_stats_from_base(src_name="hal", df=hal_df, statistiques=stats)

    if scopus_df is not None:
        extract_stats_from_base(src_name="scopus", df=scopus_df, statistiques=stats)

    if wos_df is not None:
        extract_stats_from_base(src_name="wos", df=wos_df, statistiques=stats)

    if pubmed_df is not None:
        extract_stats_from_base(src_name="pubmed", df=pubmed_df, statistiques=stats)

    if lens_df is not None:
        extract_stats_from_base(src_name="lens", df=lens_df, statistiques=stats)

    return stats


def chargement_tout(donnees, recherche_erreur=True, utilise_api_hal=True):
    """
    Charge tous les fichiers et donne des statistiques dessus et le dataframe de tous les dataframes.
    :param bool recherche_erreur: Dit si on doit enregistrer les csv qui notent les erreurs
    :param bool utilise_api_hal: Dit si on a utilisé l'api de hal
    :param Dict[str, str] donnees: données issues du fichier settings
    :return list, dataframe: liste des statistiques sur les bases et dataframe des données chargées
    """

    if utilise_api_hal:
        hal = chargement_hal(donnees["hal_fichier_api"], skip=0)
        print("api")
    else:
        hal = chargement_hal(donnees["hal_manuel"], skip=1)

    # chargements depuis toutes les bases de données
    scopus = chargement_scopus(donnees["scopus_fichier"])
    wos = chargement_wos(donnees["wos_fichier"])
    pubmed = chargement_pubmed(donnees["pubmed_fichier"])
    lens = chargement_lens(donnees["lens_fichier"])

    df_charge = pd.concat([hal, scopus, wos, pubmed, lens])  # dataframe avec toutes les données

    # Recherche d'erreurs si spécifiée, les fichiers csv résultant sont dans resultats/fichiers_csv/erreurs
    if recherche_erreur:
        identifie_hal_sans_doi_to_csv(df_charge)
        identifie_doublons_titres_to_csv(df_charge)

    # Dédoublonnage
    clean_doi = dedoublonnage_doi(df_charge)
    clean_doi_title = dedoublonnage_titre(clean_doi)
    final_df = doi_ou_hal(clean_doi_title)

    # Statistiques sur les bases
    stats = statistiques_bases(hal, scopus, wos, pubmed, lens)  # donne les statistiques pour toutes les bases
    # Ajoute les statistiques finales sur toutes les bases
    stats.append([
        "retenu",
        len(final_df),
        len(final_df[final_df["doi"].notna()]),
        len(final_df[final_df["doi"].isna()])])
    # Noms des colonnes
    stat_table = pd.DataFrame(stats, columns=["name", "all", "doi", "no_doi"])
    stat_table.to_csv("./resultats/fichiers_csv/statistiques_sur_les_bases.csv", index=False)

    # extraire le jeu de données final
    final_df.drop(columns=["title", "title_norm"], inplace=True)
    final_df.to_csv("./resultats/fichiers_csv/consolider_doi_hal_id.csv",
                    index=False, encoding="utf8")

    return final_df


def identifie_hal_sans_doi_to_csv(rawdf):
    """
    Identifier les documents HAL sans DOI et dont le titre correspond à un document avec DOI.
    Enregistre dans un csv pour voir les erreurs.
    :param pd.Dataframe rawdf: dataframe non dedoublonné
    """
    doi_only = rawdf[(
            rawdf["doi"].notna() & rawdf["halId"].isna())].copy()  # possèdent un doi mais pas de hal_id
    doi_only["doi"] = doi_only["doi"].str.lower()
    doi_only.drop_duplicates("doi", inplace=True)
    del doi_only["halId"]

    hal_only = rawdf[(
            rawdf["doi"].isna() & rawdf["halId"].notna())].copy()  # possèdent un hal_id mais pas de doi
    del hal_only["doi"]

    hal_verify_doi = pd.merge(doi_only, hal_only, on="title_norm")
    hal_verify_doi.sort_values("title_norm", inplace=True)  # sélectionne les doublons de titre, donc les documents HAL visés
    hal_verify_doi.drop(columns=["title_y", "title_norm"], inplace=True)
    hal_verify_doi.to_csv("./resultats/fichiers_csv/erreurs/hal_sans_doi.csv", index=False, encoding="utf8")


def identifie_doublons_titres_to_csv(rawdf):
    """
    Identifier les doublons de titre sur les notices HAL sans DOI.
    :param pd.Dataframe rawdf: dataframe non dédoublonné
    """
    hal_only = rawdf[(
            rawdf["doi"].isna() & rawdf["halId"].notna())].copy()
    # identification des doublons de titre
    hal_only["duplicated"] = hal_only.duplicated("title_norm", keep=False)
    hal_only_doubl = hal_only[hal_only["duplicated"]].copy()
    hal_only_doubl.sort_values("title", inplace=True)
    hal_only_doubl.drop(["doi", "title_norm", "duplicated"], axis=1, inplace=True)
    hal_only_doubl.to_csv("./resultats/fichiers_csv/erreurs/doublons_titres.csv", index=False, encoding="utf8")
