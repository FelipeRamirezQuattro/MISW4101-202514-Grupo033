import sys
from src.vista.InterfazRecetario import App_Recetario
from src.logica.LogicaRecetario import LogicaRecetario
from src.logica.LogicaMock import LogicaMock
from src.modelo.Declarative_base import Base, Session, engine
from src.modelo.Receta import Receta
from src.modelo.Ingrediente import Ingrediente
from src.modelo.IngredienteReceta import IngredienteReceta

if __name__ == '__main__':
    logica = LogicaRecetario()

    app = App_Recetario(sys.argv, logica)
    sys.exit(app.exec_())