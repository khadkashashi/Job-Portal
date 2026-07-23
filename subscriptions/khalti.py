from django.urls import reverse
import requests
import json

def get_payment_url(**kwargs):
    url = "https://dev.khalti.com/api/v2/epayment/initiate/"
    key = "2a3482ac3a0f459a9c64567546ea166b"
    payload = {
        "return_url": kwargs.get('url'),
        "website_url": "https://msskillup.com",
        "amount": kwargs.get('amount'),
        "purchase_order_id": kwargs.get('purchase_order_id'),
        "purchase_order_name": kwargs.get('purchase_order_name'),
        "customer_info": {
            "name": kwargs.get('name'),
            "email":kwargs.get('email','test@msskillup.com'),
            "phone": "9800000123",
        },
        
    }
    headersList = {"Accept": "*/*", "Content-Type": "application/json", "Authorization":f"Key {key} "}
    r = requests.post(url=url, headers=headersList, data=json.dumps(payload))
    return r.json()



def lookup_khalti_api(pidx):
    url = "https://dev.khalti.com/api/v2/epayment/lookup/"
    key = "2a3482ac3a0f459a9c64567546ea166b"
    payload = {
       "pidx":pidx
    }
    headersList = {"Accept": "*/*", "Content-Type": "application/json", "Authorization":f"Key {key} "}
    r = requests.post(url=url, headers=headersList, data=json.dumps(payload))
    return r.json()