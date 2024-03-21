import re

from explorador.ComponenteLexico import ComponenteLexico, TipoComponenteLexico

class Explorador:

    descriptoresComponentes = []

    def __init__(self, archivo):
        self.archivo = archivo
        self.componentes = []
        self.errores = []

    def __explorar(self):
        counter = 1
        for linea in self.archivo:
            resultado = self.__procesarLinea(linea, counter)
            self.componentes = self.componentes + resultado
            counter += 1

    def __procesarLinea(self, linea, numeroLinea):
        componentes = []
    
        while (linea != ""):

            for tipoComponente, regex in self.descriptoresComponentes:

                respuesta = re.match(regex, linea)

                nuevoComponente = ComponenteLexico(respuesta.group(), tipoComponente, numeroLinea, respuesta.span[0])

                # Si se encuentra algo diferente a un comentario o espacios agrega el componente lexico
                if tipoComponente is not TipoComponenteLexico.COMENTARIO and tipoComponente is not TipoComponenteLexico.BLANCOS:
                    componentes.append(nuevoComponente)

                # Si no identifico ningun patron y la linea no esta vacia es un error
                # Deja de explorar la linea actual y sigue con la siguiente para buscar mas errores
                if tipoComponente is TipoComponenteLexico.NO_IDENTIFICADO:
                    self.errores.append(nuevoComponente)
                    return componentes

                linea = linea[respuesta.end():]
                break;

        return componentes
