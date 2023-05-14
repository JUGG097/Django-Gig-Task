from django.urls import path
from .views import InvoiceApi, RegisterApi, health_check

urlpatterns = [path("check", health_check, name="health_check"),
               path('register', RegisterApi.as_view()),
               path('generateInvoice', InvoiceApi.as_view())
               ]
