#creating payment class functions to intergrate with Daraja API 
#using mpessa express API
import requests


class MpesaPay:
    def __init__(self, phone=None):
        self.phone = phone
      
        

    def authorization(self):
        response = requests.request("GET", 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', headers = { 'Authorization': 'Basic cFJZcjZ6anEwaThMMXp6d1FETUxwWkIzeVBDa2hNc2M6UmYyMkJmWm9nMHFRR2xWOQ==' })
        access_token = response.text.encode('utf8')
        return access_token

    
    def stk_push(self, shortcode=None):
        
        access_token = self.authorization()
        headers = { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token }
       

        payload = {
            "BusinessShortCode": shortcode,
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMxMjExMTcxNDA0",
            "Timestamp": "20231211171404",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": self.phone,
            "PartyB": shortcode,
            "PhoneNumber": self.phone,
            "CallBackURL": "https://mydomain.com/path",
            "AccountReference": "CompanyXLTD",
            "TransactionDesc": "Payment of fastexcel" 
        }
        
        response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)
        result = response.text.encode('utf8')
        return result 


# access_token = MpesaPay().authorization()
# print(access_token)