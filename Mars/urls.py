from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('object/<int:object_id>/', views.service_detail, name='service_detail'),
    path('request/<int:request_id>/', views.view_request, name='view_request'),
]
