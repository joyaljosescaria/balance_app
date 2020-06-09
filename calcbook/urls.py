from django.urls import path , include
from . import views

app_name = 'calcbook'

urlpatterns = [
    path('welcome/', views.welcome , name='welcome'),
    path('', views.user_login , name="user_login"),
    path('user_logout/', views.user_logout , name="user_logout"),
]
