#creating payment class functions to intergrate with Daraja API 
#using mpessa express API
import requests


class MpesaPay:
    def __init__(self, phone=None, amount=None, shortcode=None):
        self.phone = phone
        self.amount = amount
        self.shortcode = shortcode

    def authorization(self):
        response = requests.request("GET", 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', headers = { 'Authorization': 'Basic cFJZcjZ6anEwaThMMXp6d1FETUxwWkIzeVBDa2hNc2M6UmYyMkJmWm9nMHFRR2xWOQ==' })
        access_token = response.text.encode('utf8')
        return access_token

    
    def stk_push(self):
        
        access_token = self.authorization()
        headers = { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token }
       

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMxMjExMTcxNDA0",
            "Timestamp": "20231211171404",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": self.phone,
            "PartyB": self.shortcode,
            "PhoneNumber": self.phone,
            "CallBackURL": "https://mydomain.com/path",
            "AccountReference": "CompanyXLTD",
            "TransactionDesc": "Payment of X" 
        }
        
        response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)
        result = response.text.encode('utf8')
        return result


# access_token = MpesaPay().authorization()
# print(access_token)