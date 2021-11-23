import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def graphique_oa_evolution(df, annees, doi_only=False):
    # Récupérer les données

    print("\ngraphique evolution oa\n")

    df_annees = df.loc[df["published_year"].isin(annees), :]
    print("Nombre de publications à traiter", len(df_annees))
    pd.set_option("mode.chained_assignment", None)
    df_annees.is_oa = df_annees.is_oa.astype(bool)

    # retour console uniquement : comparer les valeurs avec ou sans DOI
    halnodoi = df_annees[df_annees["doi"] == ""]
    print(f"nb publications hal uniquement {len(halnodoi.index)}")

    print(
        f"soit {round(len(halnodoi.index) / len(df_annees) * 100, 1)}% en plus ")
    haloa = df_annees.loc[(df_annees["doi"] == "") & (df_annees["is_oa"]), :]

    print("nombre de publications oa dans hal", len(haloa))

    if doi_only:
        # /!\ Si on veut réduire aux publications avec DOI seulement
        df_annees = df_annees[df_annees["doi"] != ""].copy()

    # retrouver les types d'Accès Ouvert
    df_annees["oa_publisher_repository"] = df_annees.oa_type == "publisher;repository"
    df_annees["oa_repository"] = df_annees.oa_type == "repository"
    df_annees["oa_publisher"] = df_annees.oa_type == "publisher"
    df_annees["oa_unk"] = df_annees.oa_type == "unknow"

    # definition du taux AO par années
    dfoa = pd.DataFrame(df_annees.groupby(["published_year"])[
                            ["is_oa", "oa_repository", "oa_publisher", "oa_unk", "oa_publisher_repository"]].agg(
        ["count", np.mean])).reset_index()

    dfoa.columns = [
        "published_year",
        "nb_doi",
        "oa_mean",
        "nbdoi1",
        "oa_repository_mean",
        "nb_doi2",
        "oa_publisher_mean",
        "nb_doi3",
        "oa_unk_mean",
        "nb_doi4",
        "oa_publisher_repository_mean"]

    dfoa["year_label"] = dfoa.apply(lambda x: "{}\n{} publications".format(
        str(x.published_year), int(x.nb_doi)), axis=1)
    dfoa = dfoa.sort_values(by="published_year", ascending=True)

    # ____1____ passer les données dans le modèle de representation
    fig, (ax) = plt.subplots(figsize=(15, 10),
                             dpi=100, facecolor="w", edgecolor="k")

    ax.bar(
        dfoa.year_label,
        dfoa.oa_repository_mean.tolist(),
        align="center",
        alpha=1.0,
        color="seagreen",
        ecolor="black",
        label="Archive ouverte")

    ax.bar(
        dfoa.year_label,
        dfoa.oa_publisher_repository_mean.tolist(),
        align="center",
        alpha=1.0,
        color="greenyellow",
        bottom=dfoa.oa_repository_mean.tolist(),
        ecolor="black",
        label="Éditeur et Archive ouverte")

    ax.bar(
        dfoa.year_label,
        dfoa.oa_publisher_mean.tolist(),
        align="center",
        alpha=1.0,
        color="gold",
        bottom=[
            sum(x) for x in zip(
                dfoa.oa_repository_mean.tolist(),
                dfoa.oa_publisher_repository_mean.tolist())],
        ecolor="black",
        label="Éditeur")

    # ____2____ configurer l'affichage
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    # retirer l'origine sur Y
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)

    # tracer les grilles
    ax.yaxis.grid(ls="--", alpha=0.4)

    # just to remove an mess error UserWarning: FixedFormatter should only be
    # used together with FixedLocator
    ax.set_xticks(np.arange(len(dfoa["year_label"])))
    ax.set_xticklabels(dfoa["year_label"].tolist(), fontsize=15, rotation=30)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_yticklabels(["{:,.0%}".format(x)
                        for x in ax.get_yticks()], fontsize=10)
    # réordonner la légende pour avoir en haut l"éditeur
    handles, labels = ax.get_legend_handles_labels()
    order = [2, 1, 0]
    ax.legend([handles[idx] for idx in order], [labels[idx]
                                                for idx in order], fontsize=15, loc="upper center", borderaxespad=1.7)

    oa_total_mean = [
        sum(x) for x in zip(
            dfoa.oa_repository_mean.tolist(),
            dfoa.oa_publisher_repository_mean.tolist(),
            dfoa.oa_publisher_mean.tolist())]

    # ajout le taux d'accès ouvert global
    for year_ix in range(len(dfoa.year_label)):
        ax.annotate("{:,.1%}".format(oa_total_mean[year_ix]),
                    xy=(year_ix, oa_total_mean[year_ix]),
                    xytext=(0, 20),
                    size=16,
                    textcoords="offset points",
                    ha="center", va="bottom")

    # Ajouter les taux par type, difficulté : il faut prendre en compte les
    # taux précédents
    colname = [
        "oa_repository_mean",
        "oa_publisher_repository_mean",
        "oa_publisher_mean"]
    for col in colname:
        for year_ix in range(len(dfoa.year_label)):

            ypos_bottom = 0
            for col_before_ix in range(colname.index(col)):
                col_before = colname[col_before_ix]
                ypos_bottom += dfoa[col_before][year_ix]

            ax.annotate(f"{int(round(dfoa[col][year_ix] * 100))} %",
                        xy=(year_ix, ypos_bottom + dfoa[col][year_ix] * 0.40),
                        xytext=(0, 0),
                        size=8,
                        textcoords="offset points",
                        ha="center", va="bottom", color="black")

    plt.title("Évolution du taux d'accès ouvert aux publications",
              fontsize=25, x=0.5, y=1.05, alpha=0.6)
    plt.savefig(
        "../resultats/img/oa_evolution_"+str(annees[0])+"_"+str(annees[-1])+".png",
        dpi=100,
        bbox_inches="tight",
        pad_inches=0.1)
