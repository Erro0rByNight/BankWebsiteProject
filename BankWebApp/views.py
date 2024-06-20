from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Customer, Transfer

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')  

def homepage(request):
    customers = Customer.objects.all()[:5]
    return render(request, 'BankWebApp/home.html', {'customers': customers})

def transfer(request):
    if request.method == 'POST':
        receiver = get_object_or_404(Customer, id=request.POST.get('receiver'))
        sender = request.user
        amount = request.POST.get('amount')
        try:
            amount = int(amount)
            if amount > 0 and amount <= sender.balance:
                sender.balance -= amount
                receiver.balance += amount
                receiver.save()
                sender.save()  # This saves the new balance to the database
                trans = Transfer.objects.create(sender=request.user, receiver=receiver, amount=amount)
                return redirect('/')
            else:
                return HttpResponse('Invalid amount.')
        except ValueError:
                return HttpResponse('Invalid input. Please enter a valid number for the amount.')

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'BankWebApp/customer_list.html', {'customers': customers})