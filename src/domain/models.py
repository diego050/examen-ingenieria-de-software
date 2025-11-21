from dataclasses import dataclass

# Usamos dataclass para definir nuestras entidades de negocio.
# Son simples contenedores de datos, sin lógica.

@dataclass
class Personaje:
    id: int
    nombre: str
    aldea: str
    jutsu_principal: str

@dataclass
class Comentario:
    id: int
    personaje_id: int
    autor: str
    texto: str