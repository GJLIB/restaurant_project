from django.urls import path
from .views import* 

urlpatterns = [
   path('', menu_list.as_view(), name = 'menu_list'),
 
   path("order_list/", OrderListView.as_view(), name="order_list"),
   path("create_order/", OrderCreateView.as_view(), name="order_create"),
   path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
]