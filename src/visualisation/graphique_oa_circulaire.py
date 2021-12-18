import matplotlib.pyplot as plt
import pandas as pd
from datetime import date


def graphique_circulaire_oa(df, dossier, annee=None):
    """
    Graphique circulaire de bilan open access
    :param pd.Dataframe df: dataframe utilisé
    :param str dossier: dossier unique dans lequel enregistrer les résultats
    :param annee: int, list ou None. Désigne les années à sélectionner. None laisse toutes les publications
    """

    print("graphique discipline oa circulaire", annee)

    if isinstance(annee, int):
        dfpie = df[df["published_year"] == annee].copy()
    elif isinstance(annee, list):  # une liste d'années
        dfpie = df[df["published_year"].isin(annee)].copy()
    else:  # Sinon on prend tout
        dfpie = df.copy()

    oa_bool = dfpie["is_oa"].value_counts().sort_index()
    oa_bool = oa_bool.rename({True: "Accès ouvert", False: "Accès fermé"})

    oa_type = dfpie["oa_type"].value_counts().sort_index()
    oa_type = oa_type.rename({"closed": "Accès fermé",
                              "publisher": "Éditeur",
                              "repository": "Archive ouverte",
                              "publisher;repository": "Éditeur et Archive ouverte"})

    fig, ax = plt.subplots(dpi=100)
    ax.set_aspect("equal")
    ax.pie(
        oa_bool,
        labels=oa_bool.index,
        radius=3,
        labeldistance=None,
        colors=["tomato", "springgreen"],
        autopct=lambda x: str(round(x, 1)) + "%",
        pctdistance=0.9,
        shadow=True)
    ax.pie(
        oa_type,
        labels=oa_type.index,
        radius=2.3,
        labeldistance=None,
        colors=["firebrick", "gold", "greenyellow", "seagreen"],
        autopct=lambda x: str(round(x, 1)) + "%",
        pctdistance=0.9)

    ax.pie([1], radius=1.3, colors="white")

    # légende : réordonner les éléments
    handles, labels = ax.get_legend_handles_labels()
    order = [0, 1, 3, 4, 5]
    ax.legend([handles[idx] for idx in order],
              [labels[idx] for idx in order],
              fontsize=14,
              loc="center",
              framealpha=1,
              frameon=True,
              borderaxespad=-1)

    # ax.legend(loc="", fontsize = 12)
    mesure_en = "\nmesurée en " + str(date.today().month) + "/" + str(date.today().year)
    if isinstance(annee, int):
        plt.title("Proportion des publications en accès ouvert en " + str(annee) + mesure_en, fontsize=23, x=0.55,
                  y=1.8, alpha=0.6)
        plt.savefig("./resultats/img/" + dossier + "/" + str(annee) + "/oa_circulaire.png", dpi=150,
                    bbox_inches="tight", pad_inches=0.9)
    elif isinstance(annee, list):
        plt.title(
            "Proportion des publications en accès ouvert entre " + str(annee[0]) + " et " + str(annee[-1]) + mesure_en,
            fontsize=23, x=0.55, y=1.8, alpha=0.6)
        plt.savefig("./resultats/img/" + dossier + "/" + str(annee[0]) + "-" + str(annee[-1]) + "/oa_circulaire.png",
                    dpi=150, bbox_inches="tight", pad_inches=0.9)
    else:
        plt.title(
            "Proportion des publications en accès ouvert" + mesure_en, fontsize=23, x=0.55, y=1.8, alpha=0.6)
        plt.savefig("./resultats/img/" + dossier + "/oa_circulaire.png", dpi=150,
                    bbox_inches="tight", pad_inches=0.9)
    plt.close()
