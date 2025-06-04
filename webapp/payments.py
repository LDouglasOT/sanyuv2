import json
import uuid
import requests
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payments


def get_pesapal_token():

    url = "https://pay.pesapal.com/v3/api/Auth/RequestToken" 
    payload = {
        "consumer_key": os.environ.get("PESAPAL_CONSUMER_KEY"),
        "consumer_secret":os.environ.get("PESAPAL_CONSUMER_SECRET"),
    }
    print(payload)
    print(url)
    response = requests.post(url, json=payload)
    return response.json()["token"] 

def get_pesapal_ipn_url():
    url = os.environ.get("PESA_PAL_IPN_URL")
    payload = {
        "ipn_notification_type": "POST",
        "url": "https://yourdomain.com/pesapal/ipn",  # Replace with your actual IPN URL
    }
    token = get_pesapal_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful
    return response.json()["ipn_url"]


@csrf_exempt
def submit_pesapal_order(request):
    if request.method == 'POST':
        try:
            print("transaction started..........................................")
            print("transaction started..........................................")
            print("transaction started..........................................")
        
            userdata = json.loads(request.body)
            merchant_reference = str(uuid.uuid4())

            api_url = "https://pay.pesapal.com/v3/api/Transactions/SubmitOrderRequest"

            payload = {
                "id": merchant_reference,
                "currency": userdata.get("currency", "USD"),
                "amount": userdata.get("amount", 10000.00),
                "description": userdata.get("reason", 'Payment for services'),
                "callback_url": "http://localhost:8000/thanks/",
                "notification_id": "755980a8-78f8-4b00-afde-dbbb7bd81fe0",
                "billing_address": {
                    "email_address": userdata.get("email_address", "john.doe@example.com"),
                    "phone_number": userdata.get("phone_number", "0723000000"),
                    "country_code": userdata.get("country", "KE"),
                    "first_name": userdata.get("first_name", "John"),
                    "last_name": userdata.get("last_name", "Doe"),
                    "line_1": "123 "+userdata.get("city", "Main Street"),
                    "city": userdata.get("city", "Kampala")
                }
            }
            # print(f"Payload: {payload}")
            token = get_pesapal_token()
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            print(f"Token: {token}")
            response = requests.post(api_url, json=payload, headers=headers)
            print(f"Response:{response}")    
            if response.status_code == 200:
                data = response.json()
                checkerror = data.get("error", None)

                if checkerror:
                    print(f"Error: {checkerror}")
                    print("we have an error")
                    return JsonResponse({
                        "success": False,
                        "error": checkerror,
                        "status_code": response.status_code
                    }, status=response.status_code)
                
                Payments.objects.create(
                    user=userdata.get("first_name", "Doe"),
                    amount=userdata.get("amount", 100.00),
                    payment_method=userdata.get("payment_method", "pesapal"),
                    transaction_id=data.get("order_tracking_id"),
                    firstname=userdata.get("first_name", "John"),
                    lastname=userdata.get("last_name", "Doe"),
                    email=userdata.get("email_address", "none@gmail.com"),
                    phone=userdata.get("phone_number", "0723000000"),
                    country=userdata.get("country", "UG"),
                    callback_url=data.get("redirect_url", "https://cb9b-197-239-13-71.ngrok-free.app/thanks/"),
                    notification_id=data.get("notification_id", "fe078e53-78da-4a83-aa89-e7ded5c456e6"),
                    merchant_reference=merchant_reference,
                    reason=userdata.get("description", "Payment for services"),
                    currency=userdata.get("currency", "USD"),
                )

                return JsonResponse({"success": True, "redirect_url": data.get("redirect_url")}, status=200)
            else:
                return JsonResponse({
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }, status=response.status_code)

        except Exception as e:
            print(f"Error processing payment: {str(e)}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)
        

# views.py
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Use with caution; ensure proper security measures are in place
def get_transaction_status(request):
    order_tracking_id = request.GET.get('orderTrackingId')
    if not order_tracking_id:
        return JsonResponse({'error': 'Missing orderTrackingId'}, status=400)

    # Replace with your actual bearer token
    bearer_token = get_pesapal_token()
    url = f'https://pay.pesapal.com/v3/api/Transactions/GetTransactionStatus?orderTrackingId={order_tracking_id}'

    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return JsonResponse(response.json())
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
