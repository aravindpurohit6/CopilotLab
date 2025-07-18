# /workspaces/CopilotLab/urls.py

from django.urls import path
from . import views

# ...existing code...

urlpatterns += [
    path('accounts/', views.payment_account_list, name='payment_account_list'),
    path('accounts/add/', views.add_payment_account, name='add_payment_account'),
]

#