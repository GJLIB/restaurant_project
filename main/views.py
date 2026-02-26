from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Order, OrderItem, Menu, Category


class menu_list(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'menu/menu_list.html', {'categories': categories})
    def post(self, request):
        cart = session


class OrderListView(View):
    def get(self, request):
        orders = Order.objects.prefetch_related("items").all().order_by("-created_at")
        return render(request, "orders/order_list.html", {"orders": orders})


class OrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order.objects.prefetch_related("items__menu_item"), pk=pk)
        return render(request, "orders/order_detail.html", {"order": order})


class OrderCreateView(View):
    def get(self, request):
        menu_items = Menu.objects.all()
        return render(request, "orders/order_create.html", {"menu_items": menu_items})

    def post(self, request):
        customer_name = request.POST.get("customer_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        order = Order.objects.create(
            customer_name=customer_name,
            phone=phone,
            address=address
        )

        # Отримуємо всі позиції меню
        for item in Menu.objects.all():
            quantity = request.POST.get(f"quantity_{item.id}")
            if quantity and int(quantity) > 0:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=int(quantity)
                )

        return redirect("order_detail", pk=order.pk)