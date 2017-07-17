"""MeetingRoomWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from booking import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index,name="index"),
    url(r'^login/$',views.login,name="login"),
    url(r'^logoutall/$',views.logOutAll,name="logOutAll"),
    url(r'^register/$',views.register,name="register"),
    url(r'^(?P<username>\w+)/homepage/$',views.homepage,name="homepage"),
    url(r'^(?P<username>\w+)/admin/$',views.adminSettings,name="adminSettings"),
    url(r'^(?P<admin>\w+)/update/(?P<username>\w+)/(?P<date>[-\w]+)/(?P<time>[:\w]+)/(?P<oldroom>\w)/(?P<newroom>\w)',views.changeRoom,name="changeRoom"),
    url(r'^(?P<username>\w+)/new/(?P<room>\w)/(?P<date>\w+)/(?P<time>\w+)/',views.makeBooking,name="makeBooking"),
    url(r'^(?P<username>\w+)/new/$',views.newBooking,name="newBooking"),
    url(r'^(?P<username>\w+)/logout/$',views.logout,name="logout"),
    url(r'^(?P<username>\w+)/rooms/$',views.rooms,name="rooms"),
    url(r'^(?P<username>\w+)/all',views.allBookings,name="allBookings"),
    url(r'^(?P<username>\w+)/manage',views.manage,name="manage"),
    url(r'^(?P<username>\w+)/delete/(?P<date>[-\w]+)/(?P<time>[:\w]+)/(?P<room>\w)',views.delete,name="delete"),
    url(r'^(?P<username>\w+)/deleteOld',views.deleteOld,name="deleteOld"),
    url(r'^(?P<username>\w+)/makeAdmin/(?P<name>\w+)',views.makeAdmin,name="makeAdmin"),


]
