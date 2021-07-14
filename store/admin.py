from django.contrib import admin
from . models import Product, productVariation
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock',
                    'category', 'modified_date')
    prepopulated_fields = {'slug': ('product_name',)}


class productVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variationCategory',
                    'variationValue', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variationCategory')


admin.site.register(Product, ProductAdmin)
admin.site.register(productVariation, productVariationAdmin)
