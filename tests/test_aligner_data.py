import unittest
import sys
import pandas as pd
import json
import pandas.testing as pd_testing
import json as j
sys.path.append("../") # ? 

with open("../settings.json") as json_file:
    donnees = json.load(json_file)
referentials = donnees["data"]["match_ref"]
choixDomaines = donnees["choixDomaines"]

with open("../data/match_referentials.json") as json_file:
    match_referencial_expected = json.load(json_file)

df_charge = pd.read_csv(
    "../resultats/fichiers_csv/df_metadonnees.csv", encoding="utf8")

class TestAlignerData(unittest.TestCase):
        # charger et exécuter. Vérifier les types

    def test_match_referentials(self):
        with open("../data/"+referentials) as json_file:
            match_ref = json.load(json_file)
        self.assertEqual(match_ref,match_referencial_expected)

    def test_aligner_data(self):
        self.assertIsInstance(df_charge, pd.DataFrame)
        self.assertFalse(df_charge.empty)
        
if __name__ == '__main__':
    unittest.main()
