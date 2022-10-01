from django.urls import path
from . import views

app_name='theblog'
urlpatterns = [
    path('',views.homeblog,name='homeblog')
]