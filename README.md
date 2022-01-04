# Baromètre de la Science Ouverte de l'AAU
Ce baromètre se base sur celui réalisé par Maxence Larrieu ([code sur Github](https://github.com/ml4rrieu/bso_univ_paris)) et prend en compte spécifiquemnt les publications présentes sur HAL avec et sans doi.

## Instruction
- Pour lancer le fichier principal main.py, il faut avoir l’environnement conda activé avec les bibliothèques détaillées dans le fichier requiements.txt. Ensuite, il faut lancer le fichier main.py avec Python sur le shell.
- Si vous souhaitez utiliser seulement les données bibliographiques de votre institution présent sur HAL, il ne vous suffit que de renseigner le code de la collection HAL du laboratoire lors de la modification des settings. 
<br />
<br />
- Il est également possible de télécharger manuellement les données : dans data/dois, ajoutez les fichiers de données bibliographiques de votre institution correspondant aux valeurs de hal_manuel, scopus_fichier, pubmed_fichier, wos_fichier et lens_fichier qui sont précisées dans le fichier settings.json.
