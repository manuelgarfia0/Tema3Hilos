import threading
import time
import random


class MiThread(threading.Thread):

    def __init__(self, nombre):
        super().__init__(name=nombre)  # Asigna el nombre al hilo

    def run(self):
        # Bucle infinito
        while True:
            print(f"Soy {self.name} y estoy trabajando.")

            # Tiempo aleatorio entre 1 y 10 segundos
            tiempo_espera = random.randint(1, 10)
            time.sleep(tiempo_espera)

            print(f"Soy {self.name} y he terminado de trabajar.")


if __name__ == "__main__":
    nombres = ["Ana", "Carlos", "María", "Luis", "Elena"]

    hilos = []
    for nombre in nombres:
        hilo = MiThread(nombre)
        hilo.daemon = True  # El programa termina aunque los hilos sigan corriendo
        hilo.start()
        hilos.append(hilo)

    # Dejamos correr el programa 60 segundos para observar los hilos
    # Puedes pulsar Ctrl+C para detenerlo antes
    print("Hilos en ejecución. Pulsa Ctrl+C para detener.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nPrograma detenido por el usuario.")