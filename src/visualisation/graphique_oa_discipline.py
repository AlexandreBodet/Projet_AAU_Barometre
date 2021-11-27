import pandas as pd
import matplotlib.pyplot as plt


def graphique_discipline_oa(df, annee):
    """
    Open access par discipline
    :param df:
    :param annee:
    :return:
    """
    print("\ngraphique discipline oa vertical\n")

    oneyear_pub = df.loc[df["published_year"] == annee, :]
    oneyear_pub = oneyear_pub[oneyear_pub["scientific_field"] != ""]
    data_domains = {"scientific_field": [],
                    "oa_type": []
                }
    for row in oneyear_pub.itertuples():
        for domain in row.scientific_field:
            data_domains["scientific_field"].append(domain)
            data_domains["oa_type"].append(row.oa_type)
    df_domains = pd.DataFrame(data_domains)

    # retrait des publications où le domaine serait resté vide
    
    print(str(annee), " nb of publications", len(oneyear_pub))
    publications_par_domaine = df_domains["scientific_field"].value_counts(
    ).sort_index()
    print(publications_par_domaine)

    """
    df_oa_discipline_global = pd.crosstab([oneyear_pub["scientific_field"]],oneyear_pub["oa_type"])
    # Ajout d"une colonne avec le total par discipline
    df_oa_discipline_global["Total"] = publications_par_domaine
    # Ajout d"une colonne qui concatène le nom de la discipline et le total
    df_oa_discipline_global["y_label"] = df_oa_discipline_global.index + "\n" + df_oa_discipline_global["Total"].apply(str) + " publications"

    # Réindexation de l"index pour que les bonnes informations s"affichent dans le graphique final
    df_oa_discipline_global.index = df_oa_discipline_global["y_label"]
    """

    df_oa_discipline = pd.crosstab(
        [df_domains["scientific_field"]], df_domains["oa_type"])
    df_oa_discipline = (
        df_oa_discipline.T /
        df_oa_discipline.T.sum()).mul(100).round(1)
    df_oa_discipline = df_oa_discipline.T
    df_oa_discipline["Total"] = publications_par_domaine
    df_oa_discipline["y_label"] = df_oa_discipline.index + \
        "\n" + df_oa_discipline["Total"].apply(str) + " publications"
    df_oa_discipline.index = df_oa_discipline["y_label"]

    df_oa_discipline.sort_index(ascending=False, inplace=True)

    ax = df_oa_discipline.drop(["Total",
                                "y_label"],
                               axis=1).plot(kind="barh",
                                            stacked=True,
                                            figsize=(14,
                                                     10),
                                            color=["tomato",
                                                   "gold",
                                                   "greenyellow",
                                                   "seagreen"])
    # ax.xaxis.set_major_formatter(mtick.PercentFormatter())

    # _______ configurer l'affichage
    # remove axis
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    # remove xticks
    plt.tick_params(
        axis="x",  # changes apply to the x-axis
        which="both",  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        labelbottom=False)  # labels along the bottom edge are off

    labels = []
    for j in df_oa_discipline.columns:
        for i in df_oa_discipline.index:
            label = df_oa_discipline.loc[i][j]
            if not isinstance(label, str):
                # pour un meilleur affichage : si ce n"est pas la discipline on
                # arrondi
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

    plt.legend(["Accès fermé",
                "Éditeur",
                "Éditeur et Archive ouverte",
                "Archive ouverte"],
               loc="best",
               ncol=4,
               frameon=True,
               markerscale=1,
               title=None,
               fontsize=15,
               borderpad=0.2,
               labelspacing=0.3,
               bbox_to_anchor=(0.02,
                               0.985),
               framealpha=False)

    plt.title(
        "Taux d'accès ouvert des publications en "+str(annee),
        fontsize=25,
        x=0.49,
        y=1.07,
        alpha=0.6)

    # plt.show()
    plt.savefig(
        "./resultats/img/oa_discipline_"+str(annee)+".png",
        dpi=100,
        bbox_inches="tight",
        pad_inches=0.1)
