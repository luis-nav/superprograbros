# Analizador SuperPrograBros 

#imports
from explorador.explorador import TipoComponenteLexico, ComponenteLexico
# clase de analizador, recibe la lista de componentes lexicos del explorador

class Analizador:
    # atributos
    componenteLexicos : list
    cantidadComponentes: int
    posicionComponenteActual: int
    componenteActual : ComponenteLexico

    # constructor
    def __init__(self, listaComponentes):

        self.componenteLexicos = listaComponentes
        self.cantidadComponentes = len(listaComponentes)
        self.posicionComponenteActual = 0
        self.componenteActual = listaComponentes[self.posicionComponenteActual]

        self.asa = ArbolSintaxisAbstracta() # falta definir la estructura del arbol


    # metodos
    def imprimirArbol(self):
        #imprime el arbol de sintaxis abstracta
        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimirPreorden()

    
    