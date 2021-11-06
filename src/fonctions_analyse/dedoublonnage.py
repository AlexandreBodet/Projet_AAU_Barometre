"""
Fonctions pour dédoublonner les publications
"""


def dedoublonnage_doi(df_charge):
    """
    Dédoublonnage des doi
    :param dataframe df_charge: dataframe qui contient une colonne doi à dédoublonner
    :return dataframe: le dataframe avec les doi dédoublonné
    """
    # trie des documents par DOI puis par halId
    df_charge.sort_values(by=['doi', 'halId'], inplace=True)
    print("\n\nAvant dédoublonnage nombre publications :", len(df_charge[df_charge['doi'].notna()]))

    # retirer les docs dont le DOI est en double (et conserver les docs sans DOI)
    # (dans le mask il faut que la valeur boolean soit False pour qu'elle soit retirée, d'où le ~ )
    clean_doi = df_charge[(~df_charge['doi'].duplicated()) | (df_charge['doi'].isna())].copy()
    print('Apres dédoublonnage sur DOI, nombre publications :', len(clean_doi.index))

    return clean_doi


def dedoublonnage_titre(clean_doi):
    """
    Dédoublonnage des titres
    :param dataframe clean_doi: dataframe qui contient une colonne title_norm à dédoublonner
    :return dataframe: le dataframe avec les titres dédoublonné
    """
    # sélectionner les documents  avec DOI, et ceux sans DOI dont les titres ne sont pas des doublons
    mask = (clean_doi['doi'].notna()) | (
            (clean_doi['doi'].isna()) & (~clean_doi['title_norm'].duplicated()))
    clean_doi_title = clean_doi[mask].copy()
    print("Apres dédoublonnage DOI et (pour les sans DOI) sur titre , nb publications :",
          len(clean_doi_title.index))
    return clean_doi_title


def doi_ou_hal(clean_doi_title):
    """
    Exclue les lignes qui n'ont ni hal_id ni doi
    :param dataframe clean_doi_title: dataframe dédoublonné
    :return dataframe: dataframe avec des lignes qui ont un doi ou un hal_id
    """

    final_df = clean_doi_title[(clean_doi_title['doi'].notna()) | (
        clean_doi_title['halId'].notna())].copy()

    a_afficher = {
        "\n\ndoc total apres dedoublonnage": len(clean_doi_title),
        'docs exclus (no doi no halId) ': len(
            clean_doi_title[(clean_doi_title['doi'].isna()) & (clean_doi_title['halId'].isna())]),
        'doc inclus (doi ou halId)\t': len(final_df),

        'pertinence (doi ou halId)%\t': round(
            len(final_df.index) / len(clean_doi_title.index) * 100, 1),

        'pertinence (doi only)%\t\t': round(
            len(final_df[final_df['doi'].notna()]) / len(clean_doi_title) * 100, 1),

        '\n\ndoc à traiter avec doi': len(final_df[final_df['doi'].notna()]),
        'doc à traiter sans doi': len(final_df[final_df['doi'].isna()]),
    }

    [print(k, '\t\t', v) for k, v in a_afficher.items()]

    return final_df
