import requests as r
import pandas as pd


def req_to_pd(requete):
    """
    Fait la requête pour récupérer l'ensemble des publications du laboratoire
    :param str requete: requête url
    :return dataframe df: dataframe de la réponse
    """
    res = r.get(requete).json()["response"]["docs"]
    df = pd.json_normalize(res)
    return df


def api_to_csv(fichier_hal="", nom_labo=""):
    """
    Sauvegarder le dataframe en csv.
    :param str nom_labo: nom du labo à utiliser dans la query pour l'API
    :param str fichier_hal: du fichier à enregistrer
    """
    if fichier_hal and nom_labo:
        # query complète pour pouvoir comparer les résultats
        # fullquery_to_see = "https://api.archives-ouvertes.fr/search/?q=collCode_s:"+nom_labo+"%20AND%20docType_s:(COUV+OR+COMM+OR+ART+OR+DOUV)%20AND%20NOT%20popularLevel_s:1&rows=10000&fl=title_s,doiId_s,publicationDate_s,publicationDateY_i,journalTitle_s,journalPublisher_s,halId_s,in,submittedDate_s,openAccess_bool,licence_s,selfArchiving_bool,docType_s,submitType_s,journalIssn_s,journalEissn_s,domain_s,authFullName_s&sort=publicationDateY_i%20desc"

        query = "https://api.archives-ouvertes.fr/search/?q=collCode_s:"+nom_labo+"%20AND%20docType_s:(COUV+OR+COMM+OR+ART+OR+DOUV)%20AND%20NOT%20popularLevel_s:1&rows=101&fl=halId_s,doiId_s,title_s"

        df = req_to_pd(query)
        df.rename(columns={"doiId_s": "DOI", "halId_s": "Réf. HAL", "title_s": "Titre"}, inplace=True)
        df.to_csv("./data/dois/" + fichier_hal, index=False, encoding="utf8", sep=";")
