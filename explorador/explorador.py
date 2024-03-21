

class Explorador:

    descriptoresComponentes = []

    def __init__(self, archivo):
        self.archivo = archivo
        self.componentes = []
        self.errores = []

    def __explorar(self):
        for linea in self.archivo:
            resultado = self.__procesarLinea(linea)
            self.componentes = self.componentes + resultado

    def __procesarLinea(self, linea):
