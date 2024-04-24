# Analizador SuperPrograBros 

#imports
from explorador.explorador import TipoComponenteLexico, ComponenteLexico

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
            nuevosNodos += [self.__analizarError()]

        
        return NodoASA(TipoComponenteLexico.PROGRAMA, nodos=nuevosNodos)
    
    def __analizarAsignacion(self):
        """
        Asignación ::= Identificador [ ? ] (Literal | ExpresionMate | Invocación)
        """

        nuevosNodos = []

        # El identificador en esta posición es obligatorio
        nuevosNodos += [self.__verificarIdentificador()]

        # El asignador en esta posición es obligatorio
        nuevosNodos += [self.__verificarAsignador()]

        # Caso1: una invocación
        if self.componenteActual.tipo == TipoComponenteLexico.ASIGNADOR:
            nuevosNodos += [self.__analizarInvocacion()]

        # Caso2: un literal o una expresión matemática
        elif self.componenteActual.tipo in [TipoComponenteLexico.ENTERO, TipoComponenteLexico.FLOTANTE, TipoComponenteLexico.TEXTO, 
                                          TipoComponenteLexico.VALOR_BOOLEANO, TipoComponenteLexico.IDENTIFICADOR]:
            if self.__componenteAdelante().tipo == TipoComponenteLexico.OPERADOR: 
                nodos_nuevos += [self.__analizarExpresionMatematica()]
            else:
                nuevosNodos += [self.__analizarLiteral()]

        # Error
        else:
            nuevosNodos += [self.__analizarError()]

        return NodoASA(TipoComponenteLexico.ASIGNADOR, nodos=nuevosNodos) #####


    def __analizarExpresionMatematica(self):
        """
        ExpresionMate ::= Valor | [Expresion]
        """

        nuevosNodos = []
        
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
            nuevosNodos += [self.__analizarError()]

        return NodoASA(TipoComponenteLexico.EXPRESION_MATEMATICA, nodos=nuevosNodos) ######


    def __analizarExpresion(self):
        """
        Expresion ::= ExpresionMate Operador ExpresionMate
        """

        nuevosNodos = []

        # Una expresión matemática en esta posición es obligatoria
        nuevosNodos += [self.__analizarExpresionMatematica()]

        # Un operador en esta posición es obligatorio
        nuevosNodos += [self.__verificarOperador()]

        # Una expresión matemática en esta posición es obligatoria
        nuevosNodos += [self.__analizarExpresionMatematica()]

        return NodoASA(TipoComponenteLexico.EXPRESIÓN , nodos=nuevosNodos)

    def __analizarInvocacion(self):
        """
        Invocación ::= ir a mundo Identificador [Parámetros]
        """
        nuevosNodos = []

        # El invocador en esta posición es obligatorio
        nuevosNodos += [self.__verificarInvocador()]

        # El identificador en esta posición es obligatorio
        nuevosNodos += [self.__verificarIdentificador()]

        # El [ en esta posición es obligatorio
        self.__verificar('[')

        # Los parámetros en esta posición son obligatorios
        nuevosNodos += [self.__analizarParametrosInvocacion()]

        # El ] en esta posición es obligatorio
        self.__verificar(']')

        return NodoASA(TipoComponenteLexico.INVOCACION , nodos=nuevosNodos)
    
    def __analizarFuncion(self):
        """
        Funcion ::= mundo Identificador [Parámetros](\n|\s)*{ Instrucción * }
        """

        nuevosNodos = []

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
        return NodoASA(TipoComponenteLexico.FUNCION, \
                contenido=nuevosNodos[0].contenido, nodos=nuevosNodos)
    
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

        return NodoASA(TipoComponenteLexico.IDENTIFICADOR , nodos=nodos_nuevos) #######

    def __analizarParametrosInvocacion(self):
        """
        Parámetros Invocacion ::= Valor (,Valor)+
        """
        nuevosNodos = []

        # El valor en esta posición es obligatorio
        nuevosNodos += [self.__analizarValor()]

        # Ciclo que verificar la ',' y el valor hasta que se acaben los parámetros
        while(self.componenteActual.lexema == ','):
            self.__verificar(',')
            nuevosNodos += [self.__analizarValor()]

        return NodoASA(TipoComponenteLexico.PARAMETROS_INVOCACION , nodos=nuevosNodos) #######
    

    def __analizarInstruccion(self):
        """
        Instrucción ::= ((Retorno | Error | Invocación)[ ; ] | Repetición | Bifurcación | Asignación | Comentario)(\n|\s)* 


        Los comentarios son ignorados
        """
        nuevosNodos = []

        
        if self.componenteActual.lexema == 'bandera' or self.componenteActual.lexema == 'ir a mundo' or self.componenteActual.lexema == '[ POW ]':

            # Retorno
            if self.componenteActual.tipo == TipoComponenteLexico.RETORNO:
                nuevosNodos += [self.__analizarRetorno()]
            
            # Invocacion
            elif self.componenteActual.tipo == TipoComponenteLexico.INVOCACION:
                nuevosNodos += [self.__analizarInvocacion()]

            # Error
            elif self.componenteActual.tipo == TipoComponenteLexico.ERROR:
                nuevosNodos += [self.__analizarError()]

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

            
        return NodoASA(TipoComponenteLexico.INSTRUCCION, nodos=nuevosNodos)
    

    def __analizarRepeticion(self):
        """
        minijuego [Condicion] {Instruccion+}
        """
        nuevosNodos = []

        # analisis de la condicion
        self.__verificar('minijuego')
        self.__verificar('[')
        nuevosNodos += [self.__analizarCondicion()]
        self.__verificar(']')

        nuevosNodos += [self.__analizarBloqueInstrucciones()] #agregar nuevo

        return NodoASA(TipoComponenteLexico.REPETICION, nodos=nuevosNodos)
    

    def __analizarBifurcacion(self):
        """
        Si (Sino)?
        """
        nuevosNodos = []

        # analisis de la bifurcacion
        # Si
        nuevosNodos += [self.__analizarSi()] #agregar nuevo

        # Sino
        if self.componenteActual.lexema == 'tubo':
            nuevosNodos += [self.__analizarSino()] #agregar nuevo


        return NodoASA(TipoComponenteLexico.BIFURCACION, nodos=nuevosNodos)
    

    def __analizarSi(self):
        """
        nivel (\n|\s)*[Condición](\n|\s)*{ Instrucción + }
        """
        nuevosNodos = []

        # analizar Si
        self.__verificar('nivel')
        self.__verificar('[')
        nuevosNodos += [self.__analizarCondicion()]
        self.__verificar(']')

        nuevosNodos += [self.__analizarBloqueInstrucciones()] #agregar nuevo

        return NodoASA(TipoComponenteLexico.BIFURCACION, nodos=nuevosNodos)
    

    def __analizarSino(self):
        """
        tubo (\n|\s)*{ Instrucción + }
        """
        nuevosNodos = []

        # analizar Sino
        self.__verificar('tubo')

        nuevosNodos += [self.__analizarBloqueInstrucciones()] #agregar nuevo

        return NodoASA(TipoComponenteLexico.BIFURCACION, nodos=nuevosNodos)

    def __analizarRetorno(self):
        """
        Retorno ::= bandera Valor?
        """
        nuevosNodos = []

        # analizar retorno
        self.__verificar('bandera')
        
        # valor es opcional
        if self.componenteActual.tipo in [TipoComponenteLexico.IDENTIFICADOR, TipoComponenteLexico.ENTERO, TipoComponenteLexico.FLOTANTE,
                                          TipoComponenteLexico.TEXTO, TipoComponenteLexico.VALOR_BOOLEANO]:
            nuevosNodos += [self.__analizarValor()]

        return NodoASA(TipoComponenteLexico.RETORNO, nodos=nuevosNodos)
    

    def __analizarCondicion(self):
        """
        Condición ::= Comparación (OperadorBooleano Condición)?
        """
        nuevosNodos = []

        # se analiza la primera comparacion
        nuevosNodos += [self.__analizarComparacion()]

        # la segunda comparacion con los operadores es opcional
        if self.componenteActual.tipo == TipoComponenteLexico.OPERADOR_BOOLEANO:
            nuevosNodos = [self.__analizarOperadorBooleano()]

            # analizar la siguiente condicion 
            nuevosNodos = [self.__analizarCondicion()]


        return NodoASA(TipoComponenteLexico.BIFURCACION, nodos=nuevosNodos)
    
    def __analizarComparacion(self):
        """
        Comparación ::= Valor Comparador Valor
        """
        nuevosNodos = []

        # analisis de la comparacion
        nuevosNodos += [self.__analizarValor()]
        nuevosNodos += [self.__verificarComparador()]
        nuevosNodos += [self.__analizarValor()]


        return NodoASA(TipoComponenteLexico.COMPARACION, nodos=nuevosNodos)
    
    def __analizarOperadorBooleano(self):
        """
        ComparadorLogico ::=  [( & | | )]
        """
        # analizar operador booleano 

        self.__verificarTipoComponente(TipoComponenteLexico.OPERADOR_BOOLEANO)

        nodo = NodoASA(TipoComponenteLexico.OPERADOR_BOOLEANO, contenido=self.componenteActual.lexema)
        self.__pasarSiguienteComponente()

        return nodo
    
    def __analizarError(self):
        """
        Error ::= [ POW ] Valor 
        """
        nuevosNodos = []

        self.__verificar('[ POW ]')
        nuevosNodos += [self.__analizarValor()]

        return NodoASA(TipoComponenteLexico.ERROR, nodos=nuevosNodos)
    

    def __analizarPrincipal(self):
        """
        Principal :== juego (\n|\s)* BloqueInstrucciones
        """
        nuevosNodos = []

        self.__verificar('juego')
        nuevosNodos += [self.__analizarBloqueInstrucciones()]

        return NodoASA(TipoComponenteLexico.PRINCIPAL, nodos=nuevosNodos)
    
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
            nodo = self.__analizarError()

        return nodo
    
    def __analizarBloqueInstrucciones(self):
        """
        BloqueInstrucciones ::= { Instrucción+ }
        """
        nuevosNodos = []
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

        return "falta"
    
    def __verificarIdentificador(self):
        """
        Verifica si el tipo del componente léxico actual es un identificador

        Identificador ::= [a-zA-Z_][0-9a-zA-Z_]*
        """
        self.__verificarTipoComponente(TipoComponenteLexico.IDENTIFICADOR)

        nodo = NodoASA(TipoComponenteLexico.IDENTIFICADOR, contenido=self.componenteActual.lexema)
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
        self.__verificarTipoComponente(TipoComponenteLexico.FLOTANTE)

        nodo = NodoASA(TipoComponenteLexico.FLOTANTE, contenido =self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificarEntero(self):
        """
        Verifica si el tipo del componente léxico actual es un entero

        Entero ::= (-)?\d+
        """
        self.__verificarTipoComponente(TipoComponenteLexico.ENTERO)

        nodo = NodoASA(TipoComponenteLexico.ENTERO, contenido =self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def _verificarComparador(self):
        """
        Verifica si el tipo del componente léxico actual es un comparador
        Comparador ::= Comparador ::= [ (<>|><|>-|<-|\^\^|--) \]')

        """
        self.__verificarTipoComponente(TipoComponenteLexico.COMPARADOR)

        nodo = NodoASA(TipoComponenteLexico.COMPARADOR, contenido =self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo

    def __verificarValorBooleano(self):
        """
        Verifica si el tipo del componente léxico actual es un valor booleano

        ValorBooleano ::= peach | bowser
        """
        self.__verificarTipoComponente(TipoComponenteLexico.VALOR_BOOLEANO)

        nodo = NodoASA(TipoComponenteLexico.VALOR_BOOLEANO, contenido=self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificarOperador(self):
        """
        Verifica si el tipo del componente léxico actual es un operador

        operador ::= '(\[ (\+|-|\*|\/|) \])')
        """
        self.__verificarTipoComponente(TipoComponenteLexico.OPERADOR)

        nodo = NodoASA(TipoComponenteLexico.OPERADOR, contenido=self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificarTexto(self):
        """
        Verifica si el tipo del componente léxico actual es un texto

        Texto ::= “[a-zA-Z_0-9]*”

        """
        self.__verificarTipoComponente(TipoComponenteLexico.TEXTO)

        nodo = NodoASA(TipoComponenteLexico.TEXTO, contenido=self.componenteActual.lexema)  # Eliminar las comillas
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificarIdentificador(self):
        """
        Verifica si el tipo del componente léxico actual es un identificador

        Identificador ::= [a-zA-Z_][0-9a-zA-Z_]*
        """
        self.__verificarTipoComponente(TipoComponenteLexico.IDENTIFICADOR)

        nodo = NodoASA(TipoComponenteLexico.IDENTIFICADOR, contenido =self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificarAsignador(self):
        """
        Verifica si el tipo del componente léxico actual es un asignador

        Asignador ::= \[ \? \]
        """
        self.__verificarTipoComponente(TipoComponenteLexico.ASIGNADOR)

        nodo = NodoASA(TipoComponenteLexico.ASIGNADOR, contenido =self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificarInvocador(self):
        """
        Verifica si el tipo del componente léxico actual es un invocador

        Asignador ::= (ir a mundo)
        """
        self.__verificarTipoComponente(TipoComponenteLexico.INVOCACION)

        nodo = NodoASA(TipoComponenteLexico.INVOCACION, contenido =self.componenteActual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificar(self, textoEsperado):
        """
        Verifica si el texto del componente actual es el del texto esperado que se envia como parametro.
        Si no coinciden se imprime el error y se activa la bandera de error
        """

        if self.componenteActual.lexema != textoEsperado:
            print(f"""[Error]: Se esperaba '{textoEsperado}', no '{self.componenteActual.lexema}' en la linea {self.componenteActual.numeroLinea}, 
                  columna {self.componenteActual.numeroColumna}\n\n\t--->{self.componenteActual.lineaCodigo}\n""")
            self.error = True

        self.__pasarSiguienteComponente()

    def __verificarTipoComponente(self, tipoEsperado ):
        """
        Verifica un componente segun su tipo
        """

        if self.componenteActual.tipo != tipoEsperado:
            print(f"""[Error]: Se esperaba un token de tipo '{tipoEsperado}', no '{self.componenteActual.tipo}' en la linea {self.componenteActual.numeroLinea}, 
                  columna {self.componenteActual.numeroColumna}\n\n\t--->{self.componenteActual.lineaCodigo}\n""")
            self.error = True

    
    def __pasarSiguienteComponente(self):
        """
        Pasa al siguiente componente léxico
        """
        self.posicionComponenteActual += 1

        if self.posicionComponenteActual >= self.cantidadComponentes:
            return

        self.componenteActual = self.componentesLexicos[self.posicionComponenteActual]

    def __componenteAdelante(self, avance=1):
            """
            Retorna el componente léxico que está 'avance' posiciones más
            adelante... por default el siguiente. Esto sin adelantar el
            contador del componente actual.
            """
            return self.componentesLexicos[self.posicionComponenteActual+avance]    