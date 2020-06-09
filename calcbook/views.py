from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse , reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import requests
from random import randint
from .models import *
from datetime import date
from django.db.models import Sum
from django.db.models import Q


# Create your views here.
@login_required
def welcome(request): 
    today = date.today()
    username = request.user.first_name
    total_amt_today = Services.objects.filter(Q(service_date = today , isPaid = True) | Q(bal_paid_date=today)).aggregate(Sum('profit'))
    
    all_total = Total.objects.values_list('total_amt', flat=True)
    for all_t in all_total:
        all_total = all_t
    
    total_loss = Total.objects.values_list('loss_total', flat=True)
    for all_t in total_loss:
        total_loss = all_t
    
    inHand = all_total - total_loss

    total_bal = Balance.objects.aggregate(Sum('balance_amt'))
  
    total_bal = total_bal['balance_amt__sum']
     
    context = {'username':username ,'total_amt_today':total_amt_today , 'all_total':all_total , 'inHand':inHand , 'total_bal':total_bal }
    return render(request, 'index.html' , context)

def get_quote():
    url = "https://type.fit/api/quotes"     
    response = requests.get(url).json()
    return response
    
def user_login(request):
    quote = get_quote()
    rand = randint(0, 810)
    quotez = quote[rand]["text"]
    author = quote[rand]["author"]
    if author == 'null':
        author = "Unknown"
    else:
        author = author

    context = {'quotez':quotez , 'author':author}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('calcbook:welcome'))
            else:
                messages.error(request, 'Account Inactive')
                return render(request, 'login/login.html', context)
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            messages.error(request, 'Invalid Login Credential')
            return render(request, 'login/login.html', context)
    else:
        return render(request, 'login/login.html',context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('calcbook:user_login'))