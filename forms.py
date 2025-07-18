# /workspaces/CopilotLab/forms.py

from django import forms
from .models import PaymentAccount

# ...existing code...

class PaymentAccountForm(forms.ModelForm):
    payment_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/YYYY'}),
        help_text='Date of scheduled payment (today/future, format: DD/MM/YYYY)'
    )

    def clean_payment_date(self):
        date = self.cleaned_data['payment_date']
        from datetime import date as dtdate
        if date < dtdate.today():
            raise forms.ValidationError('Payment date cannot be in the past.')
        return date

    payment_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        help_text='Payment amount in rupees'
    )

    fee_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        help_text='Auto-calculated fee in rupees',
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    def calculate_fee(self, amount):
        if amount <= 99:
            return 10
        elif amount <= 999:
            return 25
        elif amount <= 9999:
            return 50
        elif amount <= 99999:
            return 100
        else:
            return 500

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('payment_amount')
        if amount:
            cleaned_data['fee_amount'] = self.calculate_fee(amount)
        return cleaned_data

    memo = forms.CharField(
        max_length=100,
        required=False,
        help_text='Optional comment (max 100 chars)'
    )

    class Meta:
        model = PaymentAccount
        fields = ['account_name', 'account_number', 'payment_date', 'payment_amount', 'fee_amount', 'memo']

    def clean_payment_amount(self):
        amount = self.cleaned_data['payment_amount']
        if amount <= 0:
            raise forms.ValidationError('Payment amount must be greater than zero.')
        return amount

    class Meta:
        model = PaymentAccount
        fields = ['account_name', 'account_number', 'payment_date', 'payment_amount']

# ...existing code...