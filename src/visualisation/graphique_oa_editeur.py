import matplotlib.pyplot as plt
import pandas as pd


def graphique_oa_editeur(df, dossier, annee=None):
    """
    Type d'accès ouvert par éditeur. Prend les 20 éditeurs avec le plus de publications pour une année, plusieurs années ou sur toutes les publications.

    :param pd.Dataframe df: dataframe d'entrée
    :param annee: int, list ou None. Désigne les années à sélectionner. None laisse toutes les publications
    :param str dossier: dossier unique dans lequel enregistrer les résultats
    """
    if isinstance(annee, int):
        year = df[df["published_year"] == annee].copy()
    elif isinstance(annee, list):  # une liste d'années
        year = df[df["published_year"].isin(annee)].copy()
    else:  # Sinon on prend tout
        year = df.copy()
    print("graphique oa editeur", annee)

    # Fusionner les éditeurs similaires
    year["publisher"].replace({"Elsevier BV": "Elsevier"}, inplace=True)
    year["publisher"].replace(
        {"Springer Science and Business Media LLC": "Springer"}, inplace=True)
    year["publisher"].replace(
        {"Springer International Publishing": "Springer"}, inplace=True)

    publications_par_editeur = year["publisher"].value_counts().iloc[0:20]  # 20 premiers éditeurs sélectionnés

    # Récupérer les données d'accès ouvert
    df_oa_editeur = pd.crosstab(
        [year["publisher"]], year["oa_type"])
    # Convertir le résultat en pourcentages
    df_oa_editeur = (df_oa_editeur.T / df_oa_editeur.T.sum()).mul(100).round(1)
    df_oa_editeur = df_oa_editeur.T
    df_oa_editeur["Total"] = publications_par_editeur
    df_oa_editeur.dropna(inplace=True)  # On supprime les lignes de publishers qui ne sont pas dans le top 20
    df_oa_editeur["y_label"] = df_oa_editeur.index + " - " + df_oa_editeur["Total"].astype(int).apply(
        str) + " publications"
    df_oa_editeur.index = df_oa_editeur["y_label"]
    df_oa_editeur.sort_values(by=["Total", "closed"], ascending=[False, True], inplace=True)

    # __2__ Générer le graphique

    ax = df_oa_editeur.drop(["Total",
                             "y_label"],
                            axis=1).plot(kind="barh",
                                         stacked=True,
                                         figsize=(15,
                                                  13),
                                         color=["tomato",
                                                "gold",
                                                "greenyellow",
                                                "seagreen"])

    # ___3____ Configurer l"affichage

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    # enlever xticks
    plt.tick_params(
        axis="x",  # changement sur l'axe x
        which="both",  # les ticks majeurs et mineurs sont affectés
        bottom=False,  # pas de ticks sur le bord du bas
        labelbottom=False)  # pas de labels en bas

    # Ajouter le pourcentage pour chaque type
    labels = []
    for j in df_oa_editeur.columns:
        for i in df_oa_editeur.index:
            label = df_oa_editeur.loc[i][j]
            # label = str(df_oa_editeur.loc[i][j]) + "%"
            if not isinstance(label, str):
                label = round(label)
                label = str(label) + "%"
                labels.append(label)

    patches = ax.patches
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 1:  # mettre > 0 pour avoir les faibles pourcentages, >1 pour ne pas surcharger
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            ax.text(
                x + .3 + width / 2.,
                y + height / 2.,
                label,
                ha="center",
                va="center",
                fontsize=11)

    plt.gca().invert_yaxis()
    plt.tick_params(axis="both", labelsize=18)
    plt.ylabel(None)

    # générer une première fois sans renommer les colonnes pour s'assurer que le renommage est correct
    plt.legend(["Accès fermé",
                "Éditeur",
                "Éditeur et Archive ouverte",
                "Archive ouverte"],
               loc="best",
               ncol=4,
               markerscale=1,
               title=None,
               fontsize=16,
               borderpad=0.2,
               labelspacing=0.3,
               bbox_to_anchor=(0.01,
                               0.985),
               framealpha=False)

    if isinstance(annee, int):
        plt.title(
            "Taux d'accès ouvert aux publications en " + str(annee) + " par éditeur",
            fontsize=34,
            x=0.49,
            y=1.1,
            alpha=0.6)
        plt.suptitle(
            "Visualisation des 20 premiers éditeurs par quantité de publications",
            fontsize=20,
            x=0.49,
            y=0.95,
            alpha=0.6)
        plt.savefig(
            "./resultats/img/" + dossier + "/" + str(annee) + "/oa_editeur.png",
            dpi=100,
            bbox_inches="tight",
            pad_inches=0.9)
    elif isinstance(annee, list):
        plt.title(
            "Taux d'accès ouvert aux publications entre " + str(annee[0]) + " et " + str(annee[-1]) + " par éditeur",
            fontsize=34,
            x=0.49,
            y=1.1,
            alpha=0.6)
        plt.suptitle(
            "Visualisation des 20 premiers éditeurs par quantité de publications",
            fontsize=20,
            x=0.49,
            y=0.95,
            alpha=0.6)
        plt.savefig(
            "./resultats/img/" + dossier + "/" + str(annee[0]) + "-" + str(annee[-1]) + "/oa_editeur.png",
            dpi=100,
            bbox_inches="tight",
            pad_inches=0.9)
    else:
        plt.title(
            "Taux d'accès ouvert aux publications par éditeur",
            fontsize=34,
            x=0.49,
            y=1.1,
            alpha=0.6)
        plt.suptitle(
            "Visualisation des 20 premiers éditeurs par quantité de publications",
            fontsize=20,
            x=0.49,
            y=0.95,
            alpha=0.6)
        plt.savefig(
            "./resultats/img/" + dossier + "/oa_editeur.png",
            dpi=100,
            bbox_inches="tight",
            pad_inches=0.9)
    plt.close()
