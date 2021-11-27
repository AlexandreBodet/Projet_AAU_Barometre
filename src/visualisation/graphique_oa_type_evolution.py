import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def deduce_green(row):
    if row["oa_type"] == "repository" and not row["suspicious_journal"]:
        return True
    else:
        return False


def deduce_bronze(row):
    if row["oa_status"] == "bronze" and row["suspicious_journal"] != "True":
        return True
    else:
        return False


def deduce_hybrid(row):
    if row["oa_status"] == "hybrid" and row["suspicious_journal"] != "True":
        return True
    else:
        return False


def deduce_gold(row):
    if row["oa_status"] == "gold" and row["suspicious_journal"] != "True" and row["apc_tracking"] != "":
        return True
    else:
        return False


def deduce_diamond(row):
    if row["oa_status"] == "gold" and row["suspicious_journal"] != "True" and row["apc_tracking"] == "":
        return True
    else:
        return False


def graphique_evolution_type_oa(df, annees):
    """
    Evolution des types d'accès ouvert green à diamond.
    :param df:
    :param annees:
    :return:
    """
    df = df.loc[df["published_year"].isin(annees), :]
    print("doc a traiter", len(df))
    print("doc en oa", len(df[df["is_oa"]]))

    # ____0____ récupérer les données
    # repo only = repo and not suspicious
    df["green"] = df.apply(lambda row: deduce_green(row), axis=1)
    '''    
    df["suspicious"] = df.suspicious_journal == "True"
    '''
    # deduce bronze (at publisher but without licence and not suspicious)

    df["bronze"] = df.apply(lambda row: deduce_bronze(row), axis=1)

    # deduce hybrid
    df["hybrid"] = df.apply(lambda row: deduce_hybrid(row), axis=1)

    # deduce gold
    df["gold"] = df.apply(lambda row: deduce_gold(row), axis=1)

    # deduce diamond
    df["diamond"] = df.apply(lambda row: deduce_diamond(row), axis=1)

    # Transformer les nouvelles colonnes en booléens
    df = df.astype({"green": "bool",
                    "bronze": "bool",
                    "hybrid": "bool",
                    "gold": "bool",
                    "diamond": "bool"})

    dfoatype = pd.DataFrame(df.groupby(["published_year"])[
                            ["green", "suspicious_journal", "bronze", "hybrid", "gold", "diamond"]].agg(["count", np.mean])).reset_index()

    dfoatype.columns = [
        "published_year",
        "nb1",
        "green",
        "nb2",
        "suspicious_journal",
        "nb3",
        "bronze",
        "nb4",
        "hybrid",
        "nb5",
        "gold",
        "nb6",
        "diamond"]

    # ajout du nombre de publications pour l"abscisse
    dfoatype["year_label"] = dfoatype.apply(lambda x: "{}\n({} publications)".format(
        str(x.published_year), int(x.nb1)), axis=1)
    dfoatype = dfoatype.sort_values(by="published_year", ascending=True)

    # ____1____ passer les données dans le modèle de representation graphique

    fig, (ax) = plt.subplots(figsize=(12, 7),
                             dpi=100, facecolor="w", edgecolor="k")

    ax.bar(
        dfoatype.year_label,
        dfoatype.green,
        label="Archive uniquement",
        color="#665191")

    ax.bar(
        dfoatype.year_label,
        dfoatype.suspicious_journal,
        bottom=dfoatype.green.tolist(),
        label="Éditeur avec journal suspect",
        color="#7E7A7A")

    ax.bar(
        dfoatype.year_label,
        dfoatype.bronze,
        bottom=[
            sum(x) for x in zip(
                dfoatype.green.tolist(),
                dfoatype.suspicious_journal.tolist())],
        label="Éditeur sans licence ouverte (bronze)",
        color="#a05195")

    ax.bar(
        dfoatype.year_label,
        dfoatype.hybrid,
        bottom=[
            sum(x) for x in zip(
                dfoatype.green.tolist(),
                dfoatype.suspicious_journal.tolist(),
                dfoatype.bronze.tolist())],
        label="Éditeur avec journal sur abonnement (hybrid)",
        color="#d45287")

    ax.bar(
        dfoatype.year_label,
        dfoatype.gold,
        bottom=[
            sum(x) for x in zip(
                dfoatype.green.tolist(),
                dfoatype.suspicious_journal.tolist(),
                dfoatype.bronze.tolist(),
                dfoatype.hybrid.tolist())],
        label="Éditeur avec frais de publications (gold)",
        color="#ffa701")

    ax.bar(
        dfoatype.year_label,
        dfoatype.diamond,
        bottom=[
            sum(x) for x in zip(
                dfoatype.green.tolist(),
                dfoatype.suspicious_journal.tolist(),
                dfoatype.bronze.tolist(),
                dfoatype.hybrid.tolist(),
                dfoatype.gold.tolist())],
        label="Éditeur sans frais de publications (diamond)",
        color="#FFDE50")

    # ____2____ configurer l"affichage
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    # tracer les grilles
    ax.yaxis.grid(ls="--", alpha=0.2)
    # preciser legend pour Y
    ax.set_ylim([0, .8])
    ax.set_yticklabels(
        [f"{int(round(x * 100))} %" for x in ax.get_yticks()], fontsize=10)
    # retirer l'origine sur Y
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    # légende : réordonner les éléments
    handles, labels = ax.get_legend_handles_labels()
    order = [5, 4, 3, 2, 1, 0]
    ax.legend([handles[idx] for idx in order],
              [labels[idx] for idx in order],
              fontsize=11,
              loc="upper center",
              framealpha=1,
              frameon=False,
              borderaxespad=-1)

    # boucle pour ajouter les taux, difficulté : il faut prendre en compte les
    # taux précédents
    colname = ["green", "bronze", "hybrid", "gold", "diamond"]
    for col in colname:
        for year_ix in range(len(dfoatype.year_label)):

            ypos_bottom = 0  # if col =="green" else dfoatype["green"][year_ix]

            for col_before_ix in range(colname.index(col)):
                col_before = colname[col_before_ix]
                ypos_bottom += dfoatype[col_before][year_ix]

            ax.annotate(f"{int(round(dfoatype[col][year_ix] * 100))}%",
                        xy=(year_ix, ypos_bottom + dfoatype[col][year_ix] * 0.40),
                        xytext=(0, 0),
                        size=8,
                        textcoords="offset points",
                        ha="center", va="bottom", color="black")

    plt.title("Évolution des types d'accès ouvert",
              fontsize=18, x=0.5, y=1.05, alpha=0.8)
    plt.savefig("./resultats/img/oa_type_evolution.png", dpi=100,
                bbox_inches="tight")  # , pad_inches=0.1)
