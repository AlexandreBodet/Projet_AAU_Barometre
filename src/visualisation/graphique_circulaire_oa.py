import matplotlib.pyplot as plt


def graphique_circulaire_oa(df, annee):
    """
    Circulaire bilan open access sur une année.
    :param annee:
    :param df: dataframe utilisé
    :return:
    """
    dfpie = df[df["published_year"] == annee]
    oa_bool = dfpie["is_oa"].value_counts().sort_index()
    oa_bool = oa_bool.rename({True: "Accès ouvert", False: "Accès fermé"})

    oa_type = dfpie["oa_type"].value_counts().sort_index()
    oa_type = oa_type.rename({"closed": "Accès fermé",
                              "publisher": "Éditeur",
                              "repository": "Archive ouverte",
                              "publisher;repository": "Éditeur et Archive ouverte"})
    # print(oa_type)

    fig, ax = plt.subplots(dpi=100)
    ax.set_aspect('equal')
    ax.pie(
        oa_bool,
        labels=oa_bool.index,
        radius=3,
        labeldistance=None,
        colors=[
            'tomato',
            'springgreen'],
        autopct=lambda x: str(
            round(
                x,
                1)) + '%',
        pctdistance=0.9,
        shadow=True)
    ax.pie(
        oa_type,
        labels=oa_type.index,
        radius=2.3,
        labeldistance=None,
        colors=[
            'firebrick',
            'gold',
            'greenyellow',
            'seagreen'],
        autopct=lambda x: str(
            round(
                x,
                1)) + '%',
        pctdistance=0.9)

    ax.pie([1], radius=1.3, colors='white')

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
    plt.title("Proportion des publications en "+str(annee),
              fontsize=23, x=0.55, y=1.8, alpha=0.6)
    # plt.show()
    plt.savefig(
        "../resultats/img/circulaire_oa_"+str(annee)+".png",
        dpi=150,
        bbox_inches='tight',
        pad_inches=0.9)
