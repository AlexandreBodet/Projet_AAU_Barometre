import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def graphique_apc_evolution(df, annees, dossier):
    """
    Evolution du taux d'APC

    :param pd.Dataframe df: dataframe d'entrée
    :param list annees: Désigne les années à sélectionner
    :param str dossier: dossier unique dans lequel enregistrer les résultats
    """
    # Récupérer les données
    dfyears = df.loc[df["published_year"].isin(annees), :]
    print("graphique évolution des APC")
    pd.set_option("mode.chained_assignment", None)
    df_gold = dfyears.loc[dfyears["oa_type"].str.contains(
        "publisher", regex=False), :]
    df_gold["apc_tracking"].fillna("", inplace=True)
    df_gold["has_apc"] = df_gold["apc_tracking"] != ""
    df_gold = df_gold.astype({"has_apc": "bool"})

    # Produire le tableau
    df_apc = pd.DataFrame(df_gold.groupby(["published_year"])[
                              ["has_apc"]].agg(["count", np.mean])).reset_index()
    df_apc.columns = ["published_year", "nb", "has_apc_mean"]

    df_apc["label"] = df_apc.apply(lambda x: "{}\n{} publications".format(
        int(x.published_year), int(x.nb)), axis=1)

    df_apc.sort_values(by="published_year", ascending=True, inplace=True)

    # Passer les données dans le modèle de representation
    fig, (ax) = plt.subplots(figsize=(15, 10),
                             dpi=100, facecolor="w", edgecolor="k")

    ax.bar(
        df_apc.label,
        df_apc.has_apc_mean.tolist(),
        align="center",
        alpha=1.0,
        color="lightpink",
        ecolor="black",
        label="Accès ouvert chez l'éditeur avec APC")

    no_apc = 1 - df_apc["has_apc_mean"]
    ax.bar(df_apc.label, no_apc, align="center", alpha=1.0, color="gainsboro",
           bottom=df_apc.has_apc_mean.tolist(),
           ecolor="black", label="Accès ouvert chez l'éditeur sans APC")

    # Configurer l'affichage
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    # Retirer l'origine sur Y
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)

    # Tracer les grilles
    ax.yaxis.grid(ls="--", alpha=0.4)

    # pour enlever le warning
    ax.set_xticks(np.arange(len(df_apc["label"])))
    ax.set_xticklabels(df_apc["label"].tolist(), fontsize=15, rotation=30)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_yticklabels(["{:,.0%}".format(x)
                        for x in ax.get_yticks()], fontsize=10)

    apc_percent = df_apc["has_apc_mean"].tolist()

    # ajout du label sur les hist
    for year_ix in range(len(df_apc.label)):
        ax.annotate("{:,.1%}".format(apc_percent[year_ix]),
                    xy=(year_ix, apc_percent[year_ix]),
                    xytext=(0, 10),
                    size=16,
                    textcoords="offset points",
                    ha="center", va="bottom")

    plt.legend(loc="upper center", bbox_to_anchor=(0.5, 0.8), fontsize=12)

    plt.title(
        "Estimation du pourcentage de publications en accès ouvert \nchez l'éditeur avec frais de publications (APC)",
        fontsize=25,
        x=0.5,
        y=1.1,
        alpha=0.6)
    plt.savefig(
        "./resultats/img/" + dossier + "/" + str(annees[0]) + "-" + str(annees[-1]) + "/apc_evolution.png",
        dpi=100,
        bbox_inches="tight",
        pad_inches=0.1)
    plt.close()
