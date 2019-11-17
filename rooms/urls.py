"""hotelapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import rooms.views as room_views

urlpatterns = [
    path('', room_views.viewRoom),
    path('view/', room_views.viewRoom),
    path('add/', room_views.addroom),
    path('delete/<int:room_id>/', room_views.deleteroom),
    path('search/', room_views.search),
    path('search/reservation/', room_views.reservation),
    path('search/reservation/room/', room_views.reservation_create),
    path('reservations/', room_views.my_reservations),
    path('occupancy/', room_views.hotel_occupancy),
]
