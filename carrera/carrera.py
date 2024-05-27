import sys
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


def yaGano(strJuego,final):

    caracter = moneda(strJuego,final)
    
    print("""
            \033[94mS\033[93mU\033[91mP\033[92mE\033[93mR \033[91mP\033[92mR\033[93mO\033[91mG\033[92mR\033[94mA \033[91mB\033[93mR\033[96mO\033[92mS\033[0m - \033[1m¡HORA DE DESICIÓN!\033[0m
              
\033[93m            caracter == "o"
              
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
    if ((__spbUsrInput == "peach" and caracter == "o") or (__spbUsrInput == "bowser" and not caracter == "o")):
       print("\n\n\n\n\n\n\n\n\n\n\n\n¡Tamos gucci! 😎👍")
    else:
       raise Exception("\033[91m¡Has decidido la opcion incorrecta!\033[0m 😒")
    if caracter == "o":

        return True
    else:

        return False

def movimiento(strJuego,pasosMaximos):

    pasos = bloque(0,pasosMaximos)
    largo = puntuacion(strJuego)
    ubicacion = wario(strJuego,"o")
    ubicacionFinal = pasos + ubicacion
    
    print("""
            \033[94mS\033[93mU\033[91mP\033[92mE\033[93mR \033[91mP\033[92mR\033[93mO\033[91mG\033[92mR\033[94mA \033[91mB\033[93mR\033[96mO\033[92mS\033[0m - \033[1m¡HORA DE DESICIÓN!\033[0m
              
\033[93m            ubicacionFinal >= largo
              
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
    if ((__spbUsrInput == "peach" and ubicacionFinal >= largo) or (__spbUsrInput == "bowser" and not ubicacionFinal >= largo)):
       print("\n\n\n\n\n\n\n\n\n\n\n\n¡Tamos gucci! 😎👍")
    else:
       raise Exception("\033[91m¡Has decidido la opcion incorrecta!\033[0m 😒")
    if ubicacionFinal >= largo:

        ubicacionFinal = largo - 1

    strJuego = aplastarGoomba(strJuego,ubicacion,"=")
    strJuego = aplastarGoomba(strJuego,ubicacionFinal,"o")
    return strJuego

def principal():

    pasosMaximos = 2
    pista1 = "===F"
    pista2 = "===F"
    caracol1 = "o"
    caracol2 = "o"
    strJuego1 = champiñon(caracol1,pista1)
    strJuego2 = champiñon(caracol2,pista2)
    estrella(strJuego1)
    estrella(strJuego2)
    yaGano1 = yaGano(strJuego1,4)
    yaGano2 = yaGano(strJuego2,4)
    
    print("""
            \033[94mS\033[93mU\033[91mP\033[92mE\033[93mR \033[91mP\033[92mR\033[93mO\033[91mG\033[92mR\033[94mA \033[91mB\033[93mR\033[96mO\033[92mS\033[0m - \033[1m¡HORA DE DESICIÓN!\033[0m
              
\033[93m            yaGano2 == False
              
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
    if ((__spbUsrInput == "peach" and yaGano2 == False) or (__spbUsrInput == "bowser" and not yaGano2 == False)):
       print("\n\n\n\n\n\n\n\n\n\n\n\n¡Tamos gucci! 😎👍")
    else:
       raise Exception("\033[91m¡Has decidido la opcion incorrecta!\033[0m 😒")
    while yaGano2 == False:

        strJuego1 = movimiento(strJuego1,pasosMaximos)
        estrella("Caracol 1:")
        estrella(strJuego1)
        pausa(1)
        yaGano1 = yaGano(strJuego1,4)
        
        print("""
            \033[94mS\033[93mU\033[91mP\033[92mE\033[93mR \033[91mP\033[92mR\033[93mO\033[91mG\033[92mR\033[94mA \033[91mB\033[93mR\033[96mO\033[92mS\033[0m - \033[1m¡HORA DE DESICIÓN!\033[0m
              
\033[93m            yaGano1 == True
              
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
        if ((__spbUsrInput == "peach" and yaGano1 == True) or (__spbUsrInput == "bowser" and not yaGano1 == True)):
           print("\n\n\n\n\n\n\n\n\n\n\n\n¡Tamos gucci! 😎👍")
        else:
           raise Exception("\033[91m¡Has decidido la opcion incorrecta!\033[0m 😒")
        if yaGano1 == True:

            estrella("Ha ganado el caracol 1!")
            return 

        strJuego2 = movimiento(strJuego2,pasosMaximos)
        estrella("Caracol 2:")
        estrella(strJuego2)
        pausa(1)
        yaGano2 = yaGano(strJuego2,4)
        print("""
            \033[94mS\033[93mU\033[91mP\033[92mE\033[93mR \033[91mP\033[92mR\033[93mO\033[91mG\033[92mR\033[94mA \033[91mB\033[93mR\033[96mO\033[92mS\033[0m - \033[1m¡HORA DE DESICIÓN!\033[0m
              
\033[93m            yaGano2 == False
              
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
        if ((__spbUsrInput == "peach" and yaGano2 == False) or (__spbUsrInput == "bowser" and not yaGano2 == False)):
           print("\n\n\n\n\n\n\n\n\n\n\n\n¡Tamos gucci! 😎👍")
        else:
           raise Exception("\033[91m¡Has decidido la opcion incorrecta!\033[0m 😒")
    estrella("Ha ganado el caracol 2!")


if __name__ == '__main__':
    principal()

