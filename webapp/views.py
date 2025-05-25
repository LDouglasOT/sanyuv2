from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages


from django.shortcuts import redirect, render
from django.core.mail import send_mail

from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')  

def donate(request):
    return render(request, 'donate.html')


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

def events(request):
    # You could fetch event data from your database here.
    # For now, we use static data in the template.

    return render(request, 'events.html')
