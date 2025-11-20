# tests/test_application.py
import pytest
from src.application.services import ProductService
from src.domain.models import Producto
from src.domain.ports import ProductRepository

# 1. Creamos un "Repositorio Falso" (Mock) para las pruebas.
#    Este repositorio no se conecta a ninguna base de datos, solo vive en la memoria.
class FakeProductRepository(ProductRepository):
    def __init__(self, productos=None):
        self._productos = productos or []

    def get_all(self):
        return self._productos

    def save(self, producto):
        self._productos.append(producto)
        return producto

    def find_by_id(self, producto_id):
        return next((p for p in self._productos if p.id == producto_id), None)

# 2. Escribimos nuestra primera prueba para el ProductService
def test_ver_productos_devuelve_lista_vacia_si_no_hay_productos():
    # Arrange (Preparar)
    repo = FakeProductRepository()
    service = ProductService(repo)

    # Act (Actuar)
    productos = service.ver_productos()

    # Assert (Verificar)
    assert productos == []

def test_crear_producto_con_precio_negativo_lanza_error():
    # Arrange
    repo = FakeProductRepository()
    service = ProductService(repo)

    # Act & Assert
    # Verificamos que se lance un ValueError cuando intentamos crear un producto con precio negativo.
    with pytest.raises(ValueError, match="El precio debe ser un número positivo."):
        service.crear_producto("Producto Malo", "Desc", -10, 1)