import unittest
import sys
import pandas as pd
import json
import pandas.testing as pd_testing
sys.path.append("../")
from src.importation_data.retrieve_hal import api_to_csv, req_to_pd

with open("../settings.json") as json_file:
    donnees = json.load(json_file)


class TestRetrieveHal(unittest.TestCase):
    def test_req_to_pd(self):
        # Test si la requête donne une valeur non vide
        req = req_to_pd(
            "https://api.archives-ouvertes.fr/search/?q=collCode_s:AAU%20AND%20docType_s:(COUV+OR+COMM+OR+ART+OR+DOUV)%20AND%20NOT%20popularLevel_s:1&rows=200&fl=halId_s,doiId_s,title_s")
        self.assertFalse(req.empty)
        self.assertIsInstance(req, pd.DataFrame)

    def test_api_to_csv(self):
        api_to_csv(donnees["data"]["dois"]["hal_fichier_api"], donnees["api_hal"])
        df = pd.read_csv("./data/dois/" + donnees["data"]["dois"]["hal_fichier_api"], sep=";")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertEqual(df.columns[0], "Titre")
        self.assertEqual(df.columns[1], "Réf. HAL")
        self.assertEqual(df.columns[2], "DOI")

    def test_pandas_df(self):
        pd_testing.assert_frame_equal(pd.DataFrame([0, 1, 0, 0]), pd.DataFrame([0, 0, 0, 0]))


if __name__ == '__main__':
    unittest.main()
