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
from django.views.generic import CreateView , UpdateView , View
from django.views.generic.list import ListView
from . forms import ServicesForm , CustomerAddForm , DebitForm , DateForm
from .render import Render
from datetime import date

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
            service_profitless = service.service_charge - service.profit
            balance_amt = service.service_charge
            profit = service.profit
            # all_total = Total.objects.only('id')
            print(isPaid)

            if isPaid == True:
                totalobj = Total.objects.get(id=1)
                total_bal = totalobj.total_amt + profit
                profit_bal = totalobj.profit_total + profit
                totalobj.total_amt = total_bal
                totalobj.profit_total = profit_bal
                totalobj.save()
            else:
                services = Services.objects.last()
                balobj = Balance.objects.create(service_id=services , balance_amt = balance_amt )
                balobj.save() 
                totalobj = Total.objects.get(id=1)
                total_loss = totalobj.loss_total + service_profitless
                totalobj.loss_total = total_loss
                totalobj.save()

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

class ServicesUpdateView(UpdateView):
    model = Services
    form_class = ServicesForm
    template_name = "edit_services.html"
    success_url = '/welcome/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = Services.objects.filter(id= self.object.pk)
        for nam in name:
            name = nam.customer_id.name
            isPaid = nam.isPaid
            ids = nam.id
        context['name'] = name
        context['isPaid'] = isPaid
        context['id'] = ids
        return context

def change_name(request):
    name = request.GET.get('name', None)
    ids = request.GET.get('id')
    
    obj = Customers.objects.get(id= ids)
    print(obj.name)
    obj.name = name 
    print(obj.name)
    obj.save()
    
    data = {
        'successful': True ,
    }
    return JsonResponse(data) 

def change_data(request):
    ser_id = request.GET.get('ser_id')
    profit = request.GET.get('profit')
    sercharge = request.GET.get('sercharge')

    profit = float(profit)
    sercharge = float(sercharge)
    
    balObj = Balance.objects.get(service_id = ser_id)
    balObj.delete()

    totalobj = Total.objects.get(id=1)
    tot_ls = sercharge - profit
    totalobj.loss_total = totalobj.loss_total - tot_ls
    totalobj.profit_total = totalobj.profit_total + profit
    totalobj.total_amt = totalobj.total_amt + profit
    totalobj.save()
    
    data = {
        'successful': True ,
    }
    return JsonResponse(data) 


class DebitAddViewCreateView(CreateView):
    debit = Amount_debit.objects.order_by('-id')

    def get(self, request, *args, **kwargs):
        context = {'form': DebitForm() , 'debits': self.debit}
        return render(request, 'add_debits.html', context)

    def post(self, request, *args, **kwargs):
        form = DebitForm(request.POST)
        if form.is_valid():
            debit = form.save()
            debit.save()
            
            amt = debit.debit_amt
            totalobj = Total.objects.get(id=1)
            total_ls = totalobj.loss_total + amt
            totalobj.loss_total = total_ls
            totalobj.save()
            
            return HttpResponseRedirect(reverse_lazy('calcbook:welcome'))
        return render(request, 'add_debits.html', {'form': form , 'debits': self.debit})

class ServiceListView(ListView):
    services = Services.objects.order_by('-id')

    def get(self, request, *args, **kwargs):
        context = {'form': DateForm() , 'services': self.services}
        return render(request, 'service_list.html', context)

    def post(self, request, *args, **kwargs):
        form = DateForm(request.POST)
        if form.is_valid():

            date1 = request.POST.get('date1')
            date2 = request.POST.get('date2')
            
            services = Services.objects.filter(service_date__range=(date1, date2)).order_by('-id')
            return render(request, 'service_list.html', {'form': form , 'services': services}) 

class BalanceList(ListView):
    # model = Balance
    queryset = Balance.objects.order_by('-id')
    context_object_name = 'balances'
    template_name = "balance_list.html"

class TodayPdf(View):
    today = date.today()

    def get(self, request):
        services = Services.objects.filter(service_date = self.today).order_by('-id')
        params = {
            'today': self.today,
            'sales': services,
            'request': request
        }
        return Render.render('daypdf.html', params) 