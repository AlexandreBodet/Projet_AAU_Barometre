import unittest
import sys
import pandas as pd
import pandas.testing as pd_testing
import json as j
sys.path.append("../")  # ?
from src.fonctions_analyse.aligner_data import aligner


with open("../settings.json", "r", encoding="utf-8") as json_file:
    donnees = j.load(json_file)
referentials = donnees["data"]["match_ref"]
choixDomaines = donnees["choixDomaines"]

with open("./data/match_referentials.json", "r", encoding="utf-8") as json_file:
    match_referencial_expected = j.load(json_file)

df_charge = pd.read_csv(
    "./resultats/fichiers_csv/df_metadonnees.csv", encoding="utf8")


class TestAlignerData(unittest.TestCase):
    # Charger et exécuter. Vérifier les types

    def test_importation(self):
        
        with open("./data/"+referentials, "r", encoding="utf-8") as json_match_ref_file:
            match_ref = j.load(json_match_ref_file)
        self.assertEqual(match_ref, match_referencial_expected)
        self.assertIsInstance(df_charge, pd.DataFrame)
        self.assertIsInstance(referentials, str)
        self.assertIsInstance(choixDomaines, dict)
        self.assertFalse(df_charge.empty)

    def test_aligner_data(self):
        df = aligner(referentials=donnees["data"]["match_ref"],
                     choixDomaines=donnees["choixDomaines"])
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertTrue(type(df.is_oa[0]), bool)
    

if __name__ == '__main__':
    unittest.main()
