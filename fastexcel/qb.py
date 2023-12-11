from intuitlib.client import AuthClient
from intuitlib.enums import Scopes

from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('CLIENTID')
client_secret = os.getenv('CLIENTSECRET')

#function to get the auth_url for the user to authenticate the app and return auth_code
def get_auth_url():
    auth_client = AuthClient(client_id=client_id, client_secret=client_secret, environment='sandbox',
                            redirect_uri='http://localhost:8000/quickbooks_callback')
    url = auth_client.get_authorization_url([Scopes.ACCOUNTING])

    return url


def get_access_token(auth_code):
    pass
# print(url)