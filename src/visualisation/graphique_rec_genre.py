import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import date


def graphique_genre(df, dossier, annee=None):
    """
    Nombre de publications par discipline
    :param pd.Dataframe df:
    :param str dossier: dossier unique dans lequel enregistrer les résultats
    :param annee: int, list ou None. Désigne les années à sélectionner. None laisse toutes les publications
    """
    print("graphique genre" + str(annee))

    if type(annee) == int:
        year = df[df["published_year"] == annee].copy()
    elif type(annee) == list:  # une liste d'années
        year = df[df["published_year"].isin(annee)].copy()
    else:  # Sinon on prend tout
        year = df.copy()

    df_oa = year[["genre", "is_oa"]]

    scifield = pd.crosstab(df_oa["genre"], df_oa["is_oa"])
    scifield.columns = ["not_oa", "is_oa"]
    scifield["total"] = scifield["not_oa"] + scifield["is_oa"]

    # Passer les données dans le modèle de représentation
    fig, (ax) = plt.subplots(figsize=(12, 7), dpi=100, facecolor="w", edgecolor="k")

    ax.bar(
        scifield.index,
        scifield["is_oa"].tolist(),
        color="#7E96C4",
        align="center",
        label="Accès ouvert")

    ax.bar(
        scifield.index,
        scifield["not_oa"].tolist(),
        bottom=scifield["is_oa"].tolist(),
        align="center",
        color="#BED0F4",
        label="Accès fermé")

    # Configurer l'affichage
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # ax.spines["left"].set_visible(False)
    # retirer l'origine sur Y
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    ax.yaxis.grid(ls="--", alpha=0.4)
    ax.xaxis.set_major_locator(mticker.FixedLocator(
        [x for x in range(len(scifield.index))]))  # pour éviter un warning, on fixe la position des labels
    ax.set_xticklabels(scifield.index, ha="right", rotation=30, fontsize=12)

    # plt.tight_layout()
    plt.legend(loc="upper center", fontsize=14, borderaxespad=1.7)

    if type(annee) == int:
        plt.title(
            "Nombre de publications par genre en " + str(annee) + "\nmesurée en " +
            str(date.today().month) + "/" + str(date.today().year),
            fontsize=20,
            x=0.5,
            y=1,
            alpha=0.6)
        plt.savefig("./resultats/img/" + dossier + "/" + str(annee) + "/recapitulatif_genre.png", bbox_inches="tight")
    elif type(annee) == list:
        plt.title(
            "Nombre de publications par genre entre " + str(annee[0]) + " et " + str(annee[-1]) + "\nmesurée en " +
            str(date.today().month) + "/" + str(date.today().year),
            fontsize=20,
            x=0.5,
            y=1,
            alpha=0.6)
        plt.savefig("./resultats/img/" + dossier + "/" + str(annee[0]) + "-" + str(
            annee[-1]) + "/recapitulatif_genre.png", bbox_inches="tight")
    else:
        plt.title(
            "Nombre de publications par genre" + "\nmesurée en " +
            str(date.today().month) + "/" + str(date.today().year),
            fontsize=20,
            x=0.5,
            y=1,
            alpha=0.6)
        plt.savefig("./resultats/img/" + dossier + "/recapitulatif_genre.png", bbox_inches="tight")
    plt.close()
