# Analizador SuperPrograBros 

#imports
from explorador.explorador import TipoComponenteLexico, ComponenteLexico
# clase de analizador, recibe la lista de componentes lexicos del explorador

class Analizador:
    # atributos
    componenteLexicos : list
    cantidadComponentes: int
    posicionComponenteActual: int
    componenteActual : ComponenteLexico

    # constructor
    def __init__(self, listaComponentes):

        self.componenteLexicos = listaComponentes
        self.cantidadComponentes = len(listaComponentes)
        self.posicionComponenteActual = 0
        self.componenteActual = listaComponentes[self.posicionComponenteActual]

        self.asa = ArbolSintaxisAbstracta() # falta definir la estructura del arbol


    # metodos
    def imprimirArbol(self):
        #imprime el arbol de sintaxis abstracta
        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimirPreorden()

    
    def analizarInstruccion(self):
        """
        Instrucción ::= (Repetición | Bifurcación | Asignación | Retorno |
        Error | Comentario)[ ; ](\n|\s)*

        Los comentarios son ignorados
        """
        nuevosNodos = []

        #repeticion
        if self.componenteActual.lexema == 'minijuego':
            nuevosNodos += [self.analizarRepeticion()]
        
        #bifurcacion    
        elif self.componenteActual.lexema == 'nivel':
            nuevosNodos += [self.analizarBifurcacion()]

        # asignacion
        elif self.componenteActual.tipo == TipoComponenteLexico.IDENTIFICADOR:
            nuevosNodos += [self.analizarAsignacion()]

        #invocacion
        elif self.componenteActual.lexema == 'ir a mundo':
            nuevosNodos += [self.analizarInvocacion()]

        # retorno
        elif self.componenteActual.lexema == 'bandera':
            nuevosNodos += [self.analizarRetorno()]

        #error
        else:
            nuevosNodos += [self.analizarError()]
            

        return NodoArbol(TipoComponenteLexico.INSTRUCCION, nodos=nuevosNodos)
    

    def analizarRepeticion(self):
        """
        minijuego [Condicion] {Instruccion+}
        """
        nuevosNodos = []

        # analisis de la condicion
        self.verificar('minijuego')
        self.verificar('[')
        nuevosNodos += [self.analizarCondicion()]
        self.verificar(']')

        nuevosNodos += [self.analizarBloqueCodigo()] #agregar nuevo

        return NodoArbol(TipoComponenteLexico.REPETICION, nodos=nuevosNodos)
    

    def analizarBifurcacion(self):
        """
        Si (Sino)?
        """
        nuevosNodos = []

        # analisis de la bifurcacion
        # Si
        nuevosNodos += [self.analizarSi()] #agregar nuevo

        # Sino
        if self.componenteActual.lexema == 'tubo':
            nuevosNodos += [self.analizarSino()] #agregar nuevo


        return NodoArbol(TipoComponenteLexico.SI, nodos=nuevosNodos)
    

    def analizarSi(self):
        """
        nivel (\n|\s)*[Condición](\n|\s)*{ Instrucción + }
        """
        nuevosNodos = []

        # analizar Si
        self.verificar('nivel')
        self.verificar('[')
        nuevosNodos += [self.analizarCondicion()]
        self.verificar(']')

        nuevosNodos += [self.analizarBloqueCodigo()] #agregar nuevo

        return NodoArbol(TipoComponenteLexico.SI, nodos=nuevosNodos)
    

    def analizarSino(self):
        """
        tubo (\n|\s)*{ Instrucción + }
        """
        nuevosNodos = []

        # analizar Sino
        self.verificar('tubo')

        nuevosNodos += [self.analizarBloqueCodigo()] #agregar nuevo

        return NodoArbol(TipoComponenteLexico.SI, nodos=nuevosNodos)

    def analizarRetorno(self):
        """
        Retorno ::= bandera Valor?
        """
        nuevosNodos = []

        # analizar retorno
        self.verificar('bandera')
        
        # valor es opcional
        if self.componenteActual.tipo in [TipoComponenteLexico.IDENTIFICADOR, TipoComponenteLexico.ENTERO, TipoComponenteLexico.FLOTANTE,
                                          TipoComponenteLexico.TEXTO, TipoComponenteLexico.VALOR_BOOLEANO]:
            nuevosNodos += [self.analizarValor()]

        return NodoArbol(TipoComponenteLexico.RETORNO, nodos=nuevosNodos)
    

    def analizarCondicion(self):
        """
        Condición ::= Comparación (( [ & ] | [ | ]) Condición)?
        """
        nuevosNodos = []

        # se analiza la primera comparacion
        nuevosNodos += [self.analizarComparacion()]

        # la segunda comparacion con los operadores es opcional
        if self.componenteActual.tipo == TipoComponenteLexico.OPERADOR_LOGIO:
            nuevosNodos = [self.analizarOperadorBooleano()]

            # analizar la siguiente condicion 
            nuevosNodos = [self.analizarCondicion()]


        return NodoArbol(TipoComponenteLexico.CONDICION, nodos=nuevosNodos)
    
    def analizarComparacion(self):
        """
        Comparación ::= Valor Comparador Valor
        """
        nuevosNodos = []

        # analisis de la comparacion
        nuevosNodos += [self.analizarValor()]
        nuevosNodos += [self.verificarComparador()]
        nuevosNodos += [self.analizarValor()]


        return NodoArbol(TipoComponenteLexico.COMPARACION, nodos=nuevosNodos)
    
    def analizarOperadorBooleano(self):
        """
        ComparadorLogico ::=  [( & | | )]
        """
        # analizar operador booleano 

        self.verificarTipoComponente(TipoComponenteLexico.OPERADOR_BOOLEANO)

        nodo = NodoÁrbol(TipoComponenteLexico.OPERADOR_BOOLEANO, contenido=self.componenteActual.lexema)
        self.pasarSiguienteComponente()

        return nodo


    def analizarError(self):
        """
        Error ::= [ POW ] Valor 
        """
        nuevosNodos = []

        self.__verificar('[ POW ]')
        nuevosNodos += [self.analizarValor()]

        return NodoArbol(TipoComponenteLexico.ERROR, nodos=nuevosNodos)
    

    def analizarPrincipal(self):
        """
        Principal :== juego (\n|\s)*{Instrucción *}
        """
        nuevosNodos = []

        self.verificar('juego')
        nuevosNodos += [self.analizarBloqueCodigo]

        return NodoArbol(TipoComponenteLexico.PRINCIPAL, nodos=nuevosNodos)
    
    def analizarBloqueCodigo(self):
        """
        BloqueCodigo ::= { Instrucción+ }
        """
         # Obligatorio
        self.verificar('{')

        # la primera instruccion obligatoria
        nuevosNodos += [self.analizarInstruccion()]

        # valida todas las instrucciones que haya de mas (repeticion, bifurcacion, retorno, invocacion, error)
        while self.componenteActual.lexema in ['minijuego', 'nivel', 'bandera', 'ir a mundo', '[ POW ]'] \
                or self.componenteActual.tipo == TipoComponenteLexico.IDENTIFICADOR:
        
            nuevosNodos += [self.analizarInstruccion()]

        # Obligatorio
        self.verificar('}')

        return NodoÁrbol(TipoComponenteLexico.BLOQUE_INSTRUCCIONES, nodos=nuevosNodos)


    