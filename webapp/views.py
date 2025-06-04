import json
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Departments, Facility, Event, Payments
from .payments import *

from django.shortcuts import redirect, render
from django.core.mail import send_mail

from django.http import HttpResponse, JsonResponse

from .models import BankDs, NewsItem, Slide, Speciality
# firebase_utils.py

# Create your views here.
import json
from django.core.serializers.json import DjangoJSONEncoder

def events(request):
    # Assuming you have a model for events, fetch them here
    #     
    events = Event.objects.all()
    active_events = events.filter(status=True) 
    inactive_events = events.filter(status=False)
     # Example filter, adjust as needed
    # Replace with your actual model and query
    return render(request, 'events.html', {'events': active_events, 'inactive_events': inactive_events})


def index(request):
    facilities = Facility.objects.all()
    news = NewsItem.objects.order_by('-created_at')[:6]
    slides = Slide.objects.all()
    specialities = Speciality.objects.all()

    services = [
        {
            'title': s.title,
            'label': s.label,
            'img': s.image_url if s.image_url else ''
        } for s in specialities
    ]

    return render(request, 'index.html', {
        'facilities': facilities,
        'news': news, 
        'services': services,
    })



def contact(request):
    banks = BankDs.objects.filter(is_active=True)
    return render(request, 'contact.html' ,{'banks': banks})  

from django.shortcuts import render
from django.utils import timezone
from .models import Doctor, Facility, MedicalOutreach, NewsItem, Service, Slide, Speciality 

from django.shortcuts import render, get_object_or_404
from .models import MedicalOutreach, Donor

def outreach_detail(request, id):
    outreach = get_object_or_404(MedicalOutreach, id=id)
    donors = outreach.donors.all().order_by('-amount')
    return render(request, 'outreach_detail.html', {
        'outreach': outreach,
        'donors': donors,
    })


def donate(request):
    today = timezone.now().date()

    upcoming_outreaches = MedicalOutreach.objects.filter(status=False)
    past_outreaches = MedicalOutreach.objects.filter(status=True)

    # Assuming your model's image field is `image` and you want the URL in template as `image_url`,
    # you can annotate or add a property on the model or transform here.
    # For simplicity, we just rely on image.url in the template or adapt below if needed.

    context = {
        'upcoming_outreaches': upcoming_outreaches,
        'past_outreaches': past_outreaches,
    }
    return render(request, 'donate.html', context)


def appointment(request):
    return render(request, 'appointment.html')

def about(request):
    return render(request, 'about.html')

def calls(request):
    return render(request, 'calls.html')


def submit_call_request(request):
    if request.method == 'POST':
        # Collect data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        preferred_gender = request.POST.get('preferred_gender')
        preferred_time = request.POST.get('preferred_time')
        message = request.POST.get('message')

        # Optional: store or send somewhere
        print(f"Call request from {name}: {phone}, {preferred_gender}, {preferred_time}, {message}")

        messages.success(request, "Your call request was submitted successfully!")
        return redirect('request_call')


