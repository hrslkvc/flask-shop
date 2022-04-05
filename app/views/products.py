from flask import Blueprint, jsonify
from app.models.product import Product

products = Blueprint('products', __name__, url_prefix='/products')


@products.route('/', methods=('GET',))
def all_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])


@products.route('/<product_id>', methods=('GET',))
def product(product_id):
    product = Product.get(product_id)
    return jsonify(product.to_dict())
