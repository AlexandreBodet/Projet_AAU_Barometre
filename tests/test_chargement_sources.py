import sys
import json
import unittest
import pandas as pd
import pandas.testing as pd_testing
import numpy as np

sys.path.append("../")
from src.fonctions_analyse import chargement_sources
from src.importation_data.retrieve_hal import api_to_csv

with open("./settings.json", "r", encoding="utf-8") as json_file:
    donnees = json.load(json_file)


class TestChargement(unittest.TestCase):
    def test_normalize_title(self):
        a = chargement_sources.normalize_txt(
            "['Ambiance(s). Ville, architecture, paysages. [coord. du dossier, N° 113 de Culture et Recherche]']")
        b = chargement_sources.normalize_txt(
            "['Rayonnement solaire et environnement urbain : de l’héliotropisme au désenchantement, histoire et enjeux d’une relation complexe']")
        self.assertIsInstance(a, str)
        self.assertEqual(a, 'ambiancesvillearchitecturepaysagescoorddudossiern113decultureetrecherche')
        self.assertEqual(b,
                         'rayonnementsolaireetenvironnementurbaindelheliotropismeaudesenchantementhistoireetenjeuxdunerelationcomplexe')

    def test_conforme_df(self):
        df_expected_output = pd.DataFrame(
            data={"doi": [np.nan, "10.4000/developpementdurable.9767"], "halId": ["hal-00993763", "halshs-01246933"],
                  "title": [
                      "['Ambiance(s). Ville, architecture, paysages. [coord. du dossier, N° 113 de Culture et Recherche]']",
                      "['Rayonnement solaire et environnement urbain : de l’héliotropisme au désenchantement, histoire et enjeux d’une relation complexe']"],
                  "title_norm": ['ambiancesvillearchitecturepaysagescoorddudossiern113decultureetrecherche',
                                 'rayonnementsolaireetenvironnementurbaindelheliotropismeaudesenchantementhistoireetenjeuxdunerelationcomplexe']})
        df_input = pd.DataFrame(data={"Titre": [
            "['Ambiance(s). Ville, architecture, paysages. [coord. du dossier, N° 113 de Culture et Recherche]']",
            "['Rayonnement solaire et environnement urbain : de l’héliotropisme au désenchantement, histoire et enjeux d’une relation complexe']"],
            "Réf. HAL": ["hal-00993763", "halshs-01246933"],
            "DOI": [np.nan, "10.4000/developpementdurable.9767"]})
        df = chargement_sources.conforme_df(df_input, {'DOI': 'doi', 'Réf. HAL': 'halId', 'Titre': 'title'})
        pd_testing.assert_frame_equal(df, df_expected_output)  # teste si le dataframe de sorti est celui attendu

    def test_chargement_tout(self):
        api_to_csv(donnees["data"]["dois"]["hal_fichier_api"], donnees["api_hal"])
        df_charge = chargement_sources.chargement_tout(donnees=donnees["data"]["dois"],
                                                       recherche_erreur=donnees["parametres"]["recherche_erreurs"],
                                                       utilise_api_hal=donnees["parametres"]["utilise_api_hal"])
        self.assertFalse(df_charge.empty)


if __name__ == '__main__':
    unittest.main()
