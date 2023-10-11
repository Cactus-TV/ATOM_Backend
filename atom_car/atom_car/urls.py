"""
URL configuration for atom_car project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from car.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    #car
    path('car/admin/update', CarAdminAPIUpdate.as_view()),
    path('car/admin/create', CarAdminAPICreate.as_view()),
    path('car/get', CarAPIGet.as_view()),
    path('car/update', CarUpdateAPI.as_view()),
    #door
    path('car/door/admin/update', DoorAdminAPIUpdate.as_view()),
    path('car/door/admin/create', DoorAdminAPICreate.as_view()),
    path('car/door/get', DoorAPIGet.as_view()),
    path('car/door/update', DoorUpdateAPI.as_view()),
    #trunk
    path('car/trunk/admin/update', TrunkAdminAPIUpdate.as_view()),
    path('car/trunk/admin/create', TrunkAdminAPICreate.as_view()),
    path('car/trunk/get', TrunkAPIGet.as_view()),
    path('car/trunk/update', TrunkUpdateAPI.as_view()),
    #climate
    path('car/climate/admin/update', ClimateAdminAPIUpdate.as_view()),
    path('car/climate/admin/create', ClimateAdminAPICreate.as_view()),
    path('car/climate/get', ClimateAPIGet.as_view()),
    path('car/climate/update', ClimateUpdateAPI.as_view()),
    #wipers
    path('car/wiper/admin/update', WiperAdminAPIUpdate.as_view()),
    path('car/wiper/admin/create', WiperAdminAPICreate.as_view()),
    path('car/wiper/get', WiperAPIGet.as_view()),
    path('car/wiper/update', WiperUpdateAPI.as_view()),
    #seat
    path('car/seat/admin/update', WiperAdminAPIUpdate.as_view()),
    path('car/seat/admin/create', WiperAdminAPICreate.as_view()),
    path('car/seat/get', WiperAPIGet.as_view()),
    path('car/seat/update', WiperUpdateAPI.as_view()),
    #glass
    path('car/glass/admin/update', GlassAdminAPIUpdate.as_view()),
    path('car/glass/admin/create', GlassAdminAPICreate.as_view()),
    path('car/glass/get', GlassAPIGet.as_view()),
    path('car/glass/update', GlassUpdateAPI.as_view()),
    #places
    path('car/place/admin/update', PlaceAdminAPIUpdate.as_view()),
    path('car/place/admin/create', PlaceAdminAPICreate.as_view()),
    path('car/place/get', PlaceAPIGet.as_view()),
    path('car/place/update', PlaceUpdateAPI.as_view()),
    #windows
    path('car/window/admin/update', WindowAdminAPIUpdate.as_view()),
    path('car/window/admin/create', WindowAdminAPICreate.as_view()),
    path('car/window/get', WindowAPIGet.as_view()),
    path('car/window/update', WindowUpdateAPI.as_view()),
]
