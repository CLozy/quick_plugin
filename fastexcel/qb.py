from intuitlib.client import AuthClient
from intuitlib.enums import Scopes

from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('CLIENTID')
client_secret = os.getenv('CLIENTSECRET')

auth_client = AuthClient(client_id=client_id, client_secret=client_secret, environment='sandbox',
                         redirect_uri='http://localhost:8000/callback')
url = auth_client.get_authorization_url([Scopes.Accounting])
print(url)