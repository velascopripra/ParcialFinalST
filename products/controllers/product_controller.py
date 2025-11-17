from flask import Blueprint, request, jsonify
from products.models.product_model import Products
from users.models.db import db

product_controller = Blueprint('product_controller', __name__)

# Obtener todos los productos
@product_controller.route('/api/products', methods=['GET'])
def get_products():
    print("listado de productos")
    products = Products.query.all()
    result = [
        {
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'stock': p.stock
        }
        for p in products
    ]
    return jsonify(result)

# Obtener un producto por id
@product_controller.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    print("obteniendo producto")
    product = Products.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock
    })

# Crear un nuevo producto
@product_controller.route('/api/products', methods=['POST'])
def create_product():
    print("creando producto")
    data = request.get_json(force=True)
    if not data:
        return jsonify({'error': 'No se recibió ningún JSON válido'}), 400

    new_product = Products(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

# Actualizar un producto
@product_controller.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    print("actualizando producto")
    product = Products.query.get_or_404(product_id)
    data = request.json
    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    product.stock = data['stock']
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

# Eliminar un producto
@product_controller.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    print("eliminando producto")
    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

