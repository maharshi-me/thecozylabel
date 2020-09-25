from products.models import Category


def get_categories(request):
    return {
        'all_categories': Category.objects.all(),
    }