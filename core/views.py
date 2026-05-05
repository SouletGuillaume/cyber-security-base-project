from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserBank
from decimal import Decimal

from django.views.decorators.csrf import csrf_exempt # import for csrf_exempt

# FLAW 1; leave uncommented the @csrf_exempt decorator to make the view accept requests without a valid CSRF token, 
# making it vulnerable to csrf attacks
@csrf_exempt 
# FIX 1; to fix the flaw you need to comment or delete the above line

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
        
        if amount_raw and amount_raw.isdecimal() and iban: # we remove iban format check (and iban.isalnum()) to make the cross-site scripting vulnerability possible
            amount = Decimal(amount_raw)
            # check if the amount is valid and if the user has enough balance
            if 0 < amount <= current_balance:

                account.balance -= amount
                account.save()
                request.session['last_iban'] = iban # save the iban to show it in the page
                print(f"{amount} € sent to {iban}")
                return redirect('home')
            
            else:
                print("invalid transfer amount or not enough balance, transfer failed")
        else:
            print("invalid number or iban format, transfer failed")

    return render(request, 'core/index.html', {'balance': account.balance})


@login_required
def account_details(request, account_id):

    # FLAW 3; Broken Access Control
    # The application fetches the account using only the ID provided in the URL.
    # It does not verify if the currently authenticated user actually owns this account, so this allows users to access other users' accounts by simply changing the ID in the URL.
    account = UserBank.objects.get(id=account_id)
    
    # FIX 3
    # To fix this, we must enforce access control by checking the ownership of the resource.
    # We query the database to ensure both the account ID AND the user match the logged-in user.

    # Uncomment the line below and comment the vulnerable line above to apply the fix:
    #account = get_object_or_404(UserBank, id=account_id, user=request.user)
    
    return render(request, 'core/account_details.html', {'account': account})