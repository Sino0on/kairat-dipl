from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
import random
from .models import Product, Category


def index(request):
    categories = Category.objects.all()
    all_products = list(Product.objects.filter(is_active=True))
    random_products = random.sample(all_products, min(20, len(all_products)))

    return render(request, 'index.html', {
        'categories': categories,
        'random_products': random_products,
    })


def category_products(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category, is_active=True).order_by('-created_at')

    paginator = Paginator(products, 20)  # 20 продуктов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'category_products.html', {
        'category': category,
        'page_obj': page_obj
    })


from .models import Product, StoreProduct


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    store_prices = StoreProduct.objects.filter(product=product).order_by('price')

    # Самая дешевая цена
    best_price = store_prices.first().price if store_prices.exists() else None

    return render(request, 'product_detail.html', {
        'product': product,
        'store_prices': store_prices,
        'best_price': best_price
    })


from django.http import JsonResponse
from .models import Product
from django.db.models import Q

from django.http import JsonResponse
from .models import Product
from django.db.models import Q

def search_suggest(request):
    query = request.GET.get('q', '').strip().lower()
    results = []

    if query:
        qs = Product.objects.filter(
            Q(name__icontains=query) |
            Q(name__istartswith=query) |
            Q(name__iexact=query)
        ).values('id', 'name')[:10]

        results = list(qs)

        # fallback: если ничего не нашли
        if not results and len(query) >= 2:
            fallback_qs = Product.objects.filter(
                Q(name__iregex=fr'{query[0]}.*{query[1:]}')
            ).values('id', 'name')[:10]

            results = list(fallback_qs)

    return JsonResponse(results, safe=False)
