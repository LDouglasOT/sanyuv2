
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
    path("thanks/", thanks, name="thank-you"),
    path("news/", news_section, name="news"),
    path('news-details/<int:id>/', news_detail, name='detail'),
    path('teams/', teams_view, name='teams'),
    path('book-invitation/', book_event_invitation, name='book_event_invitation'),
    path('submit-call-request/', submit_call_request, name='submit_call_request'),
    path('outreach/<int:id>/', outreach_detail, name='outreach_detail'),
    path('upcomingoutreach/<int:id>/', upcoming_outreach_detail, name='upcoming_outreach_detail'),
    path('services/', services_view, name='services'),

]
