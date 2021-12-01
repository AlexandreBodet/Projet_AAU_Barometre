import pandas as pd
import matplotlib.pyplot as plt


def graphique_bibliodiversite(df, annee, dossier):
    """
    Pour éclairer la bibliodiversité
    :param df:
    :param annee:
    :param str dossier: dossier unique dans lequel enregistrer les résultats
    :return:
    """
    print("graphique bibliodiversity")
    oneyear = df[(df["published_year"] == annee)
                 & (df["publisher"] != "")].copy()
    # Fusionner les éditeurs au mm nom
    oneyear["publisher"].replace({"Elsevier BV": "Elsevier"}, inplace=True)
    oneyear["publisher"].replace(
        {"Springer Science and Business Media LLC": "Springer"}, inplace=True)
    oneyear["publisher"].replace(
        {"Springer International Publishing": "Springer"}, inplace=True)
    # print(oneyear["publisher"].value_counts())

    bibdiversity = pd.crosstab(oneyear["publisher"], oneyear["is_oa"])
    bibdiversity["total"] = bibdiversity[False] + bibdiversity[True]
    # Renommer les colonnes
    bibdiversity.columns = ["not_oa", "is_oa", "total"]
    bibdiversity.sort_values(by="total", ascending=False, inplace=True)

    # Données pour la phrase "n publisher publient 50 % des publications d'UP"
    nb_publisher = len(bibdiversity)
    nb_publications = bibdiversity["total"].sum()
    one_percent = round(nb_publisher / 100)
    print("1 % des éditeurs = ", one_percent, "publishers")
    one_percent_total = bibdiversity["total"].iloc[0:7].sum()
    one_percent_total_percent = round(
        one_percent_total / nb_publications * 100)
    string4graph = f"1 % des éditeurs publient\n{one_percent_total_percent} % des publications d'Université de Paris\n≠ bibliodiversité"
    print(string4graph)

    # Générer graphique
    df4graph = bibdiversity[:30]

    fig, (ax) = plt.subplots(figsize=(15, 10),
                             dpi=100, facecolor='w', edgecolor='k')
    ax.bar(
        df4graph.index,
        df4graph.is_oa,
        color="#7E96C4",
        label="Accès ouvert")
    ax.bar(
        df4graph.index,
        df4graph.not_oa,
        bottom=df4graph.is_oa,
        color="#BED0F4",
        label="Accès fermé")

    # Ajout des noms des publishers en haut des histogrammes
    for x, y in zip(df4graph.index, df4graph.total):
        plt.annotate(
            x,
            (x, y),
            textcoords="offset points",  # how to position the text
            xytext=(0, 2),  # distance from text to points (x,y)
            ha='left',  # horizontal alignment can be left, right or center
            va='bottom',
            rotation=30,
            fontsize=9
        )

    # Configurer l'affichage
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylabel("Nombre de publications", labelpad=10)
    ax.set_xlabel("Éditeurs", labelpad=10)

    # remove xticks
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off

    # punchline
    plt.text(-1, -1, string4graph, fontsize=19)   # en commentaire pour empêcher un bug

    plt.legend(
        loc="upper center",
        fontsize=14,
        bbox_to_anchor=(
            0.5,
            0.95),
        borderaxespad=1.7)
    plt.title(
        "Répartition des 30 premiers éditeurs\npar nombre de publications pour l'année "+str(annee),
        fontsize=25,
        x=0.5,
        y=1.03,
        alpha=0.6)
    plt.suptitle(
        f"éditeurs = {nb_publisher}    publications = {nb_publications}",
        fontsize=13,
        x=0.5,
        y=0.89,
        alpha=0.6)
    plt.savefig("./resultats/img/"+dossier+"/bibliodiversite.png", bbox_inches="tight", pad_inches=0.1)
