from behave import given
from service.models import Product, Category

@given('the following products')
def step_impl(context):
    """ Load Products into the database """
    for row in context.table:
        product = Product()
        product.name = row['name']
        product.description = row['description']
        product.price = float(row['price'])
        product.available = row['available'] in ['True', 'true', '1']
        product.category = getattr(Category, row['category'].upper())
        product.create()
