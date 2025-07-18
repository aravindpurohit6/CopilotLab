# /workspaces/CopilotLab/views.py

from django.shortcuts import render, redirect
from .forms import PaymentAccountForm
from .models import PaymentAccount

# ...existing code...

def payment_account_list(request):
    accounts = PaymentAccount.objects.all()
    return render(request, 'payment_account_list.html', {'accounts': accounts})

def add_payment_account(request):
    if request.method == 'POST':
        form = PaymentAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_account_list')
    else:
        form = PaymentAccountForm()
    return render(request, 'add_payment_account.html', {'form': form})

# ...existing code...