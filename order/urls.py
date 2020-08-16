from django.urls import path

from . import views

app_name = "order"
urlpatterns = [
    # path('', views.MaterialList.as_view(), name='index'),
    path('', views.listing, name='index'),
    path('<int:order_id>/', views.down_word, name='detail'),
    path('download/', views.download, name='download'),
]
