import re
import sys

from ComponenteLexico import ComponenteLexico, TipoComponenteLexico

class Explorador:

    descriptoresComponentes = descriptoresComponentes = [ 
        (TipoComponenteLexico.COMENTARIO, r'^(\[ ! \]).*'),
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
            (TipoComponenteLexico.TEXTO, r'\".*\"'), # CORRECION
            (TipoComponenteLexico.VALOR_BOOLEANO, r'^(peach|bowser)'),
            (TipoComponenteLexico.COMPARADOR, r'^(\[ (<>|><|>-|<-|^^|--) \]'), # CORRECCION
            (TipoComponenteLexico.OPERADOR_BOOLEANO, r'\[ (&|\|) \]'), # backslash para usar el simbolo |
            (TipoComponenteLexico.PUNTUACION, r'^(\[|\]|\{|\})'), # CORRECCION
            (TipoComponenteLexico.IDENTIFICADOR, r'^([a-z]([a-zA-z0-9])*)'),
            (TipoComponenteLexico.BLANCOS, r'^(\s)*'),
            (TipoComponenteLexico.NO_IDENTIFICADO, r'.*')]

    def __init__(self, archivo):
        self.archivo = archivo
        self.componentes = []
        self.errores = []
        self.__explorar()

    def __explorar(self):
        counter = 1
        for linea in self.archivo:
            resultado = self.__procesarLinea(linea, counter)
            self.componentes = self.componentes + resultado
            counter += 1

        if (len(self.errores) != 0):
            self.__imprimirErrores()
            return False
        else:
            self.__imprimirComponentes()
            return True

    def __procesarLinea(self, linea, numeroLinea):
        componentes = []
    
        while (linea != ""):

            print(linea)
            for tipoComponente, regex in self.descriptoresComponentes:

                respuesta = re.match(regex, linea)

                if respuesta == None:
                    continue
                    
                    
                nuevoComponente = ComponenteLexico(respuesta.group(), tipoComponente, numeroLinea, respuesta.start, linea)


                # Si se encuentra algo diferente a un comentario o espacios agrega el componente lexico
                if tipoComponente is not TipoComponenteLexico.COMENTARIO and tipoComponente is not TipoComponenteLexico.BLANCOS:
                    componentes.append(nuevoComponente)

                # Si no identifico ningun patron y la linea no esta vacia es un error
                # Deja de explorar la linea actual y sigue con la siguiente para buscar mas errores
                if tipoComponente is TipoComponenteLexico.NO_IDENTIFICADO:
                    self.errores.append(nuevoComponente)
                    return componentes

                linea = linea[respuesta.end():]
                break

        return componentes
    
    def __imprimirComponentes(self):
        for componente in self.componentes:
            print(componente)

    def __imprimirErrores(self):
        for error in self.errores:
            print(error.errorStr())


# Entrada programa
if __name__ == "__main__":
    archivo = open("prueba.bros", "r")
    Explorador(archivo)
    # try:
    #     archivo = open("prueba.bros", "r")
    #     Explorador(archivo)

    # except:
    #     if (len(sys.argv) == 1):
    #         print("[Error]: Debe seleccionar un archivo")
    #     else:
    #         print("[Error]: No se pudo abrir el archivo")