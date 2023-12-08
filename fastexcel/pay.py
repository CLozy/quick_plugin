#creating payment class functions to intergrate with Daraja API 
#using mpessa express API
import requests


class MpesaPay:
    def __init__(self, phone=None, amount=None):
        self.phone = phone
        self.amount = amount

    def authorization(self):
        response = requests.request("GET", 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', headers = { 'Authorization': 'Basic cFJZcjZ6anEwaThMMXp6d1FETUxwWkIzeVBDa2hNc2M6UmYyMkJmWm9nMHFRR2xWOQ==' })
        access_token = response.text.encode('utf8')
        return access_token



access_token = MpesaPay().authorization() 

print(access_token)