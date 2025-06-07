from django.contrib import admin
from .models import Category, Product, StoreProduct
from import_export import resources
from import_export.admin import ExportMixin, ImportExportModelAdmin
from .models import Product, StoreProduct, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'sku', 'description', 'base_price', 'is_active', 'category__title', 'created_at')


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'sku', 'category', 'base_price', 'is_active', 'created_at')
    search_fields = ('name', 'sku', 'description')
    list_filter = ('is_active', 'category')
    autocomplete_fields = ('category',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="60" height="60" style="object-fit:contain;" />'
        return "—"
    image_tag.short_description = 'Превью'
    image_tag.allow_tags = True


from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import StoreProduct, Product


class StoreProductResource(resources.ModelResource):
    product = fields.Field(
        column_name='product',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'name')  # или 'sku' если хочешь по артикулу
    )

    class Meta:
        model = StoreProduct
        fields = ('id', 'store', 'product', 'price', 'created_at')
        export_order = ('id', 'store', 'product', 'price', 'created_at')


from import_export.admin import ImportExportModelAdmin
from .models import StoreProduct

@admin.register(StoreProduct)
class StoreProductAdmin(ImportExportModelAdmin):
    resource_class = StoreProductResource
    list_display = ('product', 'store', 'price', 'created_at')
    list_filter = ('store',)
    search_fields = ('product__name',)
    autocomplete_fields = ('product',)
    ordering = ('-created_at',)
