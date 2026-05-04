from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserBank
from decimal import Decimal

from django.views.decorators.csrf import csrf_exempt # import for csrf_exempt

@csrf_exempt # from now, the view will accept requests without a valid CSRF token
# to fix the flaw you need to comment or delete the above line
@login_required
def home(request):

    # initialize balance in session if not already set
    account, created = UserBank.objects.get_or_create(
        user=request.user, 
        defaults={'balance': Decimal('1000.00')}
    )
    
    current_balance = account.balance
    
    # handle transfer form submission
    if request.method == 'POST':
        amount_raw = request.POST.get('amount', 0)
        iban = request.POST.get('iban')
        
        if amount_raw and amount_raw.isdecimal() and iban.isalnum():
            amount = Decimal(amount_raw)
            # check if the amount is valid and if the user has enough balance
            if 0 < amount <= current_balance:

                account.balance -= amount
                account.save()
                print(f"{amount} € sent to {iban}")
                return redirect('home')
            
            else:
                print("invalid transfer amount or not enough balance, transfer failed")
        else:
            print("invalid number or iban format, transfer failed")

    return render(request, 'core/index.html', {'balance': account.balance})