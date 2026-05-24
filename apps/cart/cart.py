from decimal import Decimal
from django.conf import settings
from products.models import Products, ProductVariant

CART_SESSION_ID = 'cart'

class Cart(request):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, variant=None, override= False):
        key = str(product.id)

        if variant:
            key= f"{product.id}{variant.id}"

        if key not in self.cart:
            self.cart[key] = {
                'product.id' : product.id,
                'variant_id' : variant.id if variant else None,
                'quantity' : 0,
                'price' : str(product.price)
            }

        if override:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity 
        stock = variant.stock_quantity if variant else product.stock_quantity
        if self.cart[key]['quantity'] > stock:
            self.cart[key]['quantity'] = stock
        self.save()

    def remove(self,key):
        if key in self.cart:
            del self.cart[key]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def __iter__(self):
        product_ids = [v['product_id'] for v in self.cart.values()]
        products = Products.objects.filter(pk__in=product_ids)
        cart_copy = self.cart.copy()

        for product in products:
            for key, item in cart_copy.items():
                if item['product_id'] == product.id:
                    item ['product'] = product
                    item['total'] = Decimal(item['price'])*item['quantity']
                    yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    @property
    def subtotal(self):
        return sum (Decimal(i["price"])*i["quantity"] for i in self.cart.values())
    


