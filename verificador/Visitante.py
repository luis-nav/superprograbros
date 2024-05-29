
from verificador.TablaSimbolos import TablaSimbolos
from analizador.arbolSintaxisAbstracta import NodoASA, TipoNodo
from utils.TipoDatos import TipoDatos

class Visitante:

    tablaSimbolos: TablaSimbolos

    def __init__(self, nuevaTablaSimbolos):
        # Creamos un visitante y visitamos el nodo de error
        self.tablaSimbolos = nuevaTablaSimbolos

    def visitar(self, nodo :NodoASA):
        """
        Es necesario ya que todos los nodos son del mismo tipo en el arbol
        """

        # f = open("salida.txt", "a")
        # print(self.tablaSimbolos, file=f)
        # f.close()

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
        nodoActual.atributos['tipo'] = nodoActual.nodos[0].atributos['tipo']

    def __visitarExpresion(self, nodoActual):
        """
        Expresion ::= ExpresionMate Operador ExpresionMate
        """
        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        # Anoto el tipo de datos 'NÚMERO' (TIPO)
        if nodoActual.nodos[0].atributos['tipo'] != nodoActual.nodos[2].atributos['tipo'] \
            and nodoActual.nodos[0].atributos['tipo'] != TipoDatos.CUALQUIERA \
            and nodoActual.nodos[2].atributos['tipo'] != TipoDatos.CUALQUIERA:

            raise Exception('Tipos de datos no pueden ser operados', nodoActual.nodos[0].atributos['tipo'], nodoActual.nodos[2].atributos['tipo'], nodoActual.errorInfo)
        
        
        if nodoActual.nodos[0].atributos['tipo'] == TipoDatos.VALOR_VERDAD or nodoActual.nodos[2].atributos['tipo']  == TipoDatos.VALOR_VERDAD:
            raise Exception('No se pueden tener valores booleanos en una expresion', nodoActual.errorInfo)
        

        nodoActual.atributos['tipo'] = nodoActual.nodos[0].atributos['tipo']

    def __visitarInvocacion(self, nodoActual):
        """
        Invocación ::= ir a mundo Identificador [Parámetros]
        """
        # Verificacion del identificador de la funcion
        registro = self.tablaSimbolos.buscar(nodoActual.nodos[0].contenido)

        if registro.obtenerReferencia().tipo != TipoNodo.FUNCION:
            raise Exception("\""+registro.obtenerIdentificador() + "\" es una variable no una función", nodoActual.errorInfo)

        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        # El tipo resultado de la invocación es el tipo inferido de una
        # función previamente definida
        nodoActual.atributos['tipo'] = registro.obtenerReferencia().tipo

    def __visitarFuncion(self, nodoActual):
        """
        Funcion ::= mundo Identificador [ParametrosFunción](\n|\s)* BloqueInstrucciones
        """
        # Meto la función en la tabla de símbolos (IDENTIFICACIÓN)
        self.tablaSimbolos.incluir(nodoActual)

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

                if registro.obtenerReferencia().tipo == TipoNodo.FUNCION:
                    raise Exception('No se permitan funciones como parametros de invocacion de funcion', nodoActual.errorInfo) 

                
            # Si son otra cosa, simplemente se visitan
            nodo.visitar(self)

    def __visitarInstruccion(self, nodoActual):
        """
        Instrucción ::= ((Retorno | Error | Invocación)[ ; ] | Repetición | Bifurcación | Asignación | Comentario)(\n|\s)* 
        """

        for nodo in nodoActual.nodos:
            nodo.visitar(self)
            nodoActual.atributos['tipo'] = nodo.atributos['tipo']
    

    def __visitarBloqueInstrucciones(self, nodoActual):
        """
        BloqueInstrucciones ::= { Instrucción+ }
        """

        # For para visitar todas las instrucciones
        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        # Aquí se guarda el tipo de dato de retorno si hay
        nodoActual.atributos['tipo'] = TipoDatos.NINGUNO 

        for nodo in nodoActual.nodos:
            if nodo.atributos['tipo'] != TipoDatos.NINGUNO:
                nodoActual.atributos['tipo'] = nodo.atributos['tipo']

    def __visitarRepeticion(self, nodoActual):
        """
        Repetición ::= minijuego [Condicion] BloqueInstrucciones
        """
        # Visita la condición

        # Visita el bloque de instrucciones
        self.tablaSimbolos.iniciarBloque()

        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        self.tablaSimbolos.cerrarBloque()

        # Guarda el tipo de retorno
        nodoActual.atributos['tipo'] = nodoActual.nodos[1].tipo
    
    def __visitarBifurcacion(self, nodoActual):
        """
        Bifurcación ::= Si (Sino)?
        """

        # Visita los dos nodos en el siguiente nivel si existen
        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        nodoActual.atributos['tipo'] = TipoDatos.CUALQUIERA

    def __visitarSi(self, nodoActual):
        """
        Si ::= nivel (\n|\s)*[Condición](\n|\s)*BloqueInstrucciones
        """
        # Visita la condición

        # Visita el bloque de instrucciones
        self.tablaSimbolos.iniciarBloque()

        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        self.tablaSimbolos.cerrarBloque()

        # Guarda el tipo de retorno
        nodoActual.atributos['tipo'] = nodoActual.nodos[1].tipo

    def __visitarSiNo(self, nodoActual):
        """
        Sino ::= tubo (\n|\s)*BloqueInstrucciones
        """
        # Visita el bloque de instrucciones
        self.tablaSimbolos.iniciarBloque()

        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        self.tablaSimbolos.cerrarBloque()

        # Guarda el tipo de retorno
        nodoActual.atributos['tipo'] = nodoActual.nodos[0].atributos['tipo']

    def __visitarRetorno(self, nodoActual):
        """
        Retorno ::= bandera Valor?
        """

        for nodo in nodoActual.nodos:
            nodo.visitar(self)
        
        if nodoActual.nodos == []:
            # Si no retorna un valor no retorna un tipo específico 
            nodoActual.atributos['tipo'] = TipoDatos.NINGUNO

        else:
            for nodo in nodoActual.nodos:
                nodo.visitar(self)

                if nodo.tipo == TipoNodo.IDENTIFICADOR:
                    # Verifica si el valor es un identificador que exista
                    registro = self.tablaSimbolos.buscar(nodo.contenido)

                    # Se le da a bandera el tipo de retorno del identificador encontrado
                    nodoActual.atributos['tipo'] = registro.obtenerReferencia().atributos['tipo']
                else:
                    # Verifica si es un Literal de que tipo es
                    nodoActual.atributos['tipo'] = nodo.atributos['tipo']

    def __visitarCondicion(self, nodoActual):
        """
        Condición ::= Comparación (OperadorBooleano Condición)?
        """

        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        # Comparación retorna un valor de verdad
        nodoActual.atributos['tipo'] = TipoDatos.VALOR_VERDAD

    def __visitarBloqueCondiciones(self, nodoActual):
        """
        BloqueCondiciones ::= Condicion | ([Condicion+] (OperadorBooleano BloqueCondiciones)?)
        """
        # For para visitar todas las condiciones
        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        # Condición retorna un valor de verdad
        nodoActual.atributos['tipo'] = TipoDatos.VALOR_VERDAD

    def __visitarComparacion(self, nodoActual):
        """
        Comparación ::= Valor Comparador Valor
        """

        # Si los valores son identificadores se asegura que existan
        for nodo in nodoActual.nodos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tablaSimbolos.buscar(nodo.contenido)

            nodo.visitar(self)

        # Verificar que los tipos coincidan
        valor_izq = nodoActual.nodos[0]
        comparador = nodoActual.nodos[1]
        valor_der = nodoActual.nodos[2]

        if valor_izq.atributos['tipo'] == valor_der.atributos['tipo']:
            comparador.atributos['tipo'] = valor_izq.atributos['tipo']

            # Una comparación siempre tiene un valor de verdad
            nodoActual.atributos['tipo'] = TipoDatos.VALOR_VERDAD

        # Caso especial: Si alguno de los dos es un identificador de
        # un parámetro de función no puedo saber que tipo tiene o va a
        # tener por que este lenguaje no es tipado
        elif valor_izq.atributos['tipo'] == TipoDatos.CUALQUIERA or \
                valor_der.atributos['tipo'] == TipoDatos.CUALQUIERA:
            comparador.atributos['tipo'] = TipoDatos.CUALQUIERA
            nodoActual.atributos['tipo'] = TipoDatos.CUALQUIERA
        else:
            raise Exception('No se pueden comparar dos tipos diferentes', nodoActual.errorInfo)
    
    def __visitarOperadorBooleano(self, nodoActual):
        """
        OperadorBooleano ::=  [( & | | )]
        """
        # Operador para trabajar con valores de verdad
        nodoActual.atributos['tipo'] = TipoDatos.VALOR_VERDAD

    def __visitarError(self, nodoActual):
        """
        Error ::= [ POW ] Valor
        """
        for nodo in nodoActual.nodos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                self.tablaSimbolos.buscar(nodo.contenido)

        nodoActual.atributos['tipo'] = TipoDatos.NINGUNO 

    def __visitarValorBooleano(self, nodoActual):
        """
        ValorBooleano ::=  peach | bowser
        """
        # Marcar el tipo de dato del nodo actual como valor de verdad (booleano)
        nodoActual.atributos['tipo'] = TipoDatos.VALOR_VERDAD

    def __visitarEntero(self, nodoActual):
        """
        Entero ::=  (-)?\d+
        """

        # Marcar el tipo de dato del nodo actual como ENTERO
        nodoActual.atributos['tipo'] = TipoDatos.ENTERO

    def __visitarFlotante(self, nodoActual):
        """
        Flotante ::=  (-)?\d*.\d+*
        """

        # Marcar el tipo de dato del nodo actual como FLOTANTE
        nodoActual.atributos['tipo'] = TipoDatos.NÚMERO

     
    def __visitarTexto(self, nodoActual):
            """
            Texto ::= “[a-zA-Z_0-9]*”

            """
            # Marcar el tipo de dato del nodo actual como TEXTO
            nodoActual.atributos['tipo'] = TipoDatos.NÚMERO

    def __visitarPrincipal(self, nodoActual):
        """
        Principal ::= jugar BloqueInstrucciones
        """
        # Inicia un nuevo bloque de scope para el programa principal
        self.tablaSimbolos.iniciarBloque()

        # Visita el bloque de instrucciones del programa principal
        nodoActual.nodos[0].visitar(self)

        self.tablaSimbolos.cerrarBloque()

        nodoActual.atributos['tipo'] = nodoActual.nodos[0].atributos['tipo']

    def __visitarAsignacion(self, nodoActual):
        """
        Asignación ::= Identificador [ ? ] (Literal |ExpresionMate | Invocación)  [ ; ]
        """
        # Se ingresa el identificador a la tabla de símbolos
        self.tablaSimbolos.incluir(nodoActual.nodos[0])

        for nodo in nodoActual.nodos:
            nodo.visitar(self)

        nodoActual.atributos['tipo'] = nodoActual.nodos[1].atributos['tipo']

        nodoActual.nodos[0].atributos['tipo'] = nodoActual.nodos[1].atributos['tipo']

    def __visitarComparador(self, nodoActual):
        """
        Comparador ::= ( [ <> ] | [ >< ] | [ >- ] | [ <- ] | [^^] | [ -- ] )

        """

        """
        No estoy seguro si esto se necesita

        if nodoActual.contenido not in ['[ >< ] ', '[ <> ]' ]:
            nodoActual.atributos['tipo'] = TipoDatos.NÚMERO

        else:
        """

        nodoActual.atributos['tipo'] = TipoDatos.CUALQUIERA 

    def __visitarIdentificador(self, nodoActual):
        """
        Identificador ::= [a-z][a-zA-Z0-9]+
        """
        nodoActual.atributos['tipo'] = TipoDatos.CUALQUIERA

    def __visitarOperador(self, nodoActual):
        """
        Operador ::= ([ + ] | - ] | * ] | / ])

        """
        nodoActual.atributos['tipo'] = TipoDatos.NÚMERO
        
    