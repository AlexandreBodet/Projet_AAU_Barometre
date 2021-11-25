import os


def dossiers_data():
    """
    Crée les dossiers nécessaires s'ils n'existaient pas déjà
    """
    if not os.path.isdir("./data"):
        os.mkdir("./data")
    if not os.path.isdir("./data/dois"):
        os.mkdir("./data/dois")
    if not os.path.isdir("./data/apc_tracking"):
        os.mkdir("./data/apc_tracking")
    if not os.path.isdir("./resultats"):
        os.mkdir("./resultats")
    if not os.path.isdir("./resultats/fichiers_csv"):
        os.mkdir("./resultats/fichiers_csv")
    if not os.path.isdir("./resultats/fichiers_csv/erreurs"):
        os.mkdir("./resultats/fichiers_csv/erreurs")
    if not os.path.isdir("./resultats/img"):
        os.mkdir("./resultats/img")
