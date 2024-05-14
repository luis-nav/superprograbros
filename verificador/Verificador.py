# Clase del verificador
 
from analizador.arbolSintaxisAbstracta import ArbolSintaxisAbstracta, NodoASA, TipoNodo
from utils.TipoDatos import TipoDatos
from verificador.TablaSimbolos import TablaSimbolos
from verificador.Visitante import Visitante


class Verificador:

    asa            : ArbolSintaxisAbstracta
    visitador      : Visitante
    tablaSimbolos : TablaSimbolos

    def __init__(self, nuevoAsa: ArbolSintaxisAbstracta):

        self.asa            = nuevoAsa
        self.tablaSimbolos  = TablaSimbolos()
        self.visitador      = Visitante(self.tablaSimbolos)

        self.__ambienteEstandar()

    def imprimirAsa(self):
        """
        Imprime el árbol de sintáxis abstracta
        """
            
        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimirPreorden()

    def __ambienteEstandar(self):

        funcionesAmbienteEstandar = [ ('champiñon', TipoDatos.TEXTO),
                ('moneda', TipoDatos.TEXTO),
                ('estrella', TipoDatos.NINGUNO),
                ('puntuacion', TipoDatos.ENTERO),
                ('vidaExtra', TipoDatos.TEXTO),
                ('florFuego', TipoDatos.ENTERO),
                ('yoshi', TipoDatos.ENTERO),
                ('daisy', TipoDatos.TEXTO)]

        for nombre, tipo in  funcionesAmbienteEstandar:
            nodo = NodoASA(TipoNodo.FUNCIÓN, contenido=nombre, errorInfo={'tipo': tipo})
            self.tablaSimbolos.incluir(nombre, nodo)

    def verificar(self):
        self.visitador.visitar(self.asa.raiz)
