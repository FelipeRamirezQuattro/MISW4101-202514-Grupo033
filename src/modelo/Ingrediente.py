from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .Declarative_base import Base

class Ingrediente(Base):
    __tablename__ = 'Ingrediente'
    id = Column(Integer, primary_key = True)
    nombre = Column(String)
    unidadMedida = Column(String)
    valorUnidad = Column(Float)
    nombreProveedor = Column(String)
    recetas = relationship("IngredienteReceta", back_populates="ingrediente")