import os
import logging
import unittest
from urllib.parse import quote_plus
from service import app, status
from service.models import db, Product
from .factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "sqlite:///" + os.path.join(app.config["BASE_DIR"], "test.db")
)
BASE_URL = "/products"

class TestProductService(unittest.TestCase):
    
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
        self.client = app.test_client()
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def _create_products(self, count):
        products = []
        for _ in range(count):
            product = ProductFactory()
            product.create()
            products.append(product)
        return products

    def test_index(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_health(self):
        resp = self.client.get("/healthcheck")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["status"], "OK")

    def test_create_product(self):
        product = ProductFactory()
        resp = self.client.post(
            BASE_URL, json=product.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        new_product = resp.get_json()
        self.assertEqual(new_product["name"], product.name)
        
    # (Task 3a) READ
    def test_get_product(self):
        test_product = self._create_products(1)[0]
        resp = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_product.name)

    # (Task 3b) UPDATE
    def test_update_product(self):
        test_product = self._create_products(1)[0]
        new_product = test_product.serialize()
        new_product["name"] = "testing"
        resp = self.client.put(f"{BASE_URL}/{test_product.id}", json=new_product)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product["name"], "testing")

    # (Task 3c) DELETE
    def test_delete_product(self):
        test_product = self._create_products(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        resp = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # (Task 3d) LIST ALL
    def test_get_product_list(self):
        self._create_products(5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    # (Task 3e) LIST BY NAME
    def test_query_by_name(self):
        products = self._create_products(10)
        test_name = products[0].name
        name_count = len([product for product in products if product.name == test_name])
        resp = self.client.get(BASE_URL, query_string=f"name={quote_plus(test_name)}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), name_count)
        for product in data:
            self.assertEqual(product["name"], test_name)

    # (Task 3f) LIST BY CATEGORY
    def test_query_by_category(self):
        products = self._create_products(10)
        test_category = products[0].category
        category_count = len([product for product in products if product.category == test_category])
        resp = self.client.get(BASE_URL, query_string=f"category={test_category.name}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), category_count)
        for product in data:
            self.assertEqual(product["category"], test_category.name)

    # (Task 3g) LIST BY AVAILABILITY
    def test_query_by_availability(self):
        products = self._create_products(10)
        test_available = products[0].available
        available_count = len([product for product in products if product.available == test_available])
        resp = self.client.get(BASE_URL, query_string=f"available={test_available}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), available_count)
        for product in data:
            self.assertEqual(product["available"], test_available)
