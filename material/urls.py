from django.urls import path

from . import views

app_name = "material"
urlpatterns = [
    # path('', views.MaterialList.as_view(), name='index'),
    path('', views.listing, name='index'),
]
