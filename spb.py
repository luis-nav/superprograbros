from utils import cargar_archivo
from explorador.explorador import Explorador
from analizador.analizador import Analizador

import argparse

# argparse config
parser = argparse.ArgumentParser(description='Transpilador para el lenguaje SuperPrograBros')

parser.add_argument('--solo-explorar', dest='explorador', action='store_true', 
        help='ejecuta solo el explorador y retorna una lista de componentes léxicos')

parser.add_argument('--solo-analizar', dest='analizador', action='store_true', 
        help='ejecuta hasta el analizador y retorna un preorden del árbol sintáctico')

parser.add_argument('--solo-verificar', dest='verificador', action='store_true', 
        help='''ejecuta hasta el verificador y retorna un preorden del árbol
        sintáctico y estructuras de apoyo generadas en la verificación''')

parser.add_argument('--generar-python', dest='python', action='store_true', 
        help='''Genera código python''')

parser.add_argument('archivo',
        help='Archivo de código fuente')

def SuperPrograBros():
    """
    Funcion que se encarga de correr el transpilador de spb segun las configuraciones dadas en los args del programa
    """
    args = parser.parse_args()

    if args.explorador == True:
        archivo = cargar_archivo(args.archivo)

        explorador = Explorador(archivo)
        res_valida_explorador = explorador.explorar()
        if (not res_valida_explorador):
            return
        explorador.imprimirComponentes()

    elif args.analizador == True:
        archivo = cargar_archivo(args.archivo)

        explorador = Explorador(archivo)
        res_valida_explorador = explorador.explorar()
        if (not res_valida_explorador):
            return
        analizador = Analizador(explorador.componentes)

    elif args.verificador == True:
        print("Error: No implementado")

    elif args.python == True:
        print("Error: No implementado")

    else:
        parser.print_help()


if __name__ == "__main__":
    SuperPrograBros()
    
