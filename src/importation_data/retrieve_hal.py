import requests as r
import pandas as pd



def req_to_pd(requete):
    """Fait la requête pour récuperer l'ensemble des publications du laboratoire

    :param str requete: requête url
    :return dataframe df: dataframe de la réponse
    """
    res = r.get(requete).json()['response']['docs']
    df = pd.json_normalize(res)
    
    return df


def api_to_csv(fichier_hal="", query=""):
    """Sauvegarder le dataframe en csv.

    :param fichier_hal: str du fichier à enregistrer
    """
    if fichier_hal:
        df = req_to_pd(query)
        df.rename(columns={"doiId_s": "DOI", "halId_s": "Réf. HAL", "title_s": "Titre"}, inplace=True)
        df.to_csv("../data/dois/hal_from_api.csv", index=False, encoding='utf8', sep=';')