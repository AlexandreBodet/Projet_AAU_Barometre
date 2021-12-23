"""
Exécuter ce fichier python pour générer les fichiers de documentations html, mis à part Projet_AAU_Barometre.html généré à la main.
"""

import subprocess
import os

path = "./src"
base = "src"
subprocess.run("pydoc -w src", check=True, shell=True)
os.rename("./src.html", "./documentation/src.html")


def parcours(dossier, labase):
    """
    Fonction récursive pour générer la documentation à partir de src.

    :param str dossier: dossier initial
    :param str labase: nom du dossier
    :return: None
    """
    for item in os.listdir(dossier):
        if item == "__pycache__":
            pass
        elif os.path.isdir(dossier+"/"+item):
            print("item : "+item+" is dir")
            subprocess.run("pydoc -w " + labase + "." + item, check=True, shell=True)
            os.rename("./" + labase + "." + item + ".html", "./documentation/" + labase + "." + item + ".html")
            parcours(dossier+"/"+item, labase + "." + item)
        else:
            subprocess.run("pydoc -w " + labase + "." + item[:-3], check=True, shell=True)
            print("item " + item)
            os.rename("./" + labase + "." + item[:-3] + ".html", "./documentation/" + labase + "." + item[:-3] + ".html")


parcours(path, base)
