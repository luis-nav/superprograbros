from enum import Enum, auto

class TipoComponenteLexico(Enum):
    #Enumerable con todos los tipos de tokens en la gramatica
    COMENTARIO = auto()
    ASIGNADOR = auto()
    PRINCIPAL = auto()
    FUNCION = auto()
    OPERADOR = auto()
    INVOCACION = auto()
    REPETICION = auto()
    ERROR = auto()
    SI = auto()
    SINO = auto()
    RETORNO = auto()
    ENTERO = auto()
    FLOTANTE = auto()
    TEXTO = auto()
    IDENTIFICADOR = auto()
    VALOR_BOOLEANO = auto()
    COMPARADOR = auto()
    OPERADOR_BOOLEANO = auto()
    PUNTUACION = auto()
    BLANCOS = auto()
    FIN_INSTRUCCION = auto()
    NO_IDENTIFICADO = auto()


class ComponenteLexico:
    def __init__(self, lexema, tipo, numeroLinea, numeroColumna, lineaCodigo):
        #Constructor de un componente lexico.
        #Guarda el numero de linea, numero de columna y la linea de codigo para mensajes de error.
        self.lexema = lexema
        self.tipo = tipo
        self.numeroLinea = numeroLinea
        self.numeroColumna = numeroColumna
        self.lineaCodigo = lineaCodigo

    def toString(self):
        #Devuelve el lexema y el tipo de componente cuando se le pida a la clase ComponenteLexico su representacion como string
        return f"<{self.lexema}> : {self.tipo:30}"
    
    def errorStr(self):
        #Devuelve un string con los detalles de error de un lexema no identificado
        return f"[Error]: Token <{self.lexema}> no identificado en la linea {self.numeroLinea}, columna {self.numeroColumna}\n--->\t{self.lineaCodigo}\n"