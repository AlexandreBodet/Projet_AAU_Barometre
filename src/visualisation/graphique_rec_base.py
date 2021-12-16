import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date


def graphique_comparaison_bases(dossier):
    """
    Comparaison du nombre de publications dans les bases scopus wos hal et cie.
    :param str dossier: dossier unique dans lequel enregistrer les résultats

    """
    # Récupérer les données
    df = pd.read_csv("./resultats/fichiers_csv/statistiques_sur_les_bases.csv")
    if len(df) == 2:
        df_use = df[~df.name.isin(["retenu"])]
    else:
        df_use = df.copy()
    data = df_use.to_dict("list")
    x = np.arange(len(data["name"]))  # the label locations
    width = 0.2

    # Passer les données dans le modèle de representation graphique
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(
        x - width,
        data["all"],
        width,
        label="toutes publications",
        color="orchid")
    ax.bar(x, data["doi"], width, label="publications avec DOI", color="gold")
    ax.bar(
        x + width,
        data["no_doi"],
        width,
        label="publications sans DOI",
        color="skyblue")

    # Configurer l'affichage
    ax.yaxis.grid(ls="--", alpha=0.4)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    # Retirer l'origine sur Y
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)

    plt.yticks([i for i in range(0, 1500, 250)], fontsize=10)
    ax.set_ylabel("Nombre de publications", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels([n.capitalize() for n in data["name"]], fontsize=11)
    plt.legend(loc="upper center", fontsize=8)

    ax.set_title(
        "Quantité de publications dans les bases\nmesurée en " + str(date.today().month) + "/" + str(date.today().year),
        fontsize=16, alpha=0.6, y=1.05)
    plt.savefig("./resultats/img/" + dossier + "/recapitulatif_bases.png", dpi=150, bbox_inches="tight",
                pad_inches=0.05)
    plt.close()
