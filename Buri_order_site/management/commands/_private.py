from Buri_order_site.models import Product, Category, Ingredients
from faker import Faker
from random import randint

fake = Faker("pl_PL")


def create_category():
    Category.objects.create(name="Zupy", details="Tradycyjne zupy japońskie")
    Category.objects.create(name="Dania ciepłe", details="Tradycyjne dania japońskie")
    Category.objects.create(
        name="Hosomaki",
        details="""Jednoskładnikowa rolka sushi, z rybą lub warzywami,
        dzielona na 6 kawałków""",
    )
    Category.objects.create(
        name="Sashimi",
        details="""Jedna z tradycyjnych form japońskiego sushi.
        Kawałki pokrojonych ryb. Porcje po 10,15 lub 20 kawałków""",
    )
    Category.objects.create(
        name="Gunkan",
        details="""Kulka ryżu owinięta nori lub ogórkiem,
        z tatarem lub ikurą.
        Podawane po dwie sztuki""",
    )
    Category.objects.create(
        name="Nigiri",
        details="""Jedna z tradycyjnych form japońskiego sushi.
        Kawałek ryby lub owocu morza rozłożony na kulce ryżu""",
    )
    Category.objects.create(
        name="Futomaki",
        details="""Rolka japońskiego sushi, ryż i składniki zawinięte
        wewnątrz nori. Dzielone na 6 kawałków. Zawierają sałatę, serek,
        ogórek, oshinko i tykwę razem z rybą.
        Mogą być pieczone, surowe lub wege""",
    )
    Category.objects.create(
        name="Uramaki",
        details="""Inaczej zwane California roll. Dzielone na 8 kawałków,
        ryż na zewnątrz nori, a wypełnienie jest w jego wnętrzu.
        Zawierają serek, oshinko, tykwę oraz ogórek razem z rybą.
        Mogą być surowe, pieczone, wege oraz owiniętę w rybę lub owocę""",
    )
    Category.objects.create(
        name="Zestawy",
        details="""Zestawy sushi, zawierają różnorodne rolki,
        w różnych kombinacjach""",
    )
    Category.objects.create(
        name="Desery", details="Desery robione na miejscu przez naszą Szefową"
    )
    Category.objects.create(name="Napoje", details="Zimne lub ciepłe napoje.")
    Category.objects.create(
        name="Tatary i sałatki",
        details="""Różnorodne tatary oraz sałatki,
        robione według japońskich przepisów""",
    )
    Category.objects.create(
        name="Przystawki",
        details="""Przystawki robione na miejscu, mogą być w tempurze,
        japońskim cieście smażonym na głębokim oleju""",
    )


def create_products():
    for category in Category.objects.all():
        for _ in range(0, 10):
            category.products.create(
                name=fake.text(max_nb_chars=20),
                price=randint(20, 200),
                details=fake.text(max_nb_chars=100),
            )


def create_ingredients():
    for product in Product.objects.all():
        for i in range(3, 6):
            if i % 2 == 0:
                boolean = True
            else:
                boolean = False
            product.ingredients.create(
                name=fake.text(max_nb_chars=10),
                is_gluten=boolean,
                is_not_vegan=boolean,
                is_allergic=boolean,
            )
