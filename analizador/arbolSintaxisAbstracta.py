from enum import Enum, auto

class TipoNodo(Enum):
    #Enumerable con todos los tipos de tokens en la gramatica
    PROGRAMA = auto()
    ASIGNACION = auto()
    EXPRESION_MATEMATICA = auto()
    EXPRESION = auto()
    INVOCACION = auto()
    FUNCION = auto()
    PARAMETROS_FUNCION = auto()
    IDENTIFICADOR = auto()
    PARAMETROS_INVOCACION = auto()
    INSTRUCCION = auto()
    REPETICION = auto()
    BIFURCACION = auto()
    SI = auto()
    SINO = auto()
    RETORNO = auto()
    CONDICION = auto()
    BLOQUE_CONDICIONES = auto()
    COMPARACION = auto()
    OPERADOR_BOOLEANO = auto()
    ERROR = auto()
    PRINCIPAL = auto()
    BLOQUE_INSTRUCCIONES = auto()
    FLOTANTE = auto()
    ENTERO = auto()
    COMPARADOR = auto()
    VALOR_BOOLEANO = auto()
    ASIGNADOR = auto()
    OPERADOR = auto()
    TEXTO = auto()


class NodoASA:
    """
    Clase que representa un nodo generico del ASA.
    Cada nodo puede tener n nodos hijos y tiene su componente lexico con la informacion de error
    """
    tipo : TipoNodo
    contenido : str
    errorInfo : dict
    hijos : list

    def __init__(self, tipo, contenido = None, nodos = [], errorInfo = {}):
        self.tipo = tipo
        self.contenido = contenido
        self.nodos = nodos
        self.errorInfo = errorInfo

    def visitar(self, visitador):
        return visitador.visitar(self)
    
    def __str__(self):

        # Coloca la información del nodo
        resultado = '{:30}\t'.format(self.tipo)
        
        if self.contenido is not None:
            resultado += '{:10}\t'.format(self.contenido)
        else:
            resultado += '{:10}\t'.format('')

        resultado += '\n\t'
        if self.errorInfo != {}:
            resultado += '{:38}'.format(str(self.errorInfo))
        else:
            resultado += '{:38}\t'.format('')

        if self.nodos != []:
            resultado += '\n\t'
            resultado += '<'

            # Imprime los tipos de los nodos del nivel siguiente
            for nodo in self.nodos[:-1]:
                if nodo is not None:
                    resultado += '{},'.format(nodo.tipo)

            resultado += '{}'.format(self.nodos[-1].tipo)
            resultado += '>'

        return resultado


class ArbolSintaxisAbstracta:
    """
    Clase que representa el ASA. Guarda referencia a la raiz y imprime recursivamente los nodos
    """
    raiz : NodoASA

    def imprimirPreorden(self):
        self.__imprimirPreordenAux(self.raiz)

    def __imprimirPreordenAux(self, nodo):
        print(nodo, end='\n\n\n')

        if nodo is not None:
            for nodoHijo in nodo.nodos:
                self.__imprimirPreordenAux(nodoHijo)
