def cargar_archivo(path):
    """
    Carga un archivo
    """
    with open(path, "r", encoding="utf-8") as archivo:
        return archivo