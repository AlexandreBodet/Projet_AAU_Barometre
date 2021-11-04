"""
Fonctions pour consolider les sources
"""

import pandas as pd
import re
import unidecode


def normalize_txt(title):
    """retirer les espaces, les accents, tout en minuscules, retirer les caractères spéciaux"""
    cut = re.split("\W+", str(title))
    join_cut = "".join(cut).lower()
    return unidecode.unidecode(join_cut)


def conforme_df(df, col_name):
    """garde les colonnes de col_name, les renommes et passe en minuscule doi et titre """
    # memo : on ne supprime pas la colonne titre, car elle est utilisée pour le dédoublonnage
    df = df[list(col_name.keys())].copy()
    df.rename(columns=col_name, inplace=True)

    df["doi"] = df["doi"].str.lower()  # doi en minuscule
    df["title_norm"] = df["title"].apply(lambda row: normalize_txt(row))
    return df


def chargement_hal(hal_file=""):
    if hal_file:
        # chargement, garde certaines colonnes et transformations des titres du fichier HAL
        # fichier_hal = "../data/" + hal_file
        hal = pd.read_csv("../data/" + hal_file, sep=';',
                          skiprows=1)  # sep et skiprows afin de s'adapter au fichier csv
        hal = conforme_df(hal, {"DOI": "doi", 'Réf. HAL': 'halId', 'Titre': 'title'})
    else:  # Si le fichier n'est pas spécifié
        hal = None
    return hal


def chargement_scopus(scopus_file=""):
    if scopus_file:
        # Chargement
        # fichier_scopus = "../data/" + scopus_file
        scopus = pd.read_csv("../data/" + scopus_file, encoding='utf8')
        scopus = conforme_df(scopus, {"DOI": "doi", "Title": "title"})
    else:  # Si pas de fichier spécifié
        scopus = None
    return scopus


def chargement_wos(wos_file=[]):
    if wos_file:
        # fichier_wos = ["wos_2016a.txt", "wos_2016b.txt", "wos_2016c.txt", "wos_2017a.txt", "wos_2017b.txt",
        #               "wos_2017c.txt", "wos_2018a.txt", "wos_2018b.txt", "wos_2018c.txt", "wos_2019a.txt",
        #               "wos_2019b.txt", "wos_2019c.txt", "wos_2020a.txt", "wos_2020b.txt", "wos_2020c.txt"]
        df_buffer = []
        for f in wos_file:
            df = pd.read_csv("../data/"+f, sep="\t", index_col=False)
            df_buffer.append(df)
        wos = pd.concat(df_buffer)
        wos = conforme_df(wos, {"DI": "doi", "TI": "title"})
    else:
        wos = None
    return wos


def chargement_pubmed(pubmed_file=""):
    if pubmed_file:
        pubmed = pd.read_csv("../data/" + pubmed_file)
        pubmed = conforme_df(pubmed, {"DOI": "doi", "Title": "title"})
    else:
        pubmed = None
    return pubmed


def removeJoinDois(x):
    # retirer les listes de doi assemblé par "; "
    doi = str(x).strip()
    if "; " in doi:
        cut = doi.split("; ")
        return cut[0]
    else:
        return x


def chargement_lens(lens_file=""):
    if lens_file:
        lens = pd.read_csv("../data/" + lens_file)
        lens = conforme_df(lens, {"DOI": "doi", "Title": "title"})
        lens["doi"] = lens["doi"].apply(lambda x: removeJoinDois(x))
    else:
        lens = None
    return lens


def extract_stats_from_base(src_name, df, stats_buffer):
    """de la base extraire les données total publications, doi only, no doi"""
    if stats_buffer is None:
        stats_buffer = []
    no_doi = df["doi"].isna().sum()
    w_doi = df["doi"].str.match("10.").sum()
    if no_doi + w_doi == len(df.index):
        print(f"\n\n{src_name} imported ok\n\tdois {w_doi}\n\tno dois {no_doi}")
        stats_buffer.append([src_name, len(df.index), w_doi, no_doi])
    else:
        print(f"{src_name} not imported")


def statistiques_bases(hal_df=None, scopus_df=None, wos_df=None, pubmed_df=None):
    """" Extrait les statistiques de toutes les bases données"""
    stats = []

    if hal_df is not None:
        extract_stats_from_base("hal", hal_df, stats)

    if scopus_df is not None:
        extract_stats_from_base("scopus", scopus_df, stats)

    if wos_df is not None:
        extract_stats_from_base("wos", wos_df, stats)

    if pubmed_df is not None:
        extract_stats_from_base("pubmed", pubmed_df, stats)
