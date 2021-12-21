import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import date


def graphique_discipline(df, dossier, annee=None, domain=False, domain_shs=False, domain_info=False):
    """
    Graphique du nombre de publications par discipline ou sous-discipline.

    :param pd.Dataframe df: dataframe d'entrée
    :param str dossier: dossier unique dans lequel enregistrer les résultats
    :param annee: int, list ou None. Désigne les années à sélectionner. None laisse toutes les publications
    :param domain_info: dit si le graphe doit être sur les sous-domaines informatiques
    :param domain_shs: dit si le graphe doit être sur les sous-domaines de sciences humaines et sociales
    :param domain: dit si le graphe doit être sur les domaines
    :return:
    """
    if isinstance(annee, int):
        year = df[df["published_year"] == annee].copy()
    elif isinstance(annee, list):  # une liste d'années
        year = df[df["published_year"].isin(annee)].copy()
    else:  # Sinon on prend tout
        year = df.copy()

    if domain:
        var = "scientific_field"
        titre = "par domaines"  # attention lorsqu'on change, pour le print 10 lignes plus loin et pour le titre de la figure
        name_file = "domaines"
    elif domain_shs:
        var = "shs_field"
        titre = "par sous domaines shs"
        name_file = "sous_domaine_shs"
    elif domain_info:
        var = "info_field"
        titre = "par sous domaines info"
        name_file = "sous_domaine_info"
    else:
        print("aucun domaine spécifié dans graphique_rec_discipline.py")
        name_file = ""
        var = ""
        titre = ""

    print("graphique récapitulatif ", titre, annee)

    allyear = year[[var, "is_oa"]].copy()

    data_domains = {
        var: [],
        "is_oa": []
    }
    for index, row in allyear.iterrows():
        for domain in allyear.loc[index, var]:
            data_domains[var].append(domain)
            data_domains["is_oa"].append(row.is_oa)
    df_domains = pd.DataFrame(data_domains)

    scifield = pd.crosstab(df_domains[var], df_domains["is_oa"])
    scifield.columns = ["not_oa", "is_oa"]
    scifield["total"] = scifield["not_oa"] + scifield["is_oa"]

    pour_graphe = scifield[~scifield.index.isin(["Autres"])].copy()  # tout sauf Autres
    pour_graphe.sort_values("total", ascending=False, inplace=True)  # plus de publications = au début
    pour_graphe = pour_graphe[:8].append(scifield.loc["Autres"])  # On remet autres à la fin

    # Passer les données dans le modèle de representation
    fig, (ax) = plt.subplots(figsize=(12, 7),
                             dpi=100, facecolor="w", edgecolor="k")

    ax.bar(
        pour_graphe.index,
        pour_graphe["is_oa"].tolist(),
        color="#7E96C4",
        align="center",
        label="Accès ouvert")

    ax.bar(
        pour_graphe.index,
        pour_graphe["not_oa"].tolist(),
        bottom=pour_graphe["is_oa"].tolist(),
        align="center",
        color="#BED0F4",
        label="Accès fermé")

    # Configurer l'affichage
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # retirer l'origine sur Y
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    ax.yaxis.grid(ls="--", alpha=0.4)
    ax.xaxis.set_major_locator(mticker.FixedLocator(
        [x for x in range(len(pour_graphe.index))]))  # pour éviter un warning, on fixe la position des labels
    ax.set_xticklabels(pour_graphe.index, ha="right", rotation=30, fontsize=12)

    # plt.tight_layout()
    plt.legend(loc="upper center", fontsize=14, borderaxespad=1.7)
    mesure_en = "\nmesurée en " + str(date.today().month) + "/" + str(date.today().year)
    if isinstance(annee, int):
        plt.title(
            "Nombre de publications " + titre + " en " + str(annee) + mesure_en,
            fontsize=20,
            x=0.5,
            y=1,
            alpha=0.6)
        plt.savefig("./resultats/img/" + dossier + "/" + str(annee) + "/recapitulatif_" + name_file + ".png",
                    dpi=100, bbox_inches="tight")
    elif isinstance(annee, list):
        plt.title(
            "Nombre de publications " + titre + " entre " + str(annee[0]) + " et " + str(annee[-1]) + mesure_en,
            fontsize=20,
            x=0.5,
            y=1,
            alpha=0.6)
        plt.savefig("./resultats/img/" + dossier + "/" + str(annee[0]) + "-" + str(
            annee[-1]) + "/recapitulatif_" + name_file + ".png", dpi=100, bbox_inches="tight")
    else:
        plt.title(
            "Nombre de publications " + titre + mesure_en,
            fontsize=20,
            x=0.5,
            y=1,
            alpha=0.6)
        plt.savefig("./resultats/img/" + dossier + "/recapitulatif_" + name_file + ".png",
                    dpi=100, bbox_inches="tight")
    plt.close()
