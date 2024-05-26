from io import TextIOWrapper
from analizador.arbolSintaxisAbstracta import ArbolSintaxisAbstracta
from generador.VisitanteArbol import VisitanteArbol

import random
class Generador:
    asa         :   ArbolSintaxisAbstracta
    visitante   :   VisitanteArbol

    ambienteEstandar = """import sys
import random
import time

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

def aplastarGoomba(txt, index, caracter):
    txt = txt[:index] + caracter + txt[index+1:]
    return txt

def bloque(inicio, fin):
    return random.randint(inicio,fin)

def wario(txt, caracter):
    return txt.index(caracter)

def pausa(segundos):
    time.sleep(segundos)
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

