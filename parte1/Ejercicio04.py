import threading


# Texto sobre el que se contarán las vocales
TEXTO = """
La inteligencia artificial es una rama de la informática que se ocupa de crear sistemas
capaces de realizar tareas que normalmente requieren inteligencia humana. Estas tareas
incluyen el aprendizaje automático, el razonamiento, la resolución de problemas,
la percepción y la comprensión del lenguaje natural. En la actualidad, la inteligencia
artificial está presente en muchos aspectos de nuestra vida cotidiana, desde los asistentes
virtuales hasta los sistemas de recomendación de las plataformas de entretenimiento.
""".lower()


class ContadorVocal(threading.Thread):
    """Hilo que cuenta las ocurrencias de una vocal específica en el texto."""

    # Diccionario de clase para almacenar los resultados de todos los hilos
    resultados = {}
    lock = threading.Lock()  # Para escribir en el diccionario de forma segura

    def __init__(self, vocal, texto):
        super().__init__()
        self.vocal = vocal
        self.texto = texto

    def run(self):
        cantidad = self.texto.count(self.vocal)
        print(f"[Hilo '{self.vocal}'] Ha contado {cantidad} apariciones de '{self.vocal}'")

        # Guardamos el resultado de forma thread-safe
        with ContadorVocal.lock:
            ContadorVocal.resultados[self.vocal] = cantidad


if __name__ == "__main__":
    print("=== Cuenta de Vocales con Hilos ===\n")
    print(f"Texto analizado:\n{TEXTO}")
    print("-" * 50)

    vocales = ['a', 'e', 'i', 'o', 'u']

    # Creamos un hilo por cada vocal
    hilos = [ContadorVocal(vocal, TEXTO) for vocal in vocales]

    # Lanzamos todos los hilos
    for hilo in hilos:
        hilo.start()

    # Esperamos a que terminen todos
    for hilo in hilos:
        hilo.join()

    # Mostramos el resumen final
    print("\n=== Resultados finales ===")
    total = 0
    for vocal in vocales:
        cantidad = ContadorVocal.resultados[vocal]
        total += cantidad
        print(f"  Vocal '{vocal}': {cantidad} veces")

    print(f"\nTotal de vocales en el texto: {total}")