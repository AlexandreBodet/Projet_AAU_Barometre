"""
Fonctions pour récupérer les métadonnées associées aux publications
"""
import os
import time
import numpy as np
import requests as r
import pandas as pd
import json as j
from ast import literal_eval


def req_to_json(url):
    """
    S'assurer que la réponse de l'API est en JSON.

    :param str url: url de la requête
    :return dict res: résultat json de la requête sql
    """
    while True:
        try:
            req = r.get(url)
            break  # sort de la boucle si le serveur a répondu
        except r.exceptions.ConnectionError:
            time.sleep(0.5)
            pass  # réessaye après 0.5 seconde si le serveur ne répond pas
    res = req.json()
    return res


def get_hal_data(doi, hal_id, match):
    """
    Récupérer les métadonnées de HAL.
    Si le DOI est dans unpaywall les métadonnées de HAL communes seront écrasées.

    :param str match: dictionnaire pour match les références
    :param str doi: doi dont les données sont à récupérer
    :param str hal_id: hal id dont les données sont à récupérer
    :return dict: dictionnaire des métadonnées récupérées
    """

    if hal_id:
        query = f"halId_s:{str(hal_id)}"
    elif not hal_id and doi:
        query = "doiId_s:" + str(doi)
    else:
        print("!! problem : no doi & no halId")
        return {}

    res = req_to_json("https://api.archives-ouvertes.fr/search/?q=" + query +
                      "&fl=halId_s,title_s,authFullName_s,publicationDate_s,publicationDateY_i,docType_s,journalTitle_s,journalIssn_s,"
                      "journalEissn_s,journalPublisher_s,*_domain_s,domain_t,submittedDate_s,submitType_s,linkExtId_s,openAccess_bool,licence_s,selfArchiving_bool"
                      )

    # Si l'API renvoie une erreur ou bien si aucun document n'est trouvé
    if res.get("error") or res["response"]["numFound"] == 0:
        return {
            "hal_coverage": "missing"
        }

    res = res["response"]["docs"][0]
    # print(json.dumps(res, indent = 2))

    # déduire hal_location
    if res["submitType_s"] == "file":
        hal_location = "file"  # primauté sur les fichiers de HAL comparé a Arxiv ou pubmed
    elif res["submitType_s"] == "notice" and (
            res.get("linkExtId_s") == "arxiv" or res.get("linkExtId_s") == "pubmedcentral"):
        hal_location = res["linkExtId_s"]
    else:
        hal_location = "notice"

    # déduire les ISSNs
    issn = [res.get("journalIssn_s"), res.get("journalEissn_s")]
    issn = [item for item in issn if item]
    issn = ",".join(issn) if issn else False

    # Vérifier la présence de domaine disciplinaire (quelques notices peuvent ne pas avoir de domaine)

    domain = []
    shsdomain = []
    infodomain = []
    if res.get("level0_domain_s"):
        for e in res["level0_domain_s"]:
            e = "0." + e
            if e in match["domain"]:
                if e not in domain:
                    domain.append(e)
    if res.get("level1_domain_s"):
        for e in res["level1_domain_s"]:
            e = "1." + e
            if e in match["shsdomain"]:
                if e not in shsdomain:
                    shsdomain.append(e)
            if e in match["infodomain"]:
                if e not in infodomain:
                    infodomain.append(e)

    auth_count = False
    if res.get("authFullName_s"):
        auth_count = len(res["authFullName_s"])

    return {
        # Métadonnées partagées avec unpaywall
        "title": res["title_s"][0],
        "author_count": auth_count,
        "published_date": res.get("publicationDate_s"),
        "published_year": res.get("publicationDateY_i"),
        "journal_name": res.get("journalTitle_s"),
        "journal_issns": issn,
        "publisher": res.get("journalPublisher_s"),
        # métadonnées propres à HAL
        "halId": res.get("halId_s"),
        "hal_coverage": "in",
        "hal_submittedDate": res.get("submittedDate_s"),
        "hal_location": hal_location,
        "hal_openAccess_bool": res.get("openAccess_bool"),
        "hal_licence": res.get("licence_s"),
        "hal_selfArchiving": res.get("selfArchiving_bool"),
        "hal_docType": res.get("docType_s"),
        "hal_domain": domain,
        "hal_shsdomain": shsdomain,
        "hal_infodomain": infodomain

    }


