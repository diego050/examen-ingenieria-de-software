# src/application/services.py

from typing import List
from src.domain.models import Personaje, Comentario
from src.domain.ports import PersonajeRepository, ComentarioRepository

# Servicio para la lógica de negocio relacionada con Personajes
class PersonajeService:
    def __init__(self, repository: PersonajeRepository):
        self.repository = repository

    def listar_personajes(self) -> List[Personaje]:
        """Caso de uso: Listar todos los personajes."""
        return self.repository.get_all()

    def crear_personaje(self, nombre: str, aldea: str, jutsu_principal: str) -> Personaje:
        """Caso de uso: Crear un nuevo personaje."""
        if not nombre:
            raise ValueError("El nombre del personaje no puede estar vacío.")
        
        nuevo_personaje = Personaje(
            id=None, # La base de datos asignará el ID
            nombre=nombre,
            aldea=aldea,
            jutsu_principal=jutsu_principal
        )
        return self.repository.save(nuevo_personaje)

# Servicio para la lógica de negocio relacionada con Comentarios
class ComentarioService:
    def __init__(self, repository: ComentarioRepository, personaje_repo: PersonajeRepository):
        self.repository = repository
        self.personaje_repo = personaje_repo

    def ver_comentarios_por_personaje(self, personaje_id: int) -> List[Comentario]:
        """Caso de uso: Ver todos los comentarios de un personaje específico."""
        return self.repository.find_by_personaje_id(personaje_id)

    def agregar_comentario(self, personaje_id: int, autor: str, texto: str) -> Comentario:
        """Caso de uso: Agregar un nuevo comentario a un personaje."""
        if not texto or not autor:
            raise ValueError("El autor y el texto del comentario no pueden estar vacíos.")

        # Verificación de negocio: el personaje debe existir para poder comentarlo.
        personaje = self.personaje_repo.find_by_id(personaje_id)
        if not personaje:
            raise ValueError("El personaje no existe.")

        nuevo_comentario = Comentario(
            id=None,
            personaje_id=personaje_id,
            autor=autor,
            texto=texto
        )
        return self.repository.save(nuevo_comentario)