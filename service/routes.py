# service/routes.py

from flask import jsonify, request, url_for, abort
from service.models import Product, Category
from service.common import status  # HTTP Status Codes
from . import app

@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product
    This endpoint will return a Product based on its id
    """
    app.logger.info("Request to Retrieve a Product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    return jsonify(product.serialize()), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Update a Product
    This endpoint will update a Product based on the body that is posted
    """
    app.logger.info("Request to update a Product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    product.deserialize(request.get_json())
    product.update()
    return jsonify(product.serialize()), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a Product
    This endpoint will delete a Product based on the id specified in the path
    """
    app.logger.info("Request to delete a Product with id: %s", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()
    return '', status.HTTP_204_NO_CONTENT

@app.route("/products", methods=["GET"])
def list_products():
    """
    List all Products
    This endpoint will list all Products
    """
    app.logger.info("Request to list Products")
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")
    if name:
        products = Product.find_by_name(name)
    elif category:
        category_enum = Category[category]
        products = Product.find_by_category(category_enum)
    elif available is not None:
        available_bool = available.lower() in ['true', '1', 't', 'y', 'yes']
        products = Product.find_by_availability(available_bool)
    else:
        products = Product.all()
    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK
