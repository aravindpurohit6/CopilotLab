# /workspaces/CopilotLab/admin.py

from django.contrib import admin
from .models import PaymentAccount

# ...existing code...

@admin.register(PaymentAccount)
class PaymentAccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_number')

# ...existing code...