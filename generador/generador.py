from io import TextIOWrapper
from analizador.arbolSintaxisAbstracta import ArbolSintaxisAbstracta
from generador.VisitanteArbol import VisitanteArbol

import random
class Generador:
    asa         :   ArbolSintaxisAbstracta
    visitante   :   VisitanteArbol

    ambienteEstandar = """import sys
import random

def champiñon(txt1, txt2):
    return txt1 + txt2

def moneda(txt, index):
    return txt[index]

def estrella(valor):
    print(valor)

def puntuacion(texto):
    return len(texto)

def vidaExtra(msj):
    entrada = input(msj)
    return entrada

def florFuego(ent1,ent2):
    return ent1%ent2

def yoshi(flt):
    return int(flt)

def daisy(caracter):
    return caracter.lower()
"""

    def __init__(self, asa: ArbolSintaxisAbstracta) -> None:
        self.asa = asa
        self.visitante = VisitanteArbol()

    def generar(self, nombre) -> TextIOWrapper:
        resultado = self.asa.raiz.visitar(self.visitante)
        file = open(nombre, "w")
        print(self.ambienteEstandar, file=file)
        print(resultado, file=file)
        return file

