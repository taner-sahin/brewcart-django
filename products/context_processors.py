from .models import Category


def categories(request):
    nav_categories = Category.objects.all()

    return {
        "nav_categories": nav_categories
    }