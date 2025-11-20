# src/infrastructure/adapters/database.py

from sqlalchemy.orm import Session
from src.domain.models import Producto as DomainProducto
from src.domain.ports import ProductRepository
from sqlalchemy import Table, Column, Integer, String, Float, MetaData, select # <-- Importar 'select'

# Mapeo de la tabla de la base de datos (detalle de infraestructura)
metadata = MetaData()
productos_table = Table(
    'productos', metadata,
    Column('id', Integer, primary_key=True),
    Column('nombre', String(100)), # Aumentado para coincidir con el SQL
    Column('descripcion', String(255)),
    Column('precio', Float),
    Column('comerciante_id', Integer)
)


class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, producto_id: int):
        # Forma correcta de consultar con Core
        stmt = select(productos_table).where(productos_table.c.id == producto_id)
        row = self.session.execute(stmt).first()
        return DomainProducto(**row._asdict()) if row else None

    def get_all(self):
        # Forma correcta de consultar con Core
        stmt = select(productos_table)
        rows = self.session.execute(stmt).all()
        return [DomainProducto(**row._asdict()) for row in rows]

    def save(self, producto: DomainProducto):
        # El método save estaba casi bien, pero es mejor ser explícito
        stmt = productos_table.insert().values(
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio=producto.precio,
            comerciante_id=producto.comerciante_id
        )
        result = self.session.execute(stmt)
        self.session.commit()
        producto.id = result.inserted_primary_key[0]
        return producto