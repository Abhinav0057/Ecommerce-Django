from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name='storepage'),
    path('category/<slug:category_slug>/',
         views.store, name='storepageByCategory'),
    path('category/<slug:category_slug>/<slug:product_slug>/',
         views.productDetail, name='productDetail'),
    path('search/', views.search, name='searchpage'),

]
