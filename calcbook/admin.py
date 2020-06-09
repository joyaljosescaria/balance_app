from django.contrib import admin
from . import models

admin.site.register(models.Customers)
admin.site.register(models.Services)
admin.site.register(models.Balance)
admin.site.register(models.Amount_debit)
admin.site.register(models.Total)
admin.site.register(models.Service_sites)
