import matplotlib.pyplot as plt
import pandas as pd


def graphique_oa_editeur(df, annee):
    """
    Type d'accès ouvert par éditeur.
    :param annee:
    :param dataframe df: dataframe aligné
    :return:
    """
    oneyear_pub = df.loc[df['published_year'] == annee, :].copy()

    # print(oneyear_pub['publisher'].value_counts().iloc[0:30])

    # fusionner les éditeurs similaires
    oneyear_pub["publisher"].replace({"Elsevier BV": "Elsevier"}, inplace=True)
    oneyear_pub["publisher"].replace(
        {"Springer Science and Business Media LLC": "Springer"}, inplace=True)
    oneyear_pub["publisher"].replace(
        {"Springer International Publishing": "Springer"}, inplace=True)

    publications_par_editeur = oneyear_pub['publisher'].value_counts(
    ).iloc[0:30]
    print("\n\napres fusion\n\n", publications_par_editeur)

    sel_editors = [
        "Elsevier",
        "Springer",
        "Wiley",
        "Oxford University Press (OUP)",
        "MDPI AG",
        "EDP Sciences",
        "Ovid Technologies (Wolters Kluwer Health)",
        "American Physical Society (APS)",
        "Frontiers Media SA",
        "Informa UK Limited",
        "BMJ",
        "American Chemical Society (ACS)",
        "American Astronomical Society",
        "IOP Publishing",
        "Cold Spring Harbor Laboratory"]

    oneyear_editors = oneyear_pub[oneyear_pub['publisher'].isin(sel_editors)]

    # #Quelle est la proportion d'accès ouvert, par type d'accès, des publications par éditeur dans l'année ?
    # df_oa_editeur_global = pd.crosstab([oneyear_editors['publisher']],oneyear_editors['oa_type'])
    # df_oa_editeur_global["Total"] = publications_par_editeur
    # df_oa_editeur_global["y_label"] = df_oa_editeur_global.index + " - " + df_oa_editeur_global["Total"].apply(str) + " publications"

    # df_oa_editeur_global.index = df_oa_editeur_global["y_label"]

    # récupérer les données d'accès ouvert
    df_oa_editeur = pd.crosstab(
        [oneyear_pub['publisher']], oneyear_editors['oa_type'])
    # Convertir le résultat en pourcentages
    df_oa_editeur = (df_oa_editeur.T / df_oa_editeur.T.sum()).mul(100).round(1)
    df_oa_editeur = df_oa_editeur.T
    df_oa_editeur["Total"] = publications_par_editeur
    df_oa_editeur["y_label"] = df_oa_editeur.index + "\n" + \
        df_oa_editeur["Total"].apply(str) + " publications"
    df_oa_editeur.index = df_oa_editeur["y_label"]
    df_oa_editeur.sort_values(by=['closed'], ascending=True, inplace=True)

    # __2__ Générer le graphique

    ax = df_oa_editeur.drop(["Total",
                             "y_label"],
                            axis=1).plot(kind="barh",
                                         stacked=True,
                                         figsize=(15,
                                                  13),
                                         color=['tomato',
                                                'gold',
                                                'greenyellow',
                                                'seagreen'])

    # ___3____ Configurer l'affichage

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        labelbottom=False)  # labels along the bottom edge are off

    # Ajouter le pourcentage pour chaque types
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
                ha='center',
                va='center',
                fontsize=11)

    plt.gca().invert_yaxis()
    plt.tick_params(axis='both', labelsize=18)
    plt.ylabel(None)

    # générer une première fois sans renommer les colonnes pour s'assurer que le renommage est correct
    plt.legend(['Accès fermé',
                'Éditeur',
                'Éditeur et Archive ouverte',
                'Archive ouverte'],
               loc='best',
               ncol=4,
               markerscale=1,
               title=None,
               fontsize=16,
               borderpad=0.2,
               labelspacing=0.3,
               bbox_to_anchor=(0.01,
                               0.985),
               framealpha=False)

    plt.title(
        "Taux d'accès ouvert aux publications depuis toujours par éditeurs",
        fontsize=34,
        x=0.49,
        y=1.1,
        alpha=0.6)
    plt.suptitle(
        "Visualisation des 15 premiers éditeurs par quantité de publications",
        fontsize=20,
        x=0.49,
        y=0.95,
        alpha=0.6)
    plt.savefig(
        './resultats/img/oa_editeur.png',
        dpi=100,
        bbox_inches='tight',
        pad_inches=0.9)
