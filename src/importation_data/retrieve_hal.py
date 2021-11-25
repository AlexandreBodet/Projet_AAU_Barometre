import requests as r
import pandas as pd


def req_to_pd(requete):
    """Fait la requête pour récupérer l'ensemble des publications du laboratoire
    :param str requete: requête url
    :return dataframe df: dataframe de la réponse
    """
    res = r.get(requete).json()["response"]["docs"]
    df = pd.json_normalize(res)
    return df


def api_to_csv(fichier_hal="", query=""):
    """Sauvegarder le dataframe en csv.
    :param str query: query à utiliser dans l'API
    :param str fichier_hal: du fichier à enregistrer
    """
    if fichier_hal and query:
        df = req_to_pd(query)
        df.rename(columns={"doiId_s": "DOI", "halId_s": "Réf. HAL", "title_s": "Titre"}, inplace=True)
        df.to_csv("./data/dois/" + fichier_hal, index=False, encoding="utf8", sep=";")
