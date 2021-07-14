from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=2000)
    price = models.IntegerField(null=True)
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def getSlugUrl(self):
        return reverse('productDetail', args=[self.category.category_slug, self.slug])


class productVariationManager(models.Manager):
    def color(self):
        return super(productVariationManager, self).filter(variationCategory='color', is_active=True)

    def size(self):
        return super(productVariationManager, self).filter(variationCategory='size', is_active=True)


variationCategoryChoices = (
    ('color', 'color'),
    ('size', 'size')
)


class productVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variationCategory = models.CharField(
        max_length=100, choices=variationCategoryChoices)
    variationValue = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = productVariationManager()

    def __str__(self):
        return self.variationValue
