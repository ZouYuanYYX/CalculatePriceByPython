"""price181120 URL Configuration

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
from price import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.window),
    url(r'^index/finished_automobile_line/$', views.finished_automobile_line),
    url(r'^index/finished_automobile_price/$', views.finished_automobile_price),
    url(r'^index/js/distpicker.data.js/$', views.distpicker_data_js),
    url(r'^index/js/distpicker.js/$', views.distpicker_js),
    url(r'^index/js/main.js/$', views.main_js),
    url(r'^index/finished_automobile_price/js/distpicker.data.js/$', views.distpicker_data_js),
    url(r'^index/finished_automobile_price/js/distpicker.js/$', views.distpicker_js),
    url(r'^index/finished_automobile_price/js/main.js/$', views.main_js),
    url(r'^getDistance/$', views.getDistance),
    url(r'^calculateVehiclePrice/$',views.calculateVehiclePrice),

]
