from flask import Flask, jsonify, request
from src.application.services import ProductService
from src.infrastructure.adapters.database import SQLAlchemyProductRepository
from src.infrastructure.config import SessionLocal
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Este es el "Composition Root", el único lugar donde las clases concretas se instancian
# y se inyectan en los servicios.
def get_product_service():
    session = SessionLocal()
    repository = SQLAlchemyProductRepository(session)
    return ProductService(repository)

@app.route('/productos', methods=['GET'])
def listar_productos():
    service = get_product_service()
    productos = service.ver_productos()
    return jsonify([producto.__dict__ for producto in productos])

@app.route('/productos', methods=['POST'])
def agregar_producto():
    datos = request.json
    service = get_product_service()
    try:
        nuevo_producto = service.crear_producto(
            nombre=datos['nombre'],
            descripcion=datos['descripcion'],
            precio=float(datos['precio']),
            comerciante_id=int(datos['comerciante_id'])
        )
        return jsonify(nuevo_producto.__dict__), 201
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
