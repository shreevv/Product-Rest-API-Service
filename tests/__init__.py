import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal
from service.models import Product, Category

class ProductFactory(factory.Factory):
    """Creates fake Products"""

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    price = FuzzyDecimal(10.0, 100.0, precision=2)
    available = FuzzyChoice(choices=[True, False])
    category = FuzzyChoice(choices=[Category.CLOTHING, Category.FOOD, Category.ELECTRONICS, Category.HOUSEWARES, Category.TOYS])
