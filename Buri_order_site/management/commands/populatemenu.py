from django.core.management.base import BaseCommand
from ._private import create_products, create_category, create_ingredients
from Buri_order_site.models import Category


class Command(BaseCommand):
    help = """Creates products attached to each category in database.
    If there are no categories, creates 13 categories."""

    def handle(self, *args, **options):
        if Category.objects.count() == 0:
            create_category()
            self.stdout.write(
                self.style.SUCCESS("Succesfully populated menu with categories")
            )
        else:
            self.stdout.write(self.style.NOTICE("Categories are already present"))
        create_products()
        self.stdout.write(
            self.style.SUCCESS("Succesfully populated menu with products")
        )
        create_ingredients()
        self.stdout.write(
            self.style.SUCCESS("Succesfully populated menu with ingredients")
        )
