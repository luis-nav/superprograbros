import sys
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


def esConsonante(caracter):

    consonantes = "bcdfghjklmnpqrstvwxyz"
    cantCons = puntuacion(consonantes)
    indice = 0
    
    print("""
            \033[94mS\033[93mU\033[91mP\033[92mE\033[93mR \033[91mP\033[92mR\033[93mO\033[91mG\033[92mR\033[94mA \033[91mB\033[93mR\033[96mO\033[92mS\033[0m - \033[1m¡HORA DE DESICIÓN!\033[0m
              
\033[93m            indice < cantCons
              
\033[92m    _________                                     _________
\033[92m    |       |                                     |       |
\033[92m      |   |                                         |   |
\033[92m      |   |                                         |   |
\033[92m      |   |                                         |   |
      \033[92mpeach\033[0m                                         \033[91mbowser\033[0m
    (verdadera)                                    (falsa)

""")
    __spbUsrInput = input("La condicion va para \033[92mpeach\033[0m o para \033[91mbowser\033[0m: ")
    while (__spbUsrInput != "peach" and __spbUsrInput != "bowser"):
       __spbUsrInput = input("La condicion va para \033[92mpeach\033[0m o para \033[91mbowser\033[0m: ")
    if ((__spbUsrInput == "peach" and indice < cantCons) or (__spbUsrInput == "bowser" and indice < cantCons)):
       print("\n\n\n\n\n\n\n\n\n\n\n\n¡Tamos gucci! 😎👍")
    else:
       raise Exception("\033[91m¡Has decidido la opcion incorrecta!\033[0m 😒")
    while indice < cantCons:

        consonanteActual = moneda(consonantes,indice)
        
        print("""
            \033[94mS\033[93mU\033[91mP\033[92mE\033[93mR \033[91mP\033[92mR\033[93mO\033[91mG\033[92mR\033[94mA \033[91mB\033[93mR\033[96mO\033[92mS\033[0m - \033[1m¡HORA DE DESICIÓN!\033[0m
              
\033[93m            consonanteActual == caracter
              
\033[92m    _________                                     _________
\033[92m    |       |                                     |       |
\033[92m      |   |                                         |   |
\033[92m      |   |                                         |   |
\033[92m      |   |                                         |   |
      \033[92mpeach\033[0m                                         \033[91mbowser\033[0m
    (verdadera)                                    (falsa)

""")
        __spbUsrInput = input("La condicion va para \033[92mpeach\033[0m o para \033[91mbowser\033[0m: ")
        while (__spbUsrInput != "peach" and __spbUsrInput != "bowser"):
           __spbUsrInput = input("La condicion va para \033[92mpeach\033[0m o para \033[91mbowser\033[0m: ")
        if ((__spbUsrInput == "peach" and consonanteActual == caracter) or (__spbUsrInput == "bowser" and consonanteActual == caracter)):
           print("\n\n\n\n\n\n\n\n\n\n\n\n¡Tamos gucci! 😎👍")
        else:
           raise Exception("\033[91m¡Has decidido la opcion incorrecta!\033[0m 😒")
        if consonanteActual == caracter:

            return True

        indice = indice + 1
        print("""
            \033[94mS\033[93mU\033[91mP\033[92mE\033[93mR \033[91mP\033[92mR\033[93mO\033[91mG\033[92mR\033[94mA \033[91mB\033[93mR\033[96mO\033[92mS\033[0m - \033[1m¡HORA DE DESICIÓN!\033[0m
              
\033[93m            indice < cantCons
              
\033[92m    _________                                     _________
\033[92m    |       |                                     |       |
\033[92m      |   |                                         |   |
\033[92m      |   |                                         |   |
\033[92m      |   |                                         |   |
      \033[92mpeach\033[0m                                         \033[91mbowser\033[0m
    (verdadera)                                    (falsa)

""")
        __spbUsrInput = input("La condicion va para \033[92mpeach\033[0m o para \033[91mbowser\033[0m: ")
        while (__spbUsrInput != "peach" and __spbUsrInput != "bowser"):
           __spbUsrInput = input("La condicion va para \033[92mpeach\033[0m o para \033[91mbowser\033[0m: ")
        if ((__spbUsrInput == "peach" and indice < cantCons) or (__spbUsrInput == "bowser" and indice < cantCons)):
           print("\n\n\n\n\n\n\n\n\n\n\n\n¡Tamos gucci! 😎👍")
        else:
           raise Exception("\033[91m¡Has decidido la opcion incorrecta!\033[0m 😒")
    return False

