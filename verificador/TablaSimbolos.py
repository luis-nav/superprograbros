# Tabla de simbolos para el manejo de variables

class Registro:
    """ 
    Se almacena la informacion relevante para un registro de la tabla de Simbolos
    se almacena el nombre como string, nivel como entero y nodo como NodoASA
    """

    __identificador: str
    __nivel: int

    def __init__(self, nuevoNombre, nuevoNivel, nuevaReferencia):
        self.__identificador = nuevoNombre
        self.__nivel = nuevoNivel
        self.__referencia = nuevaReferencia

    def obtenerIdentificador(self):
        return self.__identificador
    
    def obtenerNivel(self):
        return self.__nivel
    
    def obtenerReferencia(self):
        return self.__referencia
    
    def __str__(self):
        return f"Registro: " + self.__identificador + " : "+str(self.__nivel) +" : "+ str(self.__referencia) + "\n"
    

class TablaSimbolos:
    """ 
    Se almacena información auxiliar para la decoración del asa
    con la información del tipo y alcance.

    La estructura de símbolos es una pila de registros
    """
    nivelActual : int = 0

    def __init__(self):
        self.simbolos = []

    def incluir(self, ref):
        """
        Ingresa un registro arriba de la pila
        Solo se necesita como parametro el nodo de referencia
        """
        if not self.existe(ref.contenido):

            registro = Registro(ref.contenido, self.nivelActual, ref)
            self.simbolos.append(registro)

            self.printInFile()
        
    
    def extraer(self):
        """
        Retorna el registro al tope de la pila y lo elimina
        """
        registro = self.simbolos.pop()
        return registro
    
    def inspeccionar(self):
        """
        Retorna el registro al tope de la pila
        """
        registro : Registro = self.simbolos[len(self.simbolos) - 1]
        return registro
    
    def buscar(self, identificador):
        """
        Verficia si un identificador existe cómo variable/función global o local
        """
        for registro in self.simbolos:

            # si es local
            if registro.obtenerIdentificador() == identificador and \
                    registro.obtenerNivel() <= self.nivelActual:

                return registro

        raise Exception('Error: Variable no definida', identificador)

    def iniciarBloque(self):
        """
        Inicia un bloque de alcance (scope)
        """
        self.nivelActual += 1

    def cerrarBloque(self):
        """
        Termina un bloque de alcance y al acerlo elimina todos los
        registros de la tabla que estan en ese bloque
        """

        for registro in reversed(self.simbolos):

            if registro.obtenerNivel() == self.nivelActual:
                # Saca el ultimo registro de la lista
                self.extraer()
            
            elif registro.obtenerNivel() < self.nivelActual:
                break

        self.nivelActual -= 1
        self.printInFile()

    def existe(self, identificador):
        """
        Verficia si un identificador existe cómo variable/función global o local
        """
        for registro in self.simbolos:

            # si es local
            if registro.obtenerIdentificador() == identificador and \
                    registro.obtenerNivel() <= self.nivelActual:

                return True

        return False


    def printInFile(self):
        """
        Imprime texto en un archivo de salida        
        """
        f = open("salida.txt", "a")
        print(self, file=f)
        f.close()
    
    def __str__(self):
        toStr = "------------------- TABLA DE SÍMBOLOS -----------------------------\n\n"
        toStr += "Profundidad: " + str(self.nivelActual) +'\n\n'

        for registro in self.simbolos:
            toStr += str(registro) + '\n'
        
        return toStr