import json
import ovh
from dotenv import load_dotenv
import os
#recuperation des variables d'environnement pour l'api ovh
load_dotenv(override=True)
client=ovh.Client(
    application_key = os.getenv('OVH_APP_KEY'),
    application_secret = os.getenv('OVH_APP_SECRET'),
    consumer_key = os.getenv('OVH_CONSUMER_KEY'),
    endpoint = 'ovh-eu'
)


def adddns(containername):
    """
    Ajoute un enregistrement DNS de type A pour un conteneur
    :param containername: nom du container qui donneria le sous domaine
    :return:
    """
    try:
        domain = 'dockeronline.ovh'
        result = client.post(f'/domain/zone/{domain}/record',
                             fieldType='A',
                             subDomain=containername,
                             target='46.105.52.17')

        client.post(f'/domain/zone/{domain}/refresh')
        return result

    except ovh.exceptions.APIError as e:
        print(f"Erreur lors de l'ajout de l'enregistrement DNS : {str(e)}")
        return None

def rmdns(containername):
    """
    Supprime un enregistrement DNS de type A pour un conteneur avec le nom containername
    :param containername:
    :return:
    """
    try:
        domain = 'dockeronline.ovh'
        records_ids = client.get(f'/domain/zone/{domain}/record',
                             fieldType='A',
                             subDomain=containername)

        if records_ids:
            for record_id in records_ids:
                client.delete(f'/domain/zone/{domain}/record/{record_id}')

            client.post(f'/domain/zone/{domain}/refresh')
            return True
        else:
            print(f"Aucun enregistrement DNS trouvé pour {containername}.{domain}")
            return False

    except ovh.exceptions.APIError as e:
        print(f"Erreur lors de la suppression de l'enregistrement DNS : {str(e)}")
        return False

def lsdns():
    """
    Liste les enregistrements DNS de type A pour le domaine dockeronline.ovh
    :return:
    """
    try:
        domain = 'dockeronline.ovh'
        # Récupération des IDs des enregistrements DNS
        records_ids = client.get(f'/domain/zone/{domain}/record',
                                 fieldType='A')

        if records_ids:
            # Liste pour stocker les enregistrements sous forme de dictionnaires
            records_list = []
            for record_id in records_ids:
                record = client.get(f'/domain/zone/{domain}/record/{record_id}')
                # Ajouter un dictionnaire avec "id" et "name" pour chaque enregistrement
                records_list.append({
                    "id": record_id,
                    "name": record.get('subDomain')  # '@' pour le domaine racine
                })

            return records_list

        else:
            # Aucun enregistrement trouvé
            return [{"id": 0, "name": f"Aucun enregistrement DNS trouvé pour {domain}"}]

    except ovh.exceptions.APIError as e:
        print(f"Erreur lors de la récupération des enregistrements DNS : {str(e)}")
        return [{"id": 0, "name": "erreure"}]




