from .models import Category


def categories_processor(request):
    """
    Makes the list of all categories available to every template.
    """
    categories = Category.objects.all()
    return {"categories": categories}
