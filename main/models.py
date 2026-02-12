from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва страви")
    description = models.TextField(blank=True, verbose_name="Опис")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    available = models.BooleanField(default=True, verbose_name="Доступна")
    image = models.ImageField(upload_to='menu_images', null=True, blank=True,verbose_name="Зображення")

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=100, verbose_name="Ім'я клієнта")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField(default='')

    def __str__(self):
        return f"Замовлення №{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"
