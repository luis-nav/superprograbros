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
    PUNTUACION = auto()
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

    def __str__(self):
        return f"<{self.lexema}> : {self.tipo:30}"
    
    def errorStr(self):
        return f"[Error]: Token <{self.lexema}> no identificado"