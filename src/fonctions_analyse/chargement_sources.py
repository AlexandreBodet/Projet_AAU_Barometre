"""
Fonctions pour consolider les sources
"""

import pandas as pd
import re
import unidecode
from fonctions_analyse.dedoublonnage import dedoublonnage_doi, dedoublonnage_titre, doi_ou_hal

def normalize_txt(title):
    """Retirer les espaces, les accents, tout en minuscules, retirer les caractères spéciaux.

    :param str title: titre à normaliser
    :return str join_cut: titre normalisé
    """
    cut = re.split("\W+", str(title))
    join_cut = "".join(cut).lower()
    join_cut = unidecode.unidecode(join_cut)
    return join_cut


def conforme_df(df, col_name):
    """Garde les colonnes de col_name, les renommes et passe en minuscule doi et titre.

    :param dataframe df: dataframe dont les titres et doi sont normalisés
    :param dict[str,str] col_name: colonnes à garder
    :return dataframe: dataframe modifié
    """
    # memo : on ne supprime pas la colonne titre, car elle est utilisée pour le dédoublonnage
    df = df[list(col_name.keys())].copy()
    df.rename(columns=col_name, inplace=True)

    df["doi"] = df["doi"].str.lower()  # doi en minuscule
    df["title_norm"] = df["title"].apply(lambda row: normalize_txt(row))
    return df


def chargement_hal(hal_file=""):
    """Charge un fichier hal

    :param str hal_file: du nom de fichier à charger
    :return dataframe: dataframe chargé
    """

    if hal_file:
        # chargement, garde certaines colonnes et transformations des titres du fichier HAL
        # fichier_hal = "../data/" + hal_file

        # ce qui suit a été fait par alan:
        #je mets un if pour qu'on puisse faire les tests entre l'extrHAL et l'api plus facilement
        #si extraction HAL depuis extrHAL : 
        if(hal_file == "extractionHAL.csv"):
            hal = pd.read_csv("../data/dois/" + hal_file, sep=';',
                            skiprows=1)  # !!! attention, sep et skiprows dépend du fichier !!!
            hal = conforme_df(
                hal, {"DOI": "doi", 'Réf. HAL': 'halId', 'Titre': 'title'})
        elif(hal_file == "hal_from_api.csv"):
        #si extraction HAL depuis l'API
            hal = pd.read_csv("../data/dois/" + hal_file, sep=';',
                          skiprows=0)  # !!! attention, sep et skiprows dépend du fichier !!!
        
            hal = conforme_df(hal, {"doiId_s": "doi", 'halId_s': 'halId', 'title_s': 'title'})
    else:  # Si le fichier n'est pas spécifié
        hal = None
    return hal


def chargement_scopus(scopus_file=""):
    """Charge un fichier scopus

    :param str scopus_file: nom de fichier à charger
    :return dataframe: dataframe chargé
    """
    if scopus_file:
        # Chargement
        # fichier_scopus = "../data/" + scopus_file
        scopus = pd.read_csv("../data/dois/" + scopus_file, encoding='utf8')
        scopus = conforme_df(scopus, {"DOI": "doi", "Title": "title"})
    else:  # Si pas de fichier spécifié
        scopus = None
    return scopus


def chargement_wos(wos_file=None):
    """Charge un fichier wos

    :param list wos_file: nom de fichier à charger
    :return dataframe: dataframe chargé
    """
    if wos_file:
        # fichier_wos = ["wos_2016a.txt", "wos_2016b.txt", "wos_2016c.txt", "wos_2017a.txt", "wos_2017b.txt",
        #               "wos_2017c.txt", "wos_2018a.txt", "wos_2018b.txt", "wos_2018c.txt", "wos_2019a.txt",
        #               "wos_2019b.txt", "wos_2019c.txt", "wos_2020a.txt", "wos_2020b.txt", "wos_2020c.txt"]
        df_buffer = []
        for f in wos_file:
            df = pd.read_csv("../data/dois/" + f, sep="\t", index_col=False)
            df_buffer.append(df)
        wos = pd.concat(df_buffer)
        wos = conforme_df(wos, {"DI": "doi", "TI": "title"})
    else:
        wos = None
    return wos


