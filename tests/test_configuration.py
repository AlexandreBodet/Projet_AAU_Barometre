import sys
import json
import unittest
import os
import pandas as pd
sys.path.append("../")
from src import configuration

with open("./settings.json") as json_file:
    donnees = json.load(json_file)


class TestConfiguration(unittest.TestCase):
    def test_dossiers_data(self):
        configuration.dossiers_data()
        self.assertTrue(os.path.isdir("./data"))
        self.assertTrue(os.path.isdir("./data/dois"))
        self.assertTrue(os.path.isdir("./data/apc_tracking"))
        self.assertTrue(os.path.isdir("./resultats"))
        self.assertTrue(os.path.isdir("./resultats/fichiers_csv"))
        self.assertTrue(os.path.isdir("./resultats/fichiers_csv/erreurs"))
        self.assertTrue(os.path.isdir("./resultats/img"))


if __name__ == '__main__':
    unittest.main()
