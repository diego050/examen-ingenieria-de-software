# src/application/mappers.py
from typing import Dict, Any
from src.domain.models import Personaje, Comentario


class PersonajeMapper:
    """Maps Personaje domain model to/from DTOs (Data Transfer Objects)."""

    @staticmethod
    def to_dict(personaje: Personaje) -> Dict[str, Any]:
        """Convert Personaje domain model to dictionary for API responses."""
        return {
            "id": personaje.id,
            "nombre": personaje.nombre,
            "aldea": personaje.aldea,
            "jutsu_principal": personaje.jutsu_principal
        }

    @staticmethod
    def to_personaje(data: Dict[str, Any]) -> Personaje:
        """Convert API request data to Personaje domain model."""
        return Personaje(
            id=data.get("id"),
            nombre=data["nombre"],
            aldea=data["aldea"],
            jutsu_principal=data["jutsu_principal"]
        )

    @staticmethod
    def to_list(personajes: list) -> list:
        """Convert list of Personaje models to list of dictionaries."""
        return [PersonajeMapper.to_dict(p) for p in personajes]


class ComentarioMapper:
    """Maps Comentario domain model to/from DTOs (Data Transfer Objects)."""

    @staticmethod
    def to_dict(comentario: Comentario) -> Dict[str, Any]:
        """Convert Comentario domain model to dictionary for API responses."""
        return {
            "id": comentario.id,
            "personaje_id": comentario.personaje_id,
            "autor": comentario.autor,
            "texto": comentario.texto
        }

    @staticmethod
    def to_comentario(data: Dict[str, Any]) -> Comentario:
        """Convert API request data to Comentario domain model."""
        return Comentario(
            id=data.get("id"),
            personaje_id=data["personaje_id"],
            autor=data["autor"],
            texto=data["texto"]
        )

    @staticmethod
    def to_list(comentarios: list) -> list:
        """Convert list of Comentario models to list of dictionaries."""
        return [ComentarioMapper.to_dict(c) for c in comentarios]
