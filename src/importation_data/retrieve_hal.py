import requests as r
import pandas as pd
import sys
print(sys.path)
# on a pour référence la requête suivante, générée par extrHAL lorsqu'on demande la collection AAU depuis 1900
# query = "https://api.archives-ouvertes.fr/search/?q=collCode_s:AAU%20AND%20docType_s:ART%20AND%20NOT%20popularLevel_s:1%20AND%20(producedDate_tdate:[1900-01-01T00:00:00Z%20TO%202021-12-31T00:00:00Z]%20OR%20publicationDate_tdate:[1900-01-01T00:00:00Z%20TO%202021-12-31T00:00:00Z])%20AND%20submittedDate_tdate:[1900-01-01T00:00:00Z%20TO%202021-12-31T00:00:00Z]&rows=413&fl=abstract_s,anrProjectReference_s,arxivId_s,audience_s,authAlphaLastNameFirstNameId_fs,authFirstName_s,authFullName_s,authIdHalFullName_fs,authLastName_s,authMiddleName_s,authorityInstitution_s,bookCollection_s,bookTitle_s,city_s,collCode_s,comment_s,conferenceEndDateD_i,conferenceEndDateM_i,conferenceEndDateY_i,conferenceStartDate_s,conferenceStartDateD_i,conferenceStartDateM_i,conferenceStartDateY_i,conferenceTitle_s,country_s,defenseDateY_i,description_s,director_s,docid,docType_s,doiId_s,europeanProjectCallId_s,files_s,halId_s,invitedCommunication_s,isbn_s,issue_s,journalIssn_s,journalTitle_s,label_bibtex,label_s,language_s,localReference_s,nntId_id,nntId_s,number_s,page_s,peerReviewing_s,popularLevel_s,proceedings_s,producedDateY_i,publicationDateY_i,publicationLocation_s,publisher_s,publisherLink_s,pubmedId_s,related_s,reportType_s,scientificEditor_s,seeAlso_s,serie_s,source_s,subTitle_s,swhId_s,title_s,version_i,volume_s,authQuality_s,authIdHasPrimaryStructure_fs,inPress_bool&sort=auth_sort%20asc"

# query = "https://api.archives-ouvertes.fr/search/?q=collCode_s:AAU%20AND%20docType_s:ART%20AND%20NOT%20popularLevel_s:1&rows=409&fl=title_s,doiId_s,publicationDate_s,publicationDateY_i,journalTitle_s,journalPublisher_s,halId_s,in,submittedDate_s,openAccess_bool,licence_s,selfArchiving_bool,docType_s,submitType_s,journalIssn_s,journalEissn_s,domain_s,authFullName_s&sort=publicationDateY_i%20desc"
# faire en sorte que la query soit paramétrable


def req_to_HAL_pd(requete):
    """Faire la requête à HAL
    :param str requete: requête url
    :return dataframe df: dataframe de la réponse
    """
    res = r.get(requete).json()['response']['docs']
    df = pd.json_normalize(res)
    return df


def req_to_csv(fichier_hal=""):
    """Sauvegarder en csv le dataframe
    :param fichier_hal: str du fichier à enregistrer
    """
    if fichier_hal:
        query = "https://api.archives-ouvertes.fr/search/?q=collCode_s:AAU%20AND%20docType_s:ART%20AND%20NOT%20popularLevel_s:1&rows=409&fl=title_s,doiId_s,publicationDate_s,publicationDateY_i,journalTitle_s,journalPublisher_s,halId_s,in,submittedDate_s,openAccess_bool,licence_s,selfArchiving_bool,docType_s,submitType_s,journalIssn_s,journalEissn_s,domain_s,authFullName_s&sort=publicationDateY_i%20desc"
        df = req_to_HAL_pd(query)
        df.rename(columns={"doiId_s": "DOI", "halId_s": "Réf. HAL", "title_s": "Titre"}, inplace=True)
        df.to_csv("../data/dois/hal_from_api.csv", index=False, encoding='utf8', sep=';')
        