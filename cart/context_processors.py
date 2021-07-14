from . models import Cart, Cartitems
from .views import _cart_id


def getCartQuantity(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cartitems = Cartitems.objects.filter(cart=cart[:1])
            quantity = 0
            for cartitem in cartitems:
                quantity += cartitem.quantity
        except Cart.DoesNotExist:
            quantity = 0
    return dict(quantity=quantity)
