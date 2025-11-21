# src/domain/ports.py

from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Personaje, Comentario

# Puerto para el Repositorio de Personajes
class PersonajeRepository(ABC):

    @abstractmethod
    def find_by_id(self, personaje_id: int) -> Optional[Personaje]:
        pass

    @abstractmethod
    def get_all(self) -> List[Personaje]:
        pass

    @abstractmethod
    def save(self, personaje: Personaje) -> Personaje:
        pass

# Puerto para el Repositorio de Comentarios
class ComentarioRepository(ABC):

    @abstractmethod
    def find_by_personaje_id(self, personaje_id: int) -> List[Comentario]:
        pass

    @abstractmethod
    def save(self, comentario: Comentario) -> Comentario:
        pass