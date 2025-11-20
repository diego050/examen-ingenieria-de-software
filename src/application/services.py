# src/application/services.py

from typing import List
from src.domain.models import Producto
from src.domain.ports import ProductRepository

# El servicio de aplicación contiene la lógica de negocio de alto nivel.
class ProductService:
    def __init__(self, repository: ProductRepository):
        # El servicio recibe el repositorio a través de su constructor (inyección de dependencias).
        # No sabe qué tipo de base de datos se está usando, solo sabe que cumple el contrato de ProductRepository.
        self.repository = repository

    def ver_productos(self) -> List[Producto]:
        """Caso de uso: ver todos los productos disponibles."""
        return self.repository.get_all()

    def crear_producto(self, nombre: str, descripcion: str, precio: float, comerciante_id: int) -> Producto:
        """Caso de uso: un comerciante crea un nuevo producto."""
        # Aquí podrías agregar validaciones de negocio
        if precio <= 0:
            raise ValueError("El precio debe ser un número positivo.")
        
        nuevo_producto = Producto(
            id=None, # La base de datos asignará el ID
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            comerciante_id=comerciante_id
        )
        return self.repository.save(nuevo_producto)