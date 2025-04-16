from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('object/<int:object_id>/', views.service_detail, name='service_detail'),  # Детали услуги

    # Добавление услуги в корзину (заявку-черновик)
    path('add-to-cart/<int:object_id>/', views.add_to_cart, name='add_to_cart'),

    # Просмотр текущей заявки (корзины)
    path('cart/', views.cart_view, name='cart'),

    # Удаление услуги из корзины
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Сохранение заявки (смена статуса, выбор марсохода и т.п.)
    path('save-request/', views.save_request, name='save_request'),

    # Удаление заявки (логическое, через SQL)
    path('delete-request/<int:request_id>/', views.delete_request, name='delete_request'),
]
