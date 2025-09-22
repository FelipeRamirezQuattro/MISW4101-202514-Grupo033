import unittest

from src.logica.LogicaRecetario import LogicaRecetario
from src.modelo.Receta import Receta
from src.modelo.Ingrediente import Ingrediente
from src.modelo.IngredienteReceta import IngredienteReceta
from src.modelo.Declarative_base import Session
from faker import Faker

class RecetaTestCase(unittest.TestCase):

    def setUp(self):
        '''Crea una colección para hacer las pruebas'''
        self.logica = LogicaRecetario()

        '''Inicializa Faker'''
        self.faker = Faker()

        '''Abre la sesión'''
        self.session = Session()

        '''Crear los objetos'''
        self.receta1 = Receta(nombre = 'Arroz con pollo', tiempoPreparacion = 1, nroPersonasPreparacion = 5, caloriasPorcion = 200, instrucciones = 'Preparación...')
        self.receta2 = Receta(nombre = 'Ajiaco', tiempoPreparacion = 1, nroPersonasPreparacion = 10, caloriasPorcion = 400, instrucciones = 'Preparación...')
        self.receta3 = Receta(nombre = 'Paella', tiempoPreparacion = 2, nroPersonasPreparacion = 15, caloriasPorcion = 300, instrucciones = 'Preparación...')

        self.ingrediente1 = Ingrediente(nombre="Harina", unidadMedida="g", valorUnidad=1, nombreProveedor="Molinos SA")
        self.ingrediente2 = Ingrediente(nombre="Huevo", unidadMedida="unidad", valorUnidad=2, nombreProveedor="Avícola SAS")
        self.ingrediente3 = Ingrediente(nombre="Azucar", unidadMedida="unidad", valorUnidad=3, nombreProveedor="Avícola SAS")

        self.rel1 = IngredienteReceta(receta = self.receta1, ingrediente = self.ingrediente1, cantidad = 3, unidadMedida = "g")
        self.rel2 = IngredienteReceta(receta = self.receta2, ingrediente = self.ingrediente2, cantidad = 3, unidadMedida = "g")
        self.rel3 = IngredienteReceta(receta = self.receta3, ingrediente = self.ingrediente3, cantidad = 3, unidadMedida = "g")
        
        '''Adiciona los objetos a la sesión'''
        self.session.add(self.receta1)
        self.session.add(self.receta2) 
        self.session.add(self.receta3)
        self.session.add(self.ingrediente1)
        self.session.add(self.ingrediente2) 
        self.session.add(self.ingrediente3) 
        self.session.add(self.rel1) 
        self.session.add(self.rel2) 
        self.session.add(self.rel3)

        '''Persiste los objetos y cierra la sesión'''
        self.session.commit()

    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()

        '''Consulta todos las recetas, ingrediente, Ingrediente - receta'''
        busquedaReceta = self.session.query(Receta).all()
        busquedaIngrediente = self.session.query(Ingrediente).all()
        busquedaIngredienteReceta = self.session.query(IngredienteReceta).all()

        '''Borra todos las recetas'''
        for receta in busquedaReceta:
            self.session.delete(receta)

        '''Borra todos los ingrediente'''
        for ingrediente in busquedaIngrediente:
            self.session.delete(ingrediente)

        '''Borra todos los ingrediente Receta'''
        for ingredienteReceta in busquedaIngredienteReceta:
            self.session.delete(ingredienteReceta)

        self.session.commit()
        self.session.close()

    # Pruebas Unitarias: HU001 Agregar Receta (Validaciones)
    def test_nombre_vacio(self):
        error = self.logica.validar_crear_editar_receta(
            None, "", "1", "5", "200", "Preparar..."
        )
        self.assertEqual(error, "El nombre de la receta no puede estar vacío")

    def test_tiempo_vacio(self):
        error = self.logica.validar_crear_editar_receta(
            None, "Ajiaco", "", "5", "200", "Preparar..."
        )
        self.assertEqual(error, "El tiempo de preparación no puede estar vacío")

    def test_tiempo_numero(self):
        error = self.logica.validar_crear_editar_receta(
            None, "Ajiaco", "abc", "5", "200", "Preparar..."
        )
        self.assertEqual(error, "El tiempo debe ser númerico")

    def test_personas_vacio(self):
        error = self.logica.validar_crear_editar_receta(
            None, "Ajiaco", "1", "", "200", "Preparar..."
        )
        self.assertEqual(error, "El número de personas no puede estar vacio")

    def test_personas_numero(self):
        error = self.logica.validar_crear_editar_receta(
            None, "Ajiaco", "1", "abc", "200", "Preparar..."
        )
        self.assertEqual(error, "El número de personas debe ser númerico")

    def test_calorias_vacio(self):
        error = self.logica.validar_crear_editar_receta(
            None, "Ajiaco", "1", "5", "", "Preparar..."
        )
        self.assertEqual(error, "Las el número de calorías no puede estar vacio")

    def test_calorias_numero(self):
        error = self.logica.validar_crear_editar_receta(
            None, "Ajiaco", "1", "5", "abc", "Preparar..."
        )
        self.assertEqual(error, "Las calorías deben ser númericas")

    def test_receta_existente(self):

        error = self.logica.validar_crear_editar_receta(
        "-1",
        self.receta1.nombre,
        "2", "4", "300", "Preparar..."
        )
        self.assertEqual(error, "La receta ya existe")
    
    def test_editar_cambiando_a_nombre_existente(self):
        error = self.logica.validar_crear_editar_receta(
            str(self.receta1.id), 
            "Ajiaco",  
            "1", "5", "200", "Preparar..."
        )
        self.assertEqual(error, "La receta ya existe")

    def test_editar_manteniendo_nombre(self):
        error = self.logica.validar_crear_editar_receta(
            str(self.receta1.id),
            "Arroz con pollo",
            "1", "5", "200", "Preparar..."
        )
        self.assertEqual(error, "")
    
    # Pruebas Unitarias: HU001 Agregar Receta
    def test_agregar_receta(self):
        resultado = self.logica.crear_receta(
            "Sancocho",
            1, 5, 200, "Preparar..."
        )
        self.assertEqual(resultado, True)
    
    def test_agregar_receta_incorrecto(self):
        resultado = self.logica.crear_receta(
            "Ajiaco",
            1, 5, 200, "Preparar..."
        )
        self.assertEqual(resultado, False)

    # Pruebas Unitarias HU002 Listar Receta
    def test_listar_recetas(self):
        recetas = self.logica.dar_recetas()
        self.assertEqual(len(recetas), 3)
        self.assertEqual(recetas[0]['nombre'], "Arroz con pollo")
        self.assertEqual(recetas[1]['nombre'], "Ajiaco")
        self.assertEqual(recetas[2]['nombre'], "Paella")

    # Pruebas Unitarias HU010 Listar Ingredientes de una Receta
    def test_dar_ingredientes_receta_lista(self):
        logica = LogicaRecetario()
        # Receta con id 1
        ingredientes = logica.dar_ingredientes_receta(1)
        assert isinstance(ingredientes, list)
        for ingrediente in ingredientes:
            assert "ingrediente" in ingrediente
            assert "unidad" in ingrediente
            assert "cantidad" in ingrediente

        # Pruebas Unitarias HU010 Gestionar Ingrediente Receta:  Agregar Ingrediente a Receta
    def test_agregar_ingrediente_receta(self):
        nombre_receta = self.faker.word()
        nombre_ingrediente = self.faker.word()
        unidad = self.faker.random_element(elements=("g", "ml"))
        cantidad = self.faker.random_int(min=1, max=100)

        receta = Receta(nombre=nombre_receta, tiempoPreparacion=1, nroPersonasPreparacion=5, caloriasPorcion=200, instrucciones="Preparación...")
        ingrediente = Ingrediente(nombre=nombre_ingrediente, unidadMedida=unidad, valorUnidad=1, nombreProveedor=self.faker.company())
        self.session.add(receta)
        self.session.add(ingrediente)
        self.session.commit()

        # Agrega un ingrediente a la receta
        resultado = self.logica.agregar_ingrediente_receta(receta.id, ingrediente.id, cantidad)
        self.assertTrue(resultado)
        # Verifica que el ingrediente fue agregado correctamente
        ingredientes = self.logica.dar_ingredientes_receta(receta.id)
        nombres = [i["ingrediente"] for i in ingredientes]
        self.assertIn(nombre_ingrediente, nombres)