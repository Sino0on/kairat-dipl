from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('category/<int:category_id>/', category_products, name='category_products'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('search-suggest/', search_suggest, name='search_suggest'),


]