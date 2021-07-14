from django.shortcuts import render, redirect
from store.models import Product, productVariation
from . models import Cart, Cartitems
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def minusCart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart = Cart.objects.get(cart_id=_cart_id(request))

    cartitems = Cartitems.objects.get(product=product, cart=cart)
    if cartitems.quantity > 1:
        cartitems.quantity -= 1
        cartitems.save()
    else:
        cartitems.delete()
        cartitems.save()

    return redirect('cart')


def removeCart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))

    cartitems = Cartitems.objects.get(product=product, cart=cart)
    cartitems.delete()
    cartitems.save()

    return redirect('cart')


def addCart(request, product_id):
    product = Product.objects.get(id=product_id)
    productvariation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = productVariation.objects.get(product=product,
                                                         variationCategory__iexact=key, variationValue__iexact=value)
                productvariation.append(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cartitems = Cartitems.objects.get(product=product, cart=cart)
        if len(productvariation) > 0:
            cartitems.itemVariation.clear()
            for item in productvariation:
                cartitems.itemVariation.add(item)

        cartitems.quantity += 1
        cartitems.save()
    except Cartitems.DoesNotExist:
        cartitem = Cartitems.objects.create(
            product=product, quantity=1, cart=cart)
        if len(productvariation) > 0:
            cartitem.itemVariation.clear()
            for item in productvariation:
                cartitem.itemVariation.add(item)
        cartitem.save()
    return redirect('cart')


def cart(request, total=0, quantity=0, cartitems=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cartitems = Cartitems.objects.filter(cart=cart, is_active=True)
        for cartitem in cartitems:
            total += (cartitem.product.price*cartitem.quantity)
            quantity += cartitem.quantity
    except ObjectDoesNotExist:
        pass
    context = {'total': total, 'quantity': quantity, 'cartitems': cartitems}
    return render(request, 'store/cart.html', context)
