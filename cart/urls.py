from django.urls import path
from . import views
urlpatterns = [
    path('', views.cart, name='cart'),
    path('addcart/<int:product_id>/', views.addCart, name='addcart'),
    path('minuscart/<int:product_id>/', views.minusCart, name='minuscart'),
    path('removecart/<int:product_id>/', views.removeCart, name='removecart')

]
