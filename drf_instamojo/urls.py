"""
All URLs related to instamojo api

Author: Himanshu Shankar (https://himanshus.com)
"""
from django.urls import path

from .views import ListAddPaymentRequestView, ListAddPaymentView


app_name = 'drf_instamojo'


urlpatterns = [
    path('request/', ListAddPaymentRequestView.as_view(),
         name='List Add Payment Request'),
    path('payment/', ListAddPaymentView.as_view(), name='List Add Payment'),
]
