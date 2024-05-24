# Analizador SuperPrograBros 

#imports
from explorador.explorador import TipoComponenteLexico, ComponenteLexico
from analizador.arbolSintaxisAbstracta import ArbolSintaxisAbstracta, NodoASA, TipoNodo
# clase de analizador, recibe la lista de componentes lexicos del explorador

class Analizador:
    # atributos
    componentesLexicos : list
    cantidadComponentes: int
    posicionComponenteActual: int
    componenteActual : ComponenteLexico
    error : bool

    # constructor
    def __init__(self, listaComponentes):

        self.componentesLexicos = listaComponentes
        self.cantidadComponentes = len(listaComponentes)
        self.posicionComponenteActual = 0
        self.componenteActual = listaComponentes[self.posicionComponenteActual]
        self.asa = ArbolSintaxisAbstracta()
        self.error = False


    # metodos
    def imprimirArbol(self):
        #imprime el arbol de sintaxis abstracta
        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimirPreorden()

    def analizar(self):
        self.asa.raiz = self.__analizarPrograma()
    
    def __analizarPrograma(self):
        """
        Programa ::= ((Comentario | Asignacion | Funcion)(\n|\s)*)* Principal
        """

        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }
        
        while (True):

            # Caso1: una asignación
            if self.componenteActual.tipo == TipoComponenteLexico.IDENTIFICADOR:
                nuevosNodos = [self.__analizarAsignacion()]

            # Caso2: una función
            elif self.componenteActual.tipo == TipoComponenteLexico.FUNCION:
                nuevosNodos += [self.__analizarFuncion()]

            else:
                break

        # El principal en esta posición es obligatorio
        if self.componenteActual.tipo == TipoComponenteLexico.PRINCIPAL:
            nuevosNodos += [self.__analizarPrincipal()]

        # Error
        else:
            self.__printError('juego')
            
        
        return NodoASA(TipoNodo.PROGRAMA, nodos=nuevosNodos, errorInfo=errorInfo)
    
    def __analizarAsignacion(self):
        """
        Asignación ::= Identificador [ ? ] (ExpresionMate | Invocación)  [ ; ]
        """

        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        # El identificador en esta posición es obligatorio
        nuevosNodos += [self.__verificarIdentificador()]

        # El asignador en esta posición es obligatorio
        self.__verificarAsignador()

        # Caso1: una invocación
        if self.componenteActual.tipo == TipoComponenteLexico.INVOCACION:
            nuevosNodos += [self.__analizarInvocacion()]

        # Caso2: un literal o una expresión matemática
        elif self.componenteActual.tipo in [TipoComponenteLexico.ENTERO, TipoComponenteLexico.FLOTANTE, TipoComponenteLexico.TEXTO, 
                                          TipoComponenteLexico.VALOR_BOOLEANO, TipoComponenteLexico.IDENTIFICADOR, TipoComponenteLexico.PUNTUACION]: 
            nuevosNodos += [self.__analizarExpresionMatematica()]

        # Error
        else:
            self.__printError('Asignacion')

        self.__verificar("[ ; ]")
        return NodoASA(TipoNodo.ASIGNACION, nodos=nuevosNodos, errorInfo=errorInfo)


    def __analizarExpresionMatematica(self):
        """
        ExpresionMate ::= Valor | [Expresion]
        """

        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }
        
        # Caso1: un valor
        if self.componenteActual.tipo in [TipoComponenteLexico.ENTERO, TipoComponenteLexico.FLOTANTE, TipoComponenteLexico.TEXTO, 
                                            TipoComponenteLexico.VALOR_BOOLEANO, TipoComponenteLexico.IDENTIFICADOR]:
            nuevosNodos += [self.__analizarValor()]
        
        # Caso2: una expresión
        elif self.componenteActual.tipo == TipoComponenteLexico.PUNTUACION: ######
            self.__verificar("[")
            nuevosNodos += [self.__analizarExpresion()]
            self.__verificar("]")


        # Error
        else:
            self.__printError('Expresion Matematica')

        return NodoASA(TipoNodo.EXPRESION_MATEMATICA, nodos=nuevosNodos, errorInfo=errorInfo) ######


    def __analizarExpresion(self):
        """
        Expresion ::= ExpresionMate Operador ExpresionMate
        """

        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        # Una expresión matemática en esta posición es obligatoria
        nuevosNodos += [self.__analizarExpresionMatematica()]

        # Un operador en esta posición es obligatorio
        nuevosNodos += [self.__verificarOperador()]

        # Una expresión matemática en esta posición es obligatoria
        nuevosNodos += [self.__analizarExpresionMatematica()]

        return NodoASA(TipoNodo.EXPRESION , nodos=nuevosNodos, errorInfo=errorInfo)

    def __analizarInvocacion(self):
        """
        Invocación ::= ir a mundo Identificador [Parámetros]
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        # El invocador en esta posición es obligatorio
        self.__verificarInvocador()

        # El identificador en esta posición es obligatorio
        nuevosNodos += [self.__verificarIdentificador()]

        # El [ en esta posición es obligatorio
        self.__verificar('[')
        # Los parámetros en esta posición son obligatorios
        nuevosNodos += [self.__analizarParametrosInvocacion()]

        # El ] en esta posición es obligatorio
        self.__verificar(']')

        return NodoASA(TipoNodo.INVOCACION , nodos=nuevosNodos, errorInfo=errorInfo)
    
    def __analizarFuncion(self):
        """
        Funcion ::= mundo Identificador [Parámetros](\n|\s)*{ Instrucción * }
        """

        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        # La palabra mundo en esta posición es obligatoria
        self.__verificar('mundo')

        # El identificador en esta posición es obligatorio
        nuevosNodos += [self.__verificarIdentificador()]

        # El [ en esta posición es obligatorio
        self.__verificar('[')

        nuevosNodos += [self.__analizarParametrosFuncion()]

        # El ] en esta posición es obligatorio
        self.__verificar(']')

        # El bloque de código en esta posición es obligatoria
        nuevosNodos += [self.__analizarBloqueInstrucciones()]

        # La función lleva el nombre del identificador
        return NodoASA(TipoNodo.FUNCION, \
                contenido=nuevosNodos[0].contenido, nodos=nuevosNodos, errorInfo=errorInfo)
    
    def __analizarParametrosFuncion(self):
        """
        ParametrosFunción ::= Identificador (,Identificador)*
        """
        nodos_nuevos = []

        # El identificador en esta posición es obligatorio
        nodos_nuevos += [self.__verificarIdentificador()]

        # Ciclo que verificar la ',' y el identificador hasta que se acaben los parámetros
        while( self.componenteActual.lexema == ','):
            self.__verificar(',')
            nodos_nuevos += [self.__verificarIdentificador()]

        return NodoASA(TipoNodo.PARAMETROS_FUNCION , nodos=nodos_nuevos) #######

    def __analizarParametrosInvocacion(self):
        """
        Parámetros Invocacion ::= Valor (,Valor)+
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        # El valor en esta posición es obligatorio
        nuevosNodos += [self.__analizarValor()]

        # Ciclo que verificar la ',' y el valor hasta que se acaben los parámetros
        while(self.componenteActual.lexema == ','):
            self.__verificar(',')
            nuevosNodos += [self.__analizarValor()]

        return NodoASA(TipoNodo.PARAMETROS_INVOCACION , nodos=nuevosNodos, errorInfo=errorInfo) #######
    

    def __analizarInstruccion(self):
        """
        Instrucción ::= ((Retorno | Error | Invocación)[ ; ] | Repetición | Bifurcación | Asignación | Comentario)(\n|\s)* 


        Los comentarios son ignorados
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        
        if self.componenteActual.lexema == 'bandera' or self.componenteActual.lexema == 'ir a mundo' or \
            self.componenteActual.lexema == '[ POW ]':

            # Retorno
            if self.componenteActual.tipo == TipoComponenteLexico.RETORNO:
                nuevosNodos += [self.__analizarRetorno()]
            
            # Invocacion
            elif self.componenteActual.tipo == TipoComponenteLexico.INVOCACION:
                nuevosNodos += [self.__analizarInvocacion()]

            # Error
            elif self.componenteActual.tipo == TipoComponenteLexico.ERROR:
                self.__printError('Instruccion')

            self.__verificar('[ ; ]')

        # repeticion
        elif self.componenteActual.lexema == 'minijuego':
            nuevosNodos += [self.__analizarRepeticion()]
        
        # bifurcacion    
        elif self.componenteActual.lexema == 'nivel':
            nuevosNodos += [self.__analizarBifurcacion()]

        # asignacion
        elif self.componenteActual.tipo == TipoComponenteLexico.IDENTIFICADOR:
            nuevosNodos += [self.__analizarAsignacion()]
            
        return NodoASA(TipoNodo.INSTRUCCION, nodos=nuevosNodos, errorInfo=errorInfo)
    

    def __analizarRepeticion(self):
        """
        minijuego [Condicion] {Instruccion+}
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        # analisis de la condicion
        self.__verificar('minijuego')
        self.__verificar('[')
        nuevosNodos += [self.__analizarBloqueCondiciones()]
        self.__verificar(']')

        nuevosNodos += [self.__analizarBloqueInstrucciones()] #agregar nuevo

        return NodoASA(TipoNodo.REPETICION, nodos=nuevosNodos, errorInfo=errorInfo)
    

    def __analizarBifurcacion(self):
        """
        Si (Sino)?
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        # analisis de la bifurcacion
        # Si
        nuevosNodos += [self.__analizarSi()] #agregar nuevo
        # Sino
        if self.componenteActual.lexema == 'tubo':
            nuevosNodos += [self.__analizarSino()] #agregar nuevo


        return NodoASA(TipoNodo.BIFURCACION, nodos=nuevosNodos, errorInfo=errorInfo)
    

    def __analizarSi(self):
        """
        nivel (\n|\s)*[Condición](\n|\s)*BloqueInstrucciones
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        # analizar Si
        self.__verificar('nivel')
        self.__verificar('[')
        nuevosNodos += [self.__analizarBloqueCondiciones()]
        self.__verificar(']')

        nuevosNodos += [self.__analizarBloqueInstrucciones()] #agregar nuevo

        return NodoASA(TipoNodo.SI, nodos=nuevosNodos, errorInfo=errorInfo)
    

    def __analizarSino(self):
        """
        tubo (\n|\s)*BloqueInstrucciones
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        # analizar Sino
        self.__verificar('tubo')

        nuevosNodos += [self.__analizarBloqueInstrucciones()] #agregar nuevo

        return NodoASA(TipoNodo.SINO, nodos=nuevosNodos, errorInfo=errorInfo)

    def __analizarRetorno(self):
        """
        Retorno ::= bandera Valor?
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        # analizar retorno
        self.__verificar('bandera')
        
        # valor es opcional
        if self.componenteActual.tipo in [TipoComponenteLexico.IDENTIFICADOR, TipoComponenteLexico.ENTERO, TipoComponenteLexico.FLOTANTE,
                                          TipoComponenteLexico.TEXTO, TipoComponenteLexico.VALOR_BOOLEANO]:
            nuevosNodos += [self.__analizarValor()]

        return NodoASA(TipoNodo.RETORNO, nodos=nuevosNodos, errorInfo=errorInfo)
    
    def __analizarBloqueCondiciones(self):
        """
        BloqueCondiciones ::= Condicion | ([Condicion+] (OperadorBooleano BloqueCondiciones)?)
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        if self.componenteActual.lexema == '[':
            # VIene bloque de condiciones
            self.__verificar('[')
            nuevosNodos += [self.__analizarCondicion()]

            while self.componenteActual.lexema != ']':
                nuevosNodos += [self.__analizarCondicion()]
            
            self.__verificar(']')

            if self.componenteActual.tipo == TipoComponenteLexico.OPERADOR_BOOLEANO:
                nuevosNodos = [self.__analizarOperadorBooleano()]

                # analizar la siguiente condicion 
                nuevosNodos = [self.__analizarBloqueCondiciones()]


        else:
            # viene una sola condicion 
            nuevosNodos += [self.__analizarCondicion()]

        return NodoASA(TipoNodo.BLOQUE_CONDICIONES, nodos=nuevosNodos, errorInfo=errorInfo)
    
    def __analizarCondicion(self):
        """
        Condición ::= Comparación (OperadorBooleano Condición)?
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        # se analiza la primera comparacion
        nuevosNodos += [self.__analizarComparacion()]

        # la segunda comparacion con los operadores es opcional
        if self.componenteActual.tipo == TipoComponenteLexico.OPERADOR_BOOLEANO:
            nuevosNodos = [self.__analizarOperadorBooleano()]

            # analizar la siguiente condicion 
            nuevosNodos = [self.__analizarBloqueCondiciones()]


        return NodoASA(TipoNodo.CONDICION, nodos=nuevosNodos, errorInfo=errorInfo)
    
    def __analizarComparacion(self):
        """
        Comparación ::= Valor Comparador Valor
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        # analisis de la comparacion
        nuevosNodos += [self.__analizarValor()]
        nuevosNodos += [self.__verificarComparador()]
        nuevosNodos += [self.__analizarValor()]


        return NodoASA(TipoNodo.COMPARACION, nodos=nuevosNodos, errorInfo=errorInfo)
    
    def __analizarOperadorBooleano(self):
        """
        OperadorBooleano ::=  [( & | | )]
        """
        # analizar operador booleano 

        self.__verificarTipoComponente(TipoComponenteLexico.OPERADOR_BOOLEANO)

        nodo = NodoASA(TipoNodo.OPERADOR_BOOLEANO, contenido=self.componenteActual.lexema)
        self.__pasarSiguienteComponente()

        return nodo
    
    def __analizarError(self):
        """
        Error ::= [ POW ] Valor 
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        self.__verificar('[ POW ]')
        nuevosNodos += [self.__analizarValor()]

        return NodoASA(TipoNodo.ERROR, nodos=nuevosNodos, errorInfo=errorInfo)
    

    def __analizarPrincipal(self):
        """
        Principal :== juego (\n|\s)* BloqueInstrucciones
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }

        self.__verificar('juego')
        nuevosNodos += [self.__analizarBloqueInstrucciones()]

        return NodoASA(TipoNodo.PRINCIPAL, nodos=nuevosNodos, errorInfo=errorInfo)
    
    def __analizarLiteral(self):
        """
        Literal ::= (Entero | Flotante | Texto | ValorBooleano)
        """

        if self.componenteActual.tipo == TipoComponenteLexico.ENTERO:
            nodo = self.__verificarEntero()
        elif self.componenteActual.tipo == TipoComponenteLexico.FLOTANTE:
            nodo = self.__verificarFlotante()
        elif self.componenteActual.tipo == TipoComponenteLexico.TEXTO:
            nodo = self.__verificarTexto()
        elif self.componenteActual.tipo == TipoComponenteLexico.VALOR_BOOLEANO:
            nodo = self.__verificarValorBooleano()
        else:
            # Manejo de error
            self.__printError("Literal")
            nodo = self.__analizarError()

        return nodo
    
    def __analizarBloqueInstrucciones(self):
        """
        BloqueInstrucciones ::= { Instrucción+ }
        """
        nuevosNodos = []
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }
        # Obligatorio
        self.__verificar('{')
        # la primera instruccion obligatoria
        nuevosNodos += [self.__analizarInstruccion()]

        # valida todas las instrucciones que haya de mas (repeticion, bifurcacion, retorno, invocacion, error)
        while self.componenteActual.lexema in ['minijuego', 'nivel', 'bandera', 'ir a mundo', '[ POW ]'] \
                or self.componenteActual.tipo == TipoComponenteLexico.IDENTIFICADOR:
            nuevosNodos += [self.__analizarInstruccion()]

        # Obligatorio
        self.__verificar('}')
        nodo = NodoASA(TipoNodo.BLOQUE_INSTRUCCIONES, nodos=nuevosNodos, errorInfo=errorInfo)
        return nodo
    
    def __verificarIdentificador(self):
        """
        Verifica si el tipo del componente léxico actual es un identificador

        Identificador ::= [a-zA-Z_][0-9a-zA-Z_]*
        """
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }
        self.__verificarTipoComponente(TipoComponenteLexico.IDENTIFICADOR)

        nodo = NodoASA(TipoNodo.IDENTIFICADOR, contenido=self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo

    def __analizarValor(self):
        """
        Valor ::= (Literal | Identificador)
        """
        if self.componenteActual.tipo == TipoComponenteLexico.IDENTIFICADOR :
            nodo = self.__verificarIdentificador()
        else: 
            nodo = self.__analizarLiteral()
        
        return nodo


    def __verificarFlotante(self):
        """
        Verifica si el tipo del componente léxico actual es un flotante

        Flotante ::= (-)?\d*.\d+
        """
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }
        self.__verificarTipoComponente(TipoComponenteLexico.FLOTANTE)
        
        nodo = NodoASA(TipoNodo.FLOTANTE, contenido =self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificarEntero(self):
        """
        Verifica si el tipo del componente léxico actual es un entero

        Entero ::= (-)?\d+
        """
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }
        self.__verificarTipoComponente(TipoComponenteLexico.ENTERO)

        nodo = NodoASA(TipoNodo.ENTERO, contenido =self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificarComparador(self):
        """
        Verifica si el tipo del componente léxico actual es un comparador
        Comparador ::= Comparador ::= [ (<>|><|>-|<-|\^\^|--) \]')

        """
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }
        self.__verificarTipoComponente(TipoComponenteLexico.COMPARADOR)
        nodo = NodoASA(TipoNodo.COMPARADOR, contenido =self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo

    def __verificarValorBooleano(self):
        """
        Verifica si el tipo del componente léxico actual es un valor booleano

        ValorBooleano ::= peach | bowser
        """
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }
        self.__verificarTipoComponente(TipoComponenteLexico.VALOR_BOOLEANO)
        nodo = NodoASA(TipoNodo.VALOR_BOOLEANO, contenido=self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificarOperador(self):
        """
        Verifica si el tipo del componente léxico actual es un operador

        operador ::= '(\[ (\+|-|\*|\/|) \])')
        """
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }
        self.__verificarTipoComponente(TipoComponenteLexico.OPERADOR)
        nodo = NodoASA(TipoNodo.OPERADOR, contenido=self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificarTexto(self):
        """
        Verifica si el tipo del componente léxico actual es un texto

        Texto ::= “[a-zA-Z_0-9]*”

        """
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }
        self.__verificarTipoComponente(TipoComponenteLexico.TEXTO)
        nodo = NodoASA(TipoNodo.TEXTO, contenido=self.componenteActual.lexema)  # Eliminar las comillas
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificarIdentificador(self):
        """
        Verifica si el tipo del componente léxico actual es un identificador

        Identificador ::= [a-zA-Z_][0-9a-zA-Z_]*
        """
        errorInfo = {
            "linea": self.componenteActual.lineaCodigo, 
            "numeroLinea": self.componenteActual.numeroLinea, 
            "numeroColumna": self.componenteActual.numeroColumna
        }
        self.__verificarTipoComponente(TipoComponenteLexico.IDENTIFICADOR)

        nodo = NodoASA(TipoNodo.IDENTIFICADOR, contenido =self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificarAsignador(self):
        """
        Verifica si el tipo del componente léxico actual es un asignador

        Asignador ::= \[ \? \]
        """
        self.__verificarTipoComponente(TipoComponenteLexico.ASIGNADOR)
        self.__pasarSiguienteComponente()
    
    def __verificarInvocador(self):
        """
        Verifica si el tipo del componente léxico actual es un invocador

        Asignador ::= (ir a mundo)
        """
        self.__verificarTipoComponente(TipoComponenteLexico.INVOCACION)
        self.__pasarSiguienteComponente()
    
    def __verificar(self, textoEsperado):
        """
        Verifica si el texto del componente actual es el del texto esperado que se envia como parametro.
        Si no coinciden se imprime el error y se activa la bandera de error
        """

        if self.componenteActual.lexema != textoEsperado:
            self.__printError(textoEsperado)

        self.__pasarSiguienteComponente()

    def __verificarTipoComponente(self, tipoEsperado ):
        """
        Verifica un componente segun su tipo
        """

        if self.componenteActual.tipo != tipoEsperado:
            self.__printError(tipoEsperado)

    
    def __pasarSiguienteComponente(self):
        """
        Pasa al siguiente componente léxico
        """
        self.posicionComponenteActual += 1

        if self.posicionComponenteActual >= self.cantidadComponentes:
            return

        self.componenteActual = self.componentesLexicos[self.posicionComponenteActual]

    def __printError(self, tipoNodoEsperado):
        """
        Imprime el error dado y coloca el error como true
        """
        print(f"""[ POW ]: Se esperaba un token de tipo '{tipoNodoEsperado}', no '{self.componenteActual.lexema}' en la linea {self.componenteActual.numeroLinea}, 
                  columna {self.componenteActual.numeroColumna}\n\n\t--->{self.componenteActual.lineaCodigo}\n""")
        self.error = True