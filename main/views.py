from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Order, OrderItem, Menu, Category


class menu_list(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'menu/menu_list.html', {'categories': categories})
    
class AddToCartView(View):
    def post(self, request, menu_id):
        cart = request.session.get('cart', {})
        if str(menu_id) in cart:
            cart[str(menu_id)] += 1
        else:
            cart[str(menu_id)] = 1
        request.session['cart'] = cart
        return redirect('menu_list')


class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        cart_items = []
        total_price = 0

        for menu_id, quantity in cart.items():
            menu_item = get_object_or_404(Menu, id=menu_id)
            item_total = menu_item.price * quantity
            total_price += item_total
            cart_items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'item_total': item_total
            })

        return render(request, 'cart/cart.html', {
            'cart_items': cart_items,
            'total_price': total_price
        })


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
        cart = request.session.get('cart', {})

        # Отримуємо всі позиції меню
        for item in cart:
            dish = Menu.objects.get(id = int(item))
            OrderItem.objects.create(
                order=order,
                menu_item=dish,
                quantity=cart[item]
            )
        request.session['cart'] = {}
        return redirect("order_detail", pk=order.pk)