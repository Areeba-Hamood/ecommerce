from.cart import Cart
from products.models import Wishlist 

def cart(request):
    return {'cart': Cart(request)}

def wishlist_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
            count = wishlist.products.count()
        except Exception:
            pass
    return {'wish_list_count': count}