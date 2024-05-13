
from verificador.TablaSimbolos import TablaSimbolos
from analizador.arbolSintaxisAbstracta import ArbolSintaxisAbstracta, NodoASA, TipoNodo

class Visitante:

    tablaSimbolos: TablaSimbolos

    def __init__(self, nuevaTablaSimbolos):
        self.tablaSimbolos = nuevaTablaSimbolos

    def visitar(self, nodo :NodoASA):
        """
        Es necesario ya que todos los nodos son del mismo tipo en el arbol
        """
        # -------------------- JOHN -------------------------
        if nodo.tipo is TipoNodo.PROGRAMA:
            self.__visitarPrograma(nodo)

        elif nodo.tipo is TipoNodo.ASIGNACION:
            self.__visitarAsignacion(nodo)

        elif nodo.tipo is TipoNodo.EXPRESION_MATEMATICA:
            self.__visitarExpresionMatematica(nodo)

        elif nodo.tipo is TipoNodo.EXPRESION:
            self.__visitarExpresion(nodo)

        elif nodo.tipo is TipoNodo.INVOCACION:
            self.__visitarInvocacion(nodo)

        elif nodo.tipo is TipoNodo.FUNCION:
            self.__visitarFuncion(nodo)

        elif nodo.tipo is TipoNodo.PARAMETROS_FUNCION:
            self.__visitarParametrosFuncion(nodo)

        elif nodo.tipo is TipoNodo.PARAMETROS_INVOCACION:
            self.__visitarParametrosInvocacion(nodo)

        elif nodo.tipo is TipoNodo.INSTRUCCION:
            self.__visitarInstruccion(nodo)

        # -------------------- Vicky  -------------------------
        elif nodo.tipo is TipoNodo.BLOQUE_INSTRUCCIONES:
            self.__visitarBloqueInstrucciones(nodo)

        elif nodo.tipo is TipoNodo.REPETICION:
            self.__visitarRepeticion(nodo)

        elif nodo.tipo is TipoNodo.BIFURCACION:
            self.__visitarBifurcacion(nodo)

        elif nodo.tipo is TipoNodo.SI:
            self.__visitarSi(nodo)

        elif nodo.tipo is TipoNodo.SINO:
            self.__visitarSiNo(nodo)

        elif nodo.tipo is TipoNodo.RETORNO:
            self.__visitarRetorno(nodo)

        elif nodo.tipo is TipoNodo.CONDICION:
            self.__visitarCondicion(nodo)

        elif nodo.tipo is TipoNodo.BLOQUE_CONDICIONES:
            self.__visitarBloqueCondiciones(nodo)

        elif nodo.tipo is TipoNodo.COMPARACION:
            self.__visitarComparacion(nodo)

        elif nodo.tipo is TipoNodo.OPERADOR_BOOLEANO:
            self.__visitarOperadorBooleano(nodo)

        # -------------------- Hytan  -------------------------
        elif nodo.tipo is TipoNodo.ERROR:
            self.__visitarError(nodo)
            
        elif nodo.tipo is TipoNodo.ASIGNADOR:
            self.__visitarAsignador(nodo)

        elif nodo.tipo is TipoNodo.OPERADOR:
            self.__visitarOperador(nodo)
            
        elif nodo.tipo is TipoNodo.PRINCIPAL:
            self.__visitarPrincipal(nodo)
            
        elif nodo.tipo is TipoNodo.IDENTIFICADOR:
            self.__visitarIdentificador(nodo)

        elif nodo.tipo is TipoNodo.ENTERO:
            self.__visitarEntero(nodo)
            
        elif nodo.tipo is TipoNodo.FLOTANTE:
            self.__visitarFlotante(nodo)

        elif nodo.tipo is TipoNodo.COMPARADOR:
            self.__visitarComparador(nodo)

        elif nodo.tipo is TipoNodo.VALOR_BOOLEANO:
            self.__visitarValorBooleano(nodo)

        elif nodo.tipo is TipoNodo.TEXTO:
            self.__visitarTexto(nodo)

        else:
            raise Exception('Tipo de nodo no existe')
