from django.urls import path , include
from . import views

app_name = 'calcbook'

urlpatterns = [
    path('welcome/', views.welcome , name='welcome'),
    path('', views.user_login , name="user_login"),
    path('user_logout/', views.user_logout , name="user_logout"),
    path('add_services/', views.add_services.as_view() , name="add_services"),
    path('add_debit/', views.DebitAddViewCreateView.as_view() , name="add_debit"),
    path('ajax/add_customer/', views.add_customer, name="add_customer"),
    path('ajax/change_name/', views.change_name, name="change_name"),
    path('ajax/change_data/', views.change_data, name="change_data"),
    # path('ajax/change_pending/', views.change_pending, name="change_pending"),
    path('update_services/<int:pk>/update/', views.ServicesUpdateView.as_view(), name="update_services"),
    path('balance/', views.BalanceList.as_view(), name="balance"),
    path('services/', views.ServiceListView.as_view(), name="services"),
    path('daypdf/', views.TodayPdf.as_view(), name="daypdf"),
]
