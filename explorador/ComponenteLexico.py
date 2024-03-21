from enum import Enum, auto

class TipoComponenteLexico(Enum):
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
    PUNTACION = auto()
    BLANCOS = auto()
    FIN_LINEA = auto()
    NO_IDENTIFICADO = auto()

    



class ComponenteLexico:
    def __init__(self, lexema, tipo, numeroLinea, numeroColumna, lineaCodigo):
        self.lexema = lexema
        self.tipo = tipo
        self.numeroLinea = numeroLinea
        self.numeroColumna = numeroColumna
        self.lineaCodigo = lineaCodigo