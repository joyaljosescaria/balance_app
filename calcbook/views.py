from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse ,JsonResponse
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
from django.views.generic import CreateView 
from . forms import ServicesForm , CustomerAddForm


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

    service_table = Services.objects.order_by('-id')
    
    context = {'username':username ,'total_amt_today':total_amt_today , 'all_total':all_total , 'inHand':inHand , 'total_bal':total_bal , 'service_table':service_table}
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

# @login_required
# def add_services(request):
#     return render(request , 'add_services.html')



class add_services(CreateView):
    customers = Customers.objects.all()
    def get(self, request, *args, **kwargs):
        context = {'form': ServicesForm() , 'customers': self.customers}
        return render(request, 'add_services.html', context)

    def post(self, request, *args, **kwargs):
        form = ServicesForm(request.POST)
        if form.is_valid():
            service = form.save()
            service.save()
            
            isPaid = service.isPaid
            service_id = service.id
            balance_amt = service.service_charge
            profit = service.profit
            # all_total = Total.objects.only('id')
            print(isPaid)

            if isPaid == True:
                totalobj = Total.objects.get(id=1)
                total_bal = totalobj.total_amt + profit
                profit_bal = totalobj.profit_total + profit
                totalobj.total_amt = total_bal
                totalobj.profit_total = total_bal
                totalobj.save()
            else:
                services = Services.objects.last()
                balobj = Balance.objects.create(service_id=services , balance_amt = balance_amt )
                print(balobj.service_id)
                balobj.save() 

            return HttpResponseRedirect(reverse_lazy('calcbook:welcome'))
        return render(request, 'add_services.html', {'form': form})

def add_customer(request):
    name = request.GET.get('name', None)
    phone = request.GET.get('phone', None)
    email = request.GET.get('email', None)
    print(name+phone+email) 

    obj = Customers.objects.create(name=name, phone=phone , email=email)
    obj.save()
    objid = Customers.objects.latest('id')
    
    data = {
        'successful': True ,
        'id' : objid.id ,
        'name': name ,
    }
    return JsonResponse(data)