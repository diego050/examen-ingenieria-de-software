# tests/test_application.py
import pytest
from src.application.services import PersonajeService, ComentarioService
from src.domain.models import Personaje, Comentario
from src.domain.ports import PersonajeRepository, ComentarioRepository

# 1. El "Repositorio Falso" para Personajes.
class FakePersonajeRepository(PersonajeRepository):
    def __init__(self, personajes=None):
        self._personajes = personajes or []
        self._id_counter = 1

    def get_all(self):
        return self._personajes

    def save(self, personaje):
        if personaje.id is None:
            personaje.id = self._id_counter
            self._id_counter += 1
        self._personajes.append(personaje)
        return personaje

    def find_by_id(self, personaje_id):
        return next((p for p in self._personajes if p.id == personaje_id), None)

# 2. El "Repositorio Falso" para Comentarios.
class FakeComentarioRepository(ComentarioRepository):
    def __init__(self, comentarios=None):
        self._comentarios = comentarios or []
        self._id_counter = 1

    def find_by_personaje_id(self, personaje_id):
        return [c for c in self._comentarios if c.personaje_id == personaje_id]

    def save(self, comentario):
        if comentario.id is None:
            comentario.id = self._id_counter
            self._id_counter += 1
        self._comentarios.append(comentario)
        return comentario

# ===== Tests para PersonajeService =====

def test_listar_personajes_devuelve_lista_vacia_si_no_hay_personajes():
    # Arrange
    repo = FakePersonajeRepository()
    service = PersonajeService(repo)

    # Act
    personajes = service.listar_personajes()

    # Assert
    assert personajes == []

def test_listar_personajes_devuelve_personajes_existentes():
    # Arrange
    p1 = Personaje(id=1, nombre="Naruto", aldea="Konoha", jutsu_principal="Rasengan")
    p2 = Personaje(id=2, nombre="Sasuke", aldea="Konoha", jutsu_principal="Chidori")
    repo = FakePersonajeRepository([p1, p2])
    service = PersonajeService(repo)

    # Act
    personajes = service.listar_personajes()

    # Assert
    assert len(personajes) == 2
    assert personajes[0].nombre == "Naruto"
    assert personajes[1].nombre == "Sasuke"

def test_crear_personaje_con_nombre_vacio_lanza_error():
    # Arrange
    repo = FakePersonajeRepository()
    service = PersonajeService(repo)

    # Act & Assert
    with pytest.raises(ValueError, match="El nombre del personaje no puede estar vacío."):
        service.crear_personaje("", "Konoha", "Rasengan")

def test_crear_personaje_exitosamente():
    # Arrange
    repo = FakePersonajeRepository()
    service = PersonajeService(repo)

    # Act
    personaje = service.crear_personaje("Naruto", "Konoha", "Rasengan")

    # Assert
    assert personaje.nombre == "Naruto"
    assert personaje.aldea == "Konoha"
    assert personaje.jutsu_principal == "Rasengan"
    assert personaje.id is not None
    assert len(repo.get_all()) == 1

# ===== Tests para ComentarioService =====

def test_ver_comentarios_por_personaje_vacio():
    # Arrange
    personaje_repo = FakePersonajeRepository()
    comentario_repo = FakeComentarioRepository()
    service = ComentarioService(comentario_repo, personaje_repo)

    # Act
    comentarios = service.ver_comentarios_por_personaje(1)

    # Assert
    assert comentarios == []

def test_ver_comentarios_por_personaje_existentes():
    # Arrange
    personaje_repo = FakePersonajeRepository()
    c1 = Comentario(id=1, personaje_id=1, autor="Fan1", texto="¡Naruto es el mejor!")
    c2 = Comentario(id=2, personaje_id=1, autor="Fan2", texto="¡Increíble!")
    comentario_repo = FakeComentarioRepository([c1, c2])
    service = ComentarioService(comentario_repo, personaje_repo)

    # Act
    comentarios = service.ver_comentarios_por_personaje(1)

    # Assert
    assert len(comentarios) == 2
    assert comentarios[0].autor == "Fan1"

def test_agregar_comentario_exitosamente():
    # Arrange
    p1 = Personaje(id=1, nombre="Naruto", aldea="Konoha", jutsu_principal="Rasengan")
    personaje_repo = FakePersonajeRepository([p1])
    comentario_repo = FakeComentarioRepository()
    service = ComentarioService(comentario_repo, personaje_repo)

    # Act
    comentario = service.agregar_comentario(1, "Fan1", "¡Naruto es el mejor!")

    # Assert
    assert comentario.autor == "Fan1"
    assert comentario.texto == "¡Naruto es el mejor!"
    assert comentario.personaje_id == 1

def test_agregar_comentario_con_autor_vacio_lanza_error():
    # Arrange
    p1 = Personaje(id=1, nombre="Naruto", aldea="Konoha", jutsu_principal="Rasengan")
    personaje_repo = FakePersonajeRepository([p1])
    comentario_repo = FakeComentarioRepository()
    service = ComentarioService(comentario_repo, personaje_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="El autor y el texto del comentario no pueden estar vacíos."):
        service.agregar_comentario(1, "", "texto")

def test_agregar_comentario_con_texto_vacio_lanza_error():
    # Arrange
    p1 = Personaje(id=1, nombre="Naruto", aldea="Konoha", jutsu_principal="Rasengan")
    personaje_repo = FakePersonajeRepository([p1])
    comentario_repo = FakeComentarioRepository()
    service = ComentarioService(comentario_repo, personaje_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="El autor y el texto del comentario no pueden estar vacíos."):
        service.agregar_comentario(1, "Fan1", "")

def test_agregar_comentario_a_personaje_inexistente_lanza_error():
    # Arrange
    personaje_repo = FakePersonajeRepository()
    comentario_repo = FakeComentarioRepository()
    service = ComentarioService(comentario_repo, personaje_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="El personaje no existe."):
        service.agregar_comentario(999, "Fan1", "texto")