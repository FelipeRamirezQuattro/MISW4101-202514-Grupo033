from src.logica.FachadaRecetario import FachadaRecetario
from src.modelo.Declarative_base import Base, engine, session
from src.modelo.Receta import Receta
from src.modelo.Ingrediente import Ingrediente
from src.modelo.IngredienteReceta import IngredienteReceta
class LogicaRecetario(FachadaRecetario):

    def __init__(self):
        Base.metadata.create_all(engine)

    def dar_recetas(self):
        recetas = session.query(Receta).all()
        resultado = []
        for receta in recetas:
            resultado.append({
                "id": receta.id,
                "nombre": receta.nombre,
                "tiempo": receta.tiempoPreparacion,
                "personas": receta.nroPersonasPreparacion,
                "calorias": receta.caloriasPorcion,
                "preparacion": receta.instrucciones
            })
        print(resultado)
        return resultado
    
    def dar_receta(self, id_receta):
        raise NotImplementedError("Método no implementado")
    
    def validar_crear_editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        # Validaciones
        if not receta or receta.strip() == "":
            return "El nombre de la receta no puede estar vacío"
        if not tiempo or tiempo.strip() == "":
            return "El tiempo de preparación no puede estar vacío"
        if self.es_valor_numerico(tiempo) == False:
            return "El tiempo debe ser númerico"
        if not personas or personas.strip() == "":
            return "El número de personas no puede estar vacio"
        if self.es_valor_numerico(personas) == False:
            return "El número de personas debe ser númerico"
        if not calorias or calorias.strip() == "":
            return "Las el número de calorías no puede estar vacio"
        if self.es_valor_numerico(calorias) == False:
            return "Las calorías deben ser númericas"
        # Consultar si existe otra receta con ese nombre
        busqueda = session.query(Receta).filter(Receta.nombre == receta).first()
        if id_receta is None or id_receta == "-1":
            if busqueda:
                return "La receta ya existe"
        else:
            if busqueda and busqueda.id != int(id_receta):
                return "La receta ya existe"
        return ""
    
    def crear_receta(self, receta, tiempo, personas, calorias, preparacion):
        busqueda = session.query(Receta).filter(Receta.nombre == receta).first()
        if not busqueda:
            nuevaReceta = Receta(nombre = receta, tiempoPreparacion = tiempo, nroPersonasPreparacion = personas, caloriasPorcion = calorias, instrucciones = preparacion)
            session.add(nuevaReceta)
            session.commit()
            return True
        else:
            return False
        
    def editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        raise NotImplementedError("Método no implementado")

    def eliminar_receta(self, id_receta):
        print(self)
        raise NotImplementedError("Método no implementado")

    def dar_ingredientes(self):
        ingredientes = session.query(Ingrediente).all()
        resultado = []
        for ingrediente in ingredientes:
            resultado.append({
                "id": ingrediente.id,
                "nombre": ingrediente.nombre,
                "unidad": ingrediente.unidadMedida,
                "valor": ingrediente.valorUnidad,
                "sitioCompra": ingrediente.nombreProveedor
            })
        print(resultado)
        return resultado

    def dar_ingrediente(self, id_ingrediente):
        raise NotImplementedError("Método no implementado")

    def validar_crear_editar_ingrediente(self, nombre, unidad, valor, sitioCompra):
        raise NotImplementedError("Método no implementado")
		
    def crear_ingrediente(self, nombre, unidad, valor, sitioCompras):
        raise NotImplementedError("Método no implementado")

    def editar_ingrediente(self, id_ingrediente, nombre, unidad, valor, sitioCompras):
        raise NotImplementedError("Método no implementado")

    def eliminar_ingrediente(self, id_ingrediente):
        raise NotImplementedError("Método no implementado")

    def dar_ingredientes_receta(self, id_receta): 
        print(id_receta) 
        ingredientes_receta = session.query(Receta).filter_by(id= id_receta).first() 
        print(ingredientes_receta) 
        resultado = [] 
        for relacion in ingredientes_receta.ingredientes: 
            resultado.append({ 
                "ingrediente": relacion.ingrediente.nombre, 
                "unidad": relacion.unidadMedida, 
                "cantidad": relacion.cantidad 
            }) 
        return resultado

    def agregar_ingrediente_receta(self, receta, ingrediente, cantidad):
        receta_obj = session.query(Receta).filter_by(id=receta).first()
        ingrediente_obj = session.query(Ingrediente).filter_by(id=ingrediente).first()
        if not receta_obj or not ingrediente_obj:
            return False
        relacion_existente = session.query(IngredienteReceta).filter_by(idReceta=receta, idIngrediente=ingrediente).first()
        if relacion_existente:
            return False
        nueva_relacion = IngredienteReceta(receta=receta_obj, ingrediente=ingrediente_obj, cantidad=cantidad, unidadMedida=ingrediente_obj.unidadMedida)
        session.add(nueva_relacion)
        session.commit()
        return True

    def editar_ingrediente_receta(self, id_ingrediente_receta, receta, ingrediente, cantidad):
        raise NotImplementedError("Método no implementado")

    def eliminar_ingrediente_receta(self, id_ingrediente_receta, receta):
        raise NotImplementedError("Método no implementado")

    def validar_crear_editar_ingReceta(self,receta, ingrediente, cantidad):
        raise NotImplementedError("Método no implementado")

    def dar_preparacion(self, id_receta,cantidad_personas):
        raise NotImplementedError("Método no implementado")

    def es_valor_numerico(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False
