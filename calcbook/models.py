from django.db import models

# Create your models here.
class Customers(models.Model):
    name = models.CharField(max_length = 50)
    phone = models.IntegerField(null=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Services(models.Model):
    service_name = models.CharField(max_length= 50)
    customer_id = models.ForeignKey(Customers , on_delete= models.CASCADE)
    service_charge = models.FloatField()
    profit = models.FloatField()
    isPaid = models.BooleanField()
    paid_amt = models.FloatField()
    service_date = models.DateField(auto_now=True)
    bal_paid_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.service_name

class Balance(models.Model):
    service_id = models.ForeignKey(Services , on_delete = models.CASCADE)
    balance_amt = models.FloatField()

    def __str__(self):
        return self.service_id.__str__()

class Amount_debit(models.Model):
    debit_use = models.CharField(max_length= 50)
    debit_amt = models.FloatField()
    debited_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.debit_use

class Total(models.Model):
    total_amt = models.FloatField()
    profit_total = models.FloatField()
    loss_total = models.FloatField()

    def __str__(self):
        return self.total_amt.__str__()

class Service_sites(models.Model):
    site_name = models.CharField(max_length=50)
    site_address = models.CharField(max_length=50)
    site_logo = models.CharField(max_length=100)
    site_desc = models.CharField(max_length=50)

    def __str__(self):
        return self.site_name
