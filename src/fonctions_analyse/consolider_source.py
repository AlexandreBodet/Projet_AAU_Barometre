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


def extract_stats_from_base(src_name, df, stats_buffer=None):
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


def chargement_hal(hal_file):
    if hal_file != "":
        # chargement, garde certaines colonnes et transformations des titres du fichier HAL
        fichier_hal = "../data/" + hal_file
        hal = pd.read_csv(fichier_hal, sep=';',
                          skiprows=1)  # sep et skiprows afin de s'adapter au fichier csv
        hal = conforme_df(hal, {"DOI": "doi", 'Réf. HAL': 'halId', 'Titre': 'title'})
    else:
        hal = None
    return hal


def statistiques_bases(hal_df=None):
    """ Extrait les statistiques de toutes les bases données"""
    stats = []

    if hal_df is not None:
        extract_stats_from_base("hal", hal_df, stats)