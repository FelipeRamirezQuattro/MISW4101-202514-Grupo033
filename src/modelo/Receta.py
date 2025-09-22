from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .Declarative_base import Base

class Receta(Base):
    
    __tablename__ = 'Receta'
    id = Column(Integer, primary_key = True)
    nombre = Column(String)
    tiempoPreparacion = Column(Integer)
    nroPersonasPreparacion = Column(Integer)
    caloriasPorcion = Column(Float)
    instrucciones = Column(String)
    ingredientes = relationship("IngredienteReceta", back_populates="receta")