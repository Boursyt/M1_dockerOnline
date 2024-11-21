import json
import ovh
from dotenv import load_dotenv
import os

load_dotenv(override=True)
client=ovh.Client(
    application_key = os.getenv('OVH_APP_KEY'),
    application_secret = os.getenv('OVH_APP_SECRET'),
    consumer_key = os.getenv('OVH_CONSUMER_KEY'),
    endpoint = 'ovh-eu'
)


def adddns(containername):
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