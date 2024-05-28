from generador.generador import Generador
from utils.utils import cargarArchivo
from explorador.explorador import Explorador
from analizador.analizador import Analizador
from verificador.Verificador import Verificador

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
        archivo = cargarArchivo(args.archivo)

        explorador = Explorador(archivo)
        res_valida_explorador = explorador.explorar()
        if (not res_valida_explorador):
            return
        explorador.imprimirComponentes()

    elif args.analizador == True:
        archivo = cargarArchivo(args.archivo)

        explorador = Explorador(archivo)
        res_valida_explorador = explorador.explorar()
        if (not res_valida_explorador):
            return
        analizador = Analizador(explorador.componentes)
        analizador.analizar()
        if not analizador.error:
            analizador.imprimirArbol()

    elif args.verificador == True:
        archivo = cargarArchivo(args.archivo)

        explorador = Explorador(archivo)
        res_valida_explorador = explorador.explorar()
        if (not res_valida_explorador):
            return
        analizador = Analizador(explorador.componentes)
        analizador.analizar()
        if not analizador.error:
            # Limpia el archivo de salida
            f = open("salida.txt", "w")
            f.write("")
            f.close()
            
            # Verificador
            verificador = Verificador(analizador.asa)
            verificador.verificar()

            verificador.imprimirAsa()

    elif args.python == True:
        archivo = cargarArchivo(args.archivo)

        explorador = Explorador(archivo)
        res_valida_explorador = explorador.explorar()
        if (not res_valida_explorador):
            return
        analizador = Analizador(explorador.componentes)
        analizador.analizar()
        if analizador.error:
            return
        
        # Verificador
        verificador = Verificador(analizador.asa)
        verificador.verificar()


        generador = Generador(analizador.asa)
        # Nombre y ubicacion del nuevo archivo
        indice = args.archivo.rfind(".")
        nombre = args.archivo[:indice+1] + "py"
        generador.generar(nombre)
        print("Se ha generado el archivo en ", nombre)

    else:
        parser.print_help()


if __name__ == "__main__":
    SuperPrograBros()
    
