import subprocess
import os

path = "../src"
base = "src"
subprocess.run("pydoc -w main", check=True, shell=True)
subprocess.run("pydoc -w src", check=True, shell=True)


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
            parcours(dossier+"/"+item, labase + "." + item)
        else:
            subprocess.run("pydoc -w " + labase + "." + item[:-3], check=True, shell=True)


parcours(path, base)
