import os
import logging
import unittest
from service import app, db
from service.models import Product, Category, DataValidationError
from .factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "sqlite:///" + os.path.join(app.config["BASE_DIR"], "test.db")
)

class TestProductModel(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        db.session.close()

    def setUp(self):
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_create_a_product(self):
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        found = Product.all()
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].id, product.id)
        self.assertEqual(found[0].name, product.name)
        
    # (Task 2a) READ
    def test_read_a_product(self):
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)

    # (Task 2b) UPDATE
    def test_update_a_product(self):
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        original_id = product.id
        product.description = "testing"
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, "testing")
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].description, "testing")

    # (Task 2c) DELETE
    def test_delete_a_product(self):
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    # (Task 2d) LIST ALL
    def test_list_all_products(self):
        products = Product.all()
        self.assertEqual(products, [])
        for _ in range(5):
            product = ProductFactory()
            product.create()
        products = Product.all()
        self.assertEqual(len(products), 5)

    # (Task 2e) FIND BY NAME
    def test_find_by_name(self):
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        name = products[0].name
        count = len([product for product in products if product.name == name])
        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.name, name)

    # (Task 2f) FIND BY CATEGORY
    def test_find_by_category(self):
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        category = products[0].category
        count = len([product for product in products if product.category == category])
        found = Product.find_by_category(category)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.category, category)

    # (Task 2g) FIND BY AVAILABILITY
    def test_find_by_availability(self):
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        available = products[0].available
        count = len([product for product in products if product.available == available])
        found = Product.find_by_availability(available)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.available, available)

    def test_serialize_a_product(self):
        product = ProductFactory()
        data = product.serialize()
        self.assertEqual(data["id"], product.id)
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["description"], product.description)
        self.assertEqual(data["price"], str(product.price))
        self.assertEqual(data["available"], product.available)
        self.assertEqual(data["category"], product.category.name)

    def test_deserialize_a_product(self):
        data = ProductFactory().serialize()
        product = Product()
        product.deserialize(data)
        self.assertIsNotNone(product)
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.description, data["description"])
        self.assertEqual(product.price, float(data["price"]))
        self.assertEqual(product.available, data["available"])
        self.assertEqual(product.category.name, data["category"])
