from django.urls import path
from . import views

urlpatterns = [
    #the first peramiter is the one you use in html links
    path('', views.home, name='/'),
    path('the_app/', views.TheApp, name='the_app'),
    path('removelater/', views.RemoveThisLater, name='removethislater'),

]