def get_upw_data(doi, email):
    """
    Récupérer les métadonnées de Unpaywall.

    :param str email: email utilisé pour faire la requête à l'API
    :param str doi: doi dont les métadonnées doivent être récupérées
    :return dict: dictionnaire des métadonnées récupérées
    """
    # 2021-07-16 inclure/encoder # dans caractère
    # exemple "10.1002/(sici)1521-3951(199911)216:1<135::aid-pssb135>3.0.co;2-#"
    """
    doi.replace("#", "%23")
    doi.replace(";", "%3B")
    doi.replace(",", "%2C")
    """

    res = req_to_json(
        f"https://api.unpaywall.org/v2/{doi}?email={email}")

    # Déduire upw_coverage
    if res.get("message") and "isn't in Unpaywall" in res.get("message"):
        upw_coverage = "missing"
    elif res.get("is_oa"):
        upw_coverage = "oa"
    else:
        upw_coverage = "closed"

    # Facultatif : déduire nombre auteurs
    author_count = len(res["z_authors"]) if res.get("z_authors") else False

    # Déduire upw_location
    location = licence = version = None
    if res.get("oa_locations"):
        oa_loc = res.get("oa_locations")
        location = list(set(
            [loc["host_type"] for loc in oa_loc]))
        location = ";".join(location)

        licence = list(set(
            [loc["license"] for loc in oa_loc if loc["license"]]))
        licence = ";".join(licence) if licence else None

        version = list(set(
            [loc["version"] for loc in oa_loc if loc["version"]]))
        version = ";".join(version) if version else None

    return {
        # métadonnées partagées avec HAL
        "title": res.get("title"),
        "author_count": author_count,
        "published_date": res.get("published_date"),
        "published_year": res.get("year"),
        "journal_name": res.get("journal_name"),
        "journal_issns": res.get("journal_issns"),
        "publisher": res.get("publisher"),
        # métadonnées propres à unpaywall
        "genre": res.get("genre"),
        "journal_is_in_doaj": res.get("journal_is_in_doaj"),
        "upw_coverage": upw_coverage,
        "is_paratext": res.get("is_paratext"),
        "journal_issn_l": res.get("journal_issn_l"),
        "journal_is_oa": res.get("journal_is_oa"),
        "oa_status": res.get("oa_status"),
        "upw_location": location,
        "licence": licence,
        "version": version
    }


