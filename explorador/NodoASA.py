from enum import Enum

class TipoNodo(Enum):
    pass

class ComponenteLexico:
    def __init__(self, lexema, tipo, numeroLinea, numeroColumna, lineaCodigo):
        self.lexema = lexema
        self.tipo = tipo
        self.numeroLinea = numeroLinea
        self.numeroColumna = numeroColumna
        self.lineaCodigo = lineaCodigo