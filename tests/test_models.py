# tests/test_models.py

import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    def test_read_a_product(self):
        """It should Read a product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        found_product = Product.find(product.id)
        self.assertIsNotNone(found_product)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)
        self.assertEqual(found_product.available, product.available)
        self.assertEqual(found_product.category, product.category)

    def test_update_a_product(self):
        """It should Update a product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        product.description = "Updated description"
        product.update()
        updated_product = Product.find(product.id)
        self.assertEqual(updated_product.description, "Updated description")

    def test_delete_a_product(self):
        """It should Delete a product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        product.delete()
        deleted_product = Product.find(product.id)
        self.assertIsNone(deleted_product)

    def test_list_all_products(self):
        """It should List all products"""
        products = Product.all()
        self.assertEqual(products, [])
        for _ in range(5):
            product = ProductFactory()
            product.id = None
            product.create()
        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_find_product_by_name(self):
        """It should Find a product by name"""
        products = []
        for _ in range(5):
            product = ProductFactory()
            product.id = None
            product.create()
            products.append(product)
        name = products[0].name
        found_products = Product.find_by_name(name)
        self.assertEqual(len(found_products), len([p for p in products if p.name == name]))
        for product in found_products:
            self.assertEqual(product.name, name)

    def test_find_product_by_availability(self):
        """It should Find a product by availability"""
        products = []
        for _ in range(10):
            product = ProductFactory()
            product.id = None
            product.create()
            products.append(product)
        available = products[0].available
        found_products = Product.find_by_availability(available)
        self.assertEqual(len(found_products), len([p for p in products if p.available == available]))
        for product in found_products:
            self.assertEqual(product.available, available)

    def test_find_product_by_category(self):
        """It should Find a product by category"""
        products = []
        for _ in range(10):
            product = ProductFactory()
            product.id = None
            product.create()
            products.append(product)
        category = products[0].category
        found_products = Product.find_by_category(category)
        self.assertEqual(len(found_products), len([p for p in products if p.category == category]))
        for product in found_products:
            self.assertEqual(product.category, category)
