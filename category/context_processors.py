from .models import Category


def getCategoryNameLinks(request):
    nameLinks = Category.objects.all()
    return dict(nameLinks=nameLinks)
