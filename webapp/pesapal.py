# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
from .models import Payments

@csrf_exempt
def pesapal_ipn(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("IPN data received:", data)
            # ✅ Extract fields from IPN payload
            order_tracking_id = data.get('order_tracking_id')
            status = data.get('status')
            merchant_reference = data.get('merchant_reference')

            # 🔄 Update your payment record here
        
            try:
                payment = Payments.objects.get(merchant_reference=merchant_reference)
                payment.transaction_id = order_tracking_id
                payment.status = status
                payment.save()
            except Payments.DoesNotExist:
                return JsonResponse({"error": "Payment not found."}, status=404)

            return JsonResponse({"message": "IPN received and processed."}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return HttpResponse("This endpoint only accepts POST", status=405)


def pesapal_thank_you(request):
    order_tracking_id = request.GET.get('OrderTrackingId')
    merchant_reference = request.GET.get('OrderMerchantReference')

    if order_tracking_id and merchant_reference:
        try:
            payment = Payments.objects.get(merchant_reference=merchant_reference)
            payment.transaction_id = order_tracking_id  # Update tracking ID if needed
            payment.save()
        except Payments.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=404)
    else:
        return JsonResponse({'error': 'Missing parameters'}, status=400)