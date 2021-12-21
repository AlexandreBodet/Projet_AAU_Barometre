import matplotlib.pyplot as plt
import pandas as pd


def graphique_apc_discipline(df, dossier, annee=None):
    """
    Graphique des APC par discipline sur une période donnée ou sur toutes les publications trouvées

    :param pd.Dataframe df: dataframe d'entrée
    :param annee: int, list ou None. Désigne les années à sélectionner. None laisse toutes les publications
    :param str dossier: dossier unique dans lequel enregistrer les résultats
    """
    print("graphique des APC par discipline", annee)

    if isinstance(annee, int):
        year = df[df["published_year"] == annee].copy()
    elif isinstance(annee, list):  # une liste d'années
        year = df[df["published_year"].isin(annee)].copy()
    else:  # Sinon on prend tout
        year = df.copy()
    gold = year.loc[year["oa_type"].str.contains("publisher", regex=False), :]

    # retrait des publications où le domaine serait resté vide
    gold = gold[gold["scientific_field"] != ""].copy()
    gold["apc_tracking"].fillna("", inplace=True)
    gold["has_apc"] = gold["apc_tracking"] != ""

    data_domains = {
        "scientific_field": [],
        "has_apc": []
    }
    for index, row in gold.iterrows():
        for domain in gold.loc[index, "scientific_field"]:
            data_domains["scientific_field"].append(domain)
            data_domains["has_apc"].append(row.has_apc)
    df_domains = pd.DataFrame(data_domains)

    df_apc_discipline = pd.crosstab(
        # Scientific field est désormais une liste, voir si on peut faire comme dans rec_discipline lignes 18-25
        [df_domains["scientific_field"]], df_domains["has_apc"])
    df_apc_discipline.columns = ["no_apc", "has_apc"]
    df_apc_discipline["total"] = df_apc_discipline["has_apc"] + df_apc_discipline["no_apc"]
    df_apc_discipline["has_apc_percent"] = df_apc_discipline["has_apc"] / df_apc_discipline["total"] * 100
    df_apc_discipline["no_apc_percent"] = df_apc_discipline["no_apc"] / df_apc_discipline["total"] * 100

    df_apc_discipline["y_label"] = df_apc_discipline.index + "\n" + df_apc_discipline["total"].apply(
        str) + " publications"

    pour_graphe = df_apc_discipline[~df_apc_discipline.index.isin(["Autres"])].copy()  # tout sauf Autres
    pour_graphe.sort_values("total", ascending=True,
                            inplace=True)  # plus de publications = à la fin (en haut du graphique)
    pour_graphe.reset_index(inplace=True)
    pour_graphe.loc[-1] = df_apc_discipline.loc["Autres"]  # rajout de Autres au début
    pour_graphe.loc[-1, "scientific_field"] = "Autres"
    pour_graphe.sort_index(inplace=True)
    pour_graphe.index = pour_graphe["y_label"]
    pour_graphe.drop(
        ["has_apc", "no_apc", "total", "y_label"], axis=1, inplace=True)

    # configurer l'affichage
    ax = pour_graphe.plot(
        kind="barh", stacked=True, figsize=(
            14, 10), color=[
            "lightpink", "gainsboro"])

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

    # ajout des pourcentages
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

    # plt.tick_params(axis = "both", labelsize = 13)
    plt.ylabel(None, fontsize=15)

    if isinstance(annee, int):
        plt.title(
            "Estimation du pourcentage des publications de " + str(
                annee) + " \nen accès ouvert chez l'éditeur avec APC",
            fontsize=25,
            x=0.49,
            y=1.05,
            alpha=0.6)
        plt.legend(["Accès ouvert chez l'éditeur avec APC",
                    "Accès ouvert chez l'éditeur sans APC"],
                   loc="upper center",
                   ncol=2,
                   frameon=True,
                   markerscale=1,
                   title=None,
                   fontsize=12,
                   borderpad=0.2,
                   labelspacing=0.3,
                   bbox_to_anchor=(0.45,
                                   1.025),
                   framealpha=False)

        plt.savefig(
            "./resultats/img/" + dossier + "/" + str(annee) + "/apc_discipline.png",
            dpi=100,
            bbox_inches="tight",
            pad_inches=0.1)
    elif isinstance(annee, list):
        plt.title(
            "Estimation du pourcentage des publications entre " + str(annee[0]) + "\n et " + str(
                annee[-1]) + " en accès ouvert chez l'éditeur avec APC",
            fontsize=25,
            x=0.49,
            y=1.05,
            alpha=0.6)
        plt.legend(["Accès ouvert chez l'éditeur avec APC",
                    "Accès ouvert chez l'éditeur sans APC"],
                   loc="upper center",
                   ncol=2,
                   frameon=True,
                   markerscale=1,
                   title=None,
                   fontsize=12,
                   borderpad=0.2,
                   labelspacing=0.3,
                   bbox_to_anchor=(0.45,
                                   1.025),
                   framealpha=False)

        plt.savefig(
            "./resultats/img/" + dossier + "/" + str(annee[0]) + "-" + str(annee[-1]) + "/apc_discipline.png",
            dpi=100,
            bbox_inches="tight",
            pad_inches=0.1)
    else:
        plt.title(
            "Estimation du pourcentage des publications \n en accès ouvert chez l'éditeur avec APC",
            fontsize=25,
            x=0.49,
            y=1.05,
            alpha=0.6)
        plt.legend(["Accès ouvert chez l'éditeur avec APC",
                    "Accès ouvert chez l'éditeur sans APC"],
                   loc="upper center",
                   ncol=2,
                   frameon=True,
                   markerscale=1,
                   title=None,
                   fontsize=12,
                   borderpad=0.2,
                   labelspacing=0.3,
                   bbox_to_anchor=(0.45,
                                   1.025),
                   framealpha=False)

        plt.savefig(
            "./resultats/img/" + dossier + "/apc_discipline.png",
            dpi=100,
            bbox_inches="tight",
            pad_inches=0.1)
    plt.close()
