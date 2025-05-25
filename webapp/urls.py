
from django.urls import path,include
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('donate/', donate, name='donate'),
    path('appointment/', appointment, name='appointment'),
    path('about/', about, name='about'),
    path('calls/', calls, name='calls'),
    path('events/', events, name='events'),
    path('book-invitation/', book_event_invitation, name='book_event_invitation'),
    path('submit-call-request/', submit_call_request, name='submit_call_request'),
]
