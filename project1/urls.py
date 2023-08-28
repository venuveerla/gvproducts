"""
URL configuration for project1 project.

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
from gvproducts.views import home
from django.conf.urls.static import static
from django.conf import  settings
from gvproducts.views import *
urlpatterns = [
    path("admin/", admin.site.urls),
    path("",home,name="home"),
    path("registeration/",registeration,name="registeration"),
    path("register/",registered,name="register"),
    path("product/",product,name="product"),
    path("purchase/",purchasing,name="purchase"),
    path("addaproduct/",addaproduct,name="addaproduct"),
    path("balance/",balance,name="balance"),
    path("getdetails/",getdetails,name="getdetails"),
    path("updatebalance/",updatebalance,name="updatebalance"),
     path("billpayment/",billpayment,name="billpayment"),
    path("updatebalanceafterbill/",updatebalanceafterbill,name='updatebalanceafterbill'),
    path("toadd/",toadd,name="toadd"),
    path("update/",update,name="update"),
    path("updateaproduct/",updateaproduct,name="updateaproduct"),
    path("dashboard/",dashboard,name="dashboard")
   # path("",respond,name="respond")
]


if settings.DEBUG:
    
    urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
