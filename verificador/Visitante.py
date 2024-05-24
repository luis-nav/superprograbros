
from verificador.TablaSimbolos import TablaSimbolos
from analizador.arbolSintaxisAbstracta import NodoASA, TipoNodo
from utils.TipoDatos import TipoDatos

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
    

    def __visitarPrograma(self, nodoActual):
        """
        Programa ::= ((Comentario | Asignacion | Funcion)(\n|\s)*)* Principal
        """
        for nodo in nodoActual.nodos:
            # acá 'self' quiere decir que al método 'visitar' le paso el
            # objetto visitante que estoy usando (o sea, este mismo...
            # self)
            nodo.visitar(self)

    def __visitarAsignacion(self, nodoActual):
        """
        Asignación ::= Identificador [ ? ] (ExpresionMate | Invocación)  [ ; ]
        """
        # Se ingresa el identificador a la tabla de simbolos
        self.tablaSimbolos.incluir(nodoActual.nodos[0])

        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        # Si es una función verifico el tipo que retorna para incluirlo en
        # la asignación y si es un literal puedo anotar el tipo (TIPO) 

        nodoActual.atributos['tipo'] = nodoActual.nodos[1].atributos['tipo']

        nodoActual.nodos[0].atributos['tipo'] = nodoActual.nodos[1].atributos['tipo']

    def __visitarExpresionMatematica(self, nodoActual):
        """
        ExpresionMate ::= Valor | [Expresion]
        """
        for nodo in nodoActual.nodos:

            # Verifico que exista si es un identificador (IDENTIFICACIÓN)
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tablaSimbolos.buscar(nodo.contenido)

            nodo.visitar(self)

        # Anoto el tipo de datos 'NÚMERO' (TIPO)
        nodoActual.atributos['tipo'] = TipoDatos.NÚMERO

    def __visitarExpresion(self, nodoActual):
        """
        Expresion ::= ExpresionMate Operador ExpresionMate
        """
        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        # Anoto el tipo de datos 'NÚMERO' (TIPO)
        nodoActual.atributos['tipo'] = TipoDatos.NÚMERO

    def __visitarInvocacion(self, nodoActual):
        """
        Invocación ::= ir a mundo Identificador [Parámetros]
        """
        # Verificacion del identificador de la funcion
        registro = self.tablaSimbolos.buscar(nodoActual.nodos[0].contenido)

        if registro.obtenerReferencia().tipo != TipoNodo.FUNCIÓN:
            raise Exception('Es una variable', registro)

        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        # El tipo resultado de la invocación es el tipo inferido de una
        # función previamente definida
        nodoActual.atributos['tipo'] = registro.obtenerReferencia().atributos['tipo']

    def __visitarFuncion(self, nodoActual):
        """
        Funcion ::= mundo Identificador [ParametrosFunción](\n|\s)* BloqueInstrucciones
        """
        # Meto la función en la tabla de símbolos (IDENTIFICACIÓN)
        self.tablaSimbolos.nuevo_registro(nodoActual)

        self.tablaSimbolos.iniciarBloque()

        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        self.tablaSimbolos.cerrarBloque()

        # Anoto el tipo de retorno (TIPO)
        nodoActual.atributos['tipo'] = nodoActual.nodos[2].atributos['tipo']

    def __visitarParametrosFuncion(self, nodoActual):
        """
        ParametrosFunción ::= Identificador (,Identificador)*
        
        """
        for nodo in nodoActual.nodos:

            # Se verifica que el identificador exista
            self.tablaSimbolos.incluir(nodo)
            nodo.visitar(self)

    def __visitarParametrosInvocacion(self, nodoActual):
        """
        Parámetros ::= Valor (,Valor)*
        """
        for nodo in nodoActual.nodos:

            # Se busca en la tabla si es un identificador
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tablaSimbolos.buscar(nodo.contenido)

            elif nodo.tipo == TipoNodo.FUNCION:
                raise Exception('No se permitan funciones como parametros de invocacion de funcion', nodo.contenido) 

            # Si son otra cosa, simplemente se visitan
            nodo.visitar(self)

    def __visitarInstruccion(self, nodoActual):
        """
        Instrucción ::= ((Retorno | Error | Invocación)[ ; ] | Repetición | Bifurcación | Asignación | Comentario)(\n|\s)* 
        """

        for nodo in nodoActual.nodos:
            nodo.visitar(self)
            nodoActual.atributos['tipo'] = nodo.atributos['tipo']
    
