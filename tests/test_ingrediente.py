import unittest

from faker import Faker

from src.logica.LogicaRecetario import LogicaRecetario
from src.modelo.Declarative_base import Session
from src.modelo.Ingrediente import Ingrediente

class IngredienteTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.recetario = LogicaRecetario()
        self.data_factory = Faker("es_ES")

        nombre = self.data_factory.name()
        unidadMedida = self.data_factory.random_element(["kilo", "libra", "gramo", "onza", "cuacharada", "cucharadita", "arroba", "miligramo", "litro"])
        valorUnidad = self.data_factory.pydecimal(min_value=1, max_value=100000, positive=True)
        nombreProveedor = self.data_factory.name()

        self.session = Session()
        self.ingrediente1 = Ingrediente(nombre=nombre, unidadMedida=unidadMedida, valorUnidad=valorUnidad, nombreProveedor=nombreProveedor)
        self.session.add(self.ingrediente1)

        self.session.commit()

    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()

        busquedaIngrediente = self.session.query(Ingrediente).all()

        '''Borra todos los ingrediente'''
        for ingrediente in busquedaIngrediente:
            self.session.delete(ingrediente)

        self.session.commit()
        self.session.close()


    def test_listar_ingredientes(self):
        recetas = self.recetario.dar_ingredientes()
        self.assertEqual(len(recetas), 1)

