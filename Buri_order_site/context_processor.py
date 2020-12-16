from Buri_order_site.models import Category


def category_anchor_list(request):
    categories = Category.objects.all()
    ctx = {"categories": categories}
    return ctx