def chargement_pubmed(pubmed_file=""):
    """Charger un fichier pubmed

    :param str pubmed_file: nom de fichier à charger
    :return dataframe: dataframe chargé
    """
    if pubmed_file:
        pubmed = pd.read_csv("../data/dois/" + pubmed_file)
        pubmed = conforme_df(pubmed, {"DOI": "doi", "Title": "title"})
    else:
        pubmed = None
    return pubmed


def removeJoinDois(x):
    """Retirer les listes de doi assemblé par "; "

    :param str x: liste de dois ou doi
    :return str: premier doi de la liste, ou doi s'il est seul
    """

    #
    doi = str(x).strip()
    if "; " in doi:
        cut = doi.split("; ")
        return cut[0]
    else:
        return x


def chargement_lens(lens_file=""):
    """Charger un fichier lens
    
    :param str lens_file: du nom de fichier à charger
    :return dataframe: dataframe chargé
    """
    if lens_file:
        lens = pd.read_csv("../data/dois/" + lens_file)
        lens = conforme_df(lens, {"DOI": "doi", "Title": "title"})
        lens["doi"] = lens["doi"].apply(lambda x: removeJoinDois(x))
    else:
        lens = None
    return lens


def extract_stats_from_base(src_name, df, stats_buffer):
    """De la base extraire les données total publications, doi only, no doi.

    :param str src_name: nom de la base de donnée source
    :param dataframe df: dataframe chargé
    :param list stats_buffer: liste des statistiques
    """
    if stats_buffer is None:
        stats_buffer = []
    no_doi = df["doi"].isna().sum()
    w_doi = df["doi"].str.match("10.").sum()
    if no_doi + w_doi == len(df.index):
        print(f"\n\n{src_name} imported ok\n\tdois {w_doi}\n\tno dois {no_doi}")
        stats_buffer.append([src_name, len(df.index), w_doi, no_doi])
    else:
        print(f"{src_name} not imported")


def statistiques_bases(hal_df=None, scopus_df=None, wos_df=None, pubmed_df=None, lens_df=None):
    """ Extrait les statistiques de toutes les bases données

    :param dataframe hal_df: données de hal
    :param dataframe scopus_df: données de scopus
    :param dataframe wos_df: données de wos
    :param dataframe pubmed_df: données de pubmed
    :param dataframe lens_df: données de lens
    :return list: liste des statistiques extraites
    """
    stats = []

    if hal_df is not None:
        extract_stats_from_base("hal", hal_df, stats)

    if scopus_df is not None:
        extract_stats_from_base("scopus", scopus_df, stats)

    if wos_df is not None:
        extract_stats_from_base("wos", wos_df, stats)

    if pubmed_df is not None:
        extract_stats_from_base("pubmed", pubmed_df, stats)

    if lens_df is not None:
        extract_stats_from_base("lens", lens_df, stats)

    return stats


def chargement_tout(data):
    """
    Charge tous les fichiers et donne des statistiques dessus et le dataframe de tous les dataframes

    :param Dict[str,str] data: données issues du fichier settings
    :return list, dataframe: liste des statistiques sur les bases et dataframe des données chargées
    """

    hal = chargement_hal(data["hal_fichier"])
    scopus = chargement_scopus(data["scopus_fichier"])
    wos = chargement_wos(data["wos_fichier"])
    pubmed = chargement_pubmed(data["pubmed_fichier"])
    lens = chargement_lens(data["lens_fichier"])

    stats = statistiques_bases(hal, scopus, wos, pubmed, lens)

    # Dedoublonnage
    df_charge = pd.concat([hal, scopus, wos, pubmed, lens])
    clean_doi = dedoublonnage_doi(df_charge)
    clean_doi_title = dedoublonnage_titre(clean_doi)
    final_df = doi_ou_hal(clean_doi_title)

    stats.append([
        "retenu",
        len(final_df),
        len(final_df[final_df['doi'].notna()]),
        len(final_df[final_df['doi'].isna()])])

    stat_table = pd.DataFrame(stats, columns=[
        'name', 'all', 'doi', 'no_doi'])

    # Sauvegarder les statistiques sur les bases
    stat_table.to_csv(
        "../resultats/fichiers_csv/statistiques_sur_les_bases.csv", index=False)

    # extraire le jeu de données final
    final_df.drop(columns=["title", "title_norm"], inplace=True)
    final_df.to_csv("../resultats/fichiers_csv/consolider_doi_hal_id.csv",
                    index=False, encoding='utf8')

    return stat_table, final_df
