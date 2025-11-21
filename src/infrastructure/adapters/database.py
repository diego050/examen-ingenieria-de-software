# src/infrastructure/adapters/database.py
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, String, Float, MetaData, select, Text, ForeignKey
from src.domain.models import Personaje as DomainPersonaje, Comentario as DomainComentario
from src.domain.ports import PersonajeRepository, ComentarioRepository

# Mapeo de las tablas de la base de datos (detalle de infraestructura)
metadata = MetaData()

personajes_table = Table(
    'personajes', metadata,
    Column('id', Integer, primary_key=True),
    Column('nombre', String(100)),
    Column('aldea', String(100)),
    Column('jutsu_principal', String(100))
)

comentarios_table = Table(
    'comentarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('personaje_id', Integer, ForeignKey('personajes.id')),
    Column('autor', String(100)),
    Column('texto', Text)
)

# Implementación del Repositorio de Personajes
class SQLAlchemyPersonajeRepository(PersonajeRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[DomainPersonaje]:
        stmt = select(personajes_table)
        rows = self.session.execute(stmt).all()
        return [DomainPersonaje(**row._asdict()) for row in rows]

    def save(self, personaje: DomainPersonaje) -> DomainPersonaje:
        stmt = personajes_table.insert().values(
            nombre=personaje.nombre,
            aldea=personaje.aldea,
            jutsu_principal=personaje.jutsu_principal
        )
        result = self.session.execute(stmt)
        self.session.commit()
        personaje.id = result.inserted_primary_key[0]
        return personaje
    
    def find_by_id(self, personaje_id: int) -> Optional[DomainPersonaje]:
        stmt = select(personajes_table).where(personajes_table.c.id == personaje_id)
        row = self.session.execute(stmt).first()
        return DomainPersonaje(**row._asdict()) if row else None

# Implementación del Repositorio de Comentarios
class SQLAlchemyComentarioRepository(ComentarioRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def find_by_personaje_id(self, personaje_id: int) -> list[DomainComentario]:
        stmt = select(comentarios_table).where(comentarios_table.c.personaje_id == personaje_id)
        rows = self.session.execute(stmt).all()
        return [DomainComentario(**row._asdict()) for row in rows]

    def save(self, comentario: DomainComentario) -> DomainComentario:
        stmt = comentarios_table.insert().values(
            personaje_id=comentario.personaje_id,
            autor=comentario.autor,
            texto=comentario.texto
        )
        result = self.session.execute(stmt)
        self.session.commit()
        comentario.id = result.inserted_primary_key[0]
        return comentario