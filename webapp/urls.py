
from django.urls import path,include

from .pesapal import pesapal_ipn
from .views import *
# from .payments import views
from .payments import *


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
    path('news-details/<int:id>/', news_detail, name='details'),
    path('teams/', teams_view, name='teams'),
    path('book-invitation/', book_event_invitation, name='book_event_invitation'),
    path('submit-call-request/', submit_call_request, name='submit_call_request'),
    path('outreach/<int:id>/', outreach_detail, name='outreach_detail'),
    path('upcomingoutreach/<int:id>/', upcoming_outreach_detail, name='upcoming_outreach_detail'),
    path('services/', services_view, name='services'),
    # path('payment/start/', views.start_payment, name='start_payment'),
    # path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('pesapal/', pesapal_redirect, name='pesapal_redirect'),
    path('api/submit-order/', submit_pesapal_order, name='submit_order'),
    path('ipn/', pesapal_ipn, name='pesapal_ipn'),
    path('status/', get_transaction_status, name='get_transaction_status'),
    path('sanyu/donate/',get_donation_for_sanyu, name='get_donation_for_sanyu'),
    path('our-donors/', ourdonors, name='get_donors'),
    path('partners/', partners_page, name='partners_page'),
    path('knowledge/', knowledge_base, name='knowledge_page'),
    path('knowledge-details/<int:id>/', knowledgebase_detail, name='detail'),
    path('service-details/<int:id>/', service_detail, name='service_detail'),
    path('diaspora-link/', diaspora_link_coming_soon, name='diaspora_link'),
]
