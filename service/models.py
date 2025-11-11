import logging
from enum import Enum
from . import db

logger = logging.getLogger("flask.app")

class DataValidationError(Exception):
    pass

class Category(Enum):
    CLOTHING = 0
    FOOD = 1
    ELECTRONICS = 2
    HOUSEWARES = 3
    TOYS = 4

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(256))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=False)
    category = db.Column(db.Enum(Category), nullable=False)

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        logger.info("Updating %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with no id for product")
        db.session.commit()

    def delete(self):
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "available": self.available,
            "category": self.category.name,
        }

    def deserialize(self, data):
        try:
            self.name = data["name"]
            self.description = data.get("description")
            self.price = data["price"]
            self.available = data["available"]
            self.category = getattr(Category, data["category"])
        except KeyError as error:
            raise DataValidationError("Invalid product: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid product: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        logger.info("Initializing database")
        cls.query.delete()
        db.session.commit()
        db.create_all()

    @classmethod
    def all(cls):
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category):
        logger.info("Processing category query for %s ...", category.name)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available=True):
        logger.info("Processing availability query for %s ...", available)
        return cls.query.filter(cls.available == available)
