from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    sku = models.CharField(max_length=100, unique=True, verbose_name="Артикул")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стандартная цена")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name


class StoreProduct(models.Model):
    STORE_CHOICES = [
        ('globus', 'Глобус'),
        ('narodny', 'Народный'),
        ('spar', 'Спар'),
        ('borsok', 'Борсок'),
        # Добавь другие магазины по мере необходимости
    ]

    store = models.CharField(max_length=50, choices=STORE_CHOICES, verbose_name="Магазин")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='store_products', verbose_name="Продукт")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена в магазине")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.product.name} — {self.get_store_display()}"
