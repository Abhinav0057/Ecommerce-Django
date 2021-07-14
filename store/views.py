from cart.models import Cartitems
from django.shortcuts import get_object_or_404, render
from .models import Product
from category.models import Category
from cart.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug == None:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        productCount = products.count()
        categories = Category.objects.all()
        paginator = Paginator(products, 2)
        page_number = request.GET.get('page')
        pagedPaginator = paginator.get_page(page_number)
        context = {'products': pagedPaginator,
                   'productCount': productCount, 'categories': categories}

    else:
        ourcategory = get_object_or_404(Category, category_slug=category_slug)
        products = Product.objects.filter(
            category=ourcategory, is_available=True)
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        pagedPaginator = paginator.get_page(page_number)
        productCount = products.count()
        categories = Category.objects.all()

        context = {'products': pagedPaginator,
                   'productCount': productCount, 'categories': categories}
    return render(request, 'store/storepage.html', context)


def productDetail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__category_slug=category_slug, slug=product_slug)
        in_cart = Cartitems.objects.filter(cart__cart_id=_cart_id(
            request), product=single_product).exists()

    except Exception as e:
        raise e
    context = {'single_product': single_product, 'in_cart': in_cart}
    return render(request, 'store/productDetail.html', context)


def search(request):
    if 'searchkeyword' in request.GET:
        searchkeyword = request.GET['searchkeyword']
        if searchkeyword:
            products = Product.objects.order_by(
                '-modified_date').filter(Q(product_name__icontains=searchkeyword) | Q(description__icontains=searchkeyword))
            productCount = products.count()
            context = {'products': products, 'productCount': productCount}
    return render(request, 'store/storepage.html', context)
