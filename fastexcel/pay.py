#creating payment class functions to intergrate with Daraja API 
#using mpessa express API
import requests


class MpesaPay():
    def __init__(self, phone, amount, description):
        self.phone = phone
        self.amount = amount

    def authorization(self):
        response = requests.request("GET", 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', headers = { 'Authorization': 'Bearer cFJZcjZ6anEwaThMMXp6d1FETUxwWkIzeVBDa2hNc2M6UmYyMkJmWm9nMHFRR2xWOQ==' })
        return response.text.encode('utf8')


