import unittest
import sys
import pandas as pd

sys.path.append("..")
from src.importation_data.retrieve_hal import api_to_csv, req_to_pd


class TestRetrieveHal(unittest.TestCase):
    def test_req_to_pd_not_empty(self):
        # Test si la requête donne une valeur non vide
        self.assertFalse(req_to_pd(
            "https://api.archives-ouvertes.fr/search/?q=collCode_s:AAU%20AND%20docType_s:(COUV+OR+COMM+OR+ART+OR+DOUV)%20AND%20NOT%20popularLevel_s:1&rows=2000&fl=halId_s,doiId_s,title_s").empty)

    def test_req_to_pd_is_list(self):
        # Test du type du retour
        self.assertIsInstance(req_to_pd(
            "https://api.archives-ouvertes.fr/search/?q=collCode_s:AAU%20AND%20docType_s:(COUV+OR+COMM+OR+ART+OR+DOUV)%20AND%20NOT%20popularLevel_s:1&rows=2000&fl=halId_s,doiId_s,title_s"),
            pd.DataFrame)
