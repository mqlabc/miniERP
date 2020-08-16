from django.urls import path

from . import views

app_name = "debt"
urlpatterns = [
    path('', views.index, name='index'),
    path('overdue/', views.overdue, name='overdue'),
    path('charts/', views.charts, name='charts'),
    path('change/', views.change_order_status, name='change'),
]