def enrich_df(df, email, match_ref, progression_denominateur):
    """
    Pour chaque publication lancer les requêtes et ajouter les métadonnées.

    :param str match_ref: nom du fichier qui contient le dictionnaire pour match les références
    :param str email: email utilisé pour la requête Unpaywall avec l'API
    :param progression_denominateur: dénominateur pour afficher les intervalles des étapes
    :param pd.Dataframe df: dataframe auquel ajouter les métadonnées
    :return pd.Dataframe: dataframe modifié
    """
    buffer_folder = "./resultats/fichiers_csv/buffer/"
    buffer = "buffer_recuperer_data.csv"
    try:
        # Buffer si la connexion crashe pendant la récupération des données
        df_traite = pd.read_csv(buffer_folder + buffer, converters={"doi": str}, na_filter=False,
                                encoding="utf8")
        df_traite.replace("", np.nan,
                          inplace=True)  # Pour empêcher le merge de supprimer des lignes à cause de la lecture du nan comme ""
        df.replace("", np.nan, inplace=True)
        df = pd.merge(df, df_traite, on=["doi", "halId"])
    except FileNotFoundError:
        df["is_paratext"] = np.nan
        df["suspicious_journal"] = np.nan
        df["hal_domain"] = np.nan
        df["df_data_traite"] = False
        if not os.path.isdir(buffer_folder):
            os.mkdir(buffer_folder)

    with open("./data/" + match_ref, "r", encoding="utf-8") as json_file:
        match = j.load(json_file)

    for row in df.itertuples():
        if df.loc[row.Index, "df_data_traite"]:
            continue  # Passe la récupération des métadonnées pour la ligne si elle a déjà été effectuée, utilise le buffer

        # À chaque étape selon l'espacement entre les affichages voulu, afficher la progression et enregistrer un buffer
        # Le dénominateur impacte l'intervalle des étapes : 100 une étape tout les 1%, etc
        if row.Index > 0 and row.Index % int(len(df) / progression_denominateur) == 0:
            print("Ligne : ", row.Index, "Progression de la récupération des métadonnées : ",
                  round(row.Index / len(df) * progression_denominateur, 1), "%")
            df.to_csv(buffer_folder + buffer, index=False)

        # Récupérer les métadonnées de HAL
        md = get_hal_data(row.doi, row.halId, match)

        # S'il y a un DOI, prendre les données de Unpaywall.
        # Les métadonnées de HAL communes avec Unpaywall seront écrasées.
        if not pd.isna(row.doi):  # avant, c'était seulement if row.doi, mais ça passait tout le temps
            add = get_upw_data(row.doi, email)
            # Ajout des métadonnées qui ne sont pas False
            md.update((k, v) for k, v in add.items() if v)

        # Ajouter les métadonnées au dataframe
        for field in md:
            if field == "hal_domain":
                new_domain = pd.Series([md[field]], index=[row.Index], dtype="object")
                df.loc[[row.Index], "hal_domain"] = new_domain
            elif field == "hal_shsdomain":
                new_domain = pd.Series([md[field]], index=[
                    row.Index], dtype="object")
                df.loc[[row.Index], "hal_shsdomain"] = new_domain
            elif field == "hal_infodomain":
                new_domain = pd.Series([md[field]], index=[
                    row.Index], dtype="object")
                df.loc[[row.Index], "hal_infodomain"] = new_domain
            else:
                df.loc[row.Index, field] = md[field]
        df.loc[row.Index, "df_data_traite"] = True  # Utile pour le buffer

    # on supprime les données utilisées par le buffer
    os.remove(buffer_folder + buffer)
    os.rmdir(buffer_folder)
    df.drop(["df_data_traite"], axis=1, inplace=True)
    return df


def enrich_to_csv(df, email, match_ref="match_referentials.json", progression_denominateur=100):
    """
    Enrichi en métadonnées et enregistre en csv.

    :param str match_ref: nom du fichier qui contient le dictionnaire pour match les références
    :param str email: email utilisé pour la requête à l'API Unpaywall
    :param pd.Dataframe df: dataframe auquel ajouter les métadonnées
    :param progression_denominateur: dénominateur pour afficher les intervalles des étapes dans enrich_df
    :return pd.Dataframe: dataframe avec métadonnées ajoutées
    """
    df.reset_index(drop=True, inplace=True)
    df = enrich_df(df, email, match_ref, progression_denominateur)
    try:
        df_reorder = df[["doi", "halId", "hal_coverage", "upw_coverage", "title", "hal_docType", "hal_location",
                         "hal_openAccess_bool", "hal_submittedDate", "hal_licence", "hal_selfArchiving", "hal_domain",
                         "hal_shsdomain", "hal_infodomain", "published_date", "published_year", "journal_name",
                         "journal_issns", "publisher", "genre", "journal_issn_l", "oa_status", "upw_location",
                         "version", "suspicious_journal", "licence", "journal_is_in_doaj", "journal_is_oa",
                         "author_count", "is_paratext"]]
    except KeyError:
        print("\n\n\n\n\n!!!\n!Vérifier l'adresse mail dans les settings, certaines informations sont manquantes!\n!!!\n")
        df_reorder = df.copy()
    df_reorder.to_csv("./resultats/fichiers_csv/df_metadonnees.csv", index=False, encoding="utf8")