def cantidadConsonantes(palabra):

    largoPalabra = puntuacion(palabra)
    indice = 0
    contador = 0
    
    print("""
            \033[94mS\033[93mU\033[91mP\033[92mE\033[93mR \033[91mP\033[92mR\033[93mO\033[91mG\033[92mR\033[94mA \033[91mB\033[93mR\033[96mO\033[92mS\033[0m - \033[1m¡HORA DE DESICIÓN!\033[0m
              
\033[93m            indice < largoPalabra
              
\033[92m    _________                                     _________
\033[92m    |       |                                     |       |
\033[92m      |   |                                         |   |
\033[92m      |   |                                         |   |
\033[92m      |   |                                         |   |
      \033[92mpeach\033[0m                                         \033[91mbowser\033[0m
    (verdadera)                                    (falsa)

""")
    __spbUsrInput = input("La condicion va para \033[92mpeach\033[0m o para \033[91mbowser\033[0m: ")
    while (__spbUsrInput != "peach" and __spbUsrInput != "bowser"):
       __spbUsrInput = input("La condicion va para \033[92mpeach\033[0m o para \033[91mbowser\033[0m: ")
    if ((__spbUsrInput == "peach" and indice < largoPalabra) or (__spbUsrInput == "bowser" and indice < largoPalabra)):
       print("\n\n\n\n\n\n\n\n\n\n\n\n¡Tamos gucci! 😎👍")
    else:
       raise Exception("\033[91m¡Has decidido la opcion incorrecta!\033[0m 😒")
    while indice < largoPalabra:

        char = moneda(palabra,indice)
        lowerChar = daisy(char)
        isConsonante = esConsonante(lowerChar)
        
        print("""
            \033[94mS\033[93mU\033[91mP\033[92mE\033[93mR \033[91mP\033[92mR\033[93mO\033[91mG\033[92mR\033[94mA \033[91mB\033[93mR\033[96mO\033[92mS\033[0m - \033[1m¡HORA DE DESICIÓN!\033[0m
              
\033[93m            isConsonante == True
              
\033[92m    _________                                     _________
\033[92m    |       |                                     |       |
\033[92m      |   |                                         |   |
\033[92m      |   |                                         |   |
\033[92m      |   |                                         |   |
      \033[92mpeach\033[0m                                         \033[91mbowser\033[0m
    (verdadera)                                    (falsa)

""")
        __spbUsrInput = input("La condicion va para \033[92mpeach\033[0m o para \033[91mbowser\033[0m: ")
        while (__spbUsrInput != "peach" and __spbUsrInput != "bowser"):
           __spbUsrInput = input("La condicion va para \033[92mpeach\033[0m o para \033[91mbowser\033[0m: ")
        if ((__spbUsrInput == "peach" and isConsonante == True) or (__spbUsrInput == "bowser" and isConsonante == True)):
           print("\n\n\n\n\n\n\n\n\n\n\n\n¡Tamos gucci! 😎👍")
        else:
           raise Exception("\033[91m¡Has decidido la opcion incorrecta!\033[0m 😒")
        if isConsonante == True:

            contador = contador + 1

        indice = indice + 1
        print("""
            \033[94mS\033[93mU\033[91mP\033[92mE\033[93mR \033[91mP\033[92mR\033[93mO\033[91mG\033[92mR\033[94mA \033[91mB\033[93mR\033[96mO\033[92mS\033[0m - \033[1m¡HORA DE DESICIÓN!\033[0m
              
\033[93m            indice < largoPalabra
              
\033[92m    _________                                     _________
\033[92m    |       |                                     |       |
\033[92m      |   |                                         |   |
\033[92m      |   |                                         |   |
\033[92m      |   |                                         |   |
      \033[92mpeach\033[0m                                         \033[91mbowser\033[0m
    (verdadera)                                    (falsa)

""")
        __spbUsrInput = input("La condicion va para \033[92mpeach\033[0m o para \033[91mbowser\033[0m: ")
        while (__spbUsrInput != "peach" and __spbUsrInput != "bowser"):
           __spbUsrInput = input("La condicion va para \033[92mpeach\033[0m o para \033[91mbowser\033[0m: ")
        if ((__spbUsrInput == "peach" and indice < largoPalabra) or (__spbUsrInput == "bowser" and indice < largoPalabra)):
           print("\n\n\n\n\n\n\n\n\n\n\n\n¡Tamos gucci! 😎👍")
        else:
           raise Exception("\033[91m¡Has decidido la opcion incorrecta!\033[0m 😒")
    return contador

def principal():

    cantidadConsonantes("palabra")


if __name__ == '__main__':
    principal()

