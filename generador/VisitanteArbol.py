from analizador.arbolSintaxisAbstracta import ArbolSintaxisAbstracta, NodoASA, TipoNodo

class VisitanteArbol:
    tabs = 0

    def visitar(self, nodo: NodoASA):
        """
        Este método visita un nodo del árbol de cualquier tipo 
        y lo mapea a la función de visita del respectivo tipo de nodo
        """

        resultado = ""

        match nodo.tipo:
            case TipoNodo.PROGRAMA:
                return self.__visitarPrograma(nodo)
            case TipoNodo.ASIGNACION:
                return self.__visitarAsignacion(nodo)
            case TipoNodo.EXPRESION_MATEMATICA:
                return self.__visitarExpresionMate(nodo)
            case TipoNodo.EXPRESION:
                return self.__visitarExpresion(nodo)
            case TipoNodo.INVOCACION:
                return self.__visitarInvocacion(nodo)
            case TipoNodo.FUNCION:
                return self.__visitarFunciones(nodo)
            case TipoNodo.PARAMETROS_FUNCION:
                return self.__visitarParametrosFuncion(nodo)
            case TipoNodo.PARAMETROS_INVOCACION:
                return self.__visitarParametrosInvocacion(nodo)
            case TipoNodo.BLOQUE_INSTRUCCIONES:
                return self.__visitarBloqueInstrucciones(nodo)
            case TipoNodo.INSTRUCCION:
                return self.__visitarInstruccion(nodo)
            case TipoNodo.REPETICION:
                return self.__visitarRepeticion(nodo)
            case TipoNodo.BIFURCACION:
                return self.__visitarBifuracion(nodo)
            case TipoNodo.SI:
                return self.__visitarSi(nodo)
            case TipoNodo.SINO:
                return self.__visitarSino(nodo)
            case TipoNodo.RETORNO:
                return self.__visitarRetorno(nodo)
            case TipoNodo.BLOQUE_CONDICIONES:
                return self.__visitarBloqueCondiciones(nodo)
            case TipoNodo.CONDICION:
                return self.__visitarCondicion(nodo)
            case TipoNodo.COMPARACION:
                return self.__visitarComparacion(nodo)
            case TipoNodo.OPERADOR_BOOLEANO:
                return self.__visitarOperadorBooleano(nodo)
            case TipoNodo.IDENTIFICADOR:
                return self.__visitarIdentificador(nodo)
            case TipoNodo.COMPARADOR:
                return self.__visitarComparador(nodo)
            case TipoNodo.FLOTANTE:
                return self.__visitarFlotante(nodo)
            case TipoNodo.ENTERO:
                return self.__visitarEntero(nodo)
            case TipoNodo.VALOR_BOOLEANO:
                return self.__visitarValorBooleano(nodo)
            case TipoNodo.TEXTO:
                return self.__visitarTexto(nodo)
            case TipoNodo.OPERADOR:
                return self.__visitarOperador(nodo)
            case TipoNodo.PRINCIPAL:
                return self.__visitarPrincipal(nodo)
            case TipoNodo.ERROR:
                return self.__visitarError(nodo)
            
        # No deberia llegar a este return
        return "[DEBUG NEEDED]"
    
    def __visitarPrograma(self, nodoActual):
        """
        Programa ::= ((Comentario | Asignacion | Funcion)(\n|\s)*)* Principal
        """

        instrucciones = []

        for nodo in nodoActual.nodos:
            instrucciones.append(nodo.visitar(self))

        return "\n".join(instrucciones)
    
    def __visitarAsignacion(self, nodoActual):
        """
        Asignación ::= Identificador [ ? ] (ExpresionMate | Invocación)  [ ; ]
        """

        resultado = """{} = {}"""

        instrucciones = []
        for nodo in nodoActual.nodos:
            instrucciones.append(nodo.visitar(self))
        
        return resultado.format(instrucciones[0], instrucciones[1])
    
    def __visitarExpresionMate(self, nodoActual):
        """
        ExpresionMate ::= Valor | [Expresion]
        """

        instrucciones = []
        for nodo in nodoActual.nodos:
            instrucciones.append(nodo.visitar(self))

        return " ".join(instrucciones)

    def __visitarExpresion(self, nodoActual):
        """
        Expresion ::= ExpresionMate Operador ExpresionMate
        """

        instrucciones = []
        for nodo in nodoActual.nodos:
            instrucciones.append(nodo.visitar(self))

        return " ".join(instrucciones)
    
    def __visitarInvocacion(self, nodoActual):
        """
        Invocación ::= ir a mundo Identificador [Parámetros]
        """
        resultado = """{}({})"""
        instrucciones = []
        for nodo in nodoActual.nodos:
            instrucciones.append(nodo.visitar(self))
        return resultado.format(instrucciones[0], instrucciones[1])
    
    def __visitarFunciones(self, nodoActual):
        """
        Funcion ::= mundo Identificador [Parámetros](\n|\s)*BloqueInstrucciones
        """

        resultado = """\ndef {}({}):\n{}"""

        instrucciones = []
        for nodo in nodoActual.nodos:
            instrucciones.append(nodo.visitar(self))

        return resultado.format(instrucciones[0], instrucciones[1], instrucciones[2])
    
    def __visitarParametrosFuncion(self, nodoActual):
        """
        ParametrosFunción ::= Identificador (,Identificador)*
        """

        parametros = []

        for nodo in nodoActual.nodos:
            parametros.append(nodo.visitar(self))

        if len(parametros) > 0:
            return ",".join(parametros)
        else:
            return ""
        
    def __visitarParametrosInvocacion(self, nodoActual):
        """
        Parámetros Invocacion ::= Valor (,Valor)+
        """

        parametros = []
        for nodo in nodoActual.nodos:
            parametros.append(nodo.visitar(self))

        if len(parametros) > 0:
            return ",".join(parametros)
        else:
            return ""
        
    def __visitarBloqueInstrucciones(self, nodoActual):
        """
        BloqueInstrucciones ::= { Instrucción+ }
        """

        self.tabs += 1

        resultado = "\n{}"

        instrucciones = []
        for nodo in nodoActual.nodos:
            instrucciones.append(nodo.visitar(self))

        instruccionesTabuladas = []

        for instruccion in instrucciones:
            instruccionesTabuladas.append(self.__retornarTabuladores() + instruccion)

        self.tabs -= 1

        return resultado.format("\n".join(instruccionesTabuladas))
        
    def __visitarInstruccion(self, nodoActual):
        """
        Instrucción ::= ((Retorno | Error | Invocación)[ ; ] 
        | Repetición | Bifurcación | Asignación | Comentario)(\n|\s)* 
        """

        resultado = ""

        for nodo in nodoActual.nodos:
            resultado = nodo.visitar(self)

        return resultado
    
    def __visitarRepeticion(self, nodoActual):
        """
        minijuego [Condicion] BloqueInstrucciones
        """
        resultado = """\n{}\n{}while {}:\n{}\n{}"""

        instrucciones = []
        for nodo in nodoActual.nodos:
            instrucciones.append(nodo.visitar(self))
        
        # Se hace el juego con la condicion que se saca del ASA
        # Se tiene que hacer un juego antes de iniciar con el while y al final del while
        juegoInicio = self.__retornarJuego(instrucciones[0])
        # Al juego final se le añade un tabulador extra para que este dentro de las instrucciones del while
        juegoFinal = self.__retornarJuego(instrucciones[0], 1)
        return resultado.format(juegoInicio, self.__retornarTabuladores() ,instrucciones[0], instrucciones[1], juegoFinal)
    
    def __visitarBifuracion(self, nodoActual):
        """
        Si (Sino)?
        """
        resultado = """{}\n{}"""

        instrucciones = []
        for nodo in nodoActual.nodos:
            instrucciones.append(nodo.visitar(self))
        if(len(instrucciones) == 1):
            return resultado.format(instrucciones[0], "")
        else:
            return resultado.format(instrucciones[0], instrucciones[1])
        
    def __visitarSi(self, nodoActual):
        """
        nivel (\n|\s)*[Condición](\n|\s)*BloqueInstrucciones
        """

        resultado = """\n{}\n{}if {}:\n{}"""

        instrucciones = []
        for nodo in nodoActual.nodos:
            instrucciones.append(nodo.visitar(self))

        # Se hace el juego con la condicion que se saca del ASA
        juego = self.__retornarJuego(instrucciones[0])

        return resultado.format(juego, self.__retornarTabuladores() ,instrucciones[0], instrucciones[1])
    
    def __visitarSino(self, nodoActual):
        """
        tubo (\n|\s)*BloqueInstrucciones
        """

        resultado = """{}else:\n{}"""

        instrucciones = ""
        for nodo in nodoActual.nodos:
            instrucciones = nodo.visitar(self)

        return resultado.format(self.__retornarTabuladores(), instrucciones)
    
    def __visitarRetorno(self, nodoActual):
        """
        Retorno ::= bandera Valor?
        """
    
        resultado = """return {}"""
        valor = ""

        for nodo in nodoActual.nodos:
            valor = nodo.visitar(self)

        return resultado.format(valor)
    
    def __visitarBloqueCondiciones(self, nodoActual):
        """
        BloqueCondiciones ::= Condicion | ([Condicion+] (OperadorBooleano BloqueCondiciones)?)
        """

        instrucciones = []
        for nodo in nodoActual.nodos:
            instrucciones.append(nodo.visitar(self))

        if (len(instrucciones) == 1):
            return instrucciones[0]
        # Viene un bloque de condiciones mas complejo
        resultado = "({}) {} {}"
        return resultado.format(instrucciones[0], instrucciones[1], instrucciones[2])
        
    def __visitarCondicion(self, nodoActual):
        """
        Condición ::= Comparación (OperadorBooleano Condición)?
        """
        
        instrucciones = []
        for nodo in nodoActual.nodos:
            instrucciones.append(nodo.visitar(self))

        if (len(instrucciones) == 1):
            return instrucciones[0]
        # Viene un operador y otra condicion
        resultado = "{} {} {}"
        return resultado.format(instrucciones[0], instrucciones[1], instrucciones[2])
    
    def __visitarComparacion(self, nodoActual):
        """
        Comparación ::= Valor Comparador Valor
        """
        resultado = "{} {} {}"

        instrucciones = []
        for nodo in nodoActual.nodos:
            instrucciones.append(nodo.visitar(self))

        return resultado.format(instrucciones[0], instrucciones[1], instrucciones[2])
    
    def __visitarOperadorBooleano(self, nodoActual):
        """
        OperadorBooleano ::=  [( & | | )]
        """

        if nodoActual.contenido == "[ & ]":
            return "and"
        else:
            return "or"

    def __visitarIdentificador(self, nodoActual):
        """
        Identificador ::= [a-zA-Z_][0-9a-zA-Z_]*
        """
        return nodoActual.contenido
    
    def __visitarComparador(self, nodoActual):
        """
        Comparador ::= Comparador ::= [ (<>|><|>-|<-|\^\^|--) \]')
        """
        match nodoActual.contenido:
            case "[ <> ]":
                return "=="
            case "[ >< ]":
                return "!="
            case "[ >- ]":
                return ">="
            case "[ <- ]":
                return "<="
            case "[ ^^ ]":
                return ">"
            case "[ -- ]":
                return "<"
            
    def __visitarFlotante(self, nodoActual):
        """
        Flotante ::= (-)?\d*.\d+
        """
        
        return nodoActual.contenido
    
    def __visitarEntero(self, nodoActual):
        """
        Entero ::= (-)?\d+
        """

        return nodoActual.contenido
    
    def __visitarValorBooleano(self, nodoActual):
        """
        ValorBooleano ::= peach | bowser
        """

        if (nodoActual.contenido == "peach"):
            return "True"
        return "False"
    
    def __visitarTexto(self, nodoActual):
        """
        Texto ::= "[a-zA-Z_0-9]*"
        """

        return nodoActual.contenido
    
    def __visitarOperador(self, nodoActual):
        """
        operador ::= '(\[ (\+|-|\*|\/) \])')
        """

        match nodoActual.contenido:
            case "[ + ]":
                return "+"
            case "[ - ]":
                return "-"
            case "[ * ]":
                return "*"
            case "[ / ]":
                return "/"
        
    def __visitarPrincipal(self, nodoActual):
        """
        Principal :== juego (\n|\s)* BloqueInstrucciones
        """

        resultado = """\ndef principal():\n{}\n

if __name__ == '__main__':
    principal()
"""

        bloque = nodoActual.nodos[0].visitar(self)

        return resultado.format(bloque)

    def __visitarError(self, nodoActual):
        """
        Error ::= [ POW ] Valor 
        """

        resultado = "raise Exception({})"

        valor = nodoActual.nodos[0].visitar(self)

        return resultado.format(valor)


    def __retornarTabuladores(self):
        return "    " * self.tabs

    def __retornarJuego(self, condicion, tabsExtra=0):
        self.tabs += tabsExtra
        instrucciones = [
        """print(\"\"\"
            \\033[94mS\\033[93mU\\033[91mP\\033[92mE\\033[93mR \\033[91mP\\033[92mR\\033[93mO\\033[91mG\\033[92mR\\033[94mA \\033[91mB\\033[93mR\\033[96mO\\033[92mS\\033[0m - \\033[1m¡HORA DE DESICIÓN!\\033[0m
              
\\033[93m            {}
              
\\033[92m    _________                                     _________
\\033[92m    |       |                                     |       |
\\033[92m      |   |                                         |   |
\\033[92m      |   |                                         |   |
\\033[92m      |   |                                         |   |
      \\033[92mpeach\\033[0m                                         \\033[91mbowser\\033[0m
    (verdadera)                                    (falsa)

\"\"\")""".format(condicion),
        "__spbUsrInput = input(\"La condicion va para \\033[92mpeach\\033[0m o para \\033[91mbowser\\033[0m: \")",
        "while (__spbUsrInput != \"peach\" and __spbUsrInput != \"bowser\"):",
        "   __spbUsrInput = input(\"La condicion va para \\033[92mpeach\\033[0m o para \\033[91mbowser\\033[0m: \")",
        "if ((__spbUsrInput == \"peach\" and {0}) or (__spbUsrInput == \"bowser\" and not {0})):".format(condicion),
        "   print(\"\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n¡Tamos gucci! \U0001F60E\U0001F44D\")",
        "else:",
        "   raise Exception(\"\\033[91m¡Has decidido la opcion incorrecta!\\033[0m \U0001F612\")"
        ]

        instruccionesTabuladas = []
        for instruccion in instrucciones:
            instruccionesTabuladas.append(self.__retornarTabuladores() + instruccion)
        
        self.tabs -= tabsExtra

        return "\n".join(instruccionesTabuladas)