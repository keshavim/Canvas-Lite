from django.urls import path

from .views import home
from.views import taLogin
from.views import instructorLogin
from.views import supervisorLogin


urlpatterns = [
    #the first peramiter is the one you use in html links
    path('', home, name='/'),
    path('ta/login/', taLogin, name='/ta'),
    path('instructor/login/', instructorLogin, name='/instructor'),
    path('supervisor/login/', supervisorLogin, name='/supervisor'),

]