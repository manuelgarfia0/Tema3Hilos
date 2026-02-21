import threading
import random
import time


class AdivinaNumero(threading.Thread):
    """Hilo que intenta adivinar el número oculto."""

    # Variables de clase compartidas
    numero_oculto = random.randint(0, 100)
    ya_adivinado = False
    ganador = None

    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def run(self):
        intentos = 0

        while True:
            # Comprobamos primero si otro hilo ya acertó
            if AdivinaNumero.ya_adivinado:
                print(f"[{self.nombre}] Alguien ya acertó. Termino mi búsqueda tras {intentos} intentos.")
                break

            # Generamos un número aleatorio
            intento = random.randint(0, 100)
            intentos += 1

            # Comprobamos si hemos acertado
            if intento == AdivinaNumero.numero_oculto:
                # Marcamos que ya se adivinó (puede haber condición de carrera aquí,
                # pero para el propósito del ejercicio es aceptable)
                AdivinaNumero.ya_adivinado = True
                AdivinaNumero.ganador = self.nombre
                print(f"[{self.nombre}] ¡¡ACERTÉ!! El número era {intento} (intentos: {intentos})")
                break
            else:
                # Pequeña pausa para no saturar la CPU y que el output sea legible
                time.sleep(0.01)


if __name__ == "__main__":
    print("=== Juego: Número Oculto ===")
    print(f"Número a adivinar: {AdivinaNumero.numero_oculto}  (revelado al inicio para verificar)\n")

    nombres = [f"Jugador-{i+1}" for i in range(10)]
    hilos = [AdivinaNumero(nombre) for nombre in nombres]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print(f"\n¡El ganador fue: {AdivinaNumero.ganador}!")
    print(f"El número oculto era: {AdivinaNumero.numero_oculto}")
