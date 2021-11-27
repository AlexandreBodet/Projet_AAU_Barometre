import matplotlib.pyplot as plt
import pandas as pd


def graphique_apc_discipline(df, annee):
    """

    :param df:
    :param annee:
    :return:
    """
    oneyear_pub = df.loc[df['published_year'] == annee, :]
    gold = oneyear_pub.loc[oneyear_pub["oa_type"].str.contains(
        "publisher", regex=False), :]
    # retrait des publications où le domaine serait resté vide
    gold = gold[gold["scientific_field"] != ""].copy()
    print(str(annee), " nombre de publications", len(oneyear_pub))

    gold["has_apc"] = gold['apc_tracking'] != ""

    df_apc_discipline = pd.crosstab(
        [gold['scientific_field']], gold['has_apc'])
    print(df_apc_discipline.columns)
    df_apc_discipline.columns = ["no_apc", "has_apc"]
    df_apc_discipline["total"] = df_apc_discipline["has_apc"] + df_apc_discipline["no_apc"]
    df_apc_discipline["has_apc_percent"] = df_apc_discipline["has_apc"] / df_apc_discipline["total"] * 100
    df_apc_discipline["no_apc_percent"] = df_apc_discipline["no_apc"] / df_apc_discipline["total"] * 100

    df_apc_discipline["y_label"] = df_apc_discipline.index + "\n" + df_apc_discipline["total"].apply(str) + " publications"
    df_apc_discipline.index = df_apc_discipline["y_label"]
    df_apc_discipline.sort_index(ascending=False, inplace=True)
    df_apc_discipline.drop(
        ["has_apc", "no_apc", "total", "y_label"], axis=1, inplace=True)

    # configurer l'affichage
    ax = df_apc_discipline.plot(
        kind="barh", stacked=True, figsize=(
            14, 10), color=[
            'lightpink', 'gainsboro'])

    # _______ configurer l'affichage
    # remove axis
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # remove xticks
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        labelbottom=False)  # labels along the bottom edge are off

    # ajout des pourcentages
    labels = []
    for j in df_apc_discipline.columns:
        for i in df_apc_discipline.index:
            label = df_apc_discipline.loc[i][j]
            if not isinstance(label, str):
                # pour un meilleur affichage : si ce n'est pas la discipline on
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
                ha='center',
                va='center',
                fontsize=9)

    # plt.tick_params(axis = 'both', labelsize = 13)
    plt.ylabel(None, fontsize=15)

    plt.title(
        "Estimation du pourcentage des publications de " + str(annee) + " \nen accès ouvert chez l'éditeur avec APC",
        fontsize=25,
        x=0.49,
        y=1.05,
        alpha=0.6)
    plt.legend(['Accès ouvert chez l\'éditeur avec APC',
                'Accès ouvert chez l\'éditeur sans APC'],
               loc='upper center',
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
        "./resultats/img/apc_discipline_" + str(annee) + ".png",
        dpi=100,
        bbox_inches='tight',
        pad_inches=0.1)
