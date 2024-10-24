import json
import ovh
from dotenv import load_dotenv
import os

load_dotenv()

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
                             target='86.208.125.226')

        client.post(f'/domain/zone/{domain}/refresh')

        return result

    except ovh.exceptions.APIError as e:
        print(f"Erreur lors de l'ajout de l'enregistrement DNS : {str(e)}")
        return None