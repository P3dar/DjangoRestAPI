from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items/', views.menuitems),
    path('menu-items/<int:pk>', views.SingleMenuItem),
    path('groups/manager/users', views.managers),
    path('groups/manager/users/<int:pk>', views.delManagers),
    path('groups/delivery-crew/users', views.deliverycrew),
    path('groups/delivery-crew/users/<int:pk>', views.delDelivery),
    path('cart/menu-items', views.cart),
    path('category', views.categories),
    path('orders', views.Makeorder),
    path('orders/<int:pk>', views.singleOrder),
]
