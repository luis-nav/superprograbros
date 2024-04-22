import re

from explorador.ComponenteLexico import ComponenteLexico, TipoComponenteLexico


class Explorador:

    descriptoresComponentes = [ 
        (TipoComponenteLexico.COMENTARIO, r'^(\[ ! \]).*'),
            (TipoComponenteLexico.ASIGNADOR, r'(\[ \? \])'),
            (TipoComponenteLexico.PRINCIPAL, r'^(juego)'),
            (TipoComponenteLexico.FUNCION, r'^(mundo)'),
            (TipoComponenteLexico.OPERADOR, r'(\[ (\+|-|\*|\/|) \])'),
            (TipoComponenteLexico.INVOCACION, r'^(ir a mundo)'),
            (TipoComponenteLexico.REPETICION, r'^(minijuego)'),
            (TipoComponenteLexico.SI, r'^(nivel|tubo)'), # se juntan el if con el else
            (TipoComponenteLexico.RETORNO, r'^(bandera)'), 
            (TipoComponenteLexico.ENTERO, r'(-?[0-9]+)'),
            (TipoComponenteLexico.FLOTANTE, r'(-?[0-9]+\.[0-9]+)'),
            (TipoComponenteLexico.TEXTO, r'\"[^\"]*\"'),
            (TipoComponenteLexico.VALOR_BOOLEANO, r'(peach|bowser)'),
            (TipoComponenteLexico.COMPARADOR, r'\[ (<>|><|>-|<-|\^\^|--) \]'),
            (TipoComponenteLexico.OPERADOR_BOOLEANO, r'\[ (&|\|) \]'),
            (TipoComponenteLexico.FIN_INSTRUCCION, r'\[ ; \]'), 
            (TipoComponenteLexico.PUNTUACION, r'\[|\]|\(|\)|\{|\}|\,'),
            (TipoComponenteLexico.IDENTIFICADOR, r'[a-zA-Z][a-zA-Z0-9]*'),
            (TipoComponenteLexico.BLANCOS, r'(\s)+'),
            (TipoComponenteLexico.NO_IDENTIFICADO, r'.*')]


    def __init__(self, archivo):
        # Constructor del Explorador: Cuenta con un archivo, la lista de componentes y la lista de componentes que dan error
        self.archivo = archivo
        self.componentes = []
        self.errores = []

    def explorar(self):
        # Se encarga de recorrer todas las lineas del archivo y ejecutar la funcion procesarLinea
        # Al final, si encuentra errores, los imprime y devuelve false. En caso de exito, solo imprime los tokens
        counter = 1
        for linea in self.archivo:
            resultado = self.__procesarLinea(linea, counter)
            self.componentes = self.componentes + resultado
            counter += 1

        if (len(self.errores) != 0):
            self.__imprimirErrores()
            return False
        return True

    def __procesarLinea(self, linea, numeroLinea):
        # Procesa la linea N veces comparandola con los tipos de componentes lexicos.
        # En caso de que algun componente lexico no sea identificado lo annade a los errores y salta a la siguiente linea
        # Ignora comentarios y espacios en blanco.
        lineaCompleta = linea
        componentes = []
    
        while (linea != ""):

            for tipoComponente, regex in self.descriptoresComponentes:

                respuesta = re.match(regex, linea)

                if respuesta == None:
                    continue

                nuevoComponente = ComponenteLexico(respuesta.group(), tipoComponente, numeroLinea, lineaCompleta.find(respuesta.group()), lineaCompleta)

                # Si no identifico ningun patron y la linea no esta vacia es un error
                # Deja de explorar la linea actual y sigue con la siguiente para buscar mas errores
                # Debe ir antes ya que no es un comentario ni blancos
                if tipoComponente is TipoComponenteLexico.NO_IDENTIFICADO:
                    self.errores.append(nuevoComponente)
                    return componentes
                

                # Si se encuentra algo diferente a un comentario o espacios agrega el componente lexico
                if tipoComponente is not TipoComponenteLexico.COMENTARIO and tipoComponente is not TipoComponenteLexico.BLANCOS:
                    componentes.append(nuevoComponente)


                linea = linea[respuesta.end():]
                break

        return componentes
    
    def imprimirComponentes(self):
        # Imprime los componentes
        for componente in self.componentes:
            print(componente.toString())

    def __imprimirErrores(self):
        # Imprime los errores usando la representacion de componente de error de string
        for error in self.errores:
            print(error.errorStr())


# Entrada programa
if __name__ == "__main__":
    # print("Estamos en: " + os.getcwd())
    # archivo = open(os.getcwd() + "\explorador\prueba.bros", "r", encoding="utf-8")
    archivo = open("explorador\pruebasErrores.bros", "r", encoding="utf-8")
    Explorador(archivo)

    # try:
    #     archivo = open("prueba.bros", "r")
    #     Explorador(archivo)

    # except:
    #   # Si hay algun error al abrir el archivo o en el explorador da el mensaje de error
    #     if (len(sys.argv) == 1):
    #         print("[Error]: Debe seleccionar un archivo")
    #     else:
    #         print("[Error]: No se pudo abrir el archivo")