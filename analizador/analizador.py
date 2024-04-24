# Analizador SuperPrograBros 

#imports
from explorador.explorador import TipoComponenteLexico, ComponenteLexico

class NodoASA:
    """
    Clase que representa un nodo generico del ASA.
    Cada nodo puede tener n nodos hijos y tiene su componente lexico con la informacion de error
    """
    tipo : TipoComponenteLexico
    contenido : str
    errorInfo : dict
    hijos : list

    def __init__(self, tipo, contenido = None, nodos = [], errorInfo = {}):
        self.tipo = tipo
        self.contenido = contenido
        self.nodos = nodos
        self.errorInfo = errorInfo

    def visitar(self, visitador):
        return visitador.visitar(self)
    
    def __str__(self):

        # Coloca la información del nodo
        resultado = '{:30}\t'.format(self.tipo)
        
        if self.contenido is not None:
            resultado += '{:10}\t'.format(self.contenido)
        else:
            resultado += '{:10}\t'.format('')


        if self.errorInfo != {}:
            resultado += '{:38}'.format(str(self.errorInfo))
        else:
            resultado += '{:38}\t'.format('')

        if self.nodos != []:
            resultado += '<'

            # Imprime los tipos de los nodos del nivel siguiente
            for nodo in self.nodos[:-1]:
                if nodo is not None:
                    resultado += '{},'.format(nodo.tipo)

            resultado += '{}'.format(self.nodos[-1].tipo)
            resultado += '>'

        return resultado


