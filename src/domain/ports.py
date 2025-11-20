# src/domain/ports.py

from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Producto

# Este es el "puerto" para el repositorio de productos.
# Define las operaciones que la capa de aplicación puede realizar sobre los productos,
# sin saber cómo se implementan.
class ProductRepository(ABC):

    @abstractmethod
    def find_by_id(self, producto_id: int) -> Optional[Producto]:
        """Busca un producto por su ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[Producto]:
        """Obtiene todos los productos."""
        pass

    @abstractmethod
    def save(self, producto: Producto) -> Producto:
        """Guarda o actualiza un producto en el repositorio."""
        pass