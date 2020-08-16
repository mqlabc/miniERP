"""miniERP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from login.views import logout
from material.views import listing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('debt/', include('debt.urls',namespace='debt')),
    path('order/', include('order.urls',namespace='order')),
    path('material/', include('material.urls',namespace='material')),
    path('login/', include('login.urls',namespace='login')),
    path('logout/', logout),
    path('', listing),
]