class ArbolSintaxisAbstracta:
    """
    Clase que representa el ASA. Guarda referencia a la raiz y imprime recursivamente los nodos
    """
    raiz : NodoASA

    def imprimirPreorden(self):
        self.__imprimirPreordenAux(self.raiz)

    def __imprimirPreordenAux(self, nodo):
        print(nodo)

        if nodo is not None:
            for nodoHijo in nodo.nodos:
                self.__imprimirPreordenAux(nodoHijo)

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

    
    def __analizarInstruccion(self):
        """
        Instrucción ::= (Repetición | Bifurcación | Asignación | Retorno |
        Error | Comentario)[ ; ](\n|\s)*

        Los comentarios son ignorados
        """
        nuevosNodos = []

        #repeticion
        if self.componenteActual.lexema == 'minijuego':
            nuevosNodos += [self.__analizarRepeticion()]
        
        #bifurcacion    
        elif self.componenteActual.lexema == 'nivel':
            nuevosNodos += [self.__analizarBifurcacion()]

        # asignacion
        elif self.componenteActual.tipo == TipoComponenteLexico.IDENTIFICADOR:
            nuevosNodos += [self.__analizarAsignacion()]

        #invocacion
        elif self.componenteActual.lexema == 'ir a mundo':
            nuevosNodos += [self.__analizarInvocacion()]

        # retorno
        elif self.componenteActual.lexema == 'bandera':
            nuevosNodos += [self.__analizarRetorno()]

        #error
        else:
            nuevosNodos += [self.__analizarError()]
            

        return NodoASA(TipoComponenteLexico.INSTRUCCION, nodos=nuevosNodos)
    

    def __analizarRepeticion(self):
        """
        minijuego [Condicion] {Instruccion+}
        """
        nuevosNodos = []

        # analisis de la condicion
        self.verificar('minijuego')
        self.verificar('[')
        nuevosNodos += [self.__analizarCondicion()]
        self.verificar(']')

        nuevosNodos += [self.__analizarBloqueCodigo()] #agregar nuevo

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


        return NodoASA(TipoComponenteLexico.SI, nodos=nuevosNodos)
    

    def __analizarSi(self):
        """
        nivel (\n|\s)*[Condición](\n|\s)*{ Instrucción + }
        """
        nuevosNodos = []

        # analizar Si
        self.verificar('nivel')
        self.verificar('[')
        nuevosNodos += [self.__analizarCondicion()]
        self.verificar(']')

        nuevosNodos += [self.__analizarBloqueCodigo()] #agregar nuevo

        return NodoASA(TipoComponenteLexico.SI, nodos=nuevosNodos)
    

    def __analizarSino(self):
        """
        tubo (\n|\s)*{ Instrucción + }
        """
        nuevosNodos = []

        # analizar Sino
        self.__verificar('tubo')

        nuevosNodos += [self.__analizarBloqueCodigo()] #agregar nuevo

        return NodoASA(TipoComponenteLexico.SI, nodos=nuevosNodos)

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
        if self.componenteActual.tipo == TipoComponenteLexico.OPERADOR_LOGIO:
            nuevosNodos = [self.__analizarOperadorBooleano()]

            # analizar la siguiente condicion 
            nuevosNodos = [self.__analizarCondicion()]


        return NodoASA(TipoComponenteLexico.CONDICION, nodos=nuevosNodos)
    
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
    
    def __analizarOperador(self):
            """
            Operador ::= '(\[ (\+|-|\*|\/|) \])')
            """
            # analizar operador 

            self.__verificarTipoComponente(TipoComponenteLexico.OPERADOR)

            nodo = NodoASA(TipoComponenteLexico.OPERADOR, contenido=self.componenteActual.lexema)
            self.__pasarSiguienteComponente()

            return nodo

    def __analizarNumero(self):
        """
        Numero ::= (Entero | Flotante)
        """

        if self.componenteActual.tipo == TipoComponenteLexico.ENTERO:
            nodo = self.__verificarEntero()
        elif self.componenteActual.tipo == TipoComponenteLexico.FLOTANTE:
            nodo = self.__verificarFlotante()
        else:
            # Manejo de error
            nodo = self.__analizarError()

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
        Principal :== juego (\n|\s)*{Instrucción *}
        """
        nuevosNodos = []

        self.__verificar('juego')
        nuevosNodos += [self.analizarBloqueCodigo]

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
        self.verificar('{')

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
            nodo = self.__verificarLiteral()
        
        return nodo


    def __verificarFlotante(self):
        """
        Verifica si el tipo del componente léxico actual es un flotante

        Flotante ::= (-)?\d*.\d+
        """
        self.__verificar_tipo_componente(TipoComponenteLexico.FLOTANTE)

        nodo = NodoASA(TipoComponenteLexico.FLOTANTE, contenido =self.componente_actual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def __verificarEntero(self):
        """
        Verifica si el tipo del componente léxico actual es un entero

        Entero ::= (-)?\d+
        """
        self.__verificar_tipo_componente(TipoComponenteLexico.ENTERO)

        nodo = NodoASA(TipoComponenteLexico.ENTERO, contenido =self.componente_actual.lexema)
        self.__pasarSiguienteComponente()
        return nodo
    
    def _verificarComparador(self):
        """
        Verifica si el tipo del componente léxico actual es un comparador
        Comparador ::= Comparador ::= [ (<>|><|>-|<-|\^\^|--) \]')

        """
        self.__verificar_tipo_componente(TipoComponenteLexico.COMPARADOR)

        nodo = NodoASA(TipoComponenteLexico.COMPARADOR, contenido =self.componente_actual.lexema)
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
        self.__verificar_tipo_componente(TipoComponenteLexico.IDENTIFICADOR)

        nodo = NodoASA(TipoComponenteLexico.IDENTIFICADOR, contenido =self.componente_actual.lexema)
        self.__pasarSiguienteComponente()
        return nodo

    
    def __verificar(self, textoEsperado):
        """
        Verifica si el texto del componente actual es el del texto esperado que se envia como parametro.
        Si no coinciden se imprime el error y se activa la bandera de error
        """

        if self.componenteActual.lexema != textoEsperado:
            print(f"[Error]: Se esperaba '{textoEsperado}', no '{self.componenteActual.lexema}' en la linea {self.componenteActual.numeroLinea}, columna {self.componenteActual.numeroColumna}\n\n\t--->{self.componenteActual.lineaCodigo}\n")
            self.error = True

        self.__pasarSiguienteComponente()

    def __verificarTipoComponente(self, tipoEsperado ):
        """
        Verifica un componente segun su tipo
        """

        if self.componente_actual.tipo != tipoEsperado:
            print(f"[Error]: Se esperaba un token de tipo '{tipoEsperado}', no '{self.componenteActual.tipo}' en la linea {self.componenteActual.numeroLinea}, columna {self.componenteActual.numeroColumna}\n\n\t--->{self.componenteActual.lineaCodigo}\n")
            self.error = True

    
    def __pasarSiguienteComponente(self):
        """
        Pasa al siguiente componente léxico
        """
        self.posicionComponenteActual += 1

        if self.posicionComponenteActual >= self.cantidadComponentes:
            return

        self.componente_actual = self.componentesLexicos[self.posicionComponenteActual]

    