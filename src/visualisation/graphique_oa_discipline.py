import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


def graphique_discipline_oa(df, dossier, annee=None):
    """
    Graphique d'open access par discipline

    :param pd.Dataframe df: dataframe d'entrée
    :param str dossier: dossier unique dans lequel enregistrer les résultats
    :param annee: int, list ou None. Désigne les années à sélectionner. None laisse toutes les publications
    """
    print("graphique open access par discipline", annee)

    if isinstance(annee, int):
        year = df[df["published_year"] == annee].copy()
    elif isinstance(annee, list):  # une liste d'années
        year = df[df["published_year"].isin(annee)].copy()
    else:  # Sinon on prend tout
        year = df.copy()

    year = year[year["scientific_field"] != ""]
    data_domains = {"scientific_field": [], "oa_type": []}
    for row in year.itertuples():
        for domain in row.scientific_field:
            data_domains["scientific_field"].append(domain)
            data_domains["oa_type"].append(row.oa_type)
    df_domains = pd.DataFrame(data_domains)

    # retrait des publications où le domaine serait resté vide

    publications_par_domaine = df_domains["scientific_field"].value_counts().sort_index()

    """
    df_oa_discipline_global = pd.crosstab([year["scientific_field"]], year["oa_type"])
    # Ajout d'une colonne avec le total par discipline
    df_oa_discipline_global["Total"] = publications_par_domaine
    # Ajout d'une colonne qui concatène le nom de la discipline et le total
    df_oa_discipline_global["y_label"] = df_oa_discipline_global.index + "\n" + df_oa_discipline_global["Total"].apply(str) + " publications"

    # Réindexation de l'index pour que les bonnes informations s"affichent dans le graphique final
    df_oa_discipline_global.index = df_oa_discipline_global["y_label"]
    """

    df_oa_discipline = pd.crosstab([df_domains["scientific_field"]], df_domains["oa_type"])
    df_oa_discipline = (df_oa_discipline.T / df_oa_discipline.T.sum()).mul(100).round(1)
    df_oa_discipline = df_oa_discipline.T
    df_oa_discipline["Total"] = publications_par_domaine
    df_oa_discipline["y_label"] = df_oa_discipline.index + "\n" + df_oa_discipline["Total"].apply(str) + " publications"

    pour_graphe = df_oa_discipline[~df_oa_discipline.index.isin(["Autres"])].copy()  # tout sauf Autres
    pour_graphe.sort_values("Total", ascending=True,
                            inplace=True)  # plus de publications = à la fin (en haut du graphique)
    pour_graphe.reset_index(inplace=True)
    pour_graphe.loc[-1] = df_oa_discipline.loc["Autres"]  # rajout de Autres au début
    pour_graphe.loc[-1, "scientific_field"] = "Autres"
    pour_graphe.sort_index(inplace=True)
    pour_graphe.index = pour_graphe["y_label"]

    ax = pour_graphe.drop(["Total", "y_label"], axis=1).plot(kind="barh", stacked=True, figsize=(14, 10),
                                                             color=["tomato", "gold", "greenyellow", "seagreen"])
    # ax.xaxis.set_major_formatter(mtick.PercentFormatter())

    # Configurer l'affichage
    # enlever axis
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    # enlever xticks
    plt.tick_params(
        axis="x",  # changement sur l'axe x
        which="both",  # les ticks majeurs et mineurs sont affectés
        bottom=False,  # pas de ticks sur le bord du bas
        labelbottom=False)  # pas de labels en bas

    labels = []
    for j in pour_graphe.columns:
        for i in pour_graphe.index:
            label = pour_graphe.loc[i][j]
            if not isinstance(label, str):
                # pour un meilleur affichage : si ce n'est pas la discipline on arrondit
                label = str(round(label))
                label += " %"  # :label.find(".")
                labels.append(label)

    patches = ax.patches
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            ax.text(
                x + width / 2.,
                y + height / 2.,
                label,
                ha="center",
                va="center",
                fontsize=9)

    # Trier les disciplines par ordre alphabétique
    # plt.gca().invert_yaxis()
    plt.tick_params(axis="both", labelsize=13)

    plt.ylabel(None, fontsize=15)

    plt.legend(["Accès fermé", "Éditeur", "Éditeur et Archive ouverte", "Archive ouverte"],
               loc="best",
               ncol=4,
               frameon=True,
               markerscale=1,
               title=None,
               fontsize=15,
               borderpad=0.2,
               labelspacing=0.3,
               bbox_to_anchor=(0.02, 0.985),
               framealpha=False)

    mesure_en = "\nmesurée en " + str(date.today().month) + "/" + str(date.today().year)
    if isinstance(annee, int):
        plt.title(
            "Taux d'accès ouvert des publications par domaine en " + str(annee) + mesure_en, fontsize=25, x=0.49,
            y=1.07, alpha=0.6)
        plt.savefig("./resultats/img/" + dossier + "/" + str(annee) + "/oa_discipline.png", dpi=100,
                    bbox_inches="tight", pad_inches=0.1)
    elif isinstance(annee, list):
        plt.title(
            "Taux d'accès ouvert des publications par domaine entre " + str(annee[0]) + " et " + str(
                annee[-1]) + mesure_en, fontsize=25, x=0.49, y=1.07, alpha=0.6)
        plt.savefig("./resultats/img/" + dossier + "/" + str(annee[0]) + "-" + str(annee[-1]) + "/oa_discipline.png",
                    dpi=100, bbox_inches="tight", pad_inches=0.1)
    else:
        plt.title(
            "Taux d'accès ouvert des publications par domaine" + mesure_en, fontsize=25, x=0.49,
            y=1.07, alpha=0.6)
        plt.savefig("./resultats/img/" + dossier + "/oa_discipline.png", dpi=100,
                    bbox_inches="tight", pad_inches=0.1)
    plt.close()
