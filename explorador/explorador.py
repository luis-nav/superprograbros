from enum import Enum, auto
import re

class TipoComponenteLexico(Enum):
    COMENTARIO = auto()
    ASIGNADOR = auto()
    PRINCIPAL = auto()
    FUNCION = auto()
    OPERADOR = auto()
    INVOCACION = auto()
    REPETICION = auto()
    # ERROR = auto()  NO HAY REGLA GRAMATICA PARA LOS ERRORES   
    SI = auto()
    #SINO = auto() # se juntan el if con el else
    RETORNO = auto()
    ENTERO = auto()
    FLOTANTE = auto()
    TEXTO = auto()
    IDENTIFICADOR = auto()
    VALOR_BOOLEANO = auto()
    COMPARADOR = auto()
    OPERADOR_BOOLEANO = auto()
    PUNTUACION = auto() # no entiendo muy bien su funcion de cara a la sintaxis
    BLANCOS = auto()
    #FIN_LINEA = auto() #creo que no hace falta, al tomar la linea del archivo en explorar nada mas vamos preguntando hasta que se encuentre [ ; ]
    #NO_IDENTIFICADO = auto()



class ComponenteLexico:
    def __init__(self, lexema, tipo, numeroLinea, numeroColumna, lineaCodigo):
        self.lexema = lexema
        self.tipo = tipo
        self.numeroLinea = numeroLinea
        self.numeroColumna = numeroColumna
        self.lineaCodigo = lineaCodigo

class Explorador:

    # Probar si r'[ ! ]' detecta correctamente la sintaxis sin el backslash si no cambiarlo por \[ \! \]
    descriptoresComponentes = [ (TipoComponenteLexico.COMENTARIO, r'^(\[ ! \]).*'),
            (TipoComponenteLexico.ASIGNADOR, r'^(\[ \? \])'),
            (TipoComponenteLexico.PRINCIPAL, r'^(juego)'),
            (TipoComponenteLexico.FUNCION, r'^(mundo)'),
            (TipoComponenteLexico.OPERADOR, r'^(\[ (\+|-|\*|/|) \])'),
            (TipoComponenteLexico.INVOCACION, r'^(ir a mundo)'),
            (TipoComponenteLexico.REPETICION, r'^(minijuego)'),
            (TipoComponenteLexico.SI, r'^(nivel|tubo)'), # se juntan el if con el else
            (TipoComponenteLexico.RETORNO, r'^(bandera)'), # se juntan el if con el else
            (TipoComponenteLexico.ENTERO, r'^(-?[0-9]+)'),
            (TipoComponenteLexico.FLOTANTE, r'^(-?[0-9]+\.[0-9]+)'),
            (TipoComponenteLexico.TEXTO, r'^(~.?[^~]*)~'),
            (TipoComponenteLexico.IDENTIFICADOR, r'^([a-z]([a-zA-z0-9])*)'),
            (TipoComponenteLexico.VALOR_BOOLEANO, r'^(peach|bowser)'),
            (TipoComponenteLexico.COMPARADOR, r'^(\[ (<>|><|>-|<-|^^|--) \]'),
            (TipoComponenteLexico.OPERADOR_BOOLEANO, r'\[ (&|\|) \]'), # backslash para usar el simbolo |
            (TipoComponenteLexico.PUNTUACION, r'^([/{}()])'),
            (TipoComponenteLexico.BLANCOS, r'^(\s)*')]


    def __init__(self, archivo):
        self.archivo = archivo
        self.componentes = []
        self.errores = []

    def __explorar(self):
        for linea in self.archivo:
            resultado = self.__procesarLinea(linea)
            self.componentes = self.componentes + resultado

    def __procesarLinea(self, linea):
        return