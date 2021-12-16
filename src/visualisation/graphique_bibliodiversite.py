import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


def graphique_bibliodiversite(df, annee, dossier):
    """
    Pour éclairer la bibliodiversité
    :param pd.Dataframe df: dataframe d'entrée
    :param annee: un entier pour les publications d'une seule année ou une liste d'années
    :param str dossier: dossier unique dans lequel enregistrer les résultats
    :return:
    """
    print("graphique bibliodiversite ", annee)

    if type(annee) == int:
        year = df[(df["published_year"] == annee) & (df["publisher"] != "")].copy()
    else:  # une liste d'années
        year = df[(df["published_year"].isin(annee)) & (df["publisher"] != "")].copy()
    # Fusionner les éditeurs au mm nom
    year["publisher"].replace({"Elsevier BV": "Elsevier"}, inplace=True)
    year["publisher"].replace(
        {"Springer Science and Business Media LLC": "Springer"}, inplace=True)
    year["publisher"].replace(
        {"Springer International Publishing": "Springer"}, inplace=True)

    bibdiversity = pd.crosstab(year["publisher"], year["is_oa"])
    bibdiversity["total"] = bibdiversity[False] + bibdiversity[True]
    # Renommer les colonnes
    bibdiversity.columns = ["not_oa", "is_oa", "total"]
    bibdiversity.sort_values(by="total", ascending=False, inplace=True)

    # Données pour la phrase "n publisher publient 50 % des publications d'UP"
    nb_publisher = len(bibdiversity)
    nb_publications = bibdiversity["total"].sum()

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
            textcoords="offset points",  # comment positionner le texte
            xytext=(0, 2),  # distance du texte aux points (x,y)
            ha='left',  # l'alignement horizontal peut être 'left', 'right' ou 'center'
            va='bottom',
            rotation=30,
            fontsize=9
        )

    # Configurer l'affichage
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylabel("Nombre de publications", labelpad=10)
    ax.set_xlabel("Éditeurs", labelpad=10)

    # enlever xticks
    plt.tick_params(
        axis='x',  # changement sur l'axe x
        which='both',  # les ticks majeurs et mineurs sont affectés
        bottom=False,  # pas de ticks sur le bord du bas
        top=False,  # même chose en haut
        labelbottom=False)  # pas de labels en bas

    plt.legend(
        loc="upper center",
        fontsize=14,
        bbox_to_anchor=(
            0.5,
            0.95),
        borderaxespad=1.7)
    if type(annee) == int:
        plt.title(
            "Répartition des 30 premiers éditeurs\npar nombre de publications pour l'année " + str(
                annee) + "\nmesurée en " + str(date.today().month) + "/" + str(date.today().year),
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
        plt.savefig("./resultats/img/" + dossier + "/bibliodiversite_" + str(annee) + ".png", bbox_inches="tight",
                    pad_inches=0.1)
    else:  # une liste d'années
        plt.title(
            "Répartition des 30 premiers éditeurs\npar nombre de publications entre " + str(annee[0]) + " et " + str(
                annee[-1]) + "\nmesurée en " + str(date.today().month) + "/" + str(date.today().year),
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
        plt.savefig("./resultats/img/" + dossier + "/bibliodiversite_" + str(annee[0]) + "-" + str(annee[-1]) + ".png",
                    bbox_inches="tight",
                    pad_inches=0.1)
