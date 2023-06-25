from django.urls import path
from . import views
#
urlpatterns = [
    path('payment_notification', views.payment_notification),
]