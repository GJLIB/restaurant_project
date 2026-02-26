from django.urls import path
from .views import* 

urlpatterns = [
   path('', menu_list.as_view(), name = 'menu_list'),
   path('add_to_cart/<int:menu_id>/', AddToCartView.as_view(), name='add_to_cart'),
   path("order_list/", OrderListView.as_view(), name="order_list"),
   path("create_order/", OrderCreateView.as_view(), name="order_create"),
   path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
   path('cart/', CartView.as_view(), name = 'cart')
   
]