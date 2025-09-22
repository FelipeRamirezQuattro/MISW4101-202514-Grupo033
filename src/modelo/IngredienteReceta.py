from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .Declarative_base import Base

class IngredienteReceta(Base):
    __tablename__ = 'IngredienteReceta'
    idReceta = Column(Integer, ForeignKey('Receta.id'), primary_key = True)
    idIngrediente = Column(Integer, ForeignKey('Ingrediente.id'), primary_key = True)
    cantidad = Column(Float)
    unidadMedida = Column(String)

    receta = relationship("Receta", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente", back_populates="recetas")