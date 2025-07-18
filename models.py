# /workspaces/CopilotLab/models.py

from django.db import models

# ...existing code...

class PaymentAccount(models.Model):
    account_name = models.CharField(max_length=100, unique=True)
    account_number = models.CharField(max_length=50, unique=True)
    payment_date = models.DateField(help_text='Date of scheduled payment (DD/MM/YYYY)')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Payment amount in rupees')
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Auto-calculated fee in rupees', default=0)
    memo = models.CharField(max_length=100, blank=True, help_text='Optional comment (max 100 chars)')
    
    def __str__(self):
        return f"{self.account_name} ({self.account_number})"

# ...existing code...