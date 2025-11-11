import logging
from flask import jsonify, request, url_for, make_response, abort
from . import app, db
from .models import Product, Category, DataValidationError
from . import status  # HTTP Status Codes

# Health check endpoint
@app.route("/healthcheck")
def healthcheck():
    return jsonify(status="OK"), status.HTTP_200_OK

@app.route("/")
def index():
    return app.send_static_file("index.html")

######################################################################
# REST API ENDPOINTS
######################################################################

# ---------------------------------------------------------------------
# CREATE A NEW PRODUCT
# ---------------------------------------------------------------------
@app.route("/products", methods=["POST"])
def create_products():
    app.logger.info("Request to create a product")
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    location_url = url_for("get_products", product_id=product.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

# ---------------------------------------------------------------------
# RETRIEVE A PRODUCT (This is Task 4a)
# ---------------------------------------------------------------------
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    app.logger.info("Request for product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    app.logger.info("Returning product: %s", product.name)
    return jsonify(product.serialize()), status.HTTP_200_OK

# ---------------------------------------------------------------------
# UPDATE AN EXISTING PRODUCT (This is Task 4b)
# ---------------------------------------------------------------------
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    app.logger.info("Request to update product with id: %s", product_id)
    check_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    app.logger.info("Product with ID [%s] updated.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK

# ---------------------------------------------------------------------
# DELETE A PRODUCT (This is Task 4c)
# ---------------------------------------------------------------------
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    app.logger.info("Request to delete product with id: %s", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()
    app.logger.info("Product with ID [%s] delete complete.", product_id)
    return "", status.HTTP_204_NO_CONTENT

# ---------------------------------------------------------------------
# LIST ALL / QUERY PRODUCTS (This is Task 4d)
# ---------------------------------------------------------------------
@app.route("/products", methods=["GET"])
def list_products():
    app.logger.info("Request for product list")
    products = []
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")
    
    if name:
        products = Product.find_by_name(name)
    elif category:
        category_value = getattr(Category, category.upper())
        products = Product.find_by_category(category_value)
    elif available:
        available_value = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_value)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("Returning %d products", len(results))
    return jsonify(results), status.HTTP_200_OK

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db(app):
    Product.init_db(app)

def init_logging(app):
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

def check_content_type(media_type):
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {media_type}")
