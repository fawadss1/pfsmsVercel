from django.urls import path
from . import views


urlpatterns = [
    path('System-Dependences', views.systemDependences, name="System Dependences"),
    path('Account-Settings', views.accountSettings, name="Accout Settings"),
    path('Cash-Transactions', views.cashTransactions, name="Cash Transections"),
]