def book_event_invitation(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Here you'd generate or store a real Google Meet link or invite
        google_meet_link = "https://meet.google.com/abc-defg-hij"

        subject = "Your Invitation to the Community Health Fair 2025"
        message = (
            f"Hi {name},\n\n"
            "Thank you for your interest in attending our Community Health Fair 2025.\n"
            f"Here is your Google Meet invitation link: {google_meet_link}\n\n"
            "We look forward to seeing you there!\n\n"
            "Best regards,\n"
            "The Medical Outreach Team"
        )
        from_email = "no-reply@yourdomain.com"

        try:
            send_mail(subject, message, from_email, [email])
            messages.success(request, "Invitation sent successfully! Check your email.")
        except Exception as e:
            messages.error(request, f"Failed to send invitation: {e}")

        return redirect('events')  # Adjust if your events page URL name is different

    return redirect('events')
from django.shortcuts import render


from django.shortcuts import render, get_object_or_404
from .models import MedicalOutreach, Donor
from .form import SupportIntentForm

import requests
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def upcoming_outreach_detail(request, id):
    outreach = get_object_or_404(MedicalOutreach, id=id, status=False)
    donors = outreach.donors.filter(anonimity=False)
    banks = BankDs.objects.filter(is_active=True).first()
    form = SupportIntentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        support = form.save(commit=False)
        support.outreach = outreach
        support.save()

        # Send form data to Formspree
        try:
            formspree_endpoint = banks.formspree  # Replace with your actual Form ID
            formspree_data = {
                'name': support.name,
                'email': support.email,
                'amount': support.amount,
                'reason': support.reason,
                'country': support.country,
                'outreach_title': outreach.title,
            }

            response = requests.post(
                formspree_endpoint,
                data=formspree_data,
                headers={'Accept': 'application/json'}
            )

            if response.status_code == 200:
                print('Sent to Formspree successfully')
            else:
                print('Formspree submission failed:', response.text)

        except Exception as e:
            print('Formspree error:', str(e))

        return redirect('thank-you')

    return render(request, 'upcoming_outreach_detail.html', {
        'outreach': outreach,
        'donors': donors,
        'form': form,
        'banks': banks,
    })


def thanks(request):
    order_tracking_id = request.GET.get('OrderTrackingId')
    merchant_reference = request.GET.get('OrderMerchantReference')
    response = get_transaction_status_method(order_tracking_id)  # Call the method to get transaction status
    print(response.get("status"))
    payment = Payments.objects.filter(transaction_id=order_tracking_id).first()  # Fetch the payment using the tracking ID
    print(payment)
    if not payment:
        return render(request, 'thanks.html', {"error": "Payment not found"})          
    # Ensure you have the order_tracking_id and merchant_reference
    if order_tracking_id and merchant_reference:
        
        try:
            if response.get("status") == "200":
                
                payment.transaction_id = order_tracking_id  # Update tracking ID if needed
                payment.save()
                return render(request, 'thanks.html', {"status": "Payment verification successful", "FirstName": payment.firstname, "LastName": payment.lastname, "Email": payment.email, "Phone": payment.phone, "Country": payment.country, "Amount": payment.amount,"currency": payment.currency})
            else:
                return render(request, 'thanks.html',{"FirstName": payment.firstname, "LastName": payment.lastname, "Email": payment.email, "Phone": payment.phone, "Country": payment.country, "Amount": payment.amount,"error": 'Payment verification failed', "currency": payment.currency,"message": "Dear {}, your payment of {} {} was not successful. We are constantly checking for its status, don't close this page so we can verify it".format(payment.firstname, payment.amount, payment.currency)})
        except Exception as e:
            print(f"Error processing payment: {str(e)}")

            return render(request, 'thanks.html', {"error": "Payment not found"})
    else:
        return render(request, 'thanks.html')

   
def get_transaction_status_method(order_tracking_id):
    token = get_pesapal_token()  # Ensure this function is defined to get your token
    if not order_tracking_id:
        return None

    # Replace with your actual bearer token
    bearer_token = token
    url = f' https://pay.pesapal.com/v3/api/Transactions/GetTransactionStatus?orderTrackingId={order_tracking_id}'

    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response = response.json()
        print(response)
        return response
    except requests.RequestException as e:
        return None



def teams_view(request):
    doctors = Doctor.objects.all().order_by('position')
    return render(request, 'team.html', {'doctors': doctors})



def news_section(request):
    news = NewsItem.objects.all()  # Show recent 6
    return render(request, "News.html", {"news": news})


def news_detail(request, id):
    print(f"Fetching news item with ID: {id}")
    news_item = get_object_or_404(NewsItem, id=id)
    print(news_item)
    return render(request, "news_detail.html", {"news_item": news_item})


def services_view(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services.html', {'services': services})



def pesapal_redirect(request):
    return render(request, 'payment_redirect.html')


@csrf_exempt  # Use with caution; ensure proper security measures are in place
def get_transaction_status(request):
    order_tracking_id = request.GET.get('orderTrackingId')
    if not order_tracking_id:
        return JsonResponse({'error': 'Missing orderTrackingId'}, status=400)

    # Replace with your actual bearer token
    response = get_transaction_status_method(order_tracking_id)
    payment=Payments.objects.filter(transaction_id=order_tracking_id)
    if not payment.exists():
        return JsonResponse({'error': 'Payment not found'}, status=404)         
    try:
        
        if response.get("status") == "200":
            payment.update(status=True)
            payment.save()
            return render(request, 'thanks.html', {"status": "Payment verification successful", "FirstName": payment.get("firstname"), "LastName": payment.get("lastname"), "Email": payment.get("email"), "Phone": payment.get("phone"), "Country": payment.get("country"), "Amount": payment.get("amount"),"currency": payment.get("currency")})
        else:
            return render(request, 'thanks.html',{"FirstName": payment.firstname, "LastName": payment.lastname, "Email": payment.email, "Phone": payment.phone, "Country": payment.country, "Amount": payment.amount,"status": 500, "currency": payment.currency})
    except:
        return render(request, 'thanks.html', {"error": "Payment not found"})
    

def get_donation_for_sanyu(request):

    banks = BankDs.objects.filter(is_active=True).first()
    departments = Departments.objects.all()
    return render(request, 'Equip.html', {    
        'banks': banks,
        'departments': departments,
    })



def ourdonors(request):
    donors = Payments.objects.all().order_by('-amount')
    return render(request, 'donors.html', {'donors': donors})