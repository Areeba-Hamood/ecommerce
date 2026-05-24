from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q,Avg
from .models import Product, Category

def product_list(request):
        products = Product.objects.filter(is_active=True).select_related("category").prefetch_related("images")

        #filters
        category_slug = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        sort = request.GET.get('sort','newest')
        query = request.GET.get("q", "")

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(Q(category=category))

        if min_price:
            products = products.filter(Q(price__gte=min_price))

        if max_price:
            products = products.filter(Q(price__lte=max_price))

        if query:
            products = products.filter(Q(name__icontains=query)| Q(description__icontains=query)| Q(category__name__icontains=query))

        sort_map = {
            "newest": "-created_at",
            "price_asc": "price",
            "price_desc": "-price",
        }

        products = products.order_by(sort_map.get(sort,"-created_at"))
        paginator = Paginator(products, 10)
        page = paginator.get_page(request.GET.get('page'))

        return render(request, "products/list.html",{
            "products":page,
            "category" : Category.objects.filter(is_active=True),
            "current_sort": sort,
        })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all().order_by("order")
    variants = product.variants.all()
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:6]
    in_whishlist = False
    if request.user.is_authenticated:
        in_wishlist = request.user.wishlist.products.filter(pk=product.pk).exists()
    return render(request, "products/detail.html", {
        "product":  product,
        "images":   images,
        "variants": related,
        "in_wishlist":in_wishlist,
    })

    
        

# Create your views here.

