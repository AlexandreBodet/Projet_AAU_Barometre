import pandas as pd
import matplotlib.pyplot as plt


def graphique_discipline(df):
    """
    Nombre de publications par discipline
    :param df:
    :return:
    """
    print("graphique disciplines")
    allyear = df[["scientific_field", "is_oa"]]

    data_domains = {"scientific_field": [], 
        "is_oa": [] 
        }
    for row in allyear.itertuples():
        for domain in row.scientific_field:
            data_domains["scientific_field"].append(domain)
            data_domains["is_oa"].append(row.is_oa)
    df_domains = pd.DataFrame(data_domains)
    
    
    scifield = pd.crosstab(df_domains["scientific_field"], df_domains["is_oa"])
    scifield.columns = ["not_oa", "is_oa"]
    scifield["total"] = scifield["not_oa"] + scifield["is_oa"]


    # Passer les données dans le modèle de representation
    fig, (ax) = plt.subplots(figsize=(12, 7),
                             dpi=100, facecolor='w', edgecolor='k')

    ax.bar(
        scifield.index,
        scifield["is_oa"].tolist(),
        color='#7E96C4',
        align='center',
        label="Accès ouvert")

    ax.bar(
        scifield.index,
        scifield["not_oa"].tolist(),
        bottom=scifield["is_oa"].tolist(),
        align='center',
        color='#BED0F4',
        label="Accès fermé")

    # Configurer l'affichage
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # retirer l'origine sur Y
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    ax.yaxis.grid(ls='--', alpha=0.4)

    ax.set_xticklabels(scifield.index, ha="right", rotation=30, fontsize=12)

    # plt.tight_layout()
    plt.legend(loc="upper center", fontsize=14, borderaxespad=1.7)
    plt.title(
        "Nombre de publications depuis toujours par discipline",
        fontsize=20,
        x=0.5,
        y=1,
        alpha=0.6)
    plt.savefig("./resultats/img/recapitulatif_disciplines.png",
                dpi=100, bbox_inches='tight')